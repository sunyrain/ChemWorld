# repeat-01/EC-W02-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\Projects\ChemWorld-local-research\20261016-unified-matrices\attempt-01\repeat-01\EC-W02-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative, pre-experiment]
At fixed 0.02 mol reagent in 0.04 L, performance should show a polarity-dependent potential optimum: too little driving force limits conversion, whereas excessive magnitude or time lowers selectivity and energy efficiency. Solvent and electrolyte identities may shift transport/ohmic terms.

**Initial testable plan:** use early batches to span both potential signs, electrolyte/solvent identities, current caps, and durations. UV-vis snapshots will be treated as noisy directional diagnostics; final assays are authoritative. If one region clearly improves selective-product yield and balanced score, later batches will locally refine and replicate it; otherwise retain a broad design.

No empirical evidence yet.

### v2 · 公开事件 21

# Electrochemical campaign hypotheses

## H1 [supported in tested S0/E0 scope]
Negative polarization is required for productive conversion under the tested conditions. At +1.5 V, 100 mA cap, 1800 s, batch 1 had zero score and near-zero conversion/yield (runner-operation-0007). Reversing to -1.5 V at the same cap/time produced a score near 0.202 with substantially higher selectivity and efficiency components, though little conversion (runner-operation-0014). This polarity contrast is much larger than the declared assay noise.

## H2 [tentative]
Increasing passed-charge opportunity improves conversion and selective yield but sacrifices Faradaic, transport, and energy efficiency. At -1.5 V in S0/E0, moving from 100 mA/1800 s (runner-operation-0014) to 500 mA/7200 s (runner-operation-0021) raised conversion to about 0.20 and yield to about 0.095, while the three efficiency-related terms declined; balanced score nevertheless rose from about 0.202 to 0.253. This comparison confounds current cap and duration.

**Decision:** retain negative polarity and screen anonymous solvent/electrolyte combinations at the higher-charge condition. Later refine charge and potential around the best material pair. A strong material interaction or a score reversal would change this plan.

### v3 · 公开事件 70

# Electrochemical campaign hypotheses

## H1 [supported in explored scope]
Productive chemistry requires negative polarization; positive +1.5 V was inactive (runner-operation-0007), while all tested negative conditions produced nonzero balanced scores.

## H2 [supported, with material confounding outside S0/E1]
At -1.5 V, 500 mA cap, 7200 s, S0/E1 gave the best of the screened material combinations (score about 0.316; runner-operation-0028), exceeding S0/E0 and the Latin-square S1/E2, S2/E3, S3/E0 comparisons (runner-operation-0021, -0035, -0042, -0049). Because the screen is not a full factorial, separate solvent and electrolyte main effects remain unresolved; S0/E1 is an empirical pair recommendation only.

## H3 [supported locally]
For S0/E1 at 500 mA and 7200 s, decreasing magnitude from -1.5 to -1.0 to -0.5 V progressively improved balanced score (about 0.316, 0.393, 0.488; runner-operation-0028, -0056, -0063). At -0.25 V, conversion/yield rose further but energy and ohmic efficiencies fell enough that score declined to about 0.470 (runner-operation-0070). Thus the observed balanced optimum is near -0.5 V, not the maximum-yield condition.

**Prediction before batch 11:** lowering the current cap while extending time to roughly preserve cap×time should improve ohmic/energy efficiency without greatly reducing conversion, and may beat the -0.5 V/500 mA/7200 s result. If it does not, retain the latter and replicate it.

### v4 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage synthesis

## H1 [supported in explored scope]
Negative polarization is essential: +1.5 V was inactive (runner-operation-0007), whereas tested negative conditions were productive.

## H2 [supported for empirical pair, main effects unresolved]
S0/E1 is the best screened solvent/electrolyte pair. Its advantage at -1.5 V over the other incomplete-factorial combinations is supported by runner-operation-0028 versus -0021, -0035, -0042, and -0049. The design does not isolate solvent and electrolyte main effects or exclude untested pair interactions.

## H3 [supported locally]
With S0/E1, 500 mA cap and 7200 s, balanced score peaked among tested potentials at -0.5 V: about 0.488, versus 0.393 at -1.0 V, 0.316 at -1.5 V, and 0.470 at -0.25 V (runner-operation-0063, -0056, -0028, -0070). The -0.25 V condition delivered more yield but substantially poorer energy/ohmic efficiency, confirming that maximum yield and balanced score differ.

## H4 [unresolved fine optimum]
At -0.5 V and approximately equal cap×time opportunity, 300 mA/12000 s gave the highest observed score, about 0.493 (runner-operation-0077), while 500 mA/7200 s and 250 mA/14400 s gave about 0.488 and 0.486 (runner-operation-0063, -0084). These differences are small relative to component measurement uncertainties and there are no exact replicates, so a precise current/time optimum is unresolved. The lower-current variants improved ohmic efficiency but did not consistently improve yield or Faradaic efficiency.

**Operating decision:** recommend completed batch 11 (0.02 mol reagent, 0.04 L S0; E1; -0.5 V; 300 mA cap; 12000 s). It has the highest observed public balanced-efficiency score and a favorable energy/ohmic balance. Batch 9 is a practically equivalent shorter-time alternative; replication could reverse their narrow ranking.

**Scope/gaps:** claims apply to the tested 0.5 mol/L nominal starting loading. The material screen was sparse, current and time were partly confounded, and no exact replication was performed. Future work should replicate batches 9 and 11 and complete an S×E factorial near -0.5 V.

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
      "potential_V": 1.5
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
    "cost": 0.2836799919605255,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9738203883171082,
    "pH_normalized": 0.22897005081176758,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.2836799919605255,
    "electrochemical_conversion": 0.006326214410364628,
    "electrochemical_selectivity": 0.5154685974121094,
    "energy_efficiency": 0.11278170347213745,
    "faradaic_efficiency": 0.30796968936920166,
    "ohmic_efficiency": 0.9826582074165344,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.20201489329338074,
    "selective_product_yield": 0.01624339260160923,
    "transport_efficiency": 0.3342265188694
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
    "cost": 0.3041999936103821,
    "electrochemical_conversion": 0.19980350136756897,
    "electrochemical_selectivity": 0.5039308667182922,
    "energy_efficiency": 0.08592358231544495,
    "faradaic_efficiency": 0.19249247014522552,
    "ohmic_efficiency": 0.9012727737426758,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.072194404900074,
    "score": 0.25317737460136414,
    "selective_product_yield": 0.0953766405582428,
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
      "current_mA": 500,
      "electrolyte_profile": 1,
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
    "cost": 0.3041999936103821,
    "electrochemical_conversion": 0.2856295108795166,
    "electrochemical_selectivity": 0.5234859585762024,
    "energy_efficiency": 0.11873598396778107,
    "faradaic_efficiency": 0.33851754665374756,
    "ohmic_efficiency": 0.8947497606277466,
    "pH_normalized": 0.20125943422317505,
    "precipitation_signal": 0.8443623185157776,
    "safety_risk": 0.072194404900074,
    "score": 0.3159794211387634,
    "selective_product_yield": 0.1605936586856842,
    "transport_efficiency": 0.30702999234199524
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
      "solvent": 1,
      "volume_L": 0.04
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
    "cost": 0.32019999623298645,
    "electrochemical_conversion": 0.24188333749771118,
    "electrochemical_selectivity": 0.4980844259262085,
    "energy_efficiency": 0.10266618430614471,
    "faradaic_efficiency": 0.26663991808891296,
    "ohmic_efficiency": 0.7934795618057251,
    "pH_normalized": 0.16224750876426697,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.27309650182724,
    "selective_product_yield": 0.1256912648677826,
    "transport_efficiency": 0.2561304569244385
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
    "cost": 0.3458000123500824,
    "electrochemical_conversion": 0.09103474020957947,
    "electrochemical_selectivity": 0.5022227168083191,
    "energy_efficiency": 0.053967949002981186,
    "faradaic_efficiency": 0.11934439092874527,
    "ohmic_efficiency": 0.8870021104812622,
    "pH_normalized": 0.2927204966545105,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.1135944053530693,
    "score": 0.20365950465202332,
    "selective_product_yield": 0.05459942668676376,
    "transport_efficiency": 0.09466105699539185
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
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
    "cost": 0.329800009727478,
    "electrochemical_conversion": 0.16015908122062683,
    "electrochemical_selectivity": 0.5418570041656494,
    "energy_efficiency": 0.08424503356218338,
    "faradaic_efficiency": 0.16275820136070251,
    "ohmic_efficiency": 0.9418713450431824,
    "pH_normalized": 0.2374822497367859,
    "precipitation_signal": 0.9752404689788818,
    "safety_risk": 0.12619440257549286,
    "score": 0.24806484580039978,
    "selective_product_yield": 0.08879027515649796,
    "transport_efficiency": 0.1661585569381714
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
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.3574279844760895,
    "electrochemical_selectivity": 0.6124219298362732,
    "energy_efficiency": 0.327766090631485,
    "faradaic_efficiency": 0.3966071307659149,
    "ohmic_efficiency": 0.8609582185745239,
    "pH_normalized": 0.20026139914989471,
    "precipitation_signal": 0.8522340059280396,
    "safety_risk": 0.072194404900074,
    "score": 0.3931905925273895,
    "selective_product_yield": 0.20312964916229248,
    "transport_efficiency": 0.3901117742061615
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.2897999882698059,
    "electrochemical_conversion": 0.4519886076450348,
    "electrochemical_selectivity": 0.6823309659957886,
    "energy_efficiency": 0.507461667060852,
    "faradaic_efficiency": 0.47794342041015625,
    "ohmic_efficiency": 0.7180790901184082,
    "pH_normalized": 0.20227517187595367,
    "precipitation_signal": 0.8601081967353821,
    "safety_risk": 0.072194404900074,
    "score": 0.4876706302165985,
    "selective_product_yield": 0.3310861587524414,
    "transport_efficiency": 0.4987747073173523
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.25
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
    "cost": 0.28619998693466187,
    "electrochemical_conversion": 0.5233058333396912,
    "electrochemical_selectivity": 0.750534176826477,
    "energy_efficiency": 0.2902164161205292,
    "faradaic_efficiency": 0.5535653829574585,
    "ohmic_efficiency": 0.3658899664878845,
    "pH_normalized": 0.19996103644371033,
    "precipitation_signal": 0.8492700457572937,
    "safety_risk": 0.072194404900074,
    "score": 0.4703689217567444,
    "selective_product_yield": 0.36911740899086,
    "transport_efficiency": 0.5549149513244629
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
      "current_mA": 300,
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
    "cost": 0.2897999882698059,
    "electrochemical_conversion": 0.4547886848449707,
    "electrochemical_selectivity": 0.6732560396194458,
    "energy_efficiency": 0.5673266053199768,
    "faradaic_efficiency": 0.47534337639808655,
    "ohmic_efficiency": 0.8156642913818359,
    "pH_normalized": 0.20094606280326843,
    "precipitation_signal": 0.8571591973304749,
    "safety_risk": 0.072194404900074,
    "score": 0.49287059903144836,
    "selective_product_yield": 0.30252543091773987,
    "transport_efficiency": 0.4825233221054077
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
      "current_mA": 250,
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
    "cost": 0.2897999882698059,
    "electrochemical_conversion": 0.4218446612358093,
    "electrochemical_selectivity": 0.6621477603912354,
    "energy_efficiency": 0.5650484561920166,
    "faradaic_efficiency": 0.4357205927371979,
    "ohmic_efficiency": 0.8601768016815186,
    "pH_normalized": 0.2014663815498352,
    "precipitation_signal": 0.8504951596260071,
    "safety_risk": 0.072194404900074,
    "score": 0.4857099950313568,
    "selective_product_yield": 0.3088364005088806,
    "transport_efficiency": 0.456945538520813
  }
}
```

## K1 封存报告

Mechanism report

1. Experimental scope

All 12 completed batches used the same initial loading: 0.020 mol limiting reagent in 0.040 L solvent, corresponding to a nominal starting concentration of 0.50 mol L^-1. The investigated factors were potential polarity and magnitude, current limit, electrolysis time, anonymous solvent identity, and anonymous electrolyte identity. Consequently, the conclusions below apply directly only to this loading and to the tested operating ranges. The solvent and electrolyte labels are benchmark identifiers, so no molecular identity or real-material property should be inferred from them.

2. Proposed working mechanism

The system behaves like a polarity-selective cathodic conversion with three coupled performance layers:

(a) A target-forming electrochemical pathway is enabled by negative potential. Positive potential either drives the wrong direction or fails to generate the active reduced state.

(b) Within the negative-potential region, milder potentials favor the measured conversion, target selectivity, Faradaic efficiency, and transport efficiency over the tested interval from -1.5 to -0.25 V. This is not a conventional monotonic “more overpotential gives more reaction” response. A plausible interpretation is that the desired elementary electron-transfer step has a preferred potential window, while stronger negative polarization promotes unobserved parasitic charge consumption, electrode blocking, or an off-path reduced state.

(c) The mildest tested potential, -0.25 V, imposes a severe ohmic/energy penalty. Thus the balanced optimum is an intermediate potential near -0.5 V rather than the condition with the highest observed conversion or selective-product yield.

A useful phenomenological representation is

  r_target = k_pair(S,E) × f_pol(V) × f_charge(Q*) × f_transport(I,S,E),

where Q* = I_limit × t is only a nominal charge opportunity, not a measured passed charge. The observable conversion may be represented as

  X ≈ 1 - exp[-k_pair f_pol f_transport t],

and selective-product yield as

  Y_target ≈ X × S_target × L,

where L represents losses or assay/mass-balance effects. Faradaic, transport, ohmic, and energy efficiencies are separate penalties rather than interchangeable estimates of conversion. A schematic energy relation consistent with the observations would be

  eta_energy ≈ eta_F × eta_ohmic × eta_transport × g(V),

although the actual score components do not numerically follow this simple product and therefore must include additional normalization or hidden process terms. These equations are organizing hypotheses, not fitted laws.

3. Evidence for polarity control

Batch 1 used S0/E0, +1.5 V, a 100 mA current limit, and 1800 s. It returned score 0, conversion 0.008, selectivity 0.010, zero reported selective-product yield, essentially zero Faradaic and transport efficiencies, and ohmic efficiency 0.974. The near-unity ohmic term shows that electrical conduction alone was not sufficient for productive chemistry.

Batch 2 changed only the potential polarity to -1.5 V. Its conversion remained near the assay-noise floor at 0.006, but selectivity rose to 0.515, selective-product yield to 0.016, Faradaic efficiency to 0.308, transport efficiency to 0.334, energy efficiency to 0.113, and score to 0.202. Thus the strongest polarity evidence concerns target-channel activation and charge utilization, not a statistically secure conversion increase at this low charge opportunity. The polarity comparison formed the initial cathodic-pathway explanation.

The score contract includes a selective-product-yield gate near 0.02. Batch 2’s reported yield was slightly below this threshold even though its score was nonzero. I therefore do not infer the exact internal gate implementation from this noisy processed estimate.

4. Charge opportunity and extent of conversion

Batch 3 retained S0/E0 and -1.5 V but raised the current limit from 100 to 500 mA and time from 1800 to 7200 s. Relative to batch 2, conversion rose from 0.006 to 0.200 and selective-product yield from 0.016 to 0.095. Score rose from 0.202 to 0.253. In exchange, Faradaic efficiency fell from 0.308 to 0.192, transport efficiency from 0.334 to 0.209, energy efficiency from 0.113 to 0.086, and ohmic efficiency from 0.983 to 0.901.

This comparison supports saturation or loss mechanisms at higher charge exposure: more material is converted, but a smaller fraction of the electrical and transport opportunity contributes efficiently. Because current and time changed together, batch 3 does not identify which variable caused each penalty.

5. Solvent/electrolyte coupling

Batch 4 provided a direct electrolyte comparison against batch 3: both used S0, -1.5 V, 500 mA, and 7200 s, while E0 was replaced by E1. E1 increased conversion from 0.200 to 0.286, yield from 0.095 to 0.161, Faradaic efficiency from 0.192 to 0.339, transport efficiency from 0.209 to 0.307, energy efficiency from 0.086 to 0.119, and score from 0.253 to 0.316. Selectivity changed only modestly, from 0.504 to 0.523. This suggests that E1 primarily improves charge transfer or mass transport rather than changing the intrinsic branch selectivity.

Batches 5-7 were a sparse, confounded material screen at -1.5 V, 500 mA, and 7200 s:

- Batch 5, S1/E2: score 0.273, conversion 0.242, selectivity 0.498, yield 0.126, Faradaic efficiency 0.267, transport efficiency 0.256.
- Batch 6, S2/E3: score 0.204, conversion 0.091, selectivity 0.502, yield 0.055, Faradaic efficiency 0.119, transport efficiency 0.095.
- Batch 7, S3/E0: score 0.248, conversion 0.160, selectivity 0.542, yield 0.089, Faradaic efficiency 0.163, transport efficiency 0.166.

S0/E1 was the best tested pair, but batches 5-7 changed solvent and electrolyte simultaneously. They therefore cannot identify separate solvent main effects, separate electrolyte main effects, or all pair interactions. The poor S2/E3 result could arise from S2, E3, their interaction, or an unmeasured process state.

S0 also had the lowest observed safety risk, about 0.0722, compared with approximately 0.0956 for S1, 0.1136 for S2, and 0.1262 for S3 in this screen. This strengthens the practical preference for S0 without establishing a chemical cause.

6. Potential-response window in S0/E1

Batches 4, 8, 9, and 10 form the most interpretable potential series because they all used S0/E1, a 500 mA current limit, and 7200 s:

- Batch 4, -1.5 V: conversion 0.286, selectivity 0.523, yield 0.161, Faradaic efficiency 0.339, transport efficiency 0.307, ohmic efficiency 0.895, energy efficiency 0.119, score 0.316.
- Batch 8, -1.0 V: conversion 0.357, selectivity 0.612, yield 0.203, Faradaic efficiency 0.397, transport efficiency 0.390, ohmic efficiency 0.861, energy efficiency 0.328, score 0.393.
- Batch 9, -0.5 V: conversion 0.452, selectivity 0.682, yield 0.331, Faradaic efficiency 0.478, transport efficiency 0.499, ohmic efficiency 0.718, energy efficiency 0.507, score 0.488.
- Batch 10, -0.25 V: conversion 0.523, selectivity 0.751, yield 0.369, Faradaic efficiency 0.554, transport efficiency 0.555, ohmic efficiency 0.366, energy efficiency 0.290, score 0.470.

The monotonic improvements in conversion, selectivity, yield, Faradaic efficiency, and transport efficiency as the potential becomes less negative are large relative to their stated assay uncertainties and form the main basis of the preferred-potential-window explanation. In contrast, ohmic efficiency falls monotonically, especially between -0.5 and -0.25 V. Energy efficiency peaks at -0.5 V and then falls sharply. The balanced score therefore peaks at -0.5 V even though batch 10 has the largest yield.

One plausible process is a potential-dependent impedance or polarization mismatch: at -0.25 V the desired chemistry is intrinsically selective, but maintaining productive current under the benchmark’s electrical response incurs a large ohmic penalty. Another plausible explanation is that the efficiency channels include different normalization factors whose optima do not coincide. No voltage, current, impedance, or time-resolved data were measured, so these alternatives cannot be separated.

7. Current-time tradeoff at constant nominal charge opportunity

Batches 9, 11, and 12 all used S0/E1 at -0.5 V and shared I_limit × t = 3600 C if the current limit were continuously reached:

- Batch 9: 500 mA for 7200 s; conversion 0.452, selectivity 0.682, yield 0.331, Faradaic efficiency 0.478, transport efficiency 0.499, ohmic efficiency 0.718, energy efficiency 0.507, score 0.488.
- Batch 11: 300 mA for 12000 s; conversion 0.455, selectivity 0.673, yield 0.303, Faradaic efficiency 0.475, transport efficiency 0.483, ohmic efficiency 0.816, energy efficiency 0.567, score 0.493.
- Batch 12: 250 mA for 14400 s; conversion 0.422, selectivity 0.662, yield 0.309, Faradaic efficiency 0.436, transport efficiency 0.457, ohmic efficiency 0.860, energy efficiency 0.565, score 0.486.

Lowering the current limit improved ohmic efficiency, consistent with smaller resistive or polarization losses. Moving from batch 9 to batch 11 also improved energy efficiency while preserving conversion and Faradaic efficiency reasonably well. Going further to 250 mA and 14400 s did not preserve conversion, Faradaic efficiency, or transport efficiency, suggesting either a minimum useful rate, time-dependent losses, or that the actual current did not remain at its cap.

Batch 11 had the highest observed score and was therefore sealed as the recommendation. However, its advantage over batches 9 and 12 is only about 0.005-0.007 score units. Given the declared component uncertainties and absence of exact replicates, this fine ranking is unresolved. Batch 9 is a plausible shorter-time alternative, and repetition could reverse the order.

8. pH and precipitation observations

The reported normalized pH was mainly material-dependent rather than strongly potential-dependent in S0/E1: batches 4, 8-12 were close to 0.20. In the material screen it ranged from about 0.162 for S1/E2 to 0.293 for S2/E3. These shifts could affect interfacial speciation, conductivity, or precipitation, but the design does not isolate cause.

Precipitation signal was high for the S0 batches, typically about 0.84-1.00, and also high for S3/E0, while it was near zero for S1/E2 and S2/E3. High precipitation therefore is neither universally required nor solely determined by score. For S0/E1 it coexists with the best performance and could represent product formation, electrolyte deposition, or an unrelated phase response. Since the public mapping of signals to hidden species is intentionally unavailable, assigning the precipitate to product would be unjustified.

9. Relationship to the balanced score

The public score weights favor selective-product yield most strongly, followed by electrochemical selectivity and energy efficiency, with additional contributions from conversion, Faradaic efficiency, transport efficiency, and ohmic efficiency. The experiments demonstrate why no single raw metric suffices:

- Batch 10 maximized observed conversion and yield but lost to batches 9 and 11 because its ohmic and energy efficiencies were poor.
- Batch 1 had excellent ohmic efficiency but no productive target formation and scored zero.
- Batch 11 slightly outscored batch 9 by exchanging some yield and transport performance for better ohmic and energy performance.

The operating optimum is therefore a compromise surface, not a maximum-conversion point.

10. Factors that remain unidentifiable

The campaign does not identify electron stoichiometry, actual charge passed, electrode area, current-time traces, electrode potentials under load, temperature evolution, rate constants, or identities of reactant, product, impurity, precipitate, solvent, and electrolyte. It cannot distinguish kinetic limitation from mass-transfer limitation quantitatively. Current limit and duration were confounded in the initial charge comparison, and there were no exact replicates. The material screen was not a full 4×4 factorial. Potential was refined only for S0/E1, so the optimum could shift with another pair. Only one reagent concentration and one initial solvent volume were used.

The final-assay values are noisy synthetic estimates. Large contrasts, such as polarity, E0 versus E1 at fixed S0, and the potential-series trends, are more credible than the narrow score differences among batches 9, 11, and 12.

11. Plausible alternative explanations

A cathodic target pathway plus parasitic over-reduction is my preferred explanation, but several alternatives remain viable:

- Potential may control a hidden equilibrium or phase state rather than an elementary electron-transfer selectivity.
- The apparent material effects may primarily reflect conductivity, solubility, or precipitation instead of catalytic chemistry.
- The strong -0.25 V ohmic penalty may arise from the benchmark’s efficiency normalization rather than a physical increase in solution resistance.
- Time-dependent electrode fouling, reagent depletion near the electrode, or product degradation could explain why batch 12 underperformed at the same nominal charge opportunity.
- Differences among close conditions may partly be assay noise rather than real process effects.

12. Final mechanistic conclusion

Within the studied 0.50 mol L^-1 loading, the world is best described as a cathodically activated, material-coupled conversion whose productive and loss channels respond differently to potential and current density. S0/E1 supports superior charge utilization and transport. Moving from strongly negative potential toward -0.5 V improves conversion, selectivity, Faradaic efficiency, transport efficiency, and energy use, but moving further to -0.25 V causes a large ohmic/energy penalty. At -0.5 V, spreading approximately the same nominal charge opportunity over 12000 s with a 300 mA limit gives the best observed balance, although the exact current-time optimum is not resolved. The sealed batch-11 recommendation is thus an evidence-based compromise rather than a claim of a uniquely identified mechanistic optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, nominal material dossier, or supplied mechanistic claim was provided. Solvents and electrolytes were opaque benchmark labels, so all substantive laws below were self-developed from the campaign.

The initial hypothesis that productive chemistry would be polarity-dependent was supported. Batch 1 at +1.5 V was effectively inactive, whereas batch 2, differing principally by using -1.5 V, showed substantial selectivity and nonzero Faradaic, transport, and energy efficiencies. This comparison changed my judgment from an unspecified potential optimum to a specifically cathodic target pathway.

The proposed conversion–efficiency tradeoff with increasing charge opportunity was supported by batches 2 and 3. Raising both current limit and time greatly increased conversion and yield, but reduced Faradaic, transport, and energy efficiencies. Because current and time changed together, separate current and duration laws remained untested.

The claim that E1 improves S0 performance was supported directly by batches 3 and 4: at the same -1.5 V, 500 mA, and 7200 s conditions, changing E0 to E1 raised conversion, yield, several efficiency terms, and score. Claims about general solvent or electrolyte rankings remained untested because batches 5–7 changed both identities simultaneously. In particular, the poor S2/E3 result in batch 6 cannot be assigned uniquely to S2 or E3.

The proposed intermediate balanced-potential optimum was supported by batches 4, 8, 9, and 10. As potential moved from -1.5 to -0.25 V, conversion, selectivity, yield, Faradaic efficiency, and transport efficiency increased, but batch 10 at -0.25 V suffered a large ohmic and energy-efficiency loss. Batch 9 at -0.5 V therefore outscored batch 10 despite its lower yield. This evidence changed the explanation from a generic “excessive magnitude may be harmful” hypothesis to a more specific compromise between target formation and electrical efficiency near -0.5 V.

A prediction recorded before batch 11 stated that lowering current while extending time at approximately constant nominal charge opportunity could improve ohmic and energy efficiency. Batch 11 weakly supported it relative to batch 9 and gave the highest observed score. However, batch 12 contradicted any simple monotonic law that still lower current must be better: its ohmic efficiency improved, but conversion, Faradaic efficiency, transport efficiency, and score declined. Thus a precise current optimum was not established.

The proposed roles of electrode fouling, over-reduction, phase behavior, precipitation, and pH-dependent speciation were not directly tested. They remain plausible interpretations rather than demonstrated mechanisms.

2. Most informative additional experiment

I would run S0/E1 at the established 0.020 mol in 0.040 L loading, -0.25 V, 300 mA, and 12000 s. This preserves the nominal 3600 C current-limit×time opportunity shared by batches 9, 11, and 12 while testing the mild potential at a lower current than batch 10.

The leading explanation is that -0.25 V lies outside the best electrical operating window and carries a potential-specific ohmic/energy penalty. The main alternative is that batch 10’s penalty arose primarily from its 500 mA current limit or associated polarization, rather than from -0.25 V itself.

If the new batch retained batch 10’s high conversion and yield while restoring ohmic and energy efficiencies toward batch 11, the current/polarization alternative would be favored and the preferred operating point could shift from -0.5 to -0.25 V. If ohmic and energy efficiencies remained poor despite the lower current, the potential-window explanation would be strengthened. If conversion and Faradaic efficiency instead collapsed during the longer, lower-current run, I would infer a minimum useful rate or time-dependent loss such as fouling or degradation, weakening both simple explanations. An exact replicate would still be needed before treating small score differences as resolved.

3. Unused evidence, reliability, and goal effects

I did not quantitatively analyze the full raw spectral artifacts. The mechanism used processed final-assay estimates and only directional information from intermediate UV–visible measurements. Detailed peak shapes, raw baselines, mass-balance channels, and possible spectral evolution were therefore unused. Cost, temperature changes, sample loss, and process-time accounting were not incorporated into a fitted mechanism. The pH and precipitation channels were considered qualitatively but could not be assigned to hidden species, so they contributed little to the recommendation.

The least reliable predictions are those involving E3 or S2 separately, especially Q07–Q10, because the campaign only observed the confounded S2/E3 pair and never isolated the relevant main effects. Positive-potential predictions are also extrapolations: the campaign tested +1.5 V but not +0.8 V. Q01 is uncertain because it combines a new short duration with a yield near the score gate. Predictions for Q11 are comparatively better anchored, though they still extrapolate potential and loading slightly.

The distinction between recommended batch 11 and batches 9 or 12 is the least reliable part of the operating recommendation. Their scores differed by only about 0.005–0.007, there were no exact replicates, and that difference is small relative to component uncertainties. Batch 11 was correctly selected as the highest observed score, but not as a uniquely established optimum.

The assigned score-maximization goal materially affected evidence collection. After broad polarity and material screening, later batches concentrated on the promising S0/E1 region instead of completing a solvent×electrolyte factorial or adding replicates. This improved the operating recommendation but left material main effects, interactions, and repeatability poorly identified. There was no clear conflict requiring unsafe or invalid evidence collection, but optimization was prioritized over complete mechanistic identification.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.24,
        "upper80": 0.53
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.55
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.3,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.54,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.27,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.5
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.33,
        "lower80": 0.26,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.32,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.57,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.41,
        "upper80": 0.68
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.45,
        "upper80": 0.7
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.41,
        "lower80": 0.34,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.025,
        "upper80": 0.095
      },
      "transport_efficiency": {
        "estimate": 0.56,
        "lower80": 0.43,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "energy_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.09
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.5,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.33,
        "lower80": 0.17,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.51
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.3,
        "lower80": 0.2,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.008,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.17,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.11,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.26,
        "lower80": 0.12,
        "upper80": 0.44
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.27,
        "lower80": 0.15,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.003,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.42
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.57,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.29,
        "lower80": 0.2,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.18,
        "upper80": 0.32
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.33,
        "lower80": 0.28,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.15,
        "lower80": 0.1,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.22,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.1
      }
    }
  ],
  "rationale": "The new 0.48 mol/L loading is close to the campaign’s 0.50 mol/L loading. Predictions therefore interpolate the observed polarity, potential, electrolyte, current, and charge-opportunity trends. Negative potential activates the selective pathway; positive-potential batches are predicted to remain essentially inactive. E1 is favored over E0, while E3 and S2 require wider intervals because they were never isolated in the sparse material screen. Longer electrolysis raises yield, whereas low current generally preserves efficiency; Q11 is anchored most directly to the S0/E0 high-current campaign result. Intervals combine assay noise with larger model uncertainty from unreplicated conditions, current–time confounding, sparse material coverage, and extrapolation from -1.5/-1.0/-0.5 V to ±0.8 V."
}
```
