# repeat-03/EC-W04-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W04-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Campaign hypotheses

H1 [tentative, pre-experiment]
At fixed loading (0.020 mol reagent in 0.040 L solvent), positive polarization near +1 V is expected to give more target conversion than negative polarization, while excessive charge/potential may reduce selectivity and energy efficiency. A sign-paired baseline can falsify this.

H2 [tentative, pre-experiment]
Higher nominal conductivity should improve ohmic efficiency, but the best balanced score may require a tradeoff with diffusion, proton activity, precipitation, and hidden material residuals. Screen material combinations before local potential/time refinement.

Decision plan: use early batches for sign/material screening, then spend later batches locally refining the best observed region. Interpret final-assay noise as limiting fine comparisons; replicate the eventual leader if resources permit.

### v2 · 公开事件 35

# Campaign hypotheses

H1 [supported in tested scope]
For 0.020 mol in 0.040 L and 3600 s, negative polarization is the productive sign: +1 V/S0/E0 gave score 0 and essentially no productive efficiencies, whereas -1 V under the otherwise matched baseline scored about 0.297 (events runner-operation-0007 and -0014). Positive-sign productivity is rejected for this baseline, not necessarily for every material.

H2 [provisionally supported]
At -1 V, 500 mA cap, 3600 s, paired S2/E2 led the material screen (score about 0.320; event -0028), above S1/E1 (~0.281; -0021) and S3/E3 (~0.180; -0035). S2/E2 also avoided observed precipitation, unlike S0/E0. Because solvent and electrolyte were changed together, attribution to either material remains unresolved.

H3 [tentative]
The S2/E2 leader may benefit from a more negative potential and/or longer duration: its conversion (~0.168) and selective yield (~0.104) leave charge-time headroom, while efficiencies are only moderate. Next test a potential bracket at fixed 3600 s, then lengthen the best region. A large selectivity/energy-efficiency decline would reverse the move toward more negative potential.

### v3 · 公开事件 77

# Campaign hypotheses

H1 [supported in tested scope]
Negative polarization is the productive sign for the tested loading; the matched ±1 V comparison strongly separated outcomes (events -0007, -0014).

H2 [supported as an operating-region choice; component attribution unresolved]
S2/E2 is the leading tested material pair and avoids substantial precipitation (event -0028 versus the paired-material screen). Solvent/electrolyte main effects remain confounded.

H3 [supported locally]
For S2/E2, 500 mA cap and 3600 s, the balanced score is unimodal over the tested potential bracket: approximately 0.292 at -0.4 V, 0.336 at -0.6 V, 0.320 at -1.0 V, and 0.275 at -1.5 V (events -0056, -0049, -0028, -0042). The optimum likely lies near -0.6 to -0.8 V; fine differences remain subject to assay/process variation.

H4 [supported over tested time range]
At -0.6 V, extending time raised score from ~0.336 (3600 s) to ~0.402 (7200 s), ~0.479 (12000 s), and ~0.517 (14400 s; events -0049, -0063, -0070, -0077). Increased selective yield outweighed modest efficiency variation, with safety risk stable and below the limit. No decline was observed by the legal maximum duration, so the last batch will probe -0.75 V at 14400 s rather than shorten time.

### v4 · 公开事件 84

# Campaign hypotheses

H1 [supported in tested scope]
Negative polarization is the productive sign at 0.020 mol reagent in 0.040 L solvent. The matched S0/E0 ±1 V, 200 mA, 3600 s comparison gave score 0 at +1 V and ~0.297 at -1 V (events runner-operation-0007 and -0014). This sign claim should not be extrapolated beyond the studied system without testing.

H2 [supported as an operating-region choice; attribution unresolved]
S2/E2 was the leading paired material choice in the screen and avoided the severe precipitation observed with S0/E0 (event -0028 versus -0014). Since solvent and electrolyte were varied together, their individual and interaction contributions remain unresolved.

H3 [supported locally]
At S2/E2, 500 mA cap and 3600 s, score showed a broad local maximum around -0.6 to -1.0 V and fell at both -0.4 and -1.5 V (events -0056, -0049, -0028, -0042). The -0.75 V long-duration probe scored ~0.496, below -0.6 V at the same 14400 s (~0.517; events -0084 and -0077), supporting -0.6 V over -0.75 V for this campaign.

H4 [supported over tested interval]
At -0.6 V/S2/E2/500 mA, longer electrolysis monotonically improved observed score through the 14400 s legal maximum: ~0.336 (3600 s), ~0.402 (7200 s), ~0.479 (12000 s), ~0.517 (14400 s). The gain was mainly higher conversion and selective product yield; safety risk remained ~0.114, below the 0.65 limit. An optimum beyond 14400 s is untested and outside the legal campaign range.

Operating recommendation: batch 11 (0.020 mol reagent, 0.040 L S2, E2, -0.6 V, 500 mA cap, 14400 s). It produced the highest public score and selective yield among completed batches. Fine superiority over nearby settings is not independently replicated, so treat the exact potential as locally supported rather than exact.

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
      "current_mA": 200,
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
    "cost": 0.2849644720554352,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9356175661087036,
    "pH_normalized": 0.23443032801151276,
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
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.05115935578942299,
    "electrochemical_selectivity": 0.6655986309051514,
    "energy_efficiency": 0.205027237534523,
    "faradaic_efficiency": 0.31719881296157837,
    "ohmic_efficiency": 0.9324108958244324,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2970498204231262,
    "selective_product_yield": 0.04779233783483505,
    "transport_efficiency": 0.34345561265945435
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
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
    "cost": 0.3057999908924103,
    "electrochemical_conversion": 0.15401576459407806,
    "electrochemical_selectivity": 0.5112488865852356,
    "energy_efficiency": 0.25278714299201965,
    "faradaic_efficiency": 0.3144729733467102,
    "ohmic_efficiency": 0.72794508934021,
    "pH_normalized": 0.20570328831672668,
    "precipitation_signal": 0.7096880078315735,
    "safety_risk": 0.09559440612792969,
    "score": 0.2809411287307739,
    "selective_product_yield": 0.07286262512207031,
    "transport_efficiency": 0.33102989196777344
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
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
    "cost": 0.3314000070095062,
    "electrochemical_conversion": 0.16770870983600616,
    "electrochemical_selectivity": 0.5746636986732483,
    "energy_efficiency": 0.3396144509315491,
    "faradaic_efficiency": 0.3959493935108185,
    "ohmic_efficiency": 0.6413648128509521,
    "pH_normalized": 0.17412734031677246,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.32045942544937134,
    "selective_product_yield": 0.1042584627866745,
    "transport_efficiency": 0.36446183919906616
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
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
    "cost": 0.31540000438690186,
    "electrochemical_conversion": 0.041191667318344116,
    "electrochemical_selectivity": 0.49968501925468445,
    "energy_efficiency": 0.04927691072225571,
    "faradaic_efficiency": 0.09194889664649963,
    "ohmic_efficiency": 0.8300144076347351,
    "pH_normalized": 0.28303924202919006,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.18016700446605682,
    "selective_product_yield": 0.027081934735178947,
    "transport_efficiency": 0.08143943548202515
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
      "solvent": 2,
      "volume_L": 0.04
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
    "cost": 0.33500000834465027,
    "electrochemical_conversion": 0.13909058272838593,
    "electrochemical_selectivity": 0.5433884263038635,
    "energy_efficiency": 0.17498239874839783,
    "faradaic_efficiency": 0.3176702558994293,
    "ohmic_efficiency": 0.7617440223693848,
    "pH_normalized": 0.17581218481063843,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.1135944053530693,
    "score": 0.27527356147766113,
    "selective_product_yield": 0.0841674879193306,
    "transport_efficiency": 0.2929869294166565
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.6
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
    "cost": 0.3285199999809265,
    "electrochemical_conversion": 0.21566681563854218,
    "electrochemical_selectivity": 0.6579949259757996,
    "energy_efficiency": 0.26713162660598755,
    "faradaic_efficiency": 0.4423741102218628,
    "ohmic_efficiency": 0.43604061007499695,
    "pH_normalized": 0.17482678592205048,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.33573102951049805,
    "selective_product_yield": 0.14283253252506256,
    "transport_efficiency": 0.44577446579933167
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
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.4
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
    "cost": 0.32708001136779785,
    "electrochemical_conversion": 0.21963819861412048,
    "electrochemical_selectivity": 0.6850574016571045,
    "energy_efficiency": 0.06920644640922546,
    "faradaic_efficiency": 0.4897252023220062,
    "ohmic_efficiency": 0.1236158162355423,
    "pH_normalized": 0.17312930524349213,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.1135944053530693,
    "score": 0.2923741638660431,
    "selective_product_yield": 0.13430503010749817,
    "transport_efficiency": 0.4832298457622528
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.6
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
    "cost": 0.3328399956226349,
    "electrochemical_conversion": 0.40872564911842346,
    "electrochemical_selectivity": 0.6510042548179626,
    "energy_efficiency": 0.29854246973991394,
    "faradaic_efficiency": 0.43156296014785767,
    "ohmic_efficiency": 0.4342775344848633,
    "pH_normalized": 0.1751430779695511,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.1135944053530693,
    "score": 0.4015657603740692,
    "selective_product_yield": 0.28830668330192566,
    "transport_efficiency": 0.4523942470550537
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.6
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
    "cost": 0.3386000096797943,
    "electrochemical_conversion": 0.6997486352920532,
    "electrochemical_selectivity": 0.6791964173316956,
    "energy_efficiency": 0.28171995282173157,
    "faradaic_efficiency": 0.4492447078227997,
    "ohmic_efficiency": 0.3937284052371979,
    "pH_normalized": 0.17282894253730774,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.47938838601112366,
    "selective_product_yield": 0.4493633210659027,
    "transport_efficiency": 0.4505942761898041
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.6
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
    "cost": 0.34147998690605164,
    "electrochemical_conversion": 0.8347065448760986,
    "electrochemical_selectivity": 0.6515589952468872,
    "energy_efficiency": 0.28003817796707153,
    "faradaic_efficiency": 0.44242119789123535,
    "ohmic_efficiency": 0.4072066843509674,
    "pH_normalized": 0.17381398379802704,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.1135944053530693,
    "score": 0.5169646143913269,
    "selective_product_yield": 0.5437572598457336,
    "transport_efficiency": 0.4496011435985565
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.75
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
    "cost": 0.3458000123500824,
    "electrochemical_conversion": 0.7512412071228027,
    "electrochemical_selectivity": 0.6209283471107483,
    "energy_efficiency": 0.3256702721118927,
    "faradaic_efficiency": 0.3773704469203949,
    "ohmic_efficiency": 0.5396435260772705,
    "pH_normalized": 0.1743343025445938,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.49573254585266113,
    "selective_product_yield": 0.5010104775428772,
    "transport_efficiency": 0.39859539270401
  }
}
```

## K1 封存报告

Mechanism report

1. Overall interpretation

This world behaves like a cathodic electrochemical conversion with four coupled layers: (i) potential-dependent interfacial kinetics and product selectivity, (ii) charge delivery and ohmic loss, (iii) mass transport, and (iv) medium-dependent acid/base and precipitation behavior. The target reaction requires negative polarization in the tested operating region. Product formation increases with electrolysis time, but the efficiencies depend non-monotonically on potential because stronger polarization changes faradaic selectivity, transport demand, and voltage losses.

The best observed procedure was batch 11: 0.020 mol limiting reagent in 0.040 L solvent-S2, electrolyte-E2, −0.60 V, a 500 mA current cap, and 14,400 s. Its score was 0.51696, with conversion 0.83471, selectivity 0.65156, selective product yield 0.54376, faradaic efficiency 0.44242, transport efficiency 0.44960, ohmic efficiency 0.40721, energy efficiency 0.28004, pH_normalized 0.17381, precipitation signal 0.00524, and safety risk 0.11359. This is an empirical recommendation within the tested domain, not a claim that −0.60 V is an exact universal optimum.

2. Evidence that the target process is cathodic

Batches 1 and 2 supplied the clearest sign comparison. Both used solvent-S0, electrolyte-E0, 0.020 mol reagent, 0.040 L solvent, a 200 mA cap, and 3,600 s. Batch 1 used +1.0 V and produced score 0, conversion 0.00801, selectivity 0.01035, selective yield 0, faradaic efficiency 0.02452, and transport efficiency 0. Batch 2 used −1.0 V and produced score 0.29705, conversion 0.05116, selectivity 0.66560, selective yield 0.04779, faradaic efficiency 0.31720, and transport efficiency 0.34346. Ohmic efficiency remained high in both cases, approximately 0.936 and 0.932, so the failure at +1 V cannot be explained simply by poor electrical conduction. Instead, the polarity was wrong for productive electron transfer.

I therefore infer that a useful kinetic driving force can be represented by a cathodic overpotential, for example

η_c = E_eq,eff − E_applied,

where increasingly negative applied potential raises η_c. The effective equilibrium or onset potential, E_eq,eff, plausibly contains the declared solvent and electrolyte potential shifts plus hidden interface residuals. A positive potential in batch 1 would give negligible productive cathodic rate even though electrical current could still be carried by capacitive or side processes.

The sign conclusion is well supported for S0/E0 near ±1 V. Extrapolating it to every possible material and potential is reasonable mechanistic conjecture, but only that one matched sign pair was tested.

3. Material and medium effects

At −1.0 V and 3,600 s, the paired material screen gave:

• Batch 2, S0/E0, 200 mA cap: score 0.29705; conversion 0.05116; yield 0.04779; precipitation 1.000.
• Batch 3, S1/E1, 500 mA cap: score 0.28094; conversion 0.15402; yield 0.07286; precipitation 0.70969.
• Batch 4, S2/E2, 500 mA cap: score 0.32046; conversion 0.16771; yield 0.10426; precipitation 0.
• Batch 5, S3/E3, 500 mA cap: score 0.18017; conversion 0.04119; yield 0.02708; precipitation 0.

S2/E2 was consequently selected for refinement. Batch 4 combined the largest score and yield in this screen with no observed precipitation. Its faradaic, transport, ohmic, and energy efficiencies were 0.39595, 0.36446, 0.64136, and 0.33961, respectively. In contrast, S3/E3 in batch 5 had faradaic efficiency 0.09195, transport efficiency 0.08144, and energy efficiency 0.04928 despite an ohmic efficiency of 0.83001. Thus high ohmic efficiency alone is insufficient; an electrically conductive cell can still direct little charge toward the desired reaction or be transport/kinetically unsuitable.

The declared nominal properties give a plausible physical explanation. E2 has high nominal bulk conductivity, negligible precipitating-salt concentration relative to E0, and a positive standard-potential shift; S2 has low relative conductivity but high relative solubility product, reduced proton activity, and its own positive potential shift. The S2/E2 combination may therefore suppress precipitation and move the redox onset while retaining useful electrolyte conductivity. Its low solvent conductivity is consistent with only moderate ohmic efficiency, especially at mild applied voltage.

E0's precipitation signal of 1 in batches 1 and 2 agrees qualitatively with its high precipitating-salt concentration and low Ksp. E1 gave intermediate precipitation, and E2/E3 gave essentially none. This supports a solubility-equilibrium contribution rather than precipitation being merely an electrolysis artifact.

However, solvent and electrolyte were varied together, not factorially. The screen cannot identify whether S2, E2, or an S2×E2 interaction caused the improvement. Batch 2 also used a 200 mA rather than 500 mA cap, further weakening direct quantitative comparison with batches 3–5. Hidden, fixed world-specific transport, solvation, and interface residuals were explicitly possible, so nominal material properties should be treated as explanatory priors rather than fitted causal effects.

4. Potential dependence and competing efficiencies

With S2/E2, a 500 mA cap, and 3,600 s, batches 4, 6, 7, and 8 bracketed potential:

• −1.50 V, batch 6: score 0.27527; conversion 0.13909; selectivity 0.54339; yield 0.08417; FE 0.31767; transport 0.29299; ohmic 0.76174; energy 0.17498.
• −1.00 V, batch 4: score 0.32046; conversion 0.16771; selectivity 0.57466; yield 0.10426; FE 0.39595; transport 0.36446; ohmic 0.64136; energy 0.33961.
• −0.60 V, batch 7: score 0.33573; conversion 0.21567; selectivity 0.65799; yield 0.14283; FE 0.44237; transport 0.44577; ohmic 0.43604; energy 0.26713.
• −0.40 V, batch 8: score 0.29237; conversion 0.21964; selectivity 0.68506; yield 0.13431; FE 0.48973; transport 0.48323; ohmic 0.12362; energy 0.06921.

These observations suggest a broad balanced-score optimum around −0.6 to −1.0 V, not monotonic improvement with increasing cathodic magnitude. At −1.5 V, excessive overpotential plausibly accelerates parasitic electron transfer, solvent/electrolyte reactions, or interfacial blocking; FE, selectivity, transport efficiency, and energy efficiency all declined relative to −0.6 V. At the other extreme, −0.4 V retained good conversion, selectivity, FE, and transport over 3,600 s, but ohmic efficiency collapsed to 0.12362 and energy efficiency to 0.06921. A likely interpretation is that the useful cell voltage became too small relative to an approximately fixed resistive voltage loss, so a large fraction of the applied voltage was dissipative.

A schematic electrical relationship is

I_delivered ≈ min(I_cap, max(0, (|E_applied−E_onset|)/R_eff)),

η_ohmic ≈ max(0, 1 − I_delivered R_eff/|E_applied|).

This is only a qualitative form: no current trace or resistance was measured, and the displayed ohmic efficiency may contain additional interface terms. It does explain why mild polarization can have favorable chemical selectivity but poor voltage utilization, whereas strong polarization improves the apparent ohmic fraction but wastes energy in overpotential and side chemistry.

Faradaic selectivity could be represented schematically as a peaked function of overpotential and medium,

FE_target = f_medium(η_c) × f_transport(I/I_lim) × f_interface,

where f_medium includes hidden solvent/electrolyte residuals, and f_transport declines when reaction demand approaches the limiting flux. The observed fall in FE from 0.48973 at −0.4 V to 0.31767 at −1.5 V supports increasing parasitic charge at high overpotential. The score nevertheless did not peak at −0.4 V because energy and ohmic efficiencies were severely penalized.

5. Charge/time dependence

Batches 7, 9, 10, and 11 held S2/E2, −0.60 V, the 500 mA cap, initial reagent/solvent amounts, and all other chosen settings constant while varying electrolysis time:

• 3,600 s, batch 7: conversion 0.21567; selectivity 0.65799; yield 0.14283; score 0.33573.
• 7,200 s, batch 9: conversion 0.40873; selectivity 0.65100; yield 0.28831; score 0.40157.
• 12,000 s, batch 10: conversion 0.69975; selectivity 0.67920; yield 0.44936; score 0.47939.
• 14,400 s, batch 11: conversion 0.83471; selectivity 0.65156; yield 0.54376; score 0.51696.

Conversion and selective yield rose strongly and approximately monotonically. Selectivity stayed near 0.65–0.68 rather than collapsing, while FE remained near 0.43–0.45 and transport efficiency near 0.45. Thus longer time primarily delivered more productive charge without a demonstrated late-stage selectivity catastrophe over the tested interval.

A useful phenomenological model is

dX/dt = k_eff(η_c, medium)·(1−X)·g_transport,

with

k_eff ∝ FE_target·I_delivered/(nF N_0),

and selective product formation approximately

dY_target/dt = S_target·dX/dt − k_deg·Y_target.

Equivalently, if efficiencies are nearly stationary, conversion might resemble X(t)=1−exp(−k_app t). The four observed time points do not exactly obey a single exponential, so this equation is a conceptual model rather than an identified law. Changing concentration, local pH, electrode condition, measurement noise, and possible time-dependent current can all cause deviations.

Selective product yield was broadly linked to conversion times selectivity. For example, batch 11 gives 0.83471×0.65156≈0.544, essentially its observed yield of 0.54376. Other batches deviate more from this simple product, particularly batch 10, so yield should not be treated as an exact deterministic product of the separately noisy assay channels. Additional product loss or independently calibrated measurement noise is plausible.

No decline was observed by 14,400 s, the legal maximum. It is therefore observationally correct to say that the best tested duration was 14,400 s. It would be unjustified to claim that the true unconstrained optimum is exactly 14,400 s or that still longer electrolysis would continue to improve performance.

6. Fine potential comparison at long duration

Batch 12 tested −0.75 V at 14,400 s with S2/E2 and a 500 mA cap. It scored 0.49573, below batch 11's 0.51696 at −0.60 V. Batch 12 had higher ohmic efficiency (0.53964 versus 0.40721) and energy efficiency (0.32567 versus 0.28004), but lower conversion (0.75124 versus 0.83471), selectivity (0.62093 versus 0.65156), yield (0.50101 versus 0.54376), FE (0.37737 versus 0.44242), and transport efficiency (0.39860 versus 0.44960).

This comparison illustrates the central tradeoff. A somewhat stronger cathodic potential improved electrical voltage utilization but shifted enough current away from the productive pathway, or altered transport/interface behavior enough, to reduce the weighted total. It supports −0.60 V over −0.75 V at 14,400 s in this campaign. Because there was only one batch at each condition and final-assay noise was nonzero, it does not identify the potential optimum to high precision. A value close to −0.60 V should be viewed as a robust operating region, not a sharply known constant.

7. pH, proton activity, and precipitation couplings

The normalized pH endpoint depended strongly on paired materials but was fairly stable during S2/E2 refinement. It was about 0.232–0.234 for S0/E0, 0.20570 for S1/E1, 0.28304 for S3/E3, and about 0.173–0.176 for all S2/E2 batches. Within S2/E2, changing potential from −1.5 to −0.4 V or extending time to 14,400 s did not produce a large pH_normalized shift relative to the material-to-material differences.

I therefore regard pH primarily as a medium-buffer/electrolyte property over the studied charge range, with possible smaller electrochemical contributions. A plausible equilibrium module would calculate proton activity from declared acid concentration and pKa, modified by solvent proton activity, before coupling it to proton-consuming cathodic reactions. The data do not identify proton stoichiometry, buffer capacity, or whether protons participate directly in the target elementary step.

Precipitation appears dominated by the selected material pair: signal 1 for S0/E0, 0.70969 for S1/E1, and approximately zero for S2/E2 and S3/E3. Small nonzero S2/E2 readings, such as 0.00819 in batch 9 and 0.00524 in batch 11, are comparable to the stated small assay-scale uncertainty and do not establish meaningful precipitation. Precipitation could reduce active dissolved electrolyte, alter mass transport, or foul an interface; this is a plausible coupling, but the experiments did not separately manipulate or quantify solid formation.

8. Relationship to the public score

The balanced score is a weighted combination of conversion (0.10), selectivity (0.15), energy efficiency (0.15), faradaic efficiency (0.12), ohmic efficiency (0.08), selective yield (0.30), and transport efficiency (0.10), with a selective-yield gate. Batch 11's components reproduce approximately

0.10(0.83471)+0.15(0.65156)+0.15(0.28004)+0.12(0.44242)+0.08(0.40721)+0.30(0.54376)+0.10(0.44960) ≈ 0.517.

The large 0.30 yield weight explains why longer electrolysis improved the score even when energy and ohmic efficiencies were only moderate. Conversely, batch 8's excellent FE, transport, and selectivity could not offset its low yield and very poor energy/ohmic efficiency. The recommendation is therefore specific to the published balanced-efficiency objective. A process optimized for minimum electrical energy, maximum instantaneous selectivity, or minimum time might choose another potential or duration.

9. Safety behavior

Observed safety risk was stable within a given material recipe and well below the 0.65 limit. It was approximately 0.0722 for S0/E0, 0.0956 for S1/E1, 0.1136 for S2/E2, and 0.1262 for S3/E3. Within S2/E2 it remained about 0.1136 across potential and duration changes, including 14,400 s. This suggests that, in this benchmark, the dominant risk contribution came from charged material inventory or recipe properties rather than cumulative electrolysis time. That conclusion is restricted to the recorded public risk metric; no specific physical hazard identity was observable.

10. What is identified, what is not, and alternative explanations

Well-supported within the tested domain:

• Productive conversion requires negative rather than positive polarization for the matched S0/E0 baseline.
• S2/E2 was the best tested paired medium for the balanced objective.
• Potential has a non-monotonic effect because chemical, transport, ohmic, and energy terms trade off.
• At −0.60 V in S2/E2, longer time improved conversion, yield, and score through 14,400 s.
• Severe precipitation was associated with S0/E0 and was absent or negligible for S2/E2.

Not identifiable from this design:

• Separate solvent and electrolyte main effects, because they were screened as matched pairs.
• The importance of solvent×electrolyte interactions.
• Current-cap dependence, because current was not independently varied at a fixed optimized recipe.
• Actual current, charge passed, electron stoichiometry, exchange current, Tafel slope, cell resistance, electrode area, and limiting current.
• Whether the potential response is governed mainly by kinetic onset shifts, side-reaction thresholds, double-layer behavior, or hidden fixed residuals.
• The exact optimum potential, because nearby conditions were not replicated and assay/process noise remains.
• Long-term deactivation or product degradation beyond 14,400 s.

Plausible alternatives include: (1) S2/E2's advantage may be a favorable hidden residual rather than the nominal properties; (2) the low score at −1.5 V could be due to a specific parasitic reaction rather than a smooth FE decline; (3) the low ohmic efficiency at −0.4 V may include an algorithmic voltage-utilization term rather than literal bulk resistance alone; and (4) some apparent time-series variation in selectivity and efficiency may be measurement noise rather than real temporal changes.

11. Final mechanistic picture and scope

My working model is a medium-shifted cathodic electron-transfer process. Applied potential determines cathodic overpotential and delivered current; the medium sets redox onset, conductivity, proton activity, solvation, precipitation tendency, diffusion, and hidden interface factors. Productive FE and selectivity are highest at moderate cathodic driving force and deteriorate when polarization is excessive. Mild polarization can preserve selectivity but suffer large relative ohmic/energy losses. Charge accumulation increases conversion and yield until substrate depletion, degradation, or another limitation eventually intervenes. S2/E2 places these tradeoffs in the most favorable tested region, and −0.60 V provides a better balance than either −0.40 V or more negative settings. At that potential, extending electrolysis to the maximum tested duration supplies enough productive charge to make selective yield the dominant score advantage.

This account is confined to 0.020 mol reagent, approximately 0.040 L starting solvent, the tested anonymous materials, potentials from −1.5 to +1.0 V, current caps of 200 or 500 mA, and durations up to 14,400 s. It should not be interpreted as a physical identity claim for the anonymous materials or as a quantitatively validated model outside that domain.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific mechanism prior or known response law was supplied. The material dossier supplied nominal conductivity, diffusivity, acid, solubility, capacitance, and potential-shift properties, but explicitly did not supply the hidden selectivity, faradaic-response, or world-residual laws.

The clearest contradicted self-developed claim was my pre-experiment conjecture that positive polarization near +1 V would be more productive. Batch 1 (+1 V, S0/E0) returned score 0, yield 0, FE 0.0245, and transport efficiency 0. Batch 2, matched except for −1 V, scored 0.297 with yield 0.0478, selectivity 0.666, and FE 0.317. The batch-1 UV result already showed essentially no productive efficiencies; batch 2 then established that the negative sign was productive. This evidence reversed the polarity judgment.

Several later claims were supported within limited scope:

• S2/E2 was the best tested paired medium. In the −1 V, 3,600 s screen, batch 4 scored 0.320, versus 0.281 for S1/E1 in batch 3 and 0.180 for S3/E3 in batch 5. It also showed no precipitation, unlike S0/E0 in batch 2.
• Potential response was non-monotonic. For S2/E2 at 3,600 s, scores were 0.275 at −1.5 V (batch 6), 0.320 at −1.0 V (batch 4), 0.336 at −0.6 V (batch 7), and 0.292 at −0.4 V (batch 8). Batch 8 preserved good selectivity and FE but had very poor energy and ohmic efficiencies, while batch 6 lost chemical and transport performance at excessive polarization.
• Longer electrolysis improved the balanced objective over the tested interval. At −0.6 V, scores increased from 0.336 at 3,600 s (batch 7), to 0.402 at 7,200 s (batch 9), 0.479 at 12,000 s (batch 10), and 0.517 at 14,400 s (batch 11). Conversion and selective yield increased without a large selectivity collapse.
• The exact long-duration choice was locally supported: batch 11 at −0.6 V outperformed batch 12 at −0.75 V and the same 14,400 s, 0.517 versus 0.496. Batch 12 improved ohmic and energy efficiencies but lost conversion, yield, FE, selectivity, and transport efficiency.
• Precipitation was strongly associated with material selection: signal 1.000 for S0/E0, 0.710 for S1/E1, and approximately zero for S2/E2 and S3/E3. This was qualitatively consistent with the nominal solubility information.

Important proposed laws remain untested rather than established. These include an exponential conversion law, a particular current–voltage or ohmic-loss equation, a bell-shaped FE law in overpotential, a specific degradation term, and direct proton participation. Solvent and electrolyte effects were not separately identified because the screen changed them together. Current-cap dependence was not isolated, no condition was replicated, and behavior beyond 14,400 s was not tested. The nominal potential shifts and conductivity data offer plausible explanations, but the experiments cannot distinguish them cleanly from hidden fixed material residuals.

2. Most informative additional experiment

I would run one crossed-material experiment using S0 with E2 at the otherwise recommended settings: the same reagent concentration, −0.6 V, 500 mA cap, 14,400 s, followed by the same final assay. I would not execute it here.

This would distinguish an approximately transferable electrolyte/potential/transport explanation from an alternative in which the success of batch 11 depends on S2 specifically or on a special S2×E2 interaction.

• If S0/E2 approached batch 11 in score, yield, FE, and transport efficiency, while avoiding strong precipitation, I would increase confidence that E2 supplies most of the advantage and that its favorable behavior transfers across solvents. The claim that S2 is essential would weaken.
• If it performed between S0/E0 and S2/E2, I would favor partially additive solvent and electrolyte contributions rather than a unique pair effect.
• If it resembled the weak or precipitating S0/E0 behavior despite containing E2, I would infer that S2 is essential for solvation or precipitation control, or that a strong S2×E2 interaction exists. That would weaken the simple nominal-property explanation.
• If it produced an unexpected polarity or efficiency pattern, I would give substantially more weight to hidden pair-specific interface residuals and would stop treating the proposed overpotential/transport law as transferable between media.

One cross cannot fully decompose both main effects and their interaction; a complete 2×2 comparison would also require S2/E0. Nevertheless, S0/E2 is the single most discriminating addition because E2 was never tested outside S2.

3. Unused evidence, weak predictions, and goal-induced limitations

The raw spectral artifacts, individual peak shapes, baselines, and most mass-balance details were not used quantitatively. I relied primarily on processed estimates. Intermediate UV measurements were used as rapid directional checks, but I did not systematically model their deviations from final-assay values. Detailed physical cost, temperature changes, sample consumption, and acquisition metadata were also largely unused because they were not major score components. The pH results were summarized as medium-dependent but were not exploited to fit an acid/base or proton-stoichiometry model. Several nominal dossier variables—capacitance, diffusion-layer thickness, pKa, and potential shifts—were used only qualitatively because the design could not identify their separate effects.

The least reliable blind predictions are Q05, Q07, and Q09 because they use solvent/electrolyte combinations never tested in the campaign. Q11 is also uncertain because it changes the current cap to 500 mA in S0/E0 without an isolated current-response experiment. Q01 is fragile because its short duration puts predicted yield near or below the score gate, so a small yield error can cause a large relative score error. The positive-polarity predictions are more reliable directionally—near-zero target formation—but their exact small clipped assay values remain uncertain.

The recommendation of batch 11 is reliable as the highest observed batch, but its exact superiority over nearby settings is less reliable than the broader recommendation of S2/E2, negative polarization near −0.6 V, and long duration. Batch 11 exceeded batch 12 by only about 0.021 score units, and neither was replicated. The exact optimum could shift under repeat measurements even if the operating region remains preferred.

The assigned goal did affect evidence collection. Maximizing the public balanced score encouraged an early paired-material screen followed by aggressive exploitation of S2/E2, potential refinement, and duration extension. That strategy found a substantially better batch, but it displaced factorial solvent/electrolyte experiments, independent current sweeps, mechanistic controls, and replication. It also favored the maximum legal duration because selective yield had the largest score weight. I found no clear conflict between the score objective and the reported safety metric: all observed risks remained below 0.65. The principal conflict was between optimization and causal identifiability, not between optimization and observed safety.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.52,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.16,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.24,
        "upper80": 0.46
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.22
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.29,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.03
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.56,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.17,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.25,
        "upper80": 0.45
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.32,
        "lower80": 0.24,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.027,
        "upper80": 0.076
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.3,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.03
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.38,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.14,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.19,
        "upper80": 0.44
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.285,
        "lower80": 0.18,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.017,
        "upper80": 0.071
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.035
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.29,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.08,
        "lower80": 0.015,
        "upper80": 0.18
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0.035,
        "upper80": 0.24
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.09,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.031
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.025,
        "upper80": 0.26
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.49,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.26,
        "lower80": 0.13,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.24,
        "upper80": 0.52
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.31,
        "lower80": 0.2,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.024,
        "upper80": 0.091
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.23,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.49,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.09,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.18,
        "upper80": 0.39
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.31,
        "lower80": 0.23,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.145,
        "lower80": 0.09,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.24,
        "lower80": 0.13,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      }
    }
  ],
  "rationale": "Predictions anchor the S0/E0 cases to the campaign's matched polarity comparison: negative potential was productive, whereas positive potential gave essentially zero target formation despite high ohmic efficiency. Negative-polarity yields were scaled mainly by approximate current–time charge, with moderate adjustments for potential, transport limitation, and the observed material-pair behavior. Crossed solvent/electrolyte combinations were never isolated experimentally, so Q05, Q07, and Q09 receive wider intervals. Q11 allows more conversion but lower transport and faradaic performance at high current. Very short Q01 likely remains below the score's selective-yield gate. Intervals combine assay noise with substantially larger model and extrapolation uncertainty, and all are clipped to the public [0,1] metric range."
}
```
