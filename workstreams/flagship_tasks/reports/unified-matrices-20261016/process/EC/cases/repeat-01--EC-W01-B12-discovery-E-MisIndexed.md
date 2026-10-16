# repeat-01/EC-W01-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\Projects\ChemWorld-local-research\20261016-unified-matrices\attempt-01\repeat-01\EC-W01-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## H1 [tentative]
At fixed reagent loading, conversion should increase with electrolysis duration and with the magnitude of driving potential until limited by current/transport; excessive drive may lower selectivity and energy efficiency. Opposite potential signs may not be symmetric because solvent and electrolyte shift the effective potential.

## H2 [tentative]
Transport and ohmic metrics should track nominal conductivity and diffusivity, but selectivity/faradaic efficiency may have independent material interactions. E0/S0 is predicted to favor ohmic performance; E1 may favor mass transport; E3 carries a precipitation risk.

## Planned tests
Use 0.020 mol reagent in 0.040 L total solvent as a common loading. First establish sign/potential/current/time response in one material pair, then compare solvents/electrolytes at a shared condition and include repeats or segmented exposures where most informative. UV–vis observations will be used before termination in each batch; final assay is authoritative. A monotonic-duration claim will be weakened if the longer exposure does not materially raise conversion beyond stated uncertainty, and a simple nominal-property ranking will be weakened by material reversals.

### v2 · 公开事件 84

# Electrochemical hypothesis notebook

## H1 [supported in tested scope]
The response has a bounded operating window rather than improving monotonically with drive. At S0/E0 and 3000 s, +1.0 V/100 mA gave conversion 0.053 and selectivity 0.949 (runner-operation-0014). Reversing to -1.0 V reduced both to 0.025 and 0.602 (runner-operation-0021), while +2.0 V collapsed conversion/selectivity and transport/faradaic performance (runner-operation-0028). Thus potential sign and excessive positive drive affect chemistry, not merely rate. Testable consequence: blind conditions near +1 V should outperform matched -1 V and +2 V conditions, while the location of the optimum may shift with material standard-potential shifts.

## H2 [supported, nonlinear current-cap dependence]
At +1.0 V for 3000 s in S0/E0, lowering the cap from 100 to 20 mA reduced conversion (0.053 to 0.018) but improved faradaic/transport/energy efficiencies; increasing it to 500 mA collapsed conversion, selectivity, transport, and energy efficiency (runner-operation-0014, runner-operation-0035, runner-operation-0042). Because current is a cap rather than guaranteed delivery, this supports an intermediate-cap optimum with transport/side-reaction limitation, not a linear current law.

## H3 [supported over 300-12000 s, with caveat]
At +1.0 V/100 mA in S0/E0, conversion increased from 0.014 at 300 s to 0.053 at 3000 s and 0.234 at 12000 s (runner-operation-0007, runner-operation-0014, runner-operation-0049). The large long-time rise exceeds assay resolution and is roughly compatible with accumulated charge controlling conversion, while selectivity remained high (~0.94-0.95). Energy/faradaic/transport efficiencies declined at long duration, so yield gains trade against efficiency. The 300 s endpoint is near the conversion uncertainty and selective yield was clipped at zero, so very-short-time kinetics remain poorly resolved.

## H4 [material effects supported; simple nominal ranking rejected]
At the shared +1.0 V/100 mA/3000 s/S0 condition, E1-E3 all gave somewhat higher conversion than E0, but their efficiency fingerprints differed (runner-operation-0056, -0063, -0070 versus -0014). E1 had the strongest combined faradaic/transport/energy metrics and the best observed campaign score. E2 reduced selectivity modestly and showed near-zero precipitation signal; E3 had lower faradaic/transport performance and zero precipitation signal despite high energy efficiency. The precipitation observable therefore does not follow the naive expectation that the nominally most precipitation-prone E3 should have the largest numerical signal; its direction or coupling cannot be assumed from the label alone.

Solvent S1 improved conversion and energy/transport performance over S0 with E0, whereas S2 lowered conversion and especially selectivity (runner-operation-0077, -0084 versus -0014). S3 was not tested, and material interactions remain unresolved; extrapolation should use nominal shifts only cautiously.

## Predictive working model
Within the tested loading (0.020 mol in 0.040 L), treat conversion as increasing approximately with delivered charge/time only inside a window centered near +1 V and moderate current cap. Multiply this kinetic term by potential-window, current/transport, electrolyte, and solvent factors; treat selectivity and faradaic efficiency as separate declining penalties at reversed/excess potential or excessive current. Do not infer delivered current equals the cap. For untested combinations, expect E1 and S1 to be favorable around +1 V, E2 intermediate but slightly less selective, and S2 unfavorable; uncertainty is larger for S3 and for interactions.

## Limitations
Most contrasts are single batches and thus numerical differences are not repeatability evidence. Final-assay standard uncertainties are roughly 0.01 for conversion/yield, 0.012 for selectivity/faradaic/ohmic, 0.014 for transport, and 0.016 for energy. Batch 8 is the operating recommendation candidate because it had the highest observed score, but batch 7 produced the largest measured selective yield through long exposure.

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
    "electrochemical_conversion": 0.014311172999441624,
    "electrochemical_selectivity": 0.9495708346366882,
    "energy_efficiency": 0.8036100268363953,
    "faradaic_efficiency": 0.8346197605133057,
    "ohmic_efficiency": 0.9695378541946411,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.8059160113334656
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
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.05317157879471779,
    "electrochemical_selectivity": 0.9492443203926086,
    "energy_efficiency": 0.762840986251831,
    "faradaic_efficiency": 0.7873738408088684,
    "ohmic_efficiency": 0.9783756732940674,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5361904501914978,
    "selective_product_yield": 0.06647510826587677,
    "transport_efficiency": 0.8136307001113892
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.024985840544104576,
    "electrochemical_selectivity": 0.6022707223892212,
    "energy_efficiency": 0.2475184053182602,
    "faradaic_efficiency": 0.36521705985069275,
    "ohmic_efficiency": 0.9651492834091187,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
    "safety_risk": 0.072194404900074,
    "score": 0.11608778685331345,
    "selective_product_yield": 0.007962911389768124,
    "transport_efficiency": 0.381773978471756
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2
    },
    {
      "duration_s": 3000,
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
    "cost": 0.2849999964237213,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9879685640335083,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.072194404900074,
    "score": 0.0032642087899148464,
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.2828400135040283,
    "electrochemical_conversion": 0.017669126391410828,
    "electrochemical_selectivity": 0.9456571340560913,
    "energy_efficiency": 0.8735303282737732,
    "faradaic_efficiency": 0.925710916519165,
    "ohmic_efficiency": 0.9937994480133057,
    "pH_normalized": 0.2344796061515808,
    "precipitation_signal": 0.9868980646133423,
    "safety_risk": 0.072194404900074,
    "score": 0.5633008480072021,
    "selective_product_yield": 0.02182122692465782,
    "transport_efficiency": 0.9152014851570129
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28859999775886536,
    "electrochemical_conversion": 0.0021511756349354982,
    "electrochemical_selectivity": 0.0042426493018865585,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02405594103038311,
    "ohmic_efficiency": 0.8933091163635254,
    "pH_normalized": 0.23120366036891937,
    "precipitation_signal": 0.9975283145904541,
    "safety_risk": 0.072194404900074,
    "score": 0.04047219082713127,
    "selective_product_yield": 0.010337181389331818,
    "transport_efficiency": 0.0
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
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
    "cost": 0.2874000072479248,
    "electrochemical_conversion": 0.233635812997818,
    "electrochemical_selectivity": 0.9370536208152771,
    "energy_efficiency": 0.7077623009681702,
    "faradaic_efficiency": 0.7202739119529724,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23021826148033142,
    "precipitation_signal": 0.982570469379425,
    "safety_risk": 0.072194404900074,
    "score": 0.5739874243736267,
    "selective_product_yield": 0.2170039266347885,
    "transport_efficiency": 0.7236742973327637
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
      "duration_s": 3000,
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.06675411015748978,
    "electrochemical_selectivity": 0.9505428075790405,
    "energy_efficiency": 0.9279391765594482,
    "faradaic_efficiency": 0.9312843680381775,
    "ohmic_efficiency": 0.9921718239784241,
    "pH_normalized": 0.19805485010147095,
    "precipitation_signal": 0.8569796681404114,
    "safety_risk": 0.072194404900074,
    "score": 0.5863896012306213,
    "selective_product_yield": 0.04778366535902023,
    "transport_efficiency": 0.9247890114784241
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.06444577872753143,
    "electrochemical_selectivity": 0.9100825190544128,
    "energy_efficiency": 0.923613429069519,
    "faradaic_efficiency": 0.8448852896690369,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.15247075259685516,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.072194404900074,
    "score": 0.5729213953018188,
    "selective_product_yield": 0.07821516692638397,
    "transport_efficiency": 0.8657165169715881
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
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.0697348415851593,
    "electrochemical_selectivity": 0.9416318535804749,
    "energy_efficiency": 0.9195693731307983,
    "faradaic_efficiency": 0.7084161639213562,
    "ohmic_efficiency": 0.9700130224227905,
    "pH_normalized": 0.27186429500579834,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5340569615364075,
    "selective_product_yield": 0.04771909862756729,
    "transport_efficiency": 0.7097657322883606
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
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.29980000853538513,
    "electrochemical_conversion": 0.07919760048389435,
    "electrochemical_selectivity": 0.9466625452041626,
    "energy_efficiency": 0.9413552284240723,
    "faradaic_efficiency": 0.8480003476142883,
    "ohmic_efficiency": 0.9745150804519653,
    "pH_normalized": 0.23318053781986237,
    "precipitation_signal": 0.9957859516143799,
    "safety_risk": 0.09559440612792969,
    "score": 0.5756818056106567,
    "selective_product_yield": 0.06440029293298721,
    "transport_efficiency": 0.8551802635192871
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.3253999948501587,
    "electrochemical_conversion": 0.039947934448719025,
    "electrochemical_selectivity": 0.7323815226554871,
    "energy_efficiency": 0.7168063521385193,
    "faradaic_efficiency": 0.6908911466598511,
    "ohmic_efficiency": 0.9835156798362732,
    "pH_normalized": 0.24616383016109467,
    "precipitation_signal": 0.9843462109565735,
    "safety_risk": 0.1135944053530693,
    "score": 0.47016453742980957,
    "selective_product_yield": 0.05330589413642883,
    "transport_efficiency": 0.7121161222457886
  }
}
```

## K1 封存报告

## Scope and experimental basis

I studied 12 batches, all prepared with 0.020 mol of the anonymous limiting reagent and 0.040 L of one solvent, corresponding to a nominal initial loading of 0.50 mol L⁻¹ before sampling. Each batch was assigned one anonymous electrolyte profile, a potential, a current cap, and an electrolysis duration. Every batch received one UV–visible measurement after electrolysis and a final multichannel assay after termination. Therefore, the strongest comparisons are controlled contrasts within this common loading; concentration effects, mixed solvents, staged potentials, and most solvent–electrolyte interactions were not tested.

## Proposed working mechanism

I think the system is an electrochemical conversion with four coupled layers:

1. **Potential-dependent interfacial activation.** Productive conversion requires the applied potential to fall inside a finite window. A useful conceptual variable is an effective overpotential

   η = V_applied − [E₀ + ΔE_electrolyte + ΔE_solvent + ΔE_latent],

   where the declared material potential shifts contribute to the bracketed term and ΔE_latent represents fixed, world-specific interfacial or solvation effects. Productive charge transfer rises as η enters the correct window, but reversed or excessive drive opens inefficient or destructive pathways.

2. **Charge accumulation and conversion.** Inside that window, conversion increases with effective delivered charge rather than with nominal duration alone. A possible phenomenological form is

   q_eff = t × min(I_cap, I_ohmic, I_transport, I_kinetic),

   X = X_max[1 − exp(−k_mat q_eff/n₀)],

   where n₀ is initial reagent amount and k_mat includes electrolyte and solvent effects. This is not a fitted equation; it summarizes the observed duration and current-cap behavior.

3. **Competing efficiency losses.** Faradaic efficiency represents the fraction of delivered charge entering productive chemistry, transport efficiency represents mass-transfer access to the interface, and ohmic efficiency represents resistive delivery. I would write productive yield schematically as

   Y_product ≈ X × S × f_assay,

   with selectivity S penalized by wrong-sign potential, excessive potential, excessive current density, and unfavorable solvent coupling. The final-assay selective-product-yield channel is evidently not an exact algebraic product X×S: near the detection/noise floor it can be clipped or differ by more than simple propagation would predict.

4. **Acid/base and precipitation coupling.** Electrolytes change pH, ionic conductivity, diffusion, double-layer properties, and precipitation behavior simultaneously. These affect kinetics and transport, but the numerical `precipitation_signal` cannot safely be interpreted as a direct amount of precipitate: its direction was inconsistent with a naive ranking based only on nominal salt concentration and Ksp.

## Evidence for the potential window

Batches 1–4 establish that the voltage response is strongly nonmonotonic.

- **Batch 2**, the reference condition S0/E0 at +1.0 V, 100 mA, and 3000 s, gave final conversion 0.0532, selectivity 0.9492, faradaic efficiency 0.7874, transport efficiency 0.8136, energy efficiency 0.7628, and score 0.5362.
- **Batch 3** changed only the potential sign to −1.0 V. Conversion fell to 0.0250, selectivity to 0.6023, faradaic efficiency to 0.3652, transport efficiency to 0.3818, and energy efficiency to 0.2475; the score was 0.1161. Ohmic efficiency remained high at 0.9651. Thus the loss cannot be explained purely by bulk resistance. It indicates a wrong interfacial direction or a competing reaction at negative potential.
- **Batch 4** used +2.0 V at otherwise identical settings. Its reported conversion, selectivity, transport efficiency, and energy efficiency were all zero, while faradaic efficiency was only 0.0283 and score 0.00326. Ohmic efficiency was still 0.9880. This is strong evidence against a monotonic voltage-rate law. Excess positive drive apparently produces an unproductive interfacial regime, such as solvent/electrolyte discharge, passivation, degradation, or benchmark-equivalent side chemistry.
- **Batch 1** used the favorable +1.0 V polarity but only 300 s. Conversion was 0.0143 with selectivity 0.9496. Its selective-yield estimate was clipped to zero, so that very short exposure was near the useful assay floor even though the selectivity channel remained high.

I therefore infer a productive potential window centered approximately near +1 V for S0/E0. The exact optimum was not localized because only −1, +1, and +2 V were tested. It may move between materials because solvents and electrolytes have declared standard-potential shifts and hidden fixed residuals.

## Duration and accumulated charge

The duration series at S0/E0, +1.0 V, and 100 mA was:

- Batch 1, 300 s: conversion 0.0143, selectivity 0.9496, energy efficiency 0.8036, faradaic efficiency 0.8346, transport efficiency 0.8059.
- Batch 2, 3000 s: conversion 0.0532, selectivity 0.9492, energy efficiency 0.7628, faradaic efficiency 0.7874, transport efficiency 0.8136.
- Batch 7, 12000 s: conversion 0.2336, selectivity 0.9371, energy efficiency 0.7078, faradaic efficiency 0.7203, transport efficiency 0.7237.

The large increase from 3000 to 12000 s is well above the stated conversion uncertainty of about 0.01 and supports charge/time accumulation. Selectivity remained high, so the main long-time benefit was greater extent rather than a change in product identity. Batch 7 produced the largest measured selective-product yield, 0.2170, close to its conversion multiplied by selectivity.

Efficiency declined with prolonged operation. This suggests increasing polarization, depletion near the interface, accumulation of an inhibitory species, or progressively larger parasitic charge. Conversion therefore rises with time in the tested interval, but energetic productivity does not. I cannot determine whether conversion would ultimately saturate, decline through degradation, or continue approximately linearly beyond 12000 s.

## Nonlinear effect of current cap

At S0/E0, +1.0 V, and 3000 s:

- Batch 5 at 20 mA gave conversion 0.0177, selectivity 0.9457, faradaic efficiency 0.9257, transport efficiency 0.9152, energy efficiency 0.8735, and score 0.5633.
- Batch 2 at 100 mA gave conversion 0.0532, selectivity 0.9492, faradaic efficiency 0.7874, transport efficiency 0.8136, energy efficiency 0.7628, and score 0.5362.
- Batch 6 at 500 mA gave conversion 0.00215, selectivity 0.00424, faradaic efficiency 0.0241, zero reported transport and energy efficiencies, and score 0.0405.

A low cap sacrifices rate but preserves efficient, selective chemistry. Raising the cap from 20 to 100 mA increases conversion while lowering efficiency moderately. Raising it to 500 mA causes a qualitative collapse rather than fivefold acceleration. My preferred explanation is that 500 mA exceeds the combined mass-transfer and interfacial-kinetic capacity, producing severe concentration polarization and side reactions. An alternative is current-induced deactivation or benchmark-equivalent electrode fouling. Since the instrument reports a configured cap rather than the full current-time trace, actual delivered charge is unidentifiable. The cap must not be treated as guaranteed constant current.

The high ohmic efficiencies in batches 2 and 5, and the continued value of 0.8933 even in failed batch 6, show that bulk resistance alone is insufficient to explain the collapse. Transport and reaction selectivity are the dominant nonlinearities.

## Electrolyte effects

Batches 2 and 8–10 compared E0–E3 at S0, +1.0 V, 100 mA, and 3000 s:

- E0, batch 2: conversion 0.0532, selectivity 0.9492, faradaic 0.7874, transport 0.8136, energy 0.7628, pH-normalized 0.2295, precipitation signal 1.000, score 0.5362.
- E1, batch 8: conversion 0.0668, selectivity 0.9505, faradaic 0.9313, transport 0.9248, energy 0.9279, pH-normalized 0.1981, precipitation signal 0.8570, score 0.5864.
- E2, batch 9: conversion 0.0644, selectivity 0.9101, faradaic 0.8449, transport 0.8657, energy 0.9236, pH-normalized 0.1525, precipitation signal 0.00819, score 0.5729.
- E3, batch 10: conversion 0.0697, selectivity 0.9416, faradaic 0.7084, transport 0.7098, energy 0.9196, pH-normalized 0.2719, precipitation signal 0, score 0.5341.

All three alternatives gave somewhat higher measured conversion than E0, but they did so with distinct efficiency fingerprints. E1 was the best balanced electrolyte in this tested setting: it preserved high selectivity while increasing conversion and all three major efficiency measures. Its nominal high diffusivity and thin diffusion layer are qualitatively consistent with the strong transport efficiency, while its modest nominal conductivity did not create an observed ohmic problem.

E2 had high energy efficiency and useful transport, but selectivity was lower. Its stronger acidity is consistent with the lowest observed normalized pH, although the pH metric is a normalized synthetic observable rather than a direct reported pH value. E3 gave the highest conversion point estimate but substantially lower faradaic and transport efficiencies than E1 or E2. This is consistent with its low nominal diffusivity and relatively thick diffusion layer, although hidden material residuals and potential shifts prevent a unique attribution.

The precipitation-signal ordering—near one for E0, 0.857 for E1, near zero for E2, and zero for E3—does not follow the simplest expectation that E3's nominal salt/Ksp combination should generate the largest amount of solid. Plausible alternatives are that a low signal corresponds to stronger precipitation, that the channel measures absence of soluble precursor, or that precipitation is coupled to pH and conversion rather than nominal Ksp alone. Because no physical solid amount was measured independently, I leave the sign of this observable unresolved.

## Solvent effects

Batches 2, 11, and 12 compared S0, S1, and S2 with E0 at +1.0 V, 100 mA, and 3000 s:

- S0, batch 2: conversion 0.0532, selectivity 0.9492, faradaic 0.7874, transport 0.8136, energy 0.7628, score 0.5362.
- S1, batch 11: conversion 0.0792, selectivity 0.9467, faradaic 0.8480, transport 0.8552, energy 0.9414, score 0.5757.
- S2, batch 12: conversion 0.0399, selectivity 0.7324, faradaic 0.6909, transport 0.7121, energy 0.7168, score 0.4702.

S1 was favorable: it increased conversion and efficiency without a meaningful selectivity loss relative to assay uncertainty. Its nominal greater diffusivity may contribute to transport, while its potential shift or solvation environment may place +1 V closer to the productive window.

S2 was unfavorable at this fixed electrical setting. Its reduced nominal conductivity and proton activity can explain part of the lower transport/faradaic performance, but the large selectivity decrease suggests an interfacial or solvation change rather than resistance alone. S2 also has a +0.20 V declared standard-potential shift, so +1 V may correspond to a different effective overpotential. A shifted applied voltage might rescue S2; that was not tested.

S3 was not tested experimentally. Any prediction for it must be an extrapolation from nominal properties—moderate conductivity, low diffusivity, low double-layer capacitance, and a positive potential shift—and should carry substantially greater uncertainty.

## UV–visible evidence and assay consistency

The post-electrolysis UV–visible measurements reported the efficiency-related channels before termination. They broadly identified the same regimes as the final assays: high efficiencies for the 20 mA condition and E1/E2 cases, and near-zero transport/energy performance for +2 V and 500 mA. Exact UV and final-assay values were not identical, as expected from their different calibration/noise models and sampling. I interpret agreement in regime classification as corroboration, not as proof that either instrument directly resolves the mechanism.

The final assay stated standard uncertainties of approximately 0.01 for conversion and selective yield, 0.012 for selectivity, faradaic efficiency, and ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Several small differences between individual material conditions are therefore only suggestive. The large voltage, high-current, and long-duration effects are much more secure.

## Selective-yield channel and scoring

Selective yield generally increased with conversion under selective conditions, but it was not a deterministic product of the conversion and selectivity channels. For example, batch 1 reported conversion 0.0143 and selectivity 0.9496 but yield zero; batch 2 reported yield 0.0665 despite conversion 0.0532; and batch 9 reported yield 0.0782 with conversion 0.0644. These deviations are comparable to or somewhat larger than the individual nominal noise scales near low signal. Possible causes include independent calibrations, clipping, process-proxy uncertainty, or a different denominator. I therefore use selective yield as an independently calibrated outcome rather than forcing exact mass-balance algebra.

The sealed operating recommendation was batch 8 because it had the highest observed balanced score, 0.5864, and a strong combination of selectivity and efficiencies. This does not mean it maximized every scientific response. Batch 7 had by far the largest measured selective yield, 0.2170, but required 12000 s and had lower energy, faradaic, and transport efficiencies. Batch 5 had very high efficiencies at 20 mA but low conversion. The preferred condition consequently depends on whether the objective values throughput, material yield, electrical efficiency, or the published balanced score.

## Safety and cost observations

At the common loading, the reported safety risk after setup was approximately 0.072 for the tested batches, far below the stated 0.65 limit. No tested operating condition approached the safety constraint in the public measurements. This does not establish safety outside the studied voltage, current, duration, or loading ranges. In particular, the mechanistically failed +2 V and 500 mA regimes should not be interpreted as safe merely because the aggregate reported risk stayed low.

## What changed the explanation

The initial hypothesis was that conversion would rise with duration and drive until transport limitations appeared. Batches 1, 2, and 7 supported the duration component. Batch 5 showed the expected rate–efficiency tradeoff at low current. However, batches 4 and 6 forced a stronger revision: excessive potential or current did not merely reduce marginal efficiency; it collapsed productive chemistry. The resulting explanation is a finite interfacial operating window with nonlinear side-reaction or deactivation branches.

The nominal material dossier initially suggested that bulk conductivity and diffusivity might largely rank performance. Batches 8–12 rejected that as a complete account. E1 outperformed the more conductive E0 in combined efficiency, E3 maintained high energy efficiency despite weak transport/faradaic metrics, and solvent S2 caused a major selectivity penalty. Potential shifts, proton activity, double-layer behavior, solvation, and hidden fixed residuals must therefore be coupled to bulk transport.

## Unidentifiable factors and limitations

- Actual current-time traces, electrode potentials after ohmic drop, electrode area, and delivered charge were not observed.
- The base redox potential, electron stoichiometry, identities of products and side products, and electrode surface state are hidden.
- Only one reagent concentration and total volume were tested, so kinetic order and concentration dependence are unidentified.
- Most conditions were single batches. Differences near the stated uncertainty cannot be separated from repeatability variation.
- Only a sparse set of voltages, currents, and durations was sampled; the precise optimum and functional curvature are unknown.
- Solvent and electrolyte interactions were largely untested. Electrolytes were compared only in S0, and solvents only with E0.
- S3 was not studied.
- Temperature evolution, mixing, local pH, and physical precipitation were not independently measured.
- The precipitation-signal direction is ambiguous, and selective yield is not exactly algebraically tied to conversion and selectivity.
- Hidden world-specific residuals are fixed across the campaign but cannot be separated from the anonymous material identities with this design.

## Plausible alternative mechanisms

The observations are consistent with mass-transfer limitation and parasitic electrochemistry, but they do not uniquely prove them. Alternatives include electrode passivation at high potential/current, field-dependent catalyst or substrate deactivation, local pH excursions, precipitation blocking the interface, or a sharp change in double-layer structure. The negative-potential condition might represent the reverse reaction, a distinct low-selectivity reduction, or simply insufficient driving force after material potential shifts. Long-time efficiency loss might arise from reactant depletion, product inhibition, heating not exposed in the final data, or gradual electrode fouling.

These alternatives make similar predictions for the tested endpoints. Distinguishing them would require current-time traces, staged-potential experiments, repeats, concentration variation, intermediate time courses, independent solid analysis, or cross-factor solvent/electrolyte tests, none of which were performed here.

## Final predictive account

Within the studied 0.50 mol L⁻¹ loading, I would predict performance by first calculating a material-shifted effective potential, applying a bell-shaped productive-window factor centered near the empirically favorable +1 V region, and then limiting charge delivery by the smallest of current cap, ohmic capacity, and mass-transport capacity. Conversion accumulates with effective charge and duration, while selectivity and faradaic efficiency receive steep penalties at wrong-sign potential, excessive positive potential, and excessive current cap. Electrolyte E1 and solvent S1 appear favorable around the tested setting; E2 is efficient but somewhat less selective; E3 is transport/faradaic limited; S2 is both slower and less selective at +1 V. These are evidence-based local predictions, not universal rankings, because potential shifts and interactions can move the operating window.

## K2 封存报告

1. **Supported, contradicted, and untested claims**

No instance-specific mechanism or quantitative response prior was supplied. The material dossier provided nominal properties and cautioned that hidden residuals and solvent coupling could alter them; it did not supply a response law. The initial laws were therefore self-developed hypotheses.

The proposed duration/charge law was supported locally. At S0/E0, +1 V, and 100 mA, conversion rose from 0.0143 at 300 s in batch 1 to 0.0532 at 3000 s in batch 2 and 0.2336 at 12000 s in batch 7. Selectivity stayed near 0.94–0.95. This changed the duration hypothesis from tentative to supported over 300–12000 s, although saturation beyond that range remains untested.

A monotonic applied-potential law was contradicted. Relative to batch 2, reversing the potential to −1 V in batch 3 reduced selectivity from 0.949 to 0.602 and sharply reduced faradaic, transport, and energy efficiencies. Raising the potential to +2 V in batch 4 collapsed conversion, selectivity, transport efficiency, and energy efficiency to reported zeros. These observations changed my explanation from a simple drive-dependent rate law to a finite productive-potential window with competing reactions or deactivation outside it.

A linear current law was also contradicted. At 20 mA, batch 5 had low conversion but excellent efficiencies; at 100 mA, batch 2 had higher conversion with moderate efficiency loss; at 500 mA, batch 6 collapsed to conversion 0.0022, selectivity 0.0042, and nearly zero transport and energy efficiency. This supported an intermediate-current operating region and a transport, interfacial, or side-reaction limitation.

A simple ranking by nominal conductivity was unsupported as a complete explanation. E1 in batch 8 outperformed E0 in batch 2 across the combined efficiency profile despite E0's greater nominal bulk conductivity. E2 and E3 in batches 9 and 10 produced distinct selectivity, faradaic, transport, pH, and precipitation signatures. The evidence supported coupled roles for diffusivity, diffusion-layer thickness, potential shifts, acidity, and hidden interfacial residuals rather than one-property control.

Solvent effects were supported for the tested contrasts: S1 improved conversion and energy performance in batch 11 relative to S0 in batch 2, whereas S2 lowered conversion and selectivity in batch 12. S3, concentration dependence, kinetic order, mixed solvents, electrode history, exact charge delivery, and most solvent–electrolyte interactions remained untested. The sign and physical meaning of the precipitation signal also remained unresolved because batches 8–10 did not follow a naive nominal-Ksp ranking.

2. **One additional discriminating experiment**

I would repeat the batch-6 composition and +1 V/500 mA active condition, but deliver the 3000 s active electrolysis as ten 300 s pulses separated by low-current, near-open-circuit relaxation periods. The total active time and nominal high-current exposure would match batch 6. I would take UV–visible measurements after selected pulses and perform the normal final assay.

The leading explanation is reversible concentration polarization: high current depletes productive reactant near the electrode and favors parasitic chemistry. The principal alternative is rapid irreversible passivation or high-current chemical degradation.

If relaxation restored performance—especially if final transport, faradaic efficiency, selectivity, and conversion moved substantially upward from batch 6 toward batches 2 or 5—I would strengthen the reversible transport-limitation explanation. A saw-tooth recovery across intermediate measurements would be particularly diagnostic.

If the pulsed batch remained near batch 6 despite the rests, I would weaken the reversible-transport account and favor irreversible passivation, product/electrolyte degradation, or an intrinsically unselective high-current interfacial pathway. If only transport efficiency recovered while selectivity and faradaic efficiency remained poor, I would infer two coupled limitations: reversible mass transfer plus a separate high-current side reaction. This experiment would still not identify the chemical species involved, but it would distinguish recovery kinetics from persistent damage using the existing continuous batch as the control.

3. **Unused evidence, reliability, and goal effects**

The detailed raw spectra and most characterization artifacts were not inspected; analysis used processed estimates and the supplied peak summaries. Spectral line shapes, minor assignments, baselines, and replicate traces therefore did not contribute to the model. The nominal capacitance, acid concentration, pKa, Ksp, and potential-shift values were used only qualitatively because the design could not separate their effects. Cost and safety were recorded but varied little at the common loading and were not mechanistically informative. The pH and precipitation channels were not used in the blind quantitative predictions because those metrics were not requested and the precipitation channel's direction was ambiguous. There were no replicate batches, current-time traces, direct delivered-charge measurements, local temperature data, or independent solid analyses.

The least reliable blind predictions are Q11 and Q12 because they extrapolate the 500 mA collapse to a new potential and much longer duration. Q05, Q07, and Q09 are also weak because they combine negative potential with electrolyte or solvent effects never tested at negative polarity. Q01 and Q02 have unusually uncertain scores because their yields are near the 0.02 multiplicative score gate. Any prediction involving S2 at negative potential is especially interaction-dependent. The recommendation of batch 8 is reliable only for the published balanced score among observed batches: it rests on one realization, does not test E1 with S1, and should not be interpreted as maximizing absolute yield. Batch 7 was superior for measured selective yield but required much longer electrolysis.

The assigned primary goal—developing an explanatory and predictive account rather than merely maximizing score—did affect evidence collection. It motivated polarity reversal, extreme-potential and extreme-current failures, a duration series, and separate material contrasts. Those experiments were scientifically informative but used batches that a pure optimizer would probably have devoted to local refinement around batch 8. Consequently, the campaign gained evidence about mechanism and failure boundaries but sacrificed replication, fine mapping of the +1 V region, and a full solvent–electrolyte interaction design. I see no fundamental conflict with the goal, but there was a clear breadth-versus-precision tradeoff.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.51,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.21,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.31,
        "upper80": 0.6
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.067,
        "lower80": 0.0,
        "upper80": 0.23
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.31,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.91,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.77,
        "upper80": 0.96
      },
      "faradaic_efficiency": {
        "estimate": 0.89,
        "lower80": 0.8,
        "upper80": 0.96
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.333,
        "lower80": 0.08,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.002,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.89,
        "lower80": 0.79,
        "upper80": 0.96
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.5,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.19,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.57
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.336,
        "lower80": 0.17,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.014,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.3,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.9,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.8,
        "lower80": 0.68,
        "upper80": 0.89
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.72,
        "upper80": 0.9
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.575,
        "lower80": 0.51,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.132,
        "lower80": 0.088,
        "upper80": 0.184
      },
      "transport_efficiency": {
        "estimate": 0.82,
        "lower80": 0.71,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.48,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.29,
        "upper80": 0.65
      },
      "faradaic_efficiency": {
        "estimate": 0.56,
        "lower80": 0.37,
        "upper80": 0.72
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.402,
        "lower80": 0.2,
        "upper80": 0.53
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.014,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.61,
        "lower80": 0.41,
        "upper80": 0.77
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.9,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.92,
        "lower80": 0.84,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.93,
        "lower80": 0.85,
        "upper80": 0.98
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.628,
        "lower80": 0.56,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.155,
        "lower80": 0.103,
        "upper80": 0.216
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.35,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.04,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.11,
        "upper80": 0.51
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.282,
        "lower80": 0.07,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.004,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.09,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.87,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.97
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.6,
        "upper80": 0.83
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.58,
        "lower80": 0.49,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.098,
        "upper80": 0.232
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.59,
        "upper80": 0.83
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.21,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.02,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.07,
        "upper80": 0.44
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.177,
        "lower80": 0.02,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.06,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.74,
        "lower80": 0.61,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.57,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.69,
        "lower80": 0.56,
        "upper80": 0.8
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.483,
        "lower80": 0.39,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.073,
        "lower80": 0.034,
        "upper80": 0.126
      },
      "transport_efficiency": {
        "estimate": 0.71,
        "lower80": 0.56,
        "upper80": 0.83
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "energy_efficiency": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.27
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "faradaic_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.13
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.023,
        "lower80": 0.0,
        "upper80": 0.16
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.027
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.09
      }
    }
  ],
  "rationale": "Predictions transfer the campaign's approximately matched loading (0.48 versus 0.50 mol L⁻¹). I interpolated duration-dependent yield between the 300, 3000, and 12000 s S0/E0 results, treated +0.8 V as near the productive +1 V window, and transferred the observed E1, E3, and S2 efficiency fingerprints. Negative potential receives the experimentally observed selectivity and efficiency penalties, while 500 mA receives the severe transport/faradaic collapse seen in batch 6. Score estimates apply the published weighted formula and its selective-yield gate. Intervals include assay noise plus wider model uncertainty for untested potential–material combinations, short exposures near the yield gate, and both 500 mA extrapolations."
}
```
