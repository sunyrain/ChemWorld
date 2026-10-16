# repeat-03/EC-W05-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W05-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative; pre-experiment]
At fixed loading (0.040 mol reagent in 0.080 L solvent), balanced score should favor an intermediate overpotential and duration: charge increases conversion initially, while excessive magnitude/time should reduce selectivity and energy efficiency. Current cap may cease to matter above the transport-limited delivered current.

## H2 [tentative; pre-experiment]
Materials with high conductivity and diffusivity should improve ohmic/transport efficiency, but potential shifts mean the optimal signed potential is material-dependent. I will first compare solvent/electrolyte combinations and both potential signs, then refine the best observed region. A result contrary to nominal rankings will be treated as evidence for fixed latent material effects rather than ignored.

## H3 [tentative; pre-experiment]
Intermediate UV-vis estimates can help distinguish under-conversion from efficiency loss, but final assays are authoritative. Numerical differences near stated instrument noise remain unresolved until supported by a final-assay contrast or repetition.

### v2 · 公开事件 35

# Electrochemical campaign hypotheses

## H1 [supported qualitatively; optimum unresolved]
At fixed 0.040 mol/0.080 L loading, polarity is decisive. The +1.2 V S0/E0 batch produced essentially zero efficiency and score (final event runner-operation-0007), whereas -1.2 V under the same materials/time/cap scored 0.182 (runner-operation-0014). I therefore restrict refinement to negative potentials. The best magnitude and duration remain unresolved.

## H2 [supported only in screened scope]
Among matched material pairs at -1.2 V, 200 mA cap, 600 s, S0/E0 had the highest observed balanced score (0.182; runner-operation-0014), above S3/E3 (0.099; runner-operation-0035), S2/E2 (0.032; runner-operation-0028), and S1/E1 (0; runner-operation-0021). This is a comparison of paired combinations, not separable solvent/electrolyte effects. S0/E0 will be the refinement base.

## H3 [measurement scope]
UV-vis and final assays agree on broad efficiency ordering, but individual conversion/yield estimates can sit near zero and are noisy. Final score will drive decisions; near-zero differences will not be overinterpreted.

## Next testable consequence
If -1.2 V is under-driving conversion, increasing negative magnitude or duration on S0/E0 should raise selective yield and score until selectivity/energy penalties dominate. I will map voltage first, then charge/time around the best region.

### v3 · 公开事件 77

# Electrochemical campaign hypotheses

## H1 [supported in tested S0/E0 scope]
At 600 s and 200 mA cap, making the negative potential less extreme improved the balanced response: -0.5 V scored 0.395 (runner-operation-0063), compared with -0.8 V 0.260 (runner-operation-0042), -1.2 V 0.182 (runner-operation-0014), -1.6 V 0.128 (runner-operation-0049), and -2.0 V 0 (runner-operation-0056). The monotone observed ordering over this range supports an overpotential/efficiency penalty, though the optimum may lie nearer zero and selective-yield noise is consequential.

## H2 [material conclusion retained with scope]
S0/E0 remains the best tested paired material combination. This does not identify separable solvent and electrolyte main effects because cross-combinations were not tested.

## H3 [duration unresolved/confounded by assay noise]
At -0.8 V, extending 600 to 1200 and 2400 s increased measured conversion, but scores were non-monotone (0.260, 0.121, 0.351; runner-operation-0042, -0070, -0077) because selective product yield fluctuated near the 0.02 multiplicative gate. Thus conversion growth with time is supported, whereas a duration effect on score is unresolved from single batches.

## Final prospective test
Test -0.5 V for 1200 s on S0/E0 at the same loading and 200 mA cap. If longer time retains the favorable efficiencies while increasing selective yield, it should exceed batch 9; if selectivity/gate behavior worsens, batch 9 remains the recommendation.

### v4 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage synthesis

## H1 [supported in tested S0/E0 scope]
Negative polarity is required in this world: +1.2 V was inactive (runner-operation-0007), while negative potentials produced target and efficiency signals. At 600 s, observed score improved as magnitude decreased from -2.0 toward -0.5 V, with the best score 0.395 at -0.5 V (runner-operation-0063). This supports avoiding excessive cathodic overpotential; the precise optimum closer to zero was not mapped.

## H2 [supported for paired combinations only]
S0/E0 was the best tested paired material setting at -1.2 V/600 s (runner-operation-0014 versus -0021, -0028, -0035). Because only matched pairs were screened, solvent and electrolyte effects are not independently identifiable and cross-combination superiority remains unresolved.

## H3 [duration effect on conversion plausible; score optimum unresolved]
At -0.8 V, longer operation raised measured conversion overall, but selective yield near the scoring gate and assay noise made score non-monotone (runner-operation-0042, -0070, -0077). At -0.5 V, 600 s scored 0.395 and 1200 s scored 0.379 (runner-operation-0063, -0084); this small numerical difference is not strong evidence of a true duration effect given single batches and stated assay noise. The 600 s batch remains the best observed operating recommendation.

## Operational recommendation
Use 0.040 mol limiting reagent in 0.080 L S0; set -0.5 V with 200 mA cap and E0; electrolyze 600 s; then terminate. Batch 9 (runner-operation-0063) is selected on highest public balanced score. Caveats: current-cap dependence was not mapped, precipitation signal stayed near one for S0/E0, and the potential optimum between 0 and -0.5 V remains open.

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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.3527759909629822,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9397798180580139,
    "pH_normalized": 0.23308512568473816,
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.3527759909629822,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6197994351387024,
    "energy_efficiency": 0.208350270986557,
    "faradaic_efficiency": 0.37682637572288513,
    "ohmic_efficiency": 0.9486176371574402,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.1816537082195282,
    "selective_product_yield": 0.012553580105304718,
    "transport_efficiency": 0.4030832052230835
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
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.3847759962081909,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.43956226110458374,
    "energy_efficiency": 0.14114932715892792,
    "faradaic_efficiency": 0.23889970779418945,
    "ohmic_efficiency": 0.8827556371688843,
    "pH_normalized": 0.20443867146968842,
    "precipitation_signal": 0.7141679525375366,
    "safety_risk": 0.09559440612792969,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2554566264152527
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.4359759986400604,
    "electrochemical_conversion": 0.0005859252996742725,
    "electrochemical_selectivity": 0.43966105580329895,
    "energy_efficiency": 0.1505654752254486,
    "faradaic_efficiency": 0.3093140721321106,
    "ohmic_efficiency": 0.8678582906723022,
    "pH_normalized": 0.17094862461090088,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.031732987612485886,
    "selective_product_yield": 0.0028361838776618242,
    "transport_efficiency": 0.27782654762268066
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.4039759933948517,
    "electrochemical_conversion": 0.00631446810439229,
    "electrochemical_selectivity": 0.4552956223487854,
    "energy_efficiency": 0.09436523914337158,
    "faradaic_efficiency": 0.1953389197587967,
    "ohmic_efficiency": 0.9437451362609863,
    "pH_normalized": 0.2890998125076294,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.09918799251317978,
    "selective_product_yield": 0.009751594625413418,
    "transport_efficiency": 0.1848294585943222
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
      "current_mA": 200,
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
    "cost": 0.35258400440216064,
    "electrochemical_conversion": 0.009167621843516827,
    "electrochemical_selectivity": 0.6714441180229187,
    "energy_efficiency": 0.43016761541366577,
    "faradaic_efficiency": 0.4753786623477936,
    "ohmic_efficiency": 0.9233001470565796,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.072194404900074,
    "score": 0.2603040635585785,
    "selective_product_yield": 0.015018563717603683,
    "transport_efficiency": 0.45069533586502075
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.6
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
    "cost": 0.3529680073261261,
    "electrochemical_conversion": 0.015248425304889679,
    "electrochemical_selectivity": 0.5551259517669678,
    "energy_efficiency": 0.1269398033618927,
    "faradaic_efficiency": 0.31703460216522217,
    "ohmic_efficiency": 0.9931719303131104,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.072194404900074,
    "score": 0.1284509301185608,
    "selective_product_yield": 0.010020270012319088,
    "transport_efficiency": 0.32043495774269104
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
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
    "cost": 0.35315999388694763,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5038369297981262,
    "energy_efficiency": 0.07291747629642487,
    "faradaic_efficiency": 0.27105897665023804,
    "ohmic_efficiency": 0.9861299991607666,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2645636200904846
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
      "current_mA": 200,
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
    "cost": 0.3524399995803833,
    "electrochemical_conversion": 0.005875642877072096,
    "electrochemical_selectivity": 0.7046340703964233,
    "energy_efficiency": 0.6577547192573547,
    "faradaic_efficiency": 0.4916020333766937,
    "ohmic_efficiency": 0.9071263074874878,
    "pH_normalized": 0.23142993450164795,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.3945847451686859,
    "selective_product_yield": 0.02277730405330658,
    "transport_efficiency": 0.5124332904815674
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.3529680073261261,
    "electrochemical_conversion": 0.029402878135442734,
    "electrochemical_selectivity": 0.6862354278564453,
    "energy_efficiency": 0.45010796189308167,
    "faradaic_efficiency": 0.46035075187683105,
    "ohmic_efficiency": 0.9125494956970215,
    "pH_normalized": 0.2291157990694046,
    "precipitation_signal": 0.9925763010978699,
    "safety_risk": 0.072194404900074,
    "score": 0.12114717066287994,
    "selective_product_yield": 0.006924963556230068,
    "transport_efficiency": 0.46170035004615784
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.8
    },
    {
      "duration_s": 2400,
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
    "cost": 0.353736013174057,
    "electrochemical_conversion": 0.041517965495586395,
    "electrochemical_selectivity": 0.6585979461669922,
    "energy_efficiency": 0.44842618703842163,
    "faradaic_efficiency": 0.4535272419452667,
    "ohmic_efficiency": 0.926027774810791,
    "pH_normalized": 0.2301008403301239,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.3508780598640442,
    "selective_product_yield": 0.02032146044075489,
    "transport_efficiency": 0.4607071876525879
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3526799976825714,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.696466863155365,
    "energy_efficiency": 0.6177372336387634,
    "faradaic_efficiency": 0.46419817209243774,
    "ohmic_efficiency": 0.8934040069580078,
    "pH_normalized": 0.23062115907669067,
    "precipitation_signal": 0.9938013553619385,
    "safety_risk": 0.072194404900074,
    "score": 0.37948349118232727,
    "selective_product_yield": 0.0221148282289505,
    "transport_efficiency": 0.48542311787605286
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this world as a cathodic conversion whose observed performance is controlled by five coupled elements: effective electrode potential, delivered charge, electron partitioning between target and side reactions, mass/charge transport, and electrolyte-dependent acid/precipitation chemistry. The public final-assay channels are noisy, independently processed estimates, so small inconsistencies between conversion and selective yield should not be treated as literal violations of mass balance.

### 1. Effective potential and polarity

The clearest causal result was the polarity contrast. Batch 1 used S0/E0, +1.2 V, a 200 mA current cap, and 600 s. It was essentially inactive: final electrochemical conversion 0.0080, selectivity 0.0103, faradaic efficiency 0.0245, energy efficiency 0.0053, transport efficiency 0, and score 0. Batch 2 used the same materials, current cap, and duration but −1.2 V; it gave selectivity 0.6198, faradaic efficiency 0.3768, energy efficiency 0.2084, transport efficiency 0.4031, selective-product yield 0.0126, and score 0.1817. Thus the target-forming process is most plausibly a reduction requiring negative polarization. The tiny nonzero conversion reported in batch 1 is compatible with assay noise or a small background reaction.

A useful conceptual variable is an effective driving potential

E_eff = E_applied − ΔE_solvent − ΔE_electrolyte − ΔE_interface,

where the first two shifts have nominal public descriptors and ΔE_interface represents the fixed, hidden world residual and common electrode fixture. Target current could follow a Butler–Volmer-like or sigmoid dependence on negative overpotential. Competing reductions should rise more strongly at excessive negative overpotential.

The S0/E0 voltage series at 600 s supports that picture. Final results were:

- Batch 9, −0.5 V: selectivity 0.7046, faradaic efficiency 0.4916, energy efficiency 0.6578, transport efficiency 0.5124, selective yield 0.0228, score 0.3946.
- Batch 6, −0.8 V: selectivity 0.6714, faradaic efficiency 0.4754, energy efficiency 0.4302, transport efficiency 0.4507, selective yield 0.0150, score 0.2603.
- Batch 2, −1.2 V: selectivity 0.6198, faradaic efficiency 0.3768, energy efficiency 0.2084, selective yield 0.0126, score 0.1817.
- Batch 7, −1.6 V: selectivity 0.5551, faradaic efficiency 0.3170, energy efficiency 0.1269, selective yield 0.0100, score 0.1285.
- Batch 8, −2.0 V: selectivity 0.5038, faradaic efficiency 0.2711, energy efficiency 0.0729, reported selective yield 0, score 0.

The monotonic deterioration in selectivity and especially energy efficiency as the potential became more negative is stronger evidence than any individual near-zero conversion estimate. My explanation is that −0.5 V supplies enough cathodic activation for the target pathway, while larger magnitudes waste voltage and increasingly drive solvent, proton, impurity, or degradation reactions. The optimum may actually lie between 0 and −0.5 V; that region was not tested.

### 2. Charge, time, and conversion

A minimal process model would be

I_delivered = min(I_cap, I_kinetic(E_eff), I_transport),

Q = integral(I_delivered dt),

n_target ≈ integral(FE_target × I_delivered/(nF) dt),

conversion ≈ n_reacted/n_initial,

where FE_target incorporates both faradaic efficiency and chemical selectivity. All controlled experiments used a 200 mA cap, so neither the actual delivered current nor whether the cap was binding is identifiable.

At −0.8 V on S0/E0, final measured conversion generally increased with duration: 0.0092 at 600 s in batch 6, 0.0294 at 1200 s in batch 10, and 0.0415 at 2400 s in batch 11. This is consistent with cumulative charge driving conversion. Selectivity remained in a fairly narrow range, 0.6714, 0.6862, and 0.6586, while energy efficiency was 0.4302, 0.4501, and 0.4484. I therefore infer that this duration range mainly changes extent rather than the basic reaction regime.

The corresponding selective yields, however, were 0.0150, 0.0069, and 0.0203, producing scores 0.2603, 0.1211, and 0.3509. That nonmonotonicity is not chemically persuasive as a true yield law because the values are close to the assay noise scale and the public score has a sharp yield gate. Batch 12, at −0.5 V for 1200 s, likewise reported conversion clipped to 0 while selective yield was 0.0221. This cannot be interpreted as an exact physical mass balance; it indicates independent noisy channels near a low-concentration boundary. Batch 12 scored 0.3795, close to but below batch 9's 0.3946. With no exact replicates, I regard the difference between 600 and 1200 s at −0.5 V as unresolved rather than proof that 600 s is intrinsically superior.

### 3. Why the public score is highly sensitive to yield

The published weighted balanced-efficiency score uses conversion (0.10), selectivity (0.15), energy efficiency (0.15), faradaic efficiency (0.12), ohmic efficiency (0.08), selective-product yield (0.30), and transport efficiency (0.10), together with a multiplicative selective-yield gate at 0.02. The observations are consistent with a gate approximately like min(1, yield/0.02). Thus batches with otherwise reasonable efficiencies can lose much of their score when the noisy yield estimate falls below 0.02. Batch 6, for example, had good selectivity and energy metrics but yield 0.0150, whereas batch 9 crossed the gate with yield 0.0228. This explains much of the score jump without requiring an equally large discontinuity in the underlying chemistry.

### 4. Ohmic and transport processes

I expect cell current to be limited by a combination of kinetic resistance, solution resistance, and diffusion:

I_transport,lim ∝ n F A D C/δ,

V_cell ≈ E_kinetic + I R_solution + other losses,

ohmic efficiency ≈ 1 − (I R_solution/|V_cell|),

with bounded clipping in the synthetic observables. The public material dossier supports this structure: electrolytes differ in conductivity, diffusivity, diffusion-layer thickness, and supporting-electrolyte concentration; solvents multiply conductivity and diffusivity. The common electrode area, gap, and base contact resistance are fixed across the campaign but unknown.

Observed ohmic efficiencies were generally high, roughly 0.87–0.99 for productive negative-potential batches, so ohmic loss was not the dominant reason for failure. Transport efficiency varied more, approximately 0.18–0.54, and tracked performance more meaningfully. At −0.5 V, batch 9 had transport efficiency 0.5124 and faradaic efficiency 0.4916. Increasing negative magnitude did not rescue transport and sharply reduced energy efficiency, consistent with side-reaction current rather than useful mass transfer becoming dominant.

The current cap was never varied, so I cannot separate kinetic limitation, cap limitation, and mass-transfer limitation. An alternative explanation is that all runs were already transport-limited and voltage mainly changed side-current fractions. That alternative is compatible with the data.

### 5. Material, acid, and precipitation coupling

The matched-pair screen at −1.2 V, 200 mA, and 600 s gave:

- Batch 2, S0/E0: score 0.1817; selectivity 0.6198; faradaic efficiency 0.3768; transport efficiency 0.4031; precipitation signal 1.000.
- Batch 3, S1/E1: score 0; selectivity 0.4396; faradaic efficiency 0.2389; transport efficiency 0.2555; precipitation signal 0.714.
- Batch 4, S2/E2: score 0.0317; selectivity 0.4397; faradaic efficiency 0.3093; transport efficiency 0.2778; precipitation signal 0.
- Batch 5, S3/E3: score 0.0992; selectivity 0.4553; faradaic efficiency 0.1953; transport efficiency 0.1848; precipitation signal 0.

S0/E0 was therefore the best tested pair, but this screen confounds solvent and electrolyte: only S0/E0, S1/E1, S2/E2, and S3/E3 were compared. It does not establish that S0 and E0 are separately optimal, nor exclude a superior cross-combination.

The nominal dossier makes the pair behavior plausible but not fully predictable. E0 has relatively high conductivity but a thick diffusion layer and a comparatively strong precipitation tendency; S0 enhances conductivity but has lower relative diffusivity than S1. E0/S0 indeed showed precipitation signals near one in every tested batch, while E2/S2 and E3/S3 showed zero. A generic precipitation relation would be

precipitation if ion activity product > Ksp_eff(solvent),

and precipitation could reduce active ions, change interfacial area, or add resistance. Nevertheless, S0/E0 remained the best performer, so precipitation was neither fatal nor an explicit direct score penalty under the tested conditions. It may simply coexist with the productive pathway or reflect a spectator salt. No post-precipitation electrode characterization was available to discriminate these possibilities.

Normalized pH was about 0.23 for S0/E0, 0.204 for S1/E1, 0.171 for S2/E2, and 0.289 for S3/E3. This reflects the electrolyte acid concentration/pKa and solvent proton-activity coupling. Proton availability could affect target protonation, hydrogen evolution, and precipitate formation. However, pH was not independently manipulated, and no intermediate pH-meter measurement was taken, so its causal role is inseparable from material identity.

### 6. Safety and loading

Every batch used 0.040 mol limiting reagent in 0.080 L solvent, nominally 0.5 mol/L before small measurement withdrawals. This fixes concentration and prevents identification of concentration-order effects. Observed safety risk was approximately 0.0722 for S0 batches, 0.0956 for S1, 0.1136 for S2, and 0.1262 for S3, all well below the 0.65 limit. Within this campaign, potential and electrolysis time did not visibly increase the reported peak risk for the S0 series. That is an observation about the benchmark risk function, not evidence that real electrolysis would be risk-free.

### 7. How the explanation changed

Initially I expected an intermediate overpotential and duration optimum, with material conductivity and diffusivity controlling transport. Batch 1 versus batch 2 established the required negative polarity. Batches 2–5 shifted the working explanation toward S0/E0 despite its strong precipitation signal, demonstrating that the nominal property dossier alone could not rank materials. Batches 6–9 then showed that lower negative magnitude, not stronger driving voltage, improved nearly every efficiency component; batch 9 at −0.5 V became the leading condition. Batches 10–12 showed that time increases apparent conversion but that score changes are dominated by noisy selective yield near its multiplicative threshold. Consequently, I retained batch 9 as the best observed operating point but did not infer a sharply resolved 600 s kinetic optimum.

### 8. Scope, unidentifiable factors, and alternatives

The mechanism is supported only for this fixed synthetic world, 0.040 mol/0.080 L loading, 200 mA cap, four matched material pairs, potentials from +1.2 to −2.0 V, and durations from 600 to 2400 s. Important unidentifiable factors include actual current traces, electron stoichiometry, electrode area and resistance, individual solvent versus electrolyte effects, exact kinetic constants, product degradation rates, and the fixed latent material/interface residuals.

There were no exact replicate batches. Final-assay noise, clipping at zero, and the yield gate make low yields especially uncertain. UV-visible measurements broadly supported the efficiency ordering but did not provide independent conversion or product-identity confirmation under the restricted observation contract.

Plausible alternatives remain: the apparent voltage trend could combine true selectivity loss with voltage-dependent current limitation; precipitation might passivate the electrode beneficially rather than merely harm transport; S0/E0 superiority might arise from an unreported interaction residual rather than its nominal conductivity; and a cross-paired material or a potential between 0 and −0.5 V could outperform all tested batches. Within the measured domain, however, the most coherent explanation is a cathodic target reaction favored by modest negative polarization, with excessive overpotential diverting charge to side reactions and wasting energy, while transport, proton chemistry, precipitation, and a noisy low-yield scoring gate modulate the observed outcome.

## K2 封存报告

1. **Claims and laws tested.** No instance-specific prior or claimed true mechanism was supplied. The material dossier was only a nominal mechanistic prior and explicitly allowed hidden residuals.

- The self-developed claim that target formation requires negative polarization was strongly supported. With otherwise identical S0/E0 conditions, batch 1 at +1.2 V scored 0 and had near-floor selectivity and efficiency, whereas batch 2 at −1.2 V scored 0.1817.
- The law that excessive negative overpotential sacrifices selectivity and energy efficiency was supported over the tested range. At 600 s on S0/E0, moving from −0.5 V in batch 9 through −0.8, −1.2, −1.6, and −2.0 V in batches 6, 2, 7, and 8 progressively reduced energy efficiency and generally reduced selectivity and score. This evidence changed my emphasis from “stronger driving potential may improve conversion” to “modest negative polarization is preferable.”
- The initial expectation of an interior potential optimum was not demonstrated. The best tested point was the least-negative value, −0.5 V in batch 9; potentials between 0 and −0.5 V were untested. Thus the existence and location of an optimum remain open.
- A cumulative-charge relationship for conversion was qualitatively supported. At −0.8 V, measured conversion generally rose from batch 6 at 600 s to batches 10 and 11 at 1200 and 2400 s. However, selective yield and score were nonmonotone, so a simple law that longer electrolysis improves the objective was contradicted by the score observations or, more cautiously, left unresolved because the yield estimates were noisy near the scoring gate.
- S0/E0 was supported as the best of the four matched pairs screened in batches 2–5. The stronger claim that S0 and E0 are independently optimal was untested because no cross-factorial combinations were run.
- A simple claim that visible precipitation must harm performance was contradicted in this domain: S0/E0 repeatedly had precipitation signal near one yet produced the best scores. Precipitation could still have subtler beneficial or harmful interfacial effects.
- Laws for current-cap dependence, concentration dependence, separable solvent/electrolyte effects, acid causality, and exact kinetic or mass-transfer constants were untested. Batch 12 also showed why independent noisy assay channels cannot be treated as an exact mass balance: its conversion was clipped to zero while selective yield was 0.0221.

2. **Most informative additional experiment.** I would run the batch-9 recipe on S0/E0 at −0.30 V, 200 mA, and 600 s, with the same 0.040 mol reagent and 0.080 L solvent. This directly challenges the leading explanation that −0.5 V is already beyond the required activation threshold and that additional cathodic overpotential mainly drives side reactions. If −0.30 V retained selective yield at or above the 0.02 gate while matching or improving batch 9's selectivity and energy efficiency, I would move the proposed optimum toward zero and strengthen the overpotential-loss explanation. If efficiency remained high but conversion and yield collapsed below the gate, I would conclude that −0.5 V lies near a kinetic activation threshold and that the best score reflects a conversion–efficiency compromise. If selectivity and efficiency also fell sharply, I would weaken the monotonic overpotential interpretation and consider a narrow interfacial-potential window. A result indistinguishable from batch 9 within assay uncertainty would imply a performance plateau and would not locate the optimum.

3. **Unused evidence, reliability, and goal effects.** I relied mainly on processed UV-visible and final-assay estimates. I did not inspect or model the raw spectra, raw mass-balance packets, calibration traces, or replicate-level signals. No pH-meter experiment was performed. Detailed double-layer-capacitance, supporting-electrolyte, acid, Ksp, cost, and sample-consumption information was not quantitatively fitted. The high precipitation signals were noted but not independently characterized.

The least reliable blind predictions are the 7200 s extrapolations, especially Q11 at 500 mA, because current-cap behavior and long-time degradation or saturation were never measured. Q05, Q07, and Q09 are also weak because they use solvent/electrolyte cross-combinations absent from the campaign. Positive-polarity predictions are reliable in direction but not in their exact near-zero values because clipping and assay noise dominate. Predicted scores are particularly uncertain when selective yield may lie near 0.02. The batch-9 recommendation is the highest observed score, but its exact superiority over batch 12 is not highly secure: there were no exact replicates, and both yields were just above the gate. Untested potentials nearer zero, cross-paired materials, or different current caps could outperform it.

The assigned score-maximization goal materially shaped evidence collection. After a short material and polarity screen, experiments concentrated on exploiting S0/E0 and negative potentials rather than completing a factorial design, replicating batches, or isolating current, concentration, pH, and precipitation effects. Using every intermediate measurement and final assay improved optimization feedback but left mechanism-identification gaps. There was no clear conflict with safety—the observed risks remained well below the limit—but the objective encouraged accepting the precipitating S0/E0 system because its public score was superior.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.61,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.4,
        "upper80": 0.62
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.43,
        "upper80": 0.6
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.35,
        "lower80": 0.08,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.002,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.45,
        "upper80": 0.69
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.065
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.045
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.57,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.36,
        "upper80": 0.59
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.39,
        "upper80": 0.58
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.43,
        "lower80": 0.32,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.065,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.56,
        "lower80": 0.43,
        "upper80": 0.67
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.045
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.065
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.013,
        "lower80": 0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.46,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.33,
        "lower80": 0.19,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.41,
        "lower80": 0.28,
        "upper80": 0.52
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.36,
        "lower80": 0.24,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.035,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.35,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.045
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.065
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.013,
        "lower80": 0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.53,
        "lower80": 0.38,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.19,
        "upper80": 0.45
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.29,
        "lower80": 0.18,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.015,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.045
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.11,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.21,
        "upper80": 0.48
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.018,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.045
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.47,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.29,
        "lower80": 0.15,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.37,
        "lower80": 0.24,
        "upper80": 0.49
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.36,
        "lower80": 0.24,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.07,
        "upper80": 0.35
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.14,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.045
      }
    }
  ],
  "rationale": "Predictions anchor the negative-polarity S0/E0 cases to batches 6, 10, and 11, with adjustments for charge per mole, current-dependent transport, and long-duration saturation. Positive-polarity batches are predicted near the assay floor based on batch 1. Cross-material cases use the measured matched-pair ordering plus nominal conductivity, diffusivity, and potential-shift information; their intervals are wider because solvent–electrolyte interactions and current-cap effects were not independently identified. Score intervals also include strong sensitivity to the 0.02 selective-yield gate and clipped final-assay noise."
}
```
