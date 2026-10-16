# repeat-03/EC-W04-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W04-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

**H1 [tentative].** At fixed loading (0.020 mol in 0.040 L), conversion should increase with absolute overpotential and charge/time until depletion, while selectivity and energy efficiency may decline at excessive magnitude or duration. Opposite potential signs may be strongly asymmetric. Test with paired signs and a potential/time/current series.

**H2 [tentative].** Transport and ohmic response should vary systematically with solvent/electrolyte nominal conductivity and diffusivity, but hidden fixed residuals may reverse dossier rankings. Test material swaps at otherwise matched settings.

**H3 [tentative].** A current cap can bind below transport/kinetic demand; at sufficiently high cap, delivered current should plateau and outcomes become cap-insensitive. Test several caps at matched potential and duration.

Design decision: use all 12 complete batches in a structured screening/factorial sequence, with one intermediate UV-vis or pH measurement per batch when informative. I will interpret numerical differences cautiously given stated assay noise and will use repeat/near-repeat comparisons where possible.

### v2 · 公开事件 49

# Working hypotheses after batches 1–7

**H1 [supported for polarity; unresolved quantitatively].** Negative polarization is the productive direction in S0/E0. At +1.2 V the assay showed essentially no useful efficiency/yield (event runner-operation-0007), whereas −1.2 V produced nonzero selective yield and markedly higher selectivity/faradaic/transport efficiencies (runner-operation-0014). Thus a sign-sensitive charge-transfer step is required; a model based only on |potential| is rejected.

Within negative potentials, −0.6 V had high selectivity/energy efficiency but no resolved selective yield (runner-operation-0021); −1.8 V was less selective and energy-efficient than −1.2 V (runner-operation-0028). This supports an activation window with parasitic current at excessive cathodic drive, but single noisy assays and tiny conversion limit precision. Testable consequence: an intermediate cathodic magnitude near −1 V should balance rate and efficiency.

**H2 [unresolved].** Material-property effects remain untested.

**H3 [tentative].** Changing the cap from 20 to 300 mA at −1.2 V/300 s caused only modest assay differences (runner-operation-0035 versus runner-operation-0042), not clear evidence of cap saturation because process noise and delivered current are unobserved. Extending to 900 s raised measured conversion but not selective yield proportionally (runner-operation-0049), consistent with low-charge regime plus assay noise or time-dependent loss. A much longer run is needed to expose kinetic saturation/degradation.

Next decision: run one long baseline, then material comparisons under a cathodic setting; treat precipitation near unity in S0/E0 as a possible confound.

### v3 · 公开事件 84

# Final source-stage hypothesis record

**H1 [supported in tested scope].** The productive polarity is cathodic. S0/E0 at +1.2 V was inactive (runner-operation-0007), while −1.2 V gave nonzero product and substantially higher electrochemical efficiencies (runner-operation-0014). In S0/E0, −0.6 V was efficient/selective but below resolved product formation, −1.2 V formed product, and −1.8 V lost selectivity/energy efficiency (runner-operation-0021, runner-operation-0014, runner-operation-0028). A parsimonious response is an activation term increasing with cathodic overpotential multiplied by declining selectivity/voltage efficiency at excessive drive. The optimum is therefore intermediate and material-shifted rather than a universal absolute potential.

**H2 [supported qualitatively, decomposition unresolved].** Material choice strongly changes precipitation, pH, conversion and yield. At −1.2 V, 100 mA cap, 3600 s, paired S1/E1 reduced precipitation and delivered much higher selective yield/score than S0/E0 (runner-operation-0063 versus runner-operation-0056). S2/E2 and S3/E3 essentially eliminated precipitation but did not exceed S1/E1 yield (runner-operation-0070, runner-operation-0077). Because solvent and electrolyte changed together, their individual causal contributions are unresolved; nominal conductivity/diffusivity alone cannot rank overall performance. A precipitation penalty is plausible for S0/E0 but is not sufficient alone because low-precipitation pairs differed.

**H3 [unresolved cap law].** At S0/E0, −1.2 V/300 s, 20 and 300 mA caps gave only modest/non-monotone differences relative to assay noise and unobserved delivered current (runner-operation-0035, runner-operation-0042). Treat the cap as a ceiling: below demanded current, charge and conversion should scale with cap; above demand, results should plateau. The campaign does not locate that crossover reliably.

**H4 [tentative time law].** Conversion generally rose with longer electrolysis, but selective yield did not scale monotonically in S0/E0 (300, 900, 3600 s: runner-operation-0014, runner-operation-0049, runner-operation-0056). Candidate explanations are product loss/precipitation, changing current, and measurement/process noise. For prediction, use a saturating charge/conversion term and allow yield to peak or plateau rather than extrapolating linearly.

**Cross-check / recommended region.** S1/E1 at −0.9 V and 3600 s gave the highest observed score and selective yield close to the −1.2 V S1/E1 result, with improved energy efficiency (runner-operation-0084 versus runner-operation-0063). The numerical difference between these two single assays is not strong proof of a potential optimum, but it brackets a promising cathodic window around −0.9 to −1.2 V.

Scope: all experiments used 0.020 mol reagent in 0.040 L solvent (0.50 mol L−1 nominal initial loading), so concentration extrapolation is unsupported. Predictions across sign, time, materials and caps should preserve the qualitative structure above and report uncertainty from sparse/confounded material coverage.

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
      "potential_V": 1.2
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
    "cost": 0.28274399042129517,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9628238677978516,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.28274399042129517,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6320253610610962,
    "energy_efficiency": 0.19927366077899933,
    "faradaic_efficiency": 0.3906446099281311,
    "ohmic_efficiency": 0.9716616868972778,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.15991906821727753,
    "selective_product_yield": 0.010869380086660385,
    "transport_efficiency": 0.4169014096260071
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
      "potential_V": -0.6
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
    "cost": 0.2826719880104065,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6986279487609863,
    "energy_efficiency": 0.6310857534408569,
    "faradaic_efficiency": 0.4842647314071655,
    "ohmic_efficiency": 0.9303990602493286,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.5008216500282288
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
      "potential_V": -1.8
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
    "cost": 0.28281599283218384,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5147737860679626,
    "energy_efficiency": 0.055148832499980927,
    "faradaic_efficiency": 0.3265741467475891,
    "ohmic_efficiency": 0.9799388647079468,
    "pH_normalized": 0.23175939917564392,
    "precipitation_signal": 0.9870871305465698,
    "safety_risk": 0.072194404900074,
    "score": 0.02390240877866745,
    "selective_product_yield": 0.0020499841775745153,
    "transport_efficiency": 0.2950865924358368
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
      "potential_V": -1.2
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
    "cost": 0.2826288044452667,
    "electrochemical_conversion": 0.004049268551170826,
    "electrochemical_selectivity": 0.6246828436851501,
    "energy_efficiency": 0.1808173954486847,
    "faradaic_efficiency": 0.39711424708366394,
    "ohmic_efficiency": 0.9924566745758057,
    "pH_normalized": 0.23672018945217133,
    "precipitation_signal": 0.9864134788513184,
    "safety_risk": 0.072194404900074,
    "score": 0.12794895470142365,
    "selective_product_yield": 0.008836508728563786,
    "transport_efficiency": 0.38660478591918945
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
      "current_mA": 300,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.28303200006484985,
    "electrochemical_conversion": 0.00722397631034255,
    "electrochemical_selectivity": 0.6357333064079285,
    "energy_efficiency": 0.11481859534978867,
    "faradaic_efficiency": 0.24158966541290283,
    "ohmic_efficiency": 0.9158118367195129,
    "pH_normalized": 0.2334442436695099,
    "precipitation_signal": 0.997043788433075,
    "safety_risk": 0.072194404900074,
    "score": 0.16337670385837555,
    "selective_product_yield": 0.013540607877075672,
    "transport_efficiency": 0.2169063240289688
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
      "potential_V": -1.2
    },
    {
      "duration_s": 900,
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
    "cost": 0.28303200006484985,
    "electrochemical_conversion": 0.019466394558548927,
    "electrochemical_selectivity": 0.6198346018791199,
    "energy_efficiency": 0.2125960737466812,
    "faradaic_efficiency": 0.3929520845413208,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23245882987976074,
    "precipitation_signal": 0.9820858836174011,
    "safety_risk": 0.072194404900074,
    "score": 0.19278201460838318,
    "selective_product_yield": 0.012960618361830711,
    "transport_efficiency": 0.3963524401187897
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.28432801365852356,
    "electrochemical_conversion": 0.031442053616046906,
    "electrochemical_selectivity": 0.6165111660957336,
    "energy_efficiency": 0.20796863734722137,
    "faradaic_efficiency": 0.3988460898399353,
    "ohmic_efficiency": 0.988741934299469,
    "pH_normalized": 0.2307613641023636,
    "precipitation_signal": 0.994958758354187,
    "safety_risk": 0.072194404900074,
    "score": 0.027122465893626213,
    "selective_product_yield": 0.0018477904377505183,
    "transport_efficiency": 0.3923507332801819
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 3600,
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
    "cost": 0.2933279871940613,
    "electrochemical_conversion": 0.024673452600836754,
    "electrochemical_selectivity": 0.46948665380477905,
    "energy_efficiency": 0.19548740983009338,
    "faradaic_efficiency": 0.2762458920478821,
    "ohmic_efficiency": 0.9866313934326172,
    "pH_normalized": 0.20602844655513763,
    "precipitation_signal": 0.7261821031570435,
    "safety_risk": 0.09559440612792969,
    "score": 0.25298500061035156,
    "selective_product_yield": 0.029945993795990944,
    "transport_efficiency": 0.2970771789550781
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 3600,
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
    "cost": 0.3189280033111572,
    "electrochemical_conversion": 0.04293328896164894,
    "electrochemical_selectivity": 0.559903621673584,
    "energy_efficiency": 0.24216052889823914,
    "faradaic_efficiency": 0.30452293157577515,
    "ohmic_efficiency": 0.9296258091926575,
    "pH_normalized": 0.17282894253730774,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.16825255751609802,
    "selective_product_yield": 0.012470351532101631,
    "transport_efficiency": 0.30587252974510193
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 3600,
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
    "cost": 0.30292800068855286,
    "electrochemical_conversion": 0.03688287362456322,
    "electrochemical_selectivity": 0.44889116287231445,
    "energy_efficiency": 0.1981123685836792,
    "faradaic_efficiency": 0.2533954083919525,
    "ohmic_efficiency": 0.9746400117874146,
    "pH_normalized": 0.27776509523391724,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.12619440257549286,
    "score": 0.14708809554576874,
    "selective_product_yield": 0.01231534592807293,
    "transport_efficiency": 0.2605753540992737
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
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.9
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
    "cost": 0.2998960018157959,
    "electrochemical_conversion": 0.01400800421833992,
    "electrochemical_selectivity": 0.49474331736564636,
    "energy_efficiency": 0.25923073291778564,
    "faradaic_efficiency": 0.2919658124446869,
    "ohmic_efficiency": 0.9585464596748352,
    "pH_normalized": 0.20521965622901917,
    "precipitation_signal": 0.7165690660476685,
    "safety_risk": 0.09559440612792969,
    "score": 0.2655247747898102,
    "selective_product_yield": 0.026630530133843422,
    "transport_efficiency": 0.313190758228302
  }
}
```

## K1 封存报告

Mechanism report

1. Experimental scope

I completed 12 batches. Every batch began with 0.020 mol of limiting reagent in 0.040 L of one solvent, so the nominal initial reagent concentration was 0.50 mol L^-1. Consequently, this campaign identifies effects of polarity, potential, electrolysis time, current ceiling, and selected material combinations only at that loading. It does not identify concentration or volume scaling.

The reported values below are final-assay observations, not hidden state estimates. The assay has nonzero channel-specific noise, and several results lie close to zero. In particular, conversion and selective-product-yield occasionally disagree near their detection floor, so I do not impose the exact identity yield = conversion × selectivity on the reported channels.

2. Central mechanistic account

The system appears to be a cathodically activated electrochemical conversion with four coupled limitations:

(a) Potential-dependent electron transfer. Productive charge transfer turns on when the electrode is sufficiently cathodic relative to a material-dependent effective standard potential. Positive polarization is essentially inactive. Increasing cathodic drive initially increases reaction rate, but excessive cathodic drive promotes parasitic current and reduces selectivity and voltage/energy efficiency.

(b) Charge and time limitation. Before substrate depletion, conversion should increase with the passed productive charge. A useful latent relation is

  Q = I_actual t,
  I_actual = min(I_cap, I_demand),
  X = 1 - exp[-k_Q eta_F Q/(n F N_0)],

where I_cap is the specified current ceiling, I_demand is the kinetic/transport current demanded at the chosen potential, eta_F is faradaic efficiency, and N_0 is the initial reagent amount. The campaign did not directly measure I_actual, n, or k_Q, so this is a structural hypothesis rather than a fitted quantitative law.

(c) Transport and ohmic coupling. A conceptual current-demand model is

  1/I_demand = 1/I_kinetic + 1/I_transport,

with I_kinetic increasing with cathodic overpotential and I_transport depending on diffusivity, diffusion-layer thickness, solvent diffusivity, and concentration. The cell resistance depends on electrolyte conductivity, solvent conductivity, geometry, and hidden campaign-fixed residuals. Ohmic efficiency remained fairly high in all final assays (approximately 0.916-1.000), whereas transport efficiency was much more variable (approximately 0-0.501), suggesting that mass transport and interfacial selectivity were more important limitations than bulk ohmic loss in the tested region.

(d) Competing product loss or precipitation. The final selective yield did not scale monotonically with conversion or time, especially for S0/E0, whose precipitation signal was near unity. I therefore model isolated/selective product as something like

  Y_sel ≈ X × S(eta, materials, pH) × R_product,

where S is electrochemical selectivity and R_product is a retention/recovery factor that can fall through precipitation, secondary reaction, or degradation. The assay channels need not obey this equation exactly because they are independently noisy synthetic observables. Precipitation is a plausible contributor to R_product, but it cannot be the only contributor.

3. Evidence for cathodic activation and an intermediate potential window

Batch 1 used S0/E0, +1.2 V, a 100 mA ceiling, and 300 s. It was essentially inactive: selective yield 0, electrochemical selectivity 0.01035, faradaic efficiency 0.02452, transport efficiency 0, and energy efficiency 0.00526. Conversion was only 0.00801 and precipitation signal was 1.000.

Batch 2 changed only the sign to -1.2 V. It gave selective yield 0.01087, selectivity 0.6320, faradaic efficiency 0.3906, transport efficiency 0.4169, energy efficiency 0.1993, and score 0.1599. Its reported conversion was clipped or unresolved at 0 despite nonzero yield, which I treat as a near-floor measurement inconsistency rather than evidence for product formation without conversion. The large multichannel difference between batches 1 and 2 establishes polarity dependence much more strongly than any one near-zero channel.

Batch 3, at -0.6 V under otherwise matched S0/E0 conditions, had high selectivity (0.6986), faradaic efficiency (0.4843), transport efficiency (0.5008), and energy efficiency (0.6311), but selective yield was unresolved at 0. This is consistent with an efficient but low-rate regime below or near the productive activation threshold.

Batch 4, at -1.8 V, produced a small selective yield of 0.00205 but had lower selectivity (0.5148), faradaic efficiency (0.3266), transport efficiency (0.2951), and especially energy efficiency (0.05515) than the moderate-potential cases. Thus, increasingly negative potential is not uniformly beneficial. A plausible interpretation is that a desired cathodic pathway competes with side reduction, solvent/electrolyte reaction, or nonproductive charging at high overpotential.

A schematic potential law would be

  eta = max[0, -(V - V_onset(materials))],
  rate_desired ∝ f_activation(eta) f_transport,
  selectivity ≈ S_max / [1 + g_side(eta)],

where f_activation rises after onset but g_side rises at large eta. This produces an intermediate optimum rather than a monotonic response to |V|.

4. Current-ceiling evidence

Batches 5, 2, and 6 used S0/E0, -1.2 V, and 300 s with current ceilings of 20, 100, and 300 mA, respectively. Their selective yields were 0.00884, 0.01087, and 0.01354. Their final faradaic efficiencies were 0.3971, 0.3906, and 0.2416, while transport efficiencies were 0.3866, 0.4169, and 0.2169.

The slight increase in measured yield with the ceiling is compatible with partial current limitation, but the changes are modest and non-monotone across efficiency channels. Because delivered current was not observed and these are single batches, I cannot locate the current-saturation crossover. Two alternatives remain plausible:

• The cell demand was near or below these ceilings for much of the run, so changing the ceiling had little causal effect.
• Higher ceilings increased charge transfer but also increased transport polarization or parasitic current, explaining the lower efficiencies at 300 mA.

Accordingly, I treat current as a ceiling, not as proof that the specified current flowed. Predictions should use I_actual = min(I_cap, I_demand), with substantial uncertainty in I_demand.

5. Time dependence and possible product loss

At S0/E0, -1.2 V, and a 100 mA ceiling, batches 2, 7, and 8 used 300, 900, and 3600 s. Reported conversion was 0, 0.01947, and 0.03144, respectively, broadly supporting increasing conversion with charge/time. Selective yield, however, was 0.01087, 0.01296, and then only 0.00185. Batch 8 retained selectivity 0.6165 and faradaic efficiency 0.3988, but its precipitation signal was 0.99496.

This rules out a simple globally linear yield-versus-time law. The most plausible account is an initially rising conversion combined with a time-dependent loss or recovery penalty. Candidate processes include precipitation of target or precursor, secondary electrolysis of product, depletion-driven loss of selectivity, and ordinary process/assay variability. The data do not distinguish these. A reasonable predictive form is therefore a saturating conversion multiplied by a retention term, for example

  X(t) = X_inf[1 - exp(-k t)],
  R_product(t) = exp(-k_loss t) or 1/[1 + k_p P(t)],
  Y_sel(t) = X(t) S(t) R_product(t).

This form permits a yield maximum at finite time. It is a conjectural extrapolation, not a fitted equation.

6. Material and pH/precipitation coupling

The public dossier suggests that electrolyte and solvent jointly shift standard potential, conductivity, diffusivity, double-layer behavior, proton activity, and salt solubility. I regard those quantities as priors, not as a complete ranking, because hidden campaign-fixed material residuals were explicitly possible.

Batches 8-11 compared paired material choices at -1.2 V, 100 mA, and 3600 s:

• Batch 8, S0/E0: conversion 0.03144, selectivity 0.6165, yield 0.00185, faradaic efficiency 0.3988, transport efficiency 0.3924, ohmic efficiency 0.9887, energy efficiency 0.2080, pH_normalized 0.23076, precipitation 0.99496, score 0.02712.

• Batch 9, S1/E1: conversion 0.02467, selectivity 0.4695, yield 0.02995, faradaic efficiency 0.2762, transport efficiency 0.2971, ohmic efficiency 0.9866, energy efficiency 0.1955, pH_normalized 0.20603, precipitation 0.72618, score 0.2530.

• Batch 10, S2/E2: conversion 0.04293, selectivity 0.5599, yield 0.01247, faradaic efficiency 0.3045, transport efficiency 0.3059, ohmic efficiency 0.9296, energy efficiency 0.2422, pH_normalized 0.17283, precipitation 0, score 0.1683.

• Batch 11, S3/E3: conversion 0.03688, selectivity 0.4489, yield 0.01232, faradaic efficiency 0.2534, transport efficiency 0.2606, ohmic efficiency 0.9746, energy efficiency 0.1981, pH_normalized 0.27777, precipitation 0.00524, score 0.1471.

These observations show a strong material effect, but solvent and electrolyte were changed together, so their separate causal contributions are unidentifiable. S1/E1 delivered much more selective product than S0/E0 despite lower measured conversion and electrochemical selectivity. This supports a post-electron-transfer retention/recovery effect or reveals that the assay channels are not intended to satisfy an exact mass-action identity.

Precipitation alone does not rank the materials: S2/E2 and S3/E3 essentially suppressed precipitation but did not surpass S1/E1 yield. Thus the response likely balances several coupled effects: cathodic onset, proton availability, transport, desired-path selectivity, and product retention. The normalized pH values also moved with material choice, but because pH and material identity were not independently varied, acidity cannot be assigned a unique causal coefficient.

A material-sensitive effective-potential model would use

  V_onset = V_base + DeltaV_solvent + DeltaV_electrolyte + delta_hidden,

and separate functions for conductivity, transport, proton activity, and precipitation. The dossier shifts make such coupling plausible, but the experimental design cannot estimate each term independently.

7. Evidence around the recommended region

Batch 12 used S1/E1, -0.9 V, 100 mA, and 3600 s. It produced selective yield 0.02663, conversion 0.01401, selectivity 0.4947, faradaic efficiency 0.2920, transport efficiency 0.3132, ohmic efficiency 0.9585, energy efficiency 0.2592, pH_normalized 0.20522, precipitation 0.71657, and the highest observed score, 0.2655.

Compared with batch 9 at -1.2 V using the same materials and duration, batch 12 had slightly lower selective yield (0.02663 versus 0.02995) but higher energy efficiency (0.2592 versus 0.1955), transport efficiency (0.3132 versus 0.2971), and score (0.2655 versus 0.2530). These are single observations, so I do not claim that -0.9 V is definitively superior. Together they bracket a promising S1/E1 operating window around -0.9 to -1.2 V and illustrate the expected rate-efficiency tradeoff.

8. What changed my explanation

The batch 1 versus batch 2 sign reversal rejected my initial possibility that response might mainly depend on absolute potential magnitude. Batches 3 and 4 then changed the explanation from a simple cathodic monotonic law to an activation-plus-parasitic-reaction window.

The cap series in batches 5 and 6 failed to establish a simple proportional current law; this led me to distinguish the specified ceiling from delivered current.

The 900 and 3600 s runs in batches 7 and 8 showed that conversion can increase without proportional selective-yield improvement. This added a retention, precipitation, or secondary-loss factor to the account.

Finally, batches 9-11 showed that nominal conductivity or precipitation avoidance alone cannot rank the material pairs. Batch 12 supported the existence of a moderate cathodic S1/E1 region with a better balanced efficiency tradeoff.

9. Identifiable and unidentifiable quantities

Reasonably supported:

• Productive polarity is cathodic.
• There is a material-dependent activation region.
• Excessive cathodic magnitude lowers selectivity and energy efficiency.
• Conversion is at least partly charge/time dependent.
• Material choice strongly affects pH, precipitation, conversion, yield, and efficiencies.
• A single monotonic potential, time, or conductivity ranking is inadequate.

Not identified:

• Actual current, passed charge, electron stoichiometry, exchange current, transfer coefficient, and formal onset potential.
• Individual solvent effects versus individual electrolyte effects, because the long-duration material screen changed them in matched pairs.
• The causal effect of pH independent of material.
• Whether precipitation consumes target, precursor, or an unrelated salt.
• Whether the long-time yield loss is precipitation, target degradation, secondary electrolysis, depletion, or process variability.
• Concentration/volume scaling, since all batches used one loading.
• Repeatability and world-to-world transfer, because no exact batch was replicated and hidden residuals are campaign-specific.

10. Plausible alternative models

One alternative is that most apparent non-monotonic yield behavior is near-floor assay/process noise rather than chemical loss. This is credible for the very small S0/E0 yields and the conversion/yield inconsistencies. It is less able to explain the coherent, large polarity changes across several efficiency channels.

A second alternative is that precipitation is merely a spectator salt signal and does not remove target product. In that case, the S0/E0 long-time behavior would instead require secondary electrolysis, changing selectivity, or measurement variability.

A third alternative is a purely empirical material-specific response surface with no transferable decomposition into conductivity, pH, transport, and potential shift. The sparse paired-material data cannot reject this. Nevertheless, the mechanistic decomposition is preferable for extrapolation because it captures the observed polarity, charge, transport, ohmic, and precipitation couplings while explicitly retaining hidden residual terms.

11. Overall predictive picture

For conditions close to those tested, I would predict negligible useful conversion under positive polarization; efficient but possibly rate-limited behavior at weak cathodic drive; maximum balanced performance at intermediate cathodic potential; and declining selectivity/energy efficiency at excessive cathodic magnitude. Increasing time or a binding current ceiling should initially increase conversion, but selective yield may plateau or decline if product loss or precipitation becomes important. Material changes shift both onset and efficiency through coupled transport, ohmic, proton-activity, solubility, and hidden interfacial effects. Among observed conditions, S1/E1 at -0.9 to -1.2 V and 3600 s was the most promising region, but that is an empirical local conclusion, not evidence of a universal optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior response law or prior optimum was supplied. The only supplied priors were the nominal material dossier and general instrument/scoring contracts; the dossier explicitly allowed hidden, campaign-fixed residuals and did not supply selectivity or faradaic efficiency.

• Supported: productive conversion is cathodic and potential-sign sensitive. Batch 1 (+1.2 V, S0/E0) was essentially inactive, with zero selective yield and near-zero electrochemical efficiencies, whereas batch 2 (-1.2 V, otherwise matched) had selective yield 0.01087, selectivity 0.6320, and faradaic efficiency 0.3906. This changed my initial hypothesis from a possible dependence on absolute potential magnitude to a signed cathodic activation law.

• Supported qualitatively: there is an intermediate cathodic efficiency window rather than monotonic improvement with increasingly negative potential. Batch 3 at -0.6 V had high selectivity and energy efficiency but unresolved yield; batch 2 at -1.2 V formed measurable product; batch 4 at -1.8 V lost selectivity and energy efficiency. These results motivated an activation term combined with a growing parasitic-reaction penalty.

• Partly supported: conversion depends on charge or electrolysis time. At S0/E0 and -1.2 V, reported conversion increased from near the assay floor in batch 2 at 300 s to 0.01947 in batch 7 at 900 s and 0.03144 in batch 8 at 3600 s. A simple linear selective-yield law was contradicted, however: selective yield did not rise proportionally and was only 0.00185 in batch 8. Product loss, precipitation, secondary electrolysis, and independent assay noise remain competing explanations.

• Supported: material choice strongly affects the response. Under matched -1.2 V, 100 mA, 3600 s conditions, batches 8-11 showed large differences in pH, precipitation, conversion, yield, and efficiency. S1/E1 in batch 9 greatly outperformed S0/E0 in batch 8 in selective yield and score, while S2/E2 and S3/E3 in batches 10 and 11 nearly eliminated precipitation without giving the best yield.

• Contradicted as a sufficient law: nominal conductivity, diffusivity, or precipitation avoidance alone cannot rank performance. For example, the nearly zero precipitation in batches 10 and 11 did not make either superior to batch 9. The nominal dossier remains useful mechanistic context, but experimental evidence did not support reducing the response to one dossier property.

• Untested: separate solvent and electrolyte coefficients. Batches 9-11 changed solvent and electrolyte together, so their individual contributions and interactions were not identified. Likewise, pH was not manipulated independently.

• Untested quantitatively: the current-ceiling law. Batches 5, 2, and 6 compared 20, 100, and 300 mA ceilings, but delivered current was not observed and the differences were modest or non-monotone. These results neither established proportional scaling with the ceiling nor demonstrated a definite plateau.

• Untested: concentration scaling, exact electron stoichiometry, exchange current, formal onset potential, and world-to-world transfer. Every batch used the same 0.50 mol L^-1 nominal loading, and no exact replicate was performed.

Batch 12 changed my practical judgment by showing that S1/E1 at -0.9 V retained nearly the selective yield of batch 9 at -1.2 V while improving energy efficiency and the balanced score. It therefore narrowed the promising local region to approximately -0.9 to -1.2 V, but one observation at each potential was insufficient to establish a precise optimum.

2. One additional discriminating experiment

I would run S0/E1 at the same loading and settings used for the long material comparison: 0.020 mol reagent, 0.040 L S0, -1.2 V, 100 mA ceiling, 3600 s, followed by the final assay. This single crossover holds the solvent fixed relative to batch 8 and changes only E0 to E1; it can be compared with batch 8 (S0/E0) and batch 9 (S1/E1).

My leading explanation is that electrolyte-dependent potential, transport, acidity, and salt-solubility effects contribute materially to the batch 8 versus 9 difference, including the precipitation change. A plausible alternative is that the S1 solvent or a specific S1/E1 interaction dominates and E1 alone has little benefit.

• If S0/E1 moved both precipitation and selective yield substantially toward batch 9, I would strengthen the electrolyte-driven coupling explanation and weaken the claim that S1 is essential.

• If precipitation fell toward batch 9 but yield remained near batch 8, I would treat precipitation as an incomplete or possibly spectator marker and increase belief in solvent/interfacial control of target formation or recovery.

• If both precipitation and yield remained near batch 8, I would infer that S1 or an S1×E1 interaction is the major cause of batch 9's performance.

• An intermediate response would support contributions from both components but would not distinguish additivity from interaction.

Because selective-yield assay noise is about 0.01 and the existing batch 8 and 9 channels are internally inconsistent near that scale, one crossover batch would update rather than conclusively settle the mechanism. Exact replication would still be needed for a strong causal conclusion.

3. Unused evidence, unreliable predictions, and effect of the assigned goal

The raw UV-visible spectra and detailed signal artifacts were not used in the final model; I mainly used their processed efficiency channels and the more precise final assays. Intermediate pH measurements were used only qualitatively. I also did not develop quantitative models from cost, accumulated risk, temperature changes, or electrolysis energy cost. These fields might contain indirect information about delivered current or heating, but without a validated mapping I avoided treating them as current measurements. No direct current-time trace, charge integral, product identity, or species-resolved mass balance was available.

The least reliable predictions are the crossover-material cases Q05-Q10 because the campaign never independently crossed solvents and electrolytes. Predictions at 7200 s extrapolate beyond the longest tested duration of 3600 s, and Q11-Q12 use a 500 mA ceiling beyond the tested 300 mA maximum. The positive-potential predictions are directionally supported by batch 1 but extrapolate from +1.2 V to +0.8 V and across untested materials. The score predictions are especially uncertain because the score is multiplicatively gated by selective yield below 0.02; ordinary assay noise near zero can therefore cause a large relative score change. Q01 also combines an interpolated -0.8 V response with a short duration not directly tested at that potential.

The sealed recommendation is locally empirical rather than broadly causal: batch 12 had the best observed balanced score, but its superiority over batch 9 was small and unreplicated. It should not be interpreted as a universal optimum.

The assigned primary goal—developing an explanatory and predictive account rather than merely maximizing score—did affect evidence collection. I spent batches on polarity, potential magnitude, current ceiling, duration, and contrasting material pairs instead of repeatedly exploiting S1/E1 or replicating the apparent optimum. This produced broader mechanistic evidence but left repeatability, fine optimization, and component-wise material effects weakly resolved. I see no fundamental conflict between the stated goal and the final recommendation: exploration served the research objective, while the final sealed choice used the best observed balanced result.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.59,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.38,
        "upper80": 0.54
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.069,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.024
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.37,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.59,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.38,
        "upper80": 0.54
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.36,
        "lower80": 0.17,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.032,
        "lower80": 0.011,
        "upper80": 0.057
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.37,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.53,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.31,
        "upper80": 0.53
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.331,
        "lower80": 0.15,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.011,
        "upper80": 0.066
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.29,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.045
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.46,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.09,
        "upper80": 0.33
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.23,
        "upper80": 0.45
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.285,
        "lower80": 0.11,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.009,
        "upper80": 0.067
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.19,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.022,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.5,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.12,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.49
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.298,
        "lower80": 0.1,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.032,
        "lower80": 0.007,
        "upper80": 0.064
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.22,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "energy_efficiency": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.021,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.51,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.19,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.52
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.324,
        "lower80": 0.14,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.036,
        "lower80": 0.011,
        "upper80": 0.071
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.045
      }
    }
  ],
  "rationale": "The campaign established a strong polarity effect: cathodic operation was productive, whereas positive polarization was essentially inactive. Negative-potential estimates interpolate the observed activation/efficiency window near -0.6 to -1.2 V and use a saturating time response; the 500 mA ceiling is treated as only partly informative because delivered current was not measured. Cross-material predictions incorporate nominal potential, transport, conductivity, and precipitation differences but receive wider intervals because solvent and electrolyte effects were confounded in the campaign. Intervals also include final-assay noise, near-zero clipping, sparse material coverage, and the score's strong multiplicative sensitivity to selective yield below 0.02."
}
```
