# repeat-03/EC-W02-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W02-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative; pre-experiment]
At fixed loading (0.020 mol reagent in 0.050 L solvent), positive potential should produce more target than negative potential, but excessive magnitude or duration may reduce selectivity and energy efficiency. I will test both signs and a broad duration/potential/current range; this claim would be rejected if negative-potential batches outperform comparable positive ones.

## H2 [tentative; pre-experiment]
Transport and ohmic performance should depend jointly on solvent/electrolyte. Nominally conductive media (especially S0 and E0/E3) may improve efficiency, whereas thinner diffusion layers/high diffusivity (notably E1/E2) may improve transport. Because selectivity is unspecified and dossier misindexing is possible, empirical assay scores are authoritative.

## Decision rule
Use early factorial-style coverage, then spend later batches around the best observed region while retaining at least one sign and time contrast. Numerical differences smaller than assay uncertainty will not be treated as effects without replication.

### v2 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage interpretation

## H1 [unresolved outside positive-potential scope]
The anticipated positive-potential productive window was found, but no negative-potential batch was ultimately run, so the sign claim remains untested. Within positive conditions, magnitude strongly mattered: S2/E2 at +1.2 V gave score 0.393 at 2400 s and improved with time to 0.515 at 14400 s (final-assay events runner-operation-0021, -0042, -0049, -0056), while +2.0 V at 2400 s collapsed to score 0.028 (runner-operation-0035). This supports an overpotential/degradation optimum rather than monotonic benefit from voltage. A negative-potential assay or matched polarity pair would change the sign conclusion.

## H2 [supported qualitatively; material–potential coupling]
Material choice and potential must be treated jointly. S1/E1 at +0.85 V substantially outperformed S2/E2 at +1.2 V: score 0.662 at 7200 s and 0.698 at 12000 s (runner-operation-0063, -0070), versus the best S2/E2 score 0.515 at 14400 s (runner-operation-0056). S3/E3 at +1.2 V was poor (0.250; runner-operation-0028). These are large numerical differences relative to assay channel noise, but combinations were not replicated and solvent/electrolyte effects were not separated.

## H3 [supported in the S1/E1 local window]
At 0.020 mol in 0.050 L, 500 mA cap, S1/E1, +0.85 V, extending electrolysis from 7200 to 12000 s increased score from 0.662 to 0.698 and selective yield from 0.548 to 0.695 (runner-operation-0063, -0070). A lower +0.75 V for 14400 s gave more conversion/yield but lower balanced score 0.688 (runner-operation-0077); +0.90 V for 12000 s gave 0.693 (runner-operation-0084). Thus +0.85 V, 12000 s is the observed local best, with uncertainty about whether 12000–14400 s at exactly +0.85 V could improve it.

## Confounds and limits
All comparisons use one final assay each; no process replicates were run. Precipitation signal remained high (~0.70) in the best S1/E1 region, so the recommendation maximizes the declared balanced score rather than minimizing precipitation. The current value was a cap; delivered current was not directly measured. Intermediate UV–vis observations supported efficiency tracking but were not used to claim independent causal effects.

## Final decision
Recommend completed batch 10 (lifecycle index 10): fixed loading 0.020 mol/0.050 L, solvent S1, electrolyte E1, +0.85 V, 500 mA cap, 12000 s. This is the highest observed assay score (0.6978). I would change this choice only if a replicate or a targeted +0.85 V duration refinement exceeded it beyond assay/process variability.

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
    "electrochemical_conversion": 0.022787874564528465,
    "electrochemical_selectivity": 0.8980063199996948,
    "energy_efficiency": 0.8702253699302673,
    "faradaic_efficiency": 0.9748222827911377,
    "ohmic_efficiency": 0.9653005003929138,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
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
      "solvent": 1,
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
    "cost": 0.32659998536109924,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.010023192502558231,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.851642370223999,
    "pH_normalized": 0.2061888426542282,
    "precipitation_signal": 0.7158817648887634,
    "safety_risk": 0.08273958414793015,
    "score": 0.03364749997854233,
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
      "solvent": 2,
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.3425808250904083,
    "electrochemical_conversion": 0.11613637953996658,
    "electrochemical_selectivity": 0.9174968600273132,
    "energy_efficiency": 0.5224276185035706,
    "faradaic_efficiency": 0.37627992033958435,
    "ohmic_efficiency": 0.6260465383529663,
    "pH_normalized": 0.17439326643943787,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.3928523659706116,
    "selective_product_yield": 0.10243018716573715,
    "transport_efficiency": 0.3928368389606476
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.3227599859237671,
    "electrochemical_conversion": 0.025539623573422432,
    "electrochemical_selectivity": 0.8646482825279236,
    "energy_efficiency": 0.0961773544549942,
    "faradaic_efficiency": 0.12255826592445374,
    "ohmic_efficiency": 0.89545077085495,
    "pH_normalized": 0.27948322892189026,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.25022342801094055,
    "selective_product_yield": 0.026985013857483864,
    "transport_efficiency": 0.09107072651386261
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
      "solvent": 2,
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 2
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
    "cost": 0.3465999960899353,
    "electrochemical_conversion": 0.0034490374382585287,
    "electrochemical_selectivity": 0.006436008028686047,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.01102422270923853,
    "ohmic_efficiency": 0.7748655080795288,
    "pH_normalized": 0.1786634773015976,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.028449540957808495,
    "selective_product_yield": 0.0084654176607728,
    "transport_efficiency": 0.0005147586925886571
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.2
    },
    {
      "duration_s": 4800,
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
    "cost": 0.34816163778305054,
    "electrochemical_conversion": 0.23072245717048645,
    "electrochemical_selectivity": 0.935015857219696,
    "energy_efficiency": 0.4912004768848419,
    "faradaic_efficiency": 0.4034203886985779,
    "ohmic_efficiency": 0.6394956111907959,
    "pH_normalized": 0.17538753151893616,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.10073958337306976,
    "score": 0.4413740634918213,
    "selective_product_yield": 0.2230852246284485,
    "transport_efficiency": 0.37873706221580505
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.2
    },
    {
      "duration_s": 9600,
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
    "cost": 0.35932326316833496,
    "electrochemical_conversion": 0.4152509570121765,
    "electrochemical_selectivity": 0.9286056756973267,
    "energy_efficiency": 0.43981027603149414,
    "faradaic_efficiency": 0.3381659686565399,
    "ohmic_efficiency": 0.6710571646690369,
    "pH_normalized": 0.174402117729187,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.4904566705226898,
    "selective_product_yield": 0.38416019082069397,
    "transport_efficiency": 0.3415663242340088
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
      "potential_V": 1.2
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
    "cost": 0.3704848885536194,
    "electrochemical_conversion": 0.5359103679656982,
    "electrochemical_selectivity": 0.9252822399139404,
    "energy_efficiency": 0.38708698749542236,
    "faradaic_efficiency": 0.30731067061424255,
    "ohmic_efficiency": 0.6563531756401062,
    "pH_normalized": 0.17270465195178986,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.10073958337306976,
    "score": 0.5147081613540649,
    "selective_product_yield": 0.48264893889427185,
    "transport_efficiency": 0.3008153438568115
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.85
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
    "cost": 0.31723999977111816,
    "electrochemical_conversion": 0.5824928879737854,
    "electrochemical_selectivity": 0.898430347442627,
    "energy_efficiency": 0.7019268870353699,
    "faradaic_efficiency": 0.6178517937660217,
    "ohmic_efficiency": 0.7684444785118103,
    "pH_normalized": 0.20722901821136475,
    "precipitation_signal": 0.7148279547691345,
    "safety_risk": 0.08273958414793015,
    "score": 0.6620736718177795,
    "selective_product_yield": 0.5476157665252686,
    "transport_efficiency": 0.638683021068573
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
      "potential_V": 0.85
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
    "cost": 0.3253999948501587,
    "electrochemical_conversion": 0.7839137315750122,
    "electrochemical_selectivity": 0.9266225099563599,
    "energy_efficiency": 0.6851043701171875,
    "faradaic_efficiency": 0.503382682800293,
    "ohmic_efficiency": 0.7278953790664673,
    "pH_normalized": 0.2049148678779602,
    "precipitation_signal": 0.7039898037910461,
    "safety_risk": 0.08273958414793015,
    "score": 0.6977863311767578,
    "selective_product_yield": 0.695083737373352,
    "transport_efficiency": 0.5047322511672974
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
      "potential_V": 0.75
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
    "cost": 0.32659998536109924,
    "electrochemical_conversion": 0.8407242298126221,
    "electrochemical_selectivity": 0.8787923455238342,
    "energy_efficiency": 0.6375918388366699,
    "faradaic_efficiency": 0.44564682245254517,
    "ohmic_efficiency": 0.7065370082855225,
    "pH_normalized": 0.2058999091386795,
    "precipitation_signal": 0.7118789553642273,
    "safety_risk": 0.08273958414793015,
    "score": 0.6875274181365967,
    "selective_product_yield": 0.7357137203216553,
    "transport_efficiency": 0.45282676815986633
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
      "potential_V": 0.9
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
    "cost": 0.32659998536109924,
    "electrochemical_conversion": 0.752135694026947,
    "electrochemical_selectivity": 0.9005311727523804,
    "energy_efficiency": 0.6828176379203796,
    "faradaic_efficiency": 0.4602423906326294,
    "ohmic_efficiency": 0.7692374587059021,
    "pH_normalized": 0.20642022788524628,
    "precipitation_signal": 0.7052149176597595,
    "safety_risk": 0.08273958414793015,
    "score": 0.692571222782135,
    "selective_product_yield": 0.7164683938026428,
    "transport_efficiency": 0.4814673364162445
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this world as a charge-driven electrochemical conversion with three strongly coupled subsystems: electrode kinetics/selectivity, charge and mass transport, and medium-dependent acid/precipitation chemistry. The applied potential does not act independently of solvent and electrolyte. Instead, each solvent–electrolyte pair shifts the effective electrochemical window and changes conductivity, diffusion, interfacial capacitance, proton activity, precipitation, and probably hidden selectivity factors.

All batches used 0.020 mol reagent in 0.050 L solvent. Except for batch 1, the configured current ceiling was 500 mA. Thus most direct comparisons concern potential, duration, and the paired solvent/electrolyte identity.

### Proposed process model

A useful qualitative model is:

η = V_applied − E_effective(solvent, electrolyte, pH, hidden interfacial factors)

i_delivered = min(i_limit, i_ohmic(η, conductivity), i_transport(concentration, diffusivity, boundary layer))

Q = integral(i_delivered dt)

The productive reaction rate initially increases with useful overpotential and delivered charge. However, side reactions and degradation increase when the effective overpotential is too large or electrolysis continues after readily accessible reagent is depleted. A schematic pair of rate laws would be:

r_target = k_target(materials, η, pH) × C_reactant × f_transport

r_side = k_side(materials, η, pH) × g(Q, product concentration)

with k_target rising over a productive potential range but k_side increasing much more steeply beyond it. Conversion should therefore grow with charge only within a suitable potential window, while selectivity and Faradaic efficiency can decline at excessive voltage or dose.

Selective product yield is approximately related to conversion and selectivity, but the reported channels are independently noisy and may also represent different physical bases. Product precipitation, sequestration, degradation, and mass-balance effects can make the measured yield depart from the simple product conversion × selectivity. For example, batch 10 had conversion 0.7839 and selectivity 0.9266, whose simple product is about 0.727, while measured selective yield was 0.6951.

## Evidence that shaped the explanation

### 1. Excess potential is destructive rather than merely inefficient

The clearest matched potential comparison is between batches 3 and 5. Both used S2/E2, 500 mA, and 2400 s. At +1.2 V, batch 3 produced conversion 0.1161, selectivity 0.9175, selective yield 0.1024, and score 0.3929. Raising the potential to +2.0 V in batch 5 collapsed conversion to 0.00345, selectivity to 0.00644, selective yield to 0.00847, and score to 0.02845. Faradaic efficiency also fell from 0.3763 to 0.0110, and transport efficiency from 0.3928 to 0.000515.

This result changed the working explanation from a simple “more voltage gives more reaction” picture to a sharply bounded productive window. Plausible processes include rapid solvent/electrolyte discharge, electrode passivation, destruction of product or reactant, and diversion of current into unobserved side products. The available observations cannot distinguish these alternatives. The near-zero selectivity and Faradaic efficiency indicate that the failure is more than an ordinary ohmic penalty.

Batch 2 gives consistent but confounded evidence. With S1/E1 at +1.5 V, 500 mA, and 7200 s, it gave score 0.03365, conversion reported as zero, selectivity 0.0100, yield 0.00898, and zero reported energy and Faradaic efficiencies. In contrast, batch 9 used the same material pair and duration at +0.85 V and reached score 0.6621, conversion 0.5825, selectivity 0.8984, and yield 0.5476. The potential difference is the main controlled difference, strongly supporting catastrophic high-overpotential side chemistry in S1/E1.

### 2. Within a productive window, duration raises conversion but lowers charge efficiencies

Batches 3, 6, 7, and 8 form the best duration series. They all used S2/E2, +1.2 V, and a 500 mA ceiling, with durations of 2400, 4800, 9600, and 14400 s.

Observed conversion rose monotonically: 0.1161, 0.2307, 0.4153, and 0.5359. Selective yield likewise rose: 0.1024, 0.2231, 0.3842, and 0.4826. Selectivity stayed high and comparatively stable at 0.9175–0.9350. The balanced score increased more slowly, from 0.3929 to 0.4414, 0.4905, and 0.5147.

Meanwhile, energy efficiency generally declined from 0.5224 to 0.4912, 0.4398, and 0.3871. Faradaic efficiency was 0.3763, 0.4034, 0.3382, and 0.3073; transport efficiency was 0.3928, 0.3787, 0.3416, and 0.3008. I interpret this as diminishing productive return per additional unit of charge. Reagent depletion, concentration polarization, growing product inhibition, or increasing side-current share could all cause this pattern. Ohmic efficiency remained in a narrower 0.626–0.671 range, so the duration penalty was not primarily a worsening bulk-resistance effect.

S1/E1 showed the same basic dose tradeoff. From batch 9 at 7200 s to batch 10 at 12000 s, both at +0.85 V, conversion increased from 0.5825 to 0.7839 and selective yield from 0.5476 to 0.6951. Score increased from 0.6621 to 0.6978, but Faradaic efficiency decreased from 0.6179 to 0.5034 and transport efficiency from 0.6387 to 0.5047. Thus longer electrolysis makes more product while progressively sacrificing efficiency.

### 3. Material identity controls both transport and the location of the potential window

At the same +1.2 V, 500 mA, and 2400 s, batch 3 (S2/E2) scored 0.3929 whereas batch 4 (S3/E3) scored 0.2502. Batch 4 had conversion 0.0255, yield 0.0270, energy efficiency 0.0962, Faradaic efficiency 0.1226, and transport efficiency 0.0911, although its ohmic efficiency was relatively high at 0.8955. Therefore, high ohmic efficiency alone is insufficient: interfacial kinetics or mass transfer can remain poor even when resistive loss is modest.

The nominal material dossier suggests why the effective window shifts. Solvent and electrolyte both have declared standard-potential shifts, while their conductivity, diffusivity, diffusion-layer thickness, capacitance, and proton activity differ. These properties provide a mechanistic prior, not a complete law. Hidden fixed world residuals and solvent–electrolyte interactions were explicitly possible, and the experiments always changed solvent and electrolyte together. Consequently, I cannot identify separate solvent effects, separate electrolyte effects, or a transferable numerical standard potential from these data.

The strongest region was S1/E1 near +0.85 V. Batch 10, at +0.85 V for 12000 s, was the observed optimum: score 0.6978, conversion 0.7839, selectivity 0.9266, selective yield 0.6951, energy efficiency 0.6851, Faradaic efficiency 0.5034, transport efficiency 0.5047, and ohmic efficiency 0.7279.

Local voltage comparisons indicate a fairly broad but non-flat optimum. Batch 12 used S1/E1, +0.90 V, and 12000 s and scored 0.6926, with conversion 0.7521, selectivity 0.9005, yield 0.7165, and energy efficiency 0.6828. The score difference from batch 10 is small relative to the uncertainty implied by single noisy assays, so it is not strong evidence that +0.85 V is intrinsically superior to +0.90 V. It does show that +0.90 V remains productive, unlike +1.5 V. Batch 11 used +0.75 V for 14400 s and scored 0.6875. It achieved conversion 0.8407 and yield 0.7357 but lower selectivity (0.8788), energy efficiency (0.6376), and Faradaic efficiency (0.4456). Because both voltage and time differ from batch 10, this does not isolate the voltage effect.

### 4. Acid and precipitation chemistry are material-dependent secondary couplings

Final pH-normalized values clustered by material pair: approximately 0.174–0.179 for S2/E2, 0.204–0.207 for S1/E1, 0.279 for S3/E3, and 0.229 for S0/E0. This is consistent with electrolyte acid concentration/pKa and solvent proton-activity factors controlling a relatively stable medium property. It may also influence kinetics and selectivity, but pH was not varied independently, so causality is unidentifiable.

Precipitation was also strongly pair-specific. It was approximately 0.70–0.72 throughout the productive S1/E1 batches, essentially zero for S2/E2 and S3/E3, and 1.0 for S0/E0 in batch 1. This broadly agrees with the dossier’s different salt concentrations and solubility products. Nevertheless, S1/E1 still gave the highest balanced scores, so precipitation was not sufficient to prevent strong apparent product formation. It may represent a parallel salt process rather than direct target loss.

Batch 1 deserves caution. S0/E0 at +1.0 V, only 100 mA, and 600 s gave conversion 0.0228 and selectivity 0.8980 but selective yield reported as zero, alongside precipitation signal 1.0. One plausible interpretation is that the very small amount of product was lost or masked by precipitation; another is simple detection/noise behavior near the selective-yield gate. Because charge and duration were far lower than in the other batches, batch 1 cannot establish that S0/E0 is intrinsically poor.

## Relationship to the balanced score

The score weights yield most heavily but also rewards conversion, selectivity, Faradaic, transport, ohmic, and energy efficiency. Consequently, maximum conversion or yield alone need not maximize score. Batch 11 illustrates this: it had higher conversion and yield than batch 10, yet lower selectivity and efficiency channels produced a lower score. Batch 10 represented the best observed compromise between product formation and the diminishing efficiencies of extended electrolysis.

The multiplicative selective-yield gate also explains why low-product batches were especially poor. Batch 1 had zero reported selective yield and score zero despite excellent reported efficiency channels; these efficiencies were obtained after very little productive conversion and therefore did not constitute a useful operating point.

## Scope and uncertainties

This mechanism is supported only for the tested 0.020 mol/0.050 L loading, anonymous materials, positive potentials, and durations up to 14400 s. No negative-potential experiment was completed, so polarity dependence remains unresolved. The 500 mA setting was a ceiling; delivered current and total charge were not measured directly. Electrode area, spacing, and base resistance were fixed across the campaign but unknown, preventing extraction of intrinsic current densities or kinetic constants.

Each final condition was assayed once, with no process replicates. Small differences—particularly the scores of batches 10 and 12—should not be treated as resolved effects. Solvent and electrolyte were paired in every material comparison, so their individual contributions and interaction term cannot be separated. Temperature evolution, intermediate concentrations, actual side products, electrode passivation, and product precipitation identity were not observed. UV–visible measurements tracked public efficiency channels but did not identify chemical species.

Plausible alternative models include electrode passivation rather than molecular degradation at high voltage; precipitation-induced optical or sampling bias rather than actual product loss; and a hidden material-specific kinetic factor that dominates the nominal conductivity and diffusion properties. The data establish a bounded productive window and dose-dependent efficiency loss, but do not uniquely identify which microscopic process produces them.

Overall, my best explanation is that useful conversion is governed by delivered charge inside a material-specific potential window. Longer operation increases conversion and yield with diminishing Faradaic, transport, and energy returns. Excessive effective overpotential diverts charge into destructive or passivating pathways, causing a sharp collapse in selectivity. Solvent/electrolyte properties shift this window and independently control transport, pH, and precipitation. Within the explored region, S1/E1 at about +0.85 to +0.90 V was the best compromise, with the observed maximum balanced score at batch 10 (+0.85 V, 500 mA ceiling, 12000 s).

## K2 封存报告

1. **Supported, contradicted, and untested claims.** No instance-specific response law, prior batch outcome, or fitted model was supplied. The supplied information consisted of nominal material properties, instrument/scoring contracts, and the warning that hidden fixed residuals and solvent–electrolyte coupling could exist.

The self-developed law that productive response has a bounded, material-dependent potential window was strongly supported. With S2/E2 at identical current and duration, batch 3 at +1.2 V scored 0.3929, whereas batch 5 at +2.0 V collapsed to 0.02845, with selectivity falling from 0.9175 to 0.00644. Likewise, S1/E1 changed from a score of 0.03365 at +1.5 V in batch 2 to 0.6621 at +0.85 V in batch 9, both at 7200 s. These comparisons changed the interpretation from a potentially monotonic voltage response to a sharply nonmonotonic one involving side reactions, degradation, or passivation.

The proposed dose law—longer electrolysis increases conversion and yield but gives diminishing efficiency—was supported within the tested positive-potential region. The S2/E2 duration series in batches 3, 6, 7, and 8 increased conversion from 0.1161 to 0.5359 and yield from 0.1024 to 0.4826 as duration rose from 2400 to 14400 s. Over the same series, energy efficiency fell from 0.5224 to 0.3871 and transport efficiency from 0.3928 to 0.3008. Batches 9 and 10 showed the same tradeoff for S1/E1: longer operation increased yield from 0.5476 to 0.6951 but reduced Faradaic and transport efficiencies.

The claim that material identity and potential are coupled was qualitatively supported. At the same +1.2 V and 2400 s, S2/E2 in batch 3 outperformed S3/E3 in batch 4. However, because solvent and electrolyte were always changed together in these comparisons, separate solvent, electrolyte, and interaction effects remain unidentifiable. The stronger claim that nominal conductivity alone predicts performance was contradicted: batch 4 had high ohmic efficiency (0.8955) but poor transport efficiency (0.0911), conversion (0.0255), and score (0.2502).

The initial polarity claim—that positive potential is productive relative to negative potential—was untested, not supported experimentally. Every completed campaign batch used positive potential. Similarly, the small apparent advantage of +0.85 V over +0.90 V is unresolved: batches 10 and 12 differed in score by only about 0.0052, which is not persuasive without replication. The proposition that precipitation directly removes target product also remained unresolved. Batch 1 combined precipitation signal 1.0 with zero reported yield, but it also used a very small charge dose; batches 9–12 retained precipitation near 0.70 while producing substantial yield.

2. **One discriminating experiment.** I would use the established S1/E1 recipe and loading, expose it briefly to the problematic +1.5 V condition, measure UV–visible efficiency channels, then switch the same vessel to +0.85 V for the remainder of a 12000 s total electrolysis, measure again, terminate, and run the final assay. Batch 10 supplies the untreated +0.85 V reference, while batch 2 supplies the prolonged +1.5 V failure reference.

If the final result remained severely impaired after most of the run at +0.85 V—especially with persistently low selectivity and Faradaic efficiency—I would increase confidence in irreversible reagent/product destruction or electrode passivation caused by the high-voltage exposure. If the system recovered toward batch 10 after switching to +0.85 V, I would favor a reversible explanation such as instantaneous diversion of current into solvent/electrolyte discharge rather than lasting chemical or electrode damage. Partial recovery, accompanied by improved transport but persistently depressed selectivity, would suggest a mixture of reversible parasitic current and irreversible damage. This single-vessel intervention would still not distinguish molecular degradation from electrode passivation; electrode or chemical-species diagnostics would ultimately be required.

3. **Unused evidence, reliability, and goal effects.** Much of the intermediate UV–visible information was used only qualitatively; its raw spectra, band assignments, and detailed uncertainty fields were not fitted. Cost, small temperature changes during setup, cumulative process time, sample consumption, and most raw final-assay signals were also unused. The nominal conductivity, diffusivity, boundary-layer, capacitance, acidity, and solubility properties were interpreted mechanistically but were not sufficient to estimate a unique quantitative model. Actual delivered current and integrated charge were unavailable, so calculations based on the configured current ceiling remain uncertain.

The least reliable predictions are all negative-polarity cases (Q01, Q03, Q05, Q07, Q09, and Q11), because the campaign contained no negative-potential experiment. Predictions for untested crossed solvent–electrolyte combinations, especially Q05–Q10, are also weak because the campaign changed solvent and electrolyte together. Q12 is uncertain because it extrapolates to a smaller reagent charge and volume under a potentially excessive 500 mA dose. Even the batch 10 recommendation is only a local observed optimum: it was not replicated, and +0.85 V at 14400 s was never tested. The close scores of batches 10 and 12 make their exact ordering less reliable than the recommendation wording alone might imply.

The assigned score-maximization goal materially affected evidence collection. Later batches concentrated on the promising S1/E1 region rather than completing polarity tests, a full solvent-by-electrolyte factorial design, or process replicates. That choice improved the observed operating recommendation but weakened causal identification and prediction outside the positive-potential, paired-material region. Retrospectively, this is the clearest tension between optimization and mechanism learning; there was no separate evidence of a conflict with safety, since observed risks stayed well below the published limit.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.25
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.89,
        "lower80": 0.75,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.23,
        "lower80": 0.0,
        "upper80": 0.54
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.75,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.35
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.63,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.85,
        "lower80": 0.7,
        "upper80": 0.96
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.61,
        "lower80": 0.46,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.23,
        "lower80": 0.14,
        "upper80": 0.33
      },
      "transport_efficiency": {
        "estimate": 0.84,
        "lower80": 0.66,
        "upper80": 0.95
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.11
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.83,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.59,
        "upper80": 0.89
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.64,
        "upper80": 0.94
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.73
      },
      "selective_product_yield": {
        "estimate": 0.27,
        "lower80": 0.17,
        "upper80": 0.39
      },
      "transport_efficiency": {
        "estimate": 0.88,
        "lower80": 0.7,
        "upper80": 0.97
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.32
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.7,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.36,
        "upper80": 0.76
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.78
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.47,
        "lower80": 0.3,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.13
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.8,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.67,
        "lower80": 0.47,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.49,
        "upper80": 0.86
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.54,
        "lower80": 0.37,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.19,
        "lower80": 0.1,
        "upper80": 0.31
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.48,
        "upper80": 0.86
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "energy_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "faradaic_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.11
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.28
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.57,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.3,
        "upper80": 0.72
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.27,
        "upper80": 0.72
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.61,
        "lower80": 0.4,
        "upper80": 0.74
      },
      "selective_product_yield": {
        "estimate": 0.52,
        "lower80": 0.3,
        "upper80": 0.72
      },
      "transport_efficiency": {
        "estimate": 0.6,
        "lower80": 0.36,
        "upper80": 0.79
      }
    }
  ],
  "rationale": "Predictions use the observed positive-potential productive window, charge-duration scaling, and the decline in Faradaic, transport, and energy efficiency at high dose. Negative polarity was not tested, so it is assigned low target production with wider asymmetric uncertainty. Positive short-dose S0/E0 estimates are anchored to batch 1; longer-dose and mixed-material cases are extrapolated from the S1/E1 and S2/E2 duration series, with especially broad intervals for untested solvent–electrolyte combinations and the potentially over-electrolyzed 500 mA case."
}
```
