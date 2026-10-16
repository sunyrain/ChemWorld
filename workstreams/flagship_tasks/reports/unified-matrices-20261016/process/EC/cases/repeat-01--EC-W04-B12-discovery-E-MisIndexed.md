# repeat-01/EC-W04-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W04-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical-system hypotheses

## H1 [tentative]
At fixed loading, conversion should rise with delivered charge/time and with overpotential magnitude once the sign-specific reaction threshold is crossed, then saturate; excessive potential or duration may reduce selectivity through degradation. Current is a cap, so potential, conductivity, and transport can make charge response non-proportional.

## H2 [tentative]
Ohmic performance should favor high-conductivity media (nominally E2/E0 and S0), while transport should reflect diffusivity and diffusion-layer properties (potentially E1/E3). Product selectivity may instead depend on solvent/interface residuals, so material rankings require experiment.

## H3 [tentative]
Potential sign is mechanistically decisive: one polarity should produce substantially more target than the opposite at matched magnitude, duration, loading, and materials. Electrolyte and solvent potential shifts should translate the apparent threshold.

## Initial testable expectation
A matched-polarity screen spanning potential sign and charge, followed by material contrasts at a common reagent concentration, will reveal a sigmoidal conversion-vs-effective-potential relation and a selectivity optimum at intermediate severity. Results inconsistent across matched conditions would favor strong hidden material interactions over a transferable response law.

### v2 · 公开事件 35

# Electrochemical-system hypotheses

## H1 [supported only for moderate positive potential; nonmonotonic severity]
At S0/E0, +1 V gives a productive but slow regime: extending electrolysis from 1800 to 7200 s increased measured conversion from 0.032 to 0.096 and selective yield from 0.010 to 0.101 (events runner-operation-0007, -0035). However, +2 V at 1800 s produced essentially zero conversion/yield and zero faradaic/transport efficiency (event -0021), so potential magnitude is not monotonically beneficial. A sharp high-positive-potential shutdown, side reaction, or degradation is more plausible than simple charge control.

## H3 [revised: polarity and window both matter]
At matched S0/E0, 100 mA cap, 1800 s, -1 V retained low conversion and moderate selectivity while +1 V showed low conversion but selectivity near one (events -0014, -0007). -2 V was also weak and less selective (event -0028). Numerical differences at low yields are comparable to assay noise for conversion/yield, but the efficiency/selectivity patterns collectively favor a productive window near +1 V and an adverse regime at +2 V.

## H4 [tentative precipitation confound]
S0/E0 shows precipitation signal near one in every tested condition, so recovered selective yield and conversion may not map simply to solution-phase target. Material tests with lower nominal precipitation propensity are required.

## Next tests
Hold loading at 0.4 mol/L and compare current cap at +1 V, then compare solvent/electrolyte pairs at the same potential/time. A large current-cap effect would support charge limitation; material-dependent threshold shifts or precipitation changes would support transferable effective-potential/material terms. Replication is needed before treating low-yield polarity differences as resolved.

### v3 · 公开事件 63

# Electrochemical-system hypotheses

## H1 [supported in tested scope: kinetic accumulation plus overload]
At +1 V and 100 mA cap, longer time increased S0/E0 conversion and yield (events runner-operation-0007, -0035). Raising the cap to 400 mA at 1800 s instead collapsed faradaic and transport efficiencies and target metrics (event -0042). Thus the cap enters through an overload/transport-limitation term rather than simply multiplying charge; optimum severity is bounded in both voltage and current.

## H2 [supported qualitatively; material terms are separable only provisionally]
At the common +1 V, 100 mA, 1800 s, material pairs differed strongly (events -0007, -0049, -0056, -0063). S1/E1 gave the best balanced result (FE/transport about 0.77 and score 0.493); S2/E2 gave still higher efficiencies (~0.80) but lower measured yield; S3/E3 had weaker FE/transport. These numerical differences exceed the stated assay noise for efficiency, supporting real material effects. Because solvent and electrolyte were changed together, solvent versus electrolyte contributions remain confounded.

## H4 [supported: precipitation is material-specific]
Final precipitation was near 1 for S0/E0, about 0.71 for S1/E1, and near zero for S2/E2 and S3/E3 (events -0007, -0049, -0056, -0063). This agrees directionally with nominal solubility/precipitation properties, although it does not by itself explain selective yield.

## Provisional predictive form
Treat target formation as accumulated time-dependent conversion multiplied by a window factor in signed effective potential and a current-overload factor. Let material-specific potential shifts translate the voltage window; let conductivity/contact control ohmic efficiency and diffusion-layer/diffusivity terms control transport. Do not assume delivered current equals the cap.

## Final discriminating tests
For S1/E1, test 7200 s at +1 V, matched -1 V, and a replicate of +1 V/1800 s. The long test checks transfer of time accumulation beyond S0/E0; the polarity test checks sign transfer; replication assesses whether the observed material advantage is robust.

### v4 · 公开事件 84

# Electrochemical-system hypotheses — final source-stage record

## H1 [supported in tested moderate window; bounded extrapolation]
Target formation accumulates with time at +1 V/100 mA: 7200 s increased conversion/yield relative to 1800 s for both S0/E0 (events runner-operation-0007, -0035) and S1/E1 (events -0049, -0070). The response is not monotone in electrical severity: S0/E0 at +2 V gave zero productive response (event -0021), and a 400 mA cap at +1 V collapsed faradaic/transport efficiencies (event -0042). A useful predictive structure is therefore a saturating time/charge term multiplied by voltage-window and current-overload terms.

## H2 [supported for paired materials; component attribution unresolved]
At +1 V, 100 mA, 1800 s, paired media had reproducibly different efficiency regimes. S1/E1 was strong in two runs: selectivity ~0.77–0.78, FE ~0.73–0.77, transport ~0.75–0.77, and yield ~0.035–0.039 (events -0049, -0084). The yield agreement supports repeatability despite noisier conversion (0.046 vs 0.019). S2/E2 had higher FE/transport but lower yield (event -0056); S3/E3 was weaker in charge/transport efficiency (event -0063). Because solvent and electrolyte moved together, their individual effects and cross-interactions cannot be identified.

## H3 [supported: positive polarity is the productive direction near unit magnitude]
For both tested pairs, -1 V reduced selectivity and productive efficiency relative to +1 V at matched time and current cap (S0/E0 events -0014 versus -0007; S1/E1 events -0077 versus -0049/-0084). -2 V remained weak (event -0028). Polarity effects transfer across at least two paired materials, though precise negative-potential yields near the assay noise floor remain uncertain.

## H4 [supported: precipitation is largely a material-state descriptor]
Precipitation signal was consistently near 1 for S0/E0, ~0.71 for S1/E1, and near zero for S2/E2 and S3/E3 across the material comparison (events -0007, -0049, -0056, -0063). It is not sufficient to rank target yield or efficiency.

## Provisional predictive account
At fixed loading, use signed effective potential corrected by the declared solvent/electrolyte potential shifts. A positive-polarity productive window is centered near the tested +1 V region, with sharp suppression by high positive overdrive; negative polarity has lower faradaic efficiency/selectivity. Conversion grows with time within the window but should saturate. Current cap helps only below a transport/interface overload threshold, because delivered current is potential- and resistance-limited. Estimate ohmic efficiency primarily from conductivity/contact, transport from diffusivity and diffusion-layer terms, and apply pair-specific residuals calibrated by the four material observations.

## Scope and unresolved alternatives
The campaign used a single loading (0.02 mol in 0.05 L, 0.4 mol/L) and paired material changes; no independent solvent-by-electrolyte factorial or direct delivered-current trace was available. The +2 V collapse could represent degradation, interface shutdown, or a hidden adverse reaction. Low conversion and yield have assay uncertainties large enough that exact small differences should not be overinterpreted. Batch 10 is the strongest tested operating recommendation because S1/E1, +1 V, 100 mA cap, 7200 s combined the highest score (0.530) with increased conversion/yield and strong efficiencies without excessive reported risk.

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
    "electrochemical_conversion": 0.032129980623722076,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.5409024953842163,
    "faradaic_efficiency": 0.5415942668914795,
    "ohmic_efficiency": 0.9572166204452515,
    "pH_normalized": 0.23443032801151276,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.20992566645145416,
    "selective_product_yield": 0.009760934859514236,
    "transport_efficiency": 0.5128905177116394
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
    "electrochemical_conversion": 0.011924302205443382,
    "electrochemical_selectivity": 0.6610745787620544,
    "energy_efficiency": 0.278411328792572,
    "faradaic_efficiency": 0.427999347448349,
    "ohmic_efficiency": 0.9660544395446777,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.3227793574333191,
    "selective_product_yield": 0.021980460733175278,
    "transport_efficiency": 0.454256147146225
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
      "potential_V": 2
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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9696498513221741,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.00894889235496521,
    "electrochemical_selectivity": 0.4911956787109375,
    "energy_efficiency": 0.034897685050964355,
    "faradaic_efficiency": 0.301249623298645,
    "ohmic_efficiency": 0.9818079471588135,
    "pH_normalized": 0.23175939917564392,
    "precipitation_signal": 0.9870871305465698,
    "safety_risk": 0.05933958664536476,
    "score": 0.08287128061056137,
    "selective_product_yield": 0.007409064564853907,
    "transport_efficiency": 0.2697620689868927
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
    "electrochemical_conversion": 0.09647880494594574,
    "electrochemical_selectivity": 0.9964359998703003,
    "energy_efficiency": 0.4886839687824249,
    "faradaic_efficiency": 0.5096913576126099,
    "ohmic_efficiency": 0.9644203782081604,
    "pH_normalized": 0.23672018945217133,
    "precipitation_signal": 0.9864134788513184,
    "safety_risk": 0.05933958664536476,
    "score": 0.45082011818885803,
    "selective_product_yield": 0.10056488960981369,
    "transport_efficiency": 0.4991818964481354
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
      "current_mA": 400,
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
    "cost": 0.287880003452301,
    "electrochemical_conversion": 0.0021511756349354982,
    "electrochemical_selectivity": 0.0042426493018865585,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02405594103038311,
    "ohmic_efficiency": 0.8653464913368225,
    "pH_normalized": 0.2334442436695099,
    "precipitation_signal": 0.997043788433075,
    "safety_risk": 0.05933958664536476,
    "score": 0.03931597247719765,
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
      "duration_s": 1800,
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
    "cost": 0.29872000217437744,
    "electrochemical_conversion": 0.04615913704037666,
    "electrochemical_selectivity": 0.7835550904273987,
    "energy_efficiency": 0.7451539635658264,
    "faradaic_efficiency": 0.7698787450790405,
    "ohmic_efficiency": 0.979776918888092,
    "pH_normalized": 0.20571213960647583,
    "precipitation_signal": 0.7054350972175598,
    "safety_risk": 0.08273958414793015,
    "score": 0.4926455020904541,
    "selective_product_yield": 0.03542572259902954,
    "transport_efficiency": 0.7732791304588318
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.3307200074195862,
    "electrochemical_conversion": 0.03212687373161316,
    "electrochemical_selectivity": 0.8823772072792053,
    "energy_efficiency": 0.8198572397232056,
    "faradaic_efficiency": 0.8043240904808044,
    "ohmic_efficiency": 0.9453251957893372,
    "pH_normalized": 0.17312930524349213,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.10073958337306976,
    "score": 0.31225985288619995,
    "selective_product_yield": 0.012147356756031513,
    "transport_efficiency": 0.797828733921051
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.3107199966907501,
    "electrochemical_conversion": 0.013369985856115818,
    "electrochemical_selectivity": 0.7418451905250549,
    "energy_efficiency": 0.5061909556388855,
    "faradaic_efficiency": 0.31878581643104553,
    "ohmic_efficiency": 0.9961092472076416,
    "pH_normalized": 0.2790941894054413,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.11333958804607391,
    "score": 0.3490556478500366,
    "selective_product_yield": 0.02869497798383236,
    "transport_efficiency": 0.3396170735359192
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
    "electrochemical_conversion": 0.15859366953372955,
    "electrochemical_selectivity": 0.8047565817832947,
    "energy_efficiency": 0.759742259979248,
    "faradaic_efficiency": 0.7767493724822998,
    "ohmic_efficiency": 0.937464714050293,
    "pH_normalized": 0.2037143111228943,
    "precipitation_signal": 0.7153439521789551,
    "safety_risk": 0.08273958414793015,
    "score": 0.5295800566673279,
    "selective_product_yield": 0.1100962832570076,
    "transport_efficiency": 0.7780989408493042
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
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.3057200014591217,
    "electrochemical_conversion": 0.02800978347659111,
    "electrochemical_selectivity": 0.4923953711986542,
    "energy_efficiency": 0.2382231503725052,
    "faradaic_efficiency": 0.31433671712875366,
    "ohmic_efficiency": 0.9509429931640625,
    "pH_normalized": 0.2046993374824524,
    "precipitation_signal": 0.7232331037521362,
    "safety_risk": 0.08273958414793015,
    "score": 0.11600856482982635,
    "selective_product_yield": 0.008889270946383476,
    "transport_efficiency": 0.32151666283607483
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
      "electrolyte_profile": 1,
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
    "cost": 0.3057200014591217,
    "electrochemical_conversion": 0.019397873431444168,
    "electrochemical_selectivity": 0.7683972120285034,
    "energy_efficiency": 0.7365474104881287,
    "faradaic_efficiency": 0.7336090803146362,
    "ohmic_efficiency": 0.964291512966156,
    "pH_normalized": 0.20521965622901917,
    "precipitation_signal": 0.7165690660476685,
    "safety_risk": 0.08273958414793015,
    "score": 0.4800979793071747,
    "selective_product_yield": 0.039188943803310394,
    "transport_efficiency": 0.754833996295929
  }
}
```

## K1 封存报告

# Mechanism report

## 1. Experimental domain

All 12 batches used the same initial loading: 0.020 mol of limiting reagent in 0.050 L of solvent, or nominally 0.40 mol L⁻¹. Each batch used one solvent/electrolyte pair, a commanded potential, a current cap, and one uninterrupted electrolysis period. Thus, the conclusions below apply directly only near this loading and to the tested operating ranges.

The principal observables were electrochemical conversion, electrochemical selectivity, selective-product yield, faradaic efficiency, transport efficiency, ohmic efficiency, energy efficiency, normalized pH, and precipitation signal. Reported differences at very low conversion or yield must be interpreted cautiously because their final-assay standard deviations were about 0.01, comparable to several measured values.

## 2. Proposed physical picture

I infer a windowed, transport-coupled electrochemical process rather than a simple charge-dose law. Product formation requires the productive potential polarity, adequate interfacial driving force, and current below a transport or interface-overload threshold. Within that window, conversion accumulates with time. Outside it, charge is diverted to unproductive chemistry, transport collapses, the interface becomes inhibited, or the reactant/product degrades.

A useful conceptual decomposition is

`target yield ≈ conversion × productive selectivity × recovery/phase factor`,

with conversion represented approximately by

`X(t) = 1 − exp[−k_pair · t · ΦV(Veff) · ΦI(Icap, pair) · ηtr]`.

Here `k_pair` is a material-dependent kinetic coefficient; `Veff` is the applied potential relative to a material-dependent reaction window; `ΦV` is small at the wrong polarity, maximal in an intermediate positive-potential window, and small again under excessive positive overdrive; `ΦI` penalizes current demand above the mass-transfer or interfacial limit; and `ηtr` is a transport factor. This is a mechanistic scaffold, not a fitted quantitative law.

The commanded current is best regarded as a cap, not necessarily the delivered current. A plausible representation is

`Idel = min(Icap, Ikin(Veff), Ilim(pair, concentration))`,

where `Ilim` should scale qualitatively with diffusivity, concentration, electrode area, and inverse diffusion-layer thickness. Ohmic loss depends on the fixed cell fixture plus material conductivity. At excessive current demand, concentration polarization, passivation, gas formation, or an unproductive interfacial pathway could sharply lower faradaic and transport efficiencies.

The nominal solvent and electrolyte standard-potential shifts probably translate the productive window. For the four paired conditions, the sums of the declared shifts are −0.20 V for S0/E0, +0.02 V for S1/E1, +0.48 V for S2/E2, and +0.28 V for S3/E3. The experiment did not identify the sign convention by which these shifts enter `Veff`, so I would not simply add or subtract them in a numerical prediction without calibration. Hidden, fixed material residuals also affect transport, solvation, and interface kinetics.

## 3. Evidence for a bounded potential window

Batch 1 established the initial productive condition: S0/E0, +1 V, 100 mA cap, and 1800 s. It gave conversion 0.0321, selectivity 1.000, yield 0.00976, faradaic efficiency 0.542, transport efficiency 0.513, energy efficiency 0.541, and ohmic efficiency 0.957. Although the target yield was close to the assay uncertainty, the efficiency pattern showed that this was an electrochemically active regime.

Batch 2 reversed the polarity to −1 V while keeping all other settings fixed. Conversion was 0.0119, selectivity 0.661, yield 0.0220, faradaic efficiency 0.428, transport efficiency 0.454, and energy efficiency 0.278. The apparently larger yield than in batch 1 should not be overinterpreted: both yields were small relative to their uncertainty, and the conversion, selectivity, and efficiency channels collectively favored +1 V.

Batch 3 changed only the potential from +1 to +2 V. Conversion, selectivity, yield, faradaic efficiency, transport efficiency, and energy efficiency were all reported as zero, while ohmic efficiency remained 0.970. This observation changed the original explanation decisively: increasing positive potential does not monotonically increase reaction rate. Because ohmic efficiency remained high, ordinary bulk resistance alone cannot explain the collapse. Plausible causes include an adverse reaction, reactant or product degradation, electrode passivation, or a potential-triggered loss of interfacial transport.

Batch 4 at −2 V was also poor but not identical to the +2 V shutdown: conversion was 0.00895, selectivity 0.491, yield 0.00741, faradaic efficiency 0.301, transport efficiency 0.270, energy efficiency 0.0349, and ohmic efficiency 0.982. Thus, increasing negative magnitude did not rescue productive conversion. Together, batches 1–4 support a productive positive-polarity window near +1 V for S0/E0, bounded by inefficient negative-polarity operation and a sharp adverse regime at high positive potential.

The same polarity preference transferred to S1/E1. Batch 11, at −1 V, 100 mA, and 1800 s, produced conversion 0.0280, selectivity 0.492, yield 0.00889, faradaic efficiency 0.314, transport efficiency 0.322, and energy efficiency 0.238. By comparison, the two +1 V S1/E1 batches had selectivity about 0.77–0.78, faradaic efficiency about 0.73–0.77, transport efficiency about 0.75–0.77, and yield about 0.035–0.039. This makes the polarity effect more credible than the noisy S0/E0 yield comparison alone.

## 4. Time dependence

Batch 5 repeated the batch-1 S0/E0 electrical condition but extended electrolysis from 1800 to 7200 s. Conversion rose from 0.0321 to 0.0965 and yield from 0.00976 to 0.1006. Selectivity remained near one, at 0.996. Faradaic and transport efficiencies remained similar, changing from 0.542 and 0.513 to 0.510 and 0.499. This resembles continued accumulation at approximately stable instantaneous efficiency rather than activation of a new electrochemical regime.

The time effect transferred to S1/E1. Batch 10 used +1 V, 100 mA, and 7200 s and gave conversion 0.1586, selectivity 0.805, yield 0.1101, faradaic efficiency 0.777, transport efficiency 0.778, energy efficiency 0.760, and ohmic efficiency 0.937. The two 1800 s S1/E1 runs, batches 7 and 12, gave conversions 0.0462 and 0.0194 and yields 0.0354 and 0.0392. Their yield agreement is good, whereas their conversion spread indicates process or measurement variability at low conversion. Relative to their mean, the 7200 s batch had roughly three times the yield after four times the duration, consistent with sublinear accumulation or incipient saturation. The available points cannot distinguish first-order depletion, product loss, or a time-varying current.

## 5. Current-cap coupling

Batch 6 tested whether more commanded current simply accelerates the batch-1 process. At S0/E0, +1 V, and 1800 s, increasing the cap from 100 to 400 mA reduced conversion to 0.00215, selectivity to 0.00424, faradaic efficiency to 0.0241, transport efficiency to zero, and energy efficiency to zero. Ohmic efficiency also fell from 0.957 in batch 1 to 0.865, but that change alone is too small to account for the near-total loss of productive performance.

This behavior supports a limiting-current or interface-overload mechanism. At 400 mA demand, reagent delivery to the electrode may be inadequate, the electrode surface may passivate, or a competing reaction may dominate. The result rejects a model in which conversion is determined only by `Icap × time`. It also implies a coupling between current, material transport, and potential: an acceptable cap for one pair or potential cannot automatically be transferred to another.

## 6. Material effects

Batches 1, 7, 8, and 9 compared the four paired solvent/electrolyte choices at +1 V, 100 mA, and 1800 s.

- Batch 1, S0/E0: conversion 0.0321, selectivity 1.000, yield 0.00976, faradaic efficiency 0.542, transport efficiency 0.513, energy efficiency 0.541, ohmic efficiency 0.957, precipitation 1.000, normalized pH 0.234.
- Batch 7, S1/E1: conversion 0.0462, selectivity 0.784, yield 0.0354, faradaic efficiency 0.770, transport efficiency 0.773, energy efficiency 0.745, ohmic efficiency 0.980, precipitation 0.705, normalized pH 0.206.
- Batch 8, S2/E2: conversion 0.0321, selectivity 0.882, yield 0.0121, faradaic efficiency 0.804, transport efficiency 0.798, energy efficiency 0.820, ohmic efficiency 0.945, precipitation 0.00031, normalized pH 0.173.
- Batch 9, S3/E3: conversion 0.0134, selectivity 0.742, yield 0.0287, faradaic efficiency 0.319, transport efficiency 0.340, energy efficiency 0.506, ohmic efficiency 0.996, precipitation 0.00819, normalized pH 0.279.

These differences show that efficiency, conversion, target recovery, pH, and precipitation are controlled by different combinations of material properties. High bulk conductivity alone is not a complete predictor. S2/E2 had the highest short-run faradaic, transport, and energy efficiencies, but not the highest yield. S3/E3 had excellent measured ohmic efficiency yet weak faradaic and transport performance. S1/E1 gave the most consistently favorable combination of productive yield and efficiency.

The S1/E1 short condition was replicated in batch 12. Batch 12 gave conversion 0.0194, selectivity 0.768, yield 0.0392, faradaic efficiency 0.734, transport efficiency 0.755, energy efficiency 0.737, and precipitation 0.717. Agreement with batch 7 was strong for yield, selectivity, efficiencies, pH, and precipitation, though not for conversion. This supports the reality of the S1/E1 efficiency regime while warning against precise inference from a single low-conversion result.

The material comparison cannot identify separate solvent and electrolyte effects because both were changed together. For example, S1/E1 performance could arise from the solvent, the electrolyte, their interaction, or a hidden pair-specific residual. No crossed combinations such as S1/E0 or S0/E1 were tested.

## 7. pH and precipitation

Normalized pH behaved primarily as a material-state variable. It was approximately 0.232–0.237 across the S0/E0 potential, current, and duration experiments; approximately 0.204–0.206 for S1/E1; 0.173 for S2/E2; and 0.279 for S3/E3. Its small changes with reaction time and polarity, compared with its changes between material pairs, suggest control by electrolyte acidity, pKa, and solvent proton activity rather than by conversion over the tested range.

Precipitation was likewise strongly material-dependent: near one for S0/E0, about 0.71–0.72 for S1/E1, and near zero for S2/E2 and S3/E3. This is directionally consistent with the nominal solubility-product information. However, precipitation was not a monotonic predictor of target yield. S0/E0 had nearly complete precipitation but only achieved high yield after long electrolysis; S2/E2 had essentially no precipitation but low short-run yield; and S3/E3 had negligible precipitation with moderate measured yield. I therefore treat precipitation as a phase/recovery coupling rather than the primary electrochemical rate law.

## 8. Interpretation of the efficiency channels

Ohmic efficiency stayed high, generally about 0.94–1.00, except under the 400 mA cap, where it fell to 0.865. This is consistent with a fixed cell fixture plus pair-dependent conductivity and current-dependent IR loss. Because S3/E3 had the highest ohmic efficiency but low transport and faradaic efficiencies, good conduction is necessary but not sufficient.

Transport and faradaic efficiencies often moved together: both were about 0.5 for productive S0/E0, about 0.75–0.80 for productive S1/E1 and S2/E2, about 0.32–0.34 for S3/E3, and nearly zero in the overload or shutdown regimes. This covariance suggests that mass transfer and interfacial selectivity are coupled. It could arise because concentration polarization changes which reaction occurs, rather than transport merely controlling the speed of an otherwise fixed reaction.

Energy efficiency reflected all three effects. It was high for S1/E1 and S2/E2 at +1 V, low at negative potentials, and zero for the +2 V S0/E0 and 400 mA S0/E0 failures. A predictive model should therefore not estimate energy efficiency from ohmic efficiency alone.

## 9. How the explanation changed during the campaign

The initial hypothesis was that conversion would rise with charge and overpotential before saturating. Batch 2 suggested a polarity effect, but its low and noisy yield made the conclusion provisional. Batch 3 forced the first major revision: the complete failure at +2 V required a sharply bounded voltage window or an adverse high-potential process. Batch 4 showed that simply reversing and increasing magnitude was also ineffective.

Batch 5 established that duration can accumulate target within the productive +1 V window without materially improving faradaic or transport efficiency. Batch 6 forced the second major revision: current cap could not be treated as delivered charge, because 400 mA caused overload rather than acceleration.

Batches 7–9 established strong material control and separated ohmic performance from faradaic/transport performance. They also showed that precipitation and pH were pair-specific but insufficient to rank target yield. Batch 10 demonstrated that the beneficial time dependence transferred from S0/E0 to S1/E1. Batch 11 demonstrated that the positive-polarity advantage also transferred to S1/E1. Batch 12 confirmed the principal S1/E1 selectivity, yield, efficiency, pH, and precipitation observations while exposing variability in low conversion estimates.

## 10. Plausible alternatives

The high-positive-potential collapse could be caused by chemical degradation, a competing redox reaction, electrode passivation, gas evolution, or loss of reactant from the electroactive region. These alternatives are observationally equivalent here because no time-resolved current, product-identity-specific degradation channel, or electrode-state measurement was available.

The high-current collapse could reflect mass-transfer limitation, IR-induced movement away from the intended interfacial potential, capacitive or gas-producing current, or passivation. The decline in both ohmic and transport efficiency supports coupled limitations but does not uniquely identify one.

The apparent time accumulation could be ordinary kinetic conversion, slow release from a precipitated or adsorbed reservoir, or progressive equilibration between phases. Stable efficiency channels favor continued electrolysis, but they do not exclude phase-transfer control.

Finally, the processed observables are independently noisy synthetic estimates. At low signal, relationships such as yield being less than conversion need not hold exactly; batch 2, for example, reported yield 0.0220 with conversion 0.0119. Such discrepancies should be treated as noise or channel-definition differences, not evidence for material creation.

## 11. Scope and unidentifiable quantities

The campaign does not identify an exact rate constant, reaction order, transfer coefficient, limiting current, threshold potential, degradation rate, or saturation conversion. It also does not identify the delivered current, electrode area, electrode gap, contact resistance, temperature trajectory, or species-level mechanism. The fixed fixture is common to all batches but remains numerically unknown.

Only one reagent concentration was studied. Potential was sampled sparsely, with detailed contrasts mainly in S0/E0. Current cap was changed only once, and only for S0/E0. Solvent and electrolyte effects are completely confounded by paired changes. Most conditions have one replicate, and no zero-potential control was run. Consequently, the proposed equations express relationships and couplings supported by the observations but are not uniquely fitted laws.

Extrapolation should be conservative. I expect positive polarity near the calibrated productive window, moderate current demand, and longer duration to remain favorable, but I would not assume that +1 V or 100 mA is universally optimal after changing loading, material pairing, or fixture. Material potential shifts should move the window, and transport properties should move the tolerable-current boundary.

## 12. Overall conclusion

This world is most coherently explained by a positive-polarity electrochemical conversion operating inside a narrow potential and current window. Product accumulates with electrolysis time inside that window, while excessive positive potential or excessive current demand causes a sharp loss of transport, faradaic efficiency, selectivity, or all three. Material pairs set pH, precipitation behavior, effective potential, charge transport, and interfacial selectivity through partially independent pathways. S1/E1 provided the most reproducible balance of productive yield and efficiency, and its 7200 s condition in batch 10 was the strongest tested realization, with conversion 0.1586, yield 0.1101, selectivity 0.805, faradaic efficiency 0.777, transport efficiency 0.778, energy efficiency 0.760, and score 0.5296. This recommendation is empirical within the tested domain; the broader mechanistic account remains a bounded, testable model rather than a uniquely identified microscopic mechanism.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior mechanism or response law was supplied. The material dossier provided nominal properties and explicitly framed them as incomplete priors rather than an objective ranking.

Supported self-developed claims:
- Product formation accumulates with time inside a productive regime. For S0/E0 at +1 V and 100 mA, extending electrolysis from 1800 s in batch 1 to 7200 s in batch 5 increased conversion from 0.032 to 0.096 and yield from 0.0098 to 0.101. The corresponding S1/E1 comparison—batches 7 and 12 versus batch 10—raised yield from about 0.035–0.039 to 0.110.
- Positive polarity near +1 V is more productive than negative polarity. This was supported by the collective conversion, selectivity, and efficiency differences between batches 1 and 2 and, more clearly, between S1/E1 batches 7/12 and batch 11.
- Ohmic, transport, and faradaic performance are not interchangeable. Batch 9 had ohmic efficiency 0.996 but transport and faradaic efficiencies near 0.34 and 0.32. Batch 6 retained ohmic efficiency 0.865 while transport and energy efficiencies collapsed to zero.
- Material identity strongly controls pH and precipitation. S0/E0 batches had precipitation near one; S1/E1 was near 0.71; S2/E2 and S3/E3 were near zero. Normalized pH was also stable within a pair but different across pairs.

Contradicted or substantially revised claims:
- A simple monotonic overpotential law was contradicted by batch 3. Changing S0/E0 from +1 V to +2 V at otherwise matched conditions changed an active response into zero conversion, yield, faradaic efficiency, transport efficiency, and energy efficiency.
- A simple charge law based on `current cap × time` was contradicted by batch 6. Raising the cap from 100 to 400 mA at +1 V did not accelerate production; it nearly eliminated productive performance.
- Conductivity alone did not rank performance. Although the dossier suggested useful qualitative ohmic information, batch 8’s high-conductivity E2 pair did not have the highest ohmic efficiency, while low-conductivity E3 in batch 9 showed excellent ohmic efficiency but poor faradaic and transport behavior.
- Precipitation was not a sufficient predictor of yield: batch 8 had almost no precipitation but low yield, while long-duration S0/E0 in batch 5 combined near-complete precipitation with high yield.

Untested or unresolved claims:
- Material potential shifts may translate the productive voltage window, but only S0/E0 received a real voltage sweep. The sign and magnitude of the shift cannot be identified.
- Separate solvent, electrolyte, and interaction effects remain unidentifiable because the campaign changed them together in batches 1 and 7–9.
- The +2 V failure could be degradation, passivation, gas evolution, or reversible diversion to another electrochemical pathway. The existing observables do not distinguish them.
- Saturating kinetics were plausible but not established from only two durations per productive material pair.
- The contract’s statement that the fixture was fixed across the campaign was accepted as supplied experimental context, not independently tested.

In retrospective reconstruction, batches 3 and 6 produced the largest changes in judgment: batch 3 replaced monotonic voltage activation with a bounded voltage window, and batch 6 replaced nominal charge dosing with a transport/interface-overload picture. Batches 10–12 then showed that the time and polarity effects transferred beyond S0/E0, while batch 12 exposed meaningful variability in low conversion despite reproducible yield and efficiencies.

2. One additional discriminating experiment

I would run one staged S0/E0 experiment at the campaign loading and 100 mA cap: operate at +1 V long enough to establish an active within-batch UV–visible efficiency baseline, switch briefly to +2 V, measure again, then return to +1 V for an equal pulse and measure before termination and final assay. The measurements would be interpreted relative to the first +1 V segment in the same vessel, limiting between-batch confounding.

This distinguishes a leading reversible potential-window explanation from an irreversible degradation/passivation alternative:
- If faradaic and transport efficiency collapse during +2 V but return near the initial +1 V values after switching back, I would strongly favor reversible pathway selection, polarization, or a potential-dependent interfacial state.
- If the response remains near zero after returning to +1 V, I would shift toward irreversible reactant/product degradation or persistent electrode passivation.
- Partial or slow recovery would favor a mixed mechanism or a relaxing surface state.
- If +2 V no longer causes a collapse, the batch-3 result would require replication and might represent unexplained process variability rather than a general law.

The final assay alone could not localize when damage occurred, so the staged intermediate observations are essential to this discrimination.

3. Unused evidence, reliability, and effect of the goal

The detailed raw spectra and most artifact contents were not analyzed; the account relied primarily on processed estimates, reported uncertainties, and peak assignments summarized by the instruments. The raw UV–visible curves, chromatographic peak shapes, and other multichannel final-assay traces might have revealed whether the failed conditions formed a different spectral species. Cost and safety data were retained for operational assessment but contributed little to the proposed reaction mechanism. Nominal capacitance, acid concentration, pKa, diffusivity, diffusion-layer thickness, conductivity, and solubility data were used only qualitatively because the crossed design needed to estimate their separate coefficients was absent.

The least reliable predictions are Q05–Q10, because they contain solvent/electrolyte combinations never tested together, and Q11–Q12, because they combine a higher 500 mA cap with long electrolysis while the sole high-current observation was batch 6 at 400 mA and 1800 s. Q01 and Q02 are also uncertain because their expected yields lie near the assay noise floor and the score has a nonlinear low-yield gate. Predictions for the polarity ordering are more reliable than their exact numerical values. The recommendation of batch 10 is reliable as a ranking among the 12 observed batches, but extrapolating it to a different loading, fixture, or crossed material formulation is not.

The assigned goal did affect evidence collection. Because explanation and prediction were primary and public score was secondary, the campaign spent batches on polarity reversal, excessive voltage, current overload, duration contrasts, a material screen, and replication rather than repeatedly optimizing the best score. That produced strong qualitative falsification evidence but left fewer batches for a full solvent-by-electrolyte factorial, a dense voltage curve, delivered-current measurements, or multiple replicates. There was no clear conflict with safety—the observed risks remained below the stated limit—but there was a trade-off between breadth of mechanistic contrasts and precision of parameter estimation.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.45,
        "upper80": 0.88
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.31,
        "upper80": 0.59
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.102,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.49,
        "lower80": 0.34,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.75,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.56,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.42,
        "upper80": 0.71
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.216,
        "lower80": 0.0,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.48,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.18,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.57
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.345,
        "lower80": 0.2,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.034,
        "lower80": 0.012,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.8,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.38,
        "upper80": 0.69
      },
      "faradaic_efficiency": {
        "estimate": 0.57,
        "lower80": 0.42,
        "upper80": 0.7
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.477,
        "lower80": 0.39,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.125,
        "lower80": 0.065,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.4,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.28,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.52
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.284,
        "lower80": 0.1,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.006,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.18,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.58,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.65,
        "lower80": 0.42,
        "upper80": 0.8
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.45,
        "upper80": 0.82
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.503,
        "lower80": 0.36,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.65,
        "lower80": 0.42,
        "upper80": 0.8
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.2,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.03,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.42
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.207,
        "lower80": 0.02,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.1,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.48,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.3,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.22,
        "upper80": 0.62
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.391,
        "lower80": 0.25,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.02,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.23,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.4,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.25,
        "upper80": 0.62
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.329,
        "lower80": 0.14,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.008,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.24,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.65,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.75
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.38,
        "upper80": 0.78
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.47,
        "lower80": 0.32,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.04,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.1,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "energy_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "faradaic_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.019,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.15
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "faradaic_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.011,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.1
      }
    }
  ],
  "rationale": "Predictions use the observed positive-polarity productive window, time-dependent accumulation, and sharp high-current overload. S0/E0 anchors Q01–Q04; crossed material cases are adjusted using the campaign’s paired-material efficiencies and nominal transport/potential-shift information, with wider intervals because solvent and electrolyte effects were not separately identified. Scores apply the published weighted formula and low-yield gate. Intervals include assay noise, the new 0.48 M loading, sparse voltage coverage, and substantial uncertainty for untested material crosses and 500 mA operation."
}
```
