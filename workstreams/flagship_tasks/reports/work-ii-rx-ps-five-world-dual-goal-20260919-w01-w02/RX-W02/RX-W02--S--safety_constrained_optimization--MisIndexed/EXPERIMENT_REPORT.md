# RX-W02--S--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W02`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `73`
- Exact replay: `{'checked_steps': 73, 'max_abs_error': 0.0, 'mismatches': [], 'verified': True}`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `9`
- Rationale: Experiment 9 achieved the highest observed safe score (about 0.2346) while remaining comfortably below the 0.35 safety limit; it used water, Catalyst B, and a 370 K target for 7200 s.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.1975 | 0.6198 | 0.3225 | 0.1365 | 0.0035 | 0.1009 | 0.1208 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K × 7200 s @ 600 rpm | no | 0.4618 | 0.5716 | 0.8126 | 0.3666 | 0.1749 | 0.1664 | 0.2340 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 380 K × 7200 s @ 600 rpm | no | 0.4383 | 0.5721 | 0.7630 | 0.3388 | 0.1437 | 0.1622 | 0.2217 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 380 K × 7200 s @ 600 rpm | no | 0.4023 | 0.5199 | 0.7748 | 0.3761 | 0.1473 | 0.1599 | 0.1964 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K × 7200 s @ 600 rpm | no | 0.4165 | 0.4592 | 0.8825 | 0.4834 | 0.1979 | 0.1878 | 0.1852 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K × 7200 s @ 600 rpm | no | 0.3656 | 0.4152 | 0.8878 | 0.5310 | 0.2817 | 0.2075 | 0.1455 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K × 7200 s @ 600 rpm | no | 0.3873 | 0.4493 | 0.8888 | 0.5250 | 0.2285 | 0.2197 | 0.1573 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K × 14400 s @ 600 rpm | no | 0.3887 | 0.4172 | 0.9136 | 0.5552 | 0.2993 | 0.1508 | 0.1833 |
| 9 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K × 7200 s @ 600 rpm | no | 0.4477 | 0.5829 | 0.7763 | 0.3264 | 0.1361 | 0.1507 | 0.2346 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 365 K × 7200 s @ 600 rpm | no | 0.4348 | 0.5691 | 0.7414 | 0.3126 | 0.1216 | 0.1446 | 0.2253 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 375 K × 7200 s @ 600 rpm | no | 0.4506 | 0.5767 | 0.7935 | 0.3660 | 0.1538 | 0.1579 | 0.2327 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 371 K × 7200 s @ 600 rpm | no | 0.4330 | 0.5822 | 0.7892 | 0.3384 | 0.1336 | 0.1520 | 0.2292 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "instrument": "hplc",
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
  "end_step": 7,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.13649767637252808,
    "conversion": 0.3225175738334656,
    "cost": 1.0,
    "degradation_warning": 0.003453022800385952,
    "safety_risk": 0.10094886273145676,
    "score": 0.1207735612988472,
    "selectivity": 0.6197690367698669,
    "virtual_spectrum_summary": 0.07662758231163025,
    "yield": 0.1975163221359253
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `13`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 13,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3665979206562042,
    "conversion": 0.8125643134117126,
    "cost": 1.0,
    "degradation_warning": 0.1749381572008133,
    "safety_risk": 0.16637162864208221,
    "score": 0.23401637375354767,
    "selectivity": 0.5716028213500977,
    "virtual_spectrum_summary": 0.28035104274749756,
    "yield": 0.4618161916732788
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `19`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 19,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3387626111507416,
    "conversion": 0.7630037069320679,
    "cost": 1.0,
    "degradation_warning": 0.14366059005260468,
    "safety_risk": 0.16215969622135162,
    "score": 0.22169670462608337,
    "selectivity": 0.572140634059906,
    "virtual_spectrum_summary": 0.2509666979312897,
    "yield": 0.43833258748054504
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `25`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 25,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.376116544008255,
    "conversion": 0.7747650742530823,
    "cost": 1.0,
    "degradation_warning": 0.14729633927345276,
    "safety_risk": 0.15990111231803894,
    "score": 0.19642333686351776,
    "selectivity": 0.5199229717254639,
    "virtual_spectrum_summary": 0.27314743399620056,
    "yield": 0.4023039638996124
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `31`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 31,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.4834420680999756,
    "conversion": 0.8825247287750244,
    "cost": 1.0,
    "degradation_warning": 0.1978612095117569,
    "safety_risk": 0.18777093291282654,
    "score": 0.18515178561210632,
    "selectivity": 0.45920711755752563,
    "virtual_spectrum_summary": 0.35493066906929016,
    "yield": 0.41648614406585693
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `37`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 37,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.5310395956039429,
    "conversion": 0.8878082633018494,
    "cost": 1.0,
    "degradation_warning": 0.28168800473213196,
    "safety_risk": 0.20751458406448364,
    "score": 0.1454697549343109,
    "selectivity": 0.415245920419693,
    "virtual_spectrum_summary": 0.41883137822151184,
    "yield": 0.3656475245952606
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `43`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 43,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.5250259041786194,
    "conversion": 0.8888059258460999,
    "cost": 1.0,
    "degradation_warning": 0.22849589586257935,
    "safety_risk": 0.21974417567253113,
    "score": 0.1572655588388443,
    "selectivity": 0.4493313133716583,
    "virtual_spectrum_summary": 0.39158740639686584,
    "yield": 0.38734254240989685
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `49`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 49,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.5551927089691162,
    "conversion": 0.9136390686035156,
    "cost": 1.0,
    "degradation_warning": 0.2993077039718628,
    "safety_risk": 0.1507626622915268,
    "score": 0.1832895278930664,
    "selectivity": 0.4171563684940338,
    "virtual_spectrum_summary": 0.44004446268081665,
    "yield": 0.38869932293891907
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `55`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 55,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3263620138168335,
    "conversion": 0.7762748003005981,
    "cost": 1.0,
    "degradation_warning": 0.13612493872642517,
    "safety_risk": 0.15070588886737823,
    "score": 0.23462222516536713,
    "selectivity": 0.5829166173934937,
    "virtual_spectrum_summary": 0.2407553344964981,
    "yield": 0.4477080702781677
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `61`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 365
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 61,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3126102685928345,
    "conversion": 0.7413539886474609,
    "cost": 1.0,
    "degradation_warning": 0.12164078652858734,
    "safety_risk": 0.14456401765346527,
    "score": 0.22527268528938293,
    "selectivity": 0.5691173672676086,
    "virtual_spectrum_summary": 0.22667399048805237,
    "yield": 0.43477940559387207
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `67`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 375
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 67,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.36595457792282104,
    "conversion": 0.79348224401474,
    "cost": 1.0,
    "degradation_warning": 0.15378877520561218,
    "safety_risk": 0.1578710824251175,
    "score": 0.2327364683151245,
    "selectivity": 0.5767446756362915,
    "virtual_spectrum_summary": 0.2704799771308899,
    "yield": 0.4506101608276367
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `73`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 371
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 73,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.33838775753974915,
    "conversion": 0.7892408967018127,
    "cost": 1.0,
    "degradation_warning": 0.1336236447095871,
    "safety_risk": 0.15204772353172302,
    "score": 0.22923912107944489,
    "selectivity": 0.5821675658226013,
    "virtual_spectrum_summary": 0.2462439090013504,
    "yield": 0.4329865276813507
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidential basis

I completed 12 synthetic benchmark batches. Every batch used 0.040 mol of limiting reagent, 0.005 mol of catalyst, 0.080 L of one solvent, and 600 rpm stirring. Consequently, the campaign identifies categorical catalyst and solvent effects and a limited temperature/time response, but it does not identify concentration, catalyst-loading, reagent-loading, volume, or stirring-rate laws. The named solvents are selectable identities, but the task documentation explicitly says that their reaction effects are categorical benchmark effects; I therefore do not interpret them as validated real-solvent structure–property relationships.

All quoted values below are final-assay observations unless explicitly described otherwise. Instrument uncertainties and process variation mean that small differences, especially between neighboring temperature settings, should not be treated as exact kinetic trends.

2. Proposed reaction network

The observations are consistent with a minimal network containing a desired reversible pathway and at least one irreversible side pathway:

R ⇌ P
R → B
P → D

Here R is the anonymous limiting reactant, P is the target product, B is one or more competing byproducts, and D is degradation material. A more general version could include B → D or P ⇌ an unobserved intermediate, but the available observables cannot distinguish these possibilities.

A useful conceptual rate model is:

dR/dt = −k1 R + k−1 P − kb R
dP/dt = k1 R − k−1 P − kd P
dB/dt = kb R
dD/dt = kd P

with each rate constant depending on catalyst, solvent category, and temperature. For example,

ki(T,catalyst,solvent) = Ai(catalyst,solvent) exp[−Ei/(RT)].

This is a proposed explanatory form, not a fitted law. The initial public prior stated that the target path may have an appreciable reverse channel. The campaign does not directly isolate k−1, but the long-time behavior is compatible with reversibility plus irreversible sinks. Sequential loss of P without appreciable reversal is an equally plausible competing explanation.

3. Relationships among the public observables

Across most batches, target yield was approximately conversion multiplied by selectivity. For example:

• Batch 1: conversion 0.3225 × selectivity 0.6198 = 0.1999, versus observed yield 0.1975.
• Batch 2: 0.8126 × 0.5716 = 0.4645, versus yield 0.4618.
• Batch 9: 0.7763 × 0.5829 = 0.4524, versus yield 0.4477.

Similarly, byproduct signal was often close to conversion multiplied by one minus selectivity. In Batch 9 this estimate is 0.7763 × (1−0.5829) = 0.3238, compared with observed byproduct signal 0.3264. This suggests that conversion represents disappearance of R, selectivity partitions much of the converted material between target and non-target channels, and yield is substantially derived from that partition.

These relationships are approximate, not identities. Batch 12, for example, had conversion 0.7892 and selectivity 0.5822, whose product is about 0.4594, while reported yield was 0.4330. That discrepancy could reflect assay noise, process variability, degradation accounting, or distinct channel calibrations. The final assay reports degradation separately, so degradation warning should not automatically be added to byproduct signal as though both were nonoverlapping mass fractions.

4. Temperature and time effects in water with Catalyst B

The most informative controlled series used water, Catalyst B, 7200 s, and target temperatures from 365 to 380 K:

• Batch 10, 365 K: conversion 0.7414, yield 0.4348, selectivity 0.5691, byproduct 0.3126, degradation 0.1216, risk 0.1446, score 0.2253.
• Batch 9, 370 K: conversion 0.7763, yield 0.4477, selectivity 0.5829, byproduct 0.3264, degradation 0.1361, risk 0.1507, score 0.2346.
• Batch 12, 371 K: conversion 0.7892, yield 0.4330, selectivity 0.5822, byproduct 0.3384, degradation 0.1336, risk 0.1520, score 0.2292.
• Batch 11, 375 K: conversion 0.7935, yield 0.4506, selectivity 0.5767, byproduct 0.3660, degradation 0.1538, risk 0.1579, score 0.2327.
• Batch 2, 380 K: conversion 0.8126, yield 0.4618, selectivity 0.5716, byproduct 0.3666, degradation 0.1749, risk 0.1664, score 0.2340.

Conversion generally increased with temperature, as expected for thermally activated chemistry. Byproduct and degradation signals also increased, and selectivity did not improve systematically. Thus higher temperature accelerates desired conversion but also strengthens competing or sequential loss channels. Yield continued to rise modestly through 380 K, but the public safe score did not: the best observed score occurred at 370 K because the additional conversion at higher temperature was offset by higher byproduct, degradation, and safety risk.

The irregular difference between Batches 9 and 12—only a 1 K target change but a lower observed yield and score in Batch 12—is too large to interpret as a smooth deterministic temperature effect. It is evidence that assay/process variability matters at the resolution of this local search. Therefore, I infer a broad optimum near 370–380 K rather than a precisely established optimum at exactly 370 K.

5. Evidence for time-dependent loss and possible reversibility

Batch 8 used water and Catalyst B at 360 K for 14,400 s. It reached very high conversion, 0.9136, but only 0.3887 yield and 0.4172 selectivity. Its byproduct signal was 0.5552 and degradation warning 0.2993; its score was only 0.1833 despite a moderate risk of 0.1508.

This result strongly indicates that maximizing conversion or residence time is not equivalent to maximizing target yield or safe score. Material continues to move into non-target channels at long residence time. Three mechanisms remain plausible:

1. P undergoes sequential degradation, P → D.
2. Reversible P → R recycling gives R repeated opportunities to enter the irreversible R → B sink.
3. A slow parallel side reaction becomes dominant after the fast productive phase.

The initial structural prior favors including a reverse P → R channel, and the Batch 8 result is compatible with it, but the data do not uniquely prove reversal because no time-course concentration data were collected within an otherwise identical batch.

6. Catalyst effects

Batches 2–4 directly compared Catalysts B, C, and D in water at 380 K for 7200 s:

• Batch 2, Catalyst B: conversion 0.8126, yield 0.4618, selectivity 0.5716, degradation 0.1749, score 0.2340.
• Batch 3, Catalyst C: conversion 0.7630, yield 0.4383, selectivity 0.5721, degradation 0.1437, score 0.2217.
• Batch 4, Catalyst D: conversion 0.7748, yield 0.4023, selectivity 0.5199, degradation 0.1473, score 0.1964.

Catalyst B gave the highest conversion, yield, and score. Catalyst C preserved almost the same selectivity as B and produced less degradation, but it was less active. Catalyst D produced conversion similar to C but substantially worse target selectivity, implying greater relative promotion of the side channel.

Catalyst A was tested only in Batch 1 under much milder conditions: water, 340 K, 3600 s. It produced conversion 0.3225, yield 0.1975, selectivity 0.6198, byproduct 0.1365, degradation 0.00345, risk 0.1009, and score 0.1208. Its high selectivity and very low degradation are promising, but this is not a controlled catalyst comparison. Its low conversion may be caused by the lower temperature and shorter duration rather than low intrinsic activity. No defensible ranking of A against B or C can therefore be made at a common operating condition.

7. Solvent-category effects

Batches 2 and 5–7 compared solvents with Catalyst B at 380 K for 7200 s:

• Batch 2, water: conversion 0.8126, selectivity 0.5716, yield 0.4618, byproduct 0.3666, degradation 0.1749, risk 0.1664, score 0.2340.
• Batch 5, ethanol: conversion 0.8825, selectivity 0.4592, yield 0.4165, byproduct 0.4834, degradation 0.1979, risk 0.1878, score 0.1852.
• Batch 6, acetonitrile: conversion 0.8878, selectivity 0.4152, yield 0.3656, byproduct 0.5310, degradation 0.2817, risk 0.2075, score 0.1455.
• Batch 7, toluene: conversion 0.8888, selectivity 0.4493, yield 0.3873, byproduct 0.5250, degradation 0.2285, risk 0.2197, score 0.1573.

The three nonaqueous categories all increased overall conversion relative to water but disproportionately increased non-target chemistry. Water therefore appears to suppress kb and/or kd relative to k1, even though it also lowers the gross rate of reactant disappearance. This is why water gave the best yield and score in the solvent comparison.

Because these are calibrated categorical benchmark effects, it would be speculative to attribute the result to real-world polarity, proticity, heat capacity, or solvation without additional evidence. The supported inference is only that solvent category 0 favors the desired-to-undesired rate ratio in this benchmark.

8. Safety coupling

Every completed batch remained below the declared safety limit of 0.35. Within the water/Catalyst B temperature series, observed safety risk rose approximately monotonically from 0.1446 at 365 K to 0.1664 at 380 K. Thus thermal severity couples directly to risk.

Solvent category also affected risk at a fixed nominal temperature and duration: 0.1664 for water, 0.1878 for ethanol, 0.2075 for acetonitrile, and 0.2197 for toluene. The risk model therefore contains more than temperature alone; it includes categorical formulation effects and loading-related contributions. In Batch 1, the risk was already approximately 0.0722 after solvent, reagent, and catalyst charging, and heating to a 340 K target for 3600 s added about 0.0288, giving a final risk near 0.1009.

A qualitative decomposition consistent with the observations is:

risk ≈ rload(solvent,catalyst,amounts) + rthermal(T,time,solvent,catalyst),

where rthermal increases with temperature and exposure time. The experiment set is insufficient to establish whether risks are additive in a mechanistic sense or merely reported that way by the benchmark.

9. Interpretation of the score

The exact score equation was not exposed. Empirically, score rewards target yield/selectivity and penalizes some combination of byproduct, degradation, risk, and possibly cost. Conversion alone is clearly not the objective: Batch 8 had conversion 0.9136 but score 0.1833, whereas Batch 9 had conversion 0.7763 and score 0.2346. All final visible costs were reported as 1.0, so this campaign cannot estimate the cost coefficient.

A schematic objective consistent with the ranking is:

score = positive_function(yield, selectivity) × penalty(byproduct, degradation, safety risk, cost),

with the penalty decreasing as side signals or risk rise. This is explanatory only and is not a recovered scoring formula.

10. Why the recommended batch was selected

Batch 9 was the selected recommendation because it had the highest observed final safe score, 0.2346, while its safety risk, 0.1507, was well below 0.35. Its procedure was 0.080 L water, 0.040 mol limiting reagent, 0.005 mol Catalyst B, heating to a 370 K target for 7200 s at 600 rpm, followed by termination and final assay.

Batch 2 at 380 K was nearly tied, with score 0.2340 and higher yield, 0.4618 versus 0.4477, but also higher risk, byproduct, and degradation. Batch 11 at 375 K scored 0.2327. Given assay/process variability, these results support an operating region around 370–380 K rather than an exact singular optimum. Batch 9 is the strongest measured member of that region, not proof that 370 K is universally optimal.

11. Identifiability limits and competing explanations

The following factors remain unidentified:

• The magnitude of the reverse rate k−1 and whether reversal is direct or mediated by an intermediate.
• Whether degradation originates mainly from P, B, or a shared intermediate.
• Individual concentrations or mass fractions represented by byproduct and degradation signals.
• Activation energies, reaction orders, and equilibrium constants.
• Dependence on catalyst amount, reagent amount, solvent volume, or stirring rate, because these were held constant.
• Heat- and mass-transfer effects, because only one stirring speed and vessel scale were used.
• Whether Catalyst A would outperform B at matched temperature and duration.
• The exact safe-score equation and the relative penalty assigned to risk versus impurity signals.
• Fine-scale location of the thermal optimum, because neighboring batches show non-negligible variability and there were no exact replicates.

The principal competing model is an irreversible network R → P → D plus R → B, with no reverse P → R step. It explains the long-time loss of selectivity in Batch 8 at least as well as a reversible model. Another possibility is that catalyst or solvent state changes during prolonged heating, producing time-dependent rate constants. With only terminal assays, these alternatives cannot be separated.

12. Overall world model

The world behaves like a thermally activated, catalyst- and solvent-dependent competition between desired product formation and non-target conversion. Increasing temperature or duration raises conversion, but side-product formation and degradation grow as well. Catalyst B offers the best observed balance of activity and selectivity; water sacrifices some gross conversion but suppresses undesirable pathways more strongly than the other tested solvent categories. Target product is likely kinetically vulnerable, either through direct degradation or through a reverse channel followed by irreversible diversion. Consequently, the best safe operating policy is not to drive conversion to completion, but to stop within an intermediate-severity window where target accumulation remains favorable relative to byproduct and degradation growth.

## Q — Blind predictions

### Overall rationale

Predictions were extrapolated from the completed Catalyst B series, especially the acetonitrile batch at 380 K for 7200 s and the water temperature/time series. I treated conversion as an approximately saturating function of catalyst concentration, duration, and thermally activated exposure. Yield was constrained approximately by conversion times selectivity, while byproduct signal was centered near conversion times one minus selectivity. Selectivity was reduced at high temperature and long exposure to represent parallel byproduct formation, target degradation, and the possible reverse-channel-plus-sink mechanism described in the sealed report. Safety risk was extrapolated from its observed increase with temperature, duration, and the acetonitrile solvent category. Intervals are deliberately broad because the queries vary catalyst concentration, scale, stirring speed, and temperature beyond the directly studied design; the 465 K cases are the most uncertain. Quenching in Q10 was assigned only a small effect because it occurs after the complete heating period.

### Q01

The low catalyst concentration and short 1800 s exposure should limit conversion despite 410 K. Acetonitrile and the elevated temperature are expected to favor non-target chemistry relative to the water experiments, so selectivity is predicted near 0.50 rather than near the best water values.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1800 | 0.0800 | 0.3100 |
| conversion | 0.3600 | 0.2200 | 0.5200 |
| safety_risk | 0.1900 | 0.1500 | 0.2400 |
| score | 0.1000 | 0.0400 | 0.1700 |
| selectivity | 0.5000 | 0.3800 | 0.6200 |
| yield | 0.1800 | 0.1000 | 0.2900 |

### Q02

The eightfold longer exposure than Q01 should drive almost complete reactant disappearance even at low catalyst loading. Extrapolating from the long-duration campaign batch, prolonged heating should divert much of the converted material into byproduct or degradation channels, sharply lowering selectivity and score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7400 | 0.6000 | 0.8800 |
| conversion | 0.9700 | 0.9000 | 1.0000 |
| safety_risk | 0.3100 | 0.2500 | 0.3800 |
| score | 0.0450 | 0.0100 | 0.1000 |
| selectivity | 0.2400 | 0.1200 | 0.3800 |
| yield | 0.2300 | 0.1100 | 0.3700 |

### Q03

The high catalyst concentration compensates for the short residence time and should give substantial conversion at 410 K. Acetonitrile and high thermal severity are nevertheless expected to produce a large competing-product fraction, leaving moderate yield and a score below the observed 370–380 K water optimum.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5200 | 0.3800 | 0.6600 |
| conversion | 0.8500 | 0.7200 | 0.9400 |
| safety_risk | 0.2100 | 0.1700 | 0.2700 |
| score | 0.1100 | 0.0500 | 0.1800 |
| selectivity | 0.3900 | 0.2800 | 0.5100 |
| yield | 0.3300 | 0.2200 | 0.4500 |

### Q04

This combines high catalyst concentration, 410 K, and the maximum duration. Conversion should saturate, but the campaign indicates that severe or prolonged exposure causes target loss and byproduct accumulation. The safety-risk interval straddles the declared 0.35 limit because this is an extrapolation beyond the studied thermal-duration combinations.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9100 | 0.7900 | 0.9800 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.3400 | 0.2800 | 0.4200 |
| score | 0.0080 | 0.0000 | 0.0300 |
| selectivity | 0.0900 | 0.0200 | 0.2000 |
| yield | 0.0900 | 0.0200 | 0.2000 |

### Q05

At 350 K the low catalyst concentration should give only modest conversion over 7200 s. Lower thermal severity should preserve selectivity better than the 380 K acetonitrile campaign batch and keep safety risk relatively low, although limited conversion constrains yield and score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1600 | 0.0700 | 0.2900 |
| conversion | 0.3300 | 0.1900 | 0.4900 |
| safety_risk | 0.1500 | 0.1200 | 0.1900 |
| score | 0.1000 | 0.0400 | 0.1700 |
| selectivity | 0.5200 | 0.4000 | 0.6400 |
| yield | 0.1700 | 0.0900 | 0.2800 |

### Q06

The 465 K exposure is far above the experimental temperature range. Even with low catalyst loading, it should produce nearly complete conversion while strongly accelerating byproduct and degradation pathways. This prediction has a high probability of exceeding the safety limit and correspondingly little retained target product.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9300 | 0.8100 | 0.9900 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.3900 | 0.3200 | 0.4800 |
| score | 0.0040 | 0.0000 | 0.0200 |
| selectivity | 0.0700 | 0.0100 | 0.1800 |
| yield | 0.0700 | 0.0100 | 0.1800 |

### Q07

High catalyst concentration should give strong conversion even at 350 K, while the lower temperature should suppress target degradation relative to hotter acetonitrile conditions. This is predicted to be the strongest of the queried high-catalyst conditions, though acetonitrile still limits selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4600 | 0.3200 | 0.6000 |
| conversion | 0.8200 | 0.6800 | 0.9200 |
| safety_risk | 0.1700 | 0.1300 | 0.2200 |
| score | 0.1400 | 0.0700 | 0.2200 |
| selectivity | 0.4400 | 0.3200 | 0.5600 |
| yield | 0.3600 | 0.2400 | 0.4800 |

### Q08

High catalyst concentration, 465 K, and 7200 s constitute the most severe queried condition. Conversion should be effectively complete, but almost all converted material is expected to appear in non-target or degraded pools. Safety risk is predicted to exceed the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9750 | 0.9100 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.4300 | 0.3500 | 0.5300 |
| score | 0.0010 | 0.0000 | 0.0080 |
| selectivity | 0.0250 | 0.0000 | 0.0900 |
| yield | 0.0250 | 0.0000 | 0.0900 |

### Q09

The intermediate catalyst concentration is close to the campaign catalyst concentration on a volume basis. Raising the temperature from the observed 380 K acetonitrile condition to 410 K should push conversion toward saturation while substantially worsening selectivity, byproduct signal, and score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8000 | 0.6700 | 0.9100 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.2700 | 0.2200 | 0.3400 |
| score | 0.0300 | 0.0050 | 0.0750 |
| selectivity | 0.1900 | 0.0900 | 0.3200 |
| yield | 0.1900 | 0.0800 | 0.3200 |

### Q10

Quenching occurs only after the full 7200 s heat exposure, so it should not undo conversion or target loss already incurred. It may prevent small post-heating changes, producing at most a slight improvement relative to Q09. Safety risk is treated as a peak or accumulated exposure metric and therefore is not assumed to disappear on quenching.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7900 | 0.6600 | 0.9100 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.2700 | 0.2200 | 0.3400 |
| score | 0.0330 | 0.0060 | 0.0800 |
| selectivity | 0.2000 | 0.0900 | 0.3300 |
| yield | 0.2000 | 0.0800 | 0.3300 |

### Q11

The long 14,400 s duration should generate high conversion at 350 K, but the campaign's long-duration batch showed that extended exposure progressively transfers material into non-target channels. Lower temperature limits risk, yet the expected selectivity and score remain below those of a shorter, moderately heated process.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5400 | 0.4000 | 0.6800 |
| conversion | 0.8800 | 0.7700 | 0.9500 |
| safety_risk | 0.1900 | 0.1500 | 0.2400 |
| score | 0.1050 | 0.0450 | 0.1800 |
| selectivity | 0.3800 | 0.2500 | 0.5100 |
| yield | 0.3300 | 0.2100 | 0.4600 |

### Q12

At 465 K, even the short 1800 s interval is expected to provide very high effective reaction exposure at the intermediate catalyst concentration. The short duration keeps risk below the longer 465 K cases, but extreme temperature should still make byproduct formation and target degradation dominant.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8500 | 0.7200 | 0.9500 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.2500 | 0.2000 | 0.3200 |
| score | 0.0180 | 0.0010 | 0.0550 |
| selectivity | 0.1400 | 0.0500 | 0.2700 |
| yield | 0.1400 | 0.0400 | 0.2700 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The only substantive mechanistic prior was: “The target pathway may have an appreciable reverse channel on the public support,” with moderate confidence. The material packet otherwise supplied identities and interpretation constraints rather than a task-specific kinetic dossier. In particular, it warned that the solvent effects were calibrated categorical benchmark effects, not validated predictions from real solvent properties.

The reverse-channel prior was not directly verified. Batch 8—water, Catalyst B, 360 K, 14,400 s—gave conversion 0.9136 but only 0.3887 yield, 0.4172 selectivity, 0.5552 byproduct signal, and 0.2993 degradation warning. That is compatible with target returning to reactant and subsequently entering an irreversible side channel. However, it is equally compatible with irreversible target degradation, a slow parallel side reaction, or time-dependent catalyst behavior. Thus the proper retrospective classification is “still untested directly, with compatible circumstantial evidence,” not “supported as established.”

There was no observation that clearly contradicted the possibility of reversal. Conversely, absence of such a contradiction is not positive evidence for reversal. K1 handled this distinction reasonably: it proposed R ⇌ P alongside R → B and P → D, but explicitly stated that an irreversible R → P → D plus R → B network explained the long-time result at least as well.

The categorical-solvent interpretation was respected. Batches 2 and 5–7 demonstrated large solvent-category effects at matched nominal catalyst, temperature, and duration, but those results do not validate explanations based on real polarity, proticity, or heat capacity. K1 correctly limited the conclusion to category 0 favoring the desired-to-undesired rate ratio in this benchmark.

No initial quantitative claims about activation energies, reaction orders, catalyst loading, scale, or stirring were supplied. Those issues therefore remained open rather than being supported or refuted.

2. Experiments that actually formed or changed my judgment

Batch 1 established the first usable operating point. Its final conversion of 0.3225, selectivity of 0.6198, yield of 0.1975, and very low degradation warning of 0.00345 showed that mild operation could be selective but conversion-limited. The intermediate HPLC and final assay were also broadly consistent: HPLC gave conversion 0.3250 and yield 0.1925, while the final assay gave 0.3225 and 0.1975. That gave limited reassurance that the main observables were interpretable across those two measurements.

Batches 2–4 genuinely formed the catalyst ranking at one matched condition. At 380 K for 7200 s in water, Catalyst B gave the highest observed yield and score; Catalyst C retained nearly the same selectivity but was less active; Catalyst D had similar conversion to C but worse selectivity. This was direct comparative evidence. It did not establish Catalyst B as universally best because Catalyst A was never tested at the same condition.

Batches 5–7 materially changed the solvent interpretation. Relative to water in Batch 2, ethanol, acetonitrile, and toluene increased conversion to approximately 0.883–0.889 but reduced yield, selectivity, and score while increasing byproduct signal and safety risk. That caused me to reject conversion maximization as a useful standalone policy and to favor water for the safe-score objective.

Batch 8 was the most mechanistically informative accidental result. I selected a long 14,400 s exposure partly to test whether lower temperature plus more time could improve conversion safely. Instead, it produced the campaign’s highest conversion but poor selectivity and high byproduct/degradation signals. This changed the interpretation from “more exposure may simply approach completion” to “continued exposure transfers material into non-target pools.” It supported the broad sink-based network used in K1, although it did not identify the sink mechanism.

Batches 9–12 were primarily local optimization experiments. Batches 9, 10, and 11 mapped 370, 365, and 375 K at 7200 s; Batch 12 tested 371 K. These established a broad favorable region rather than a precise optimum. Batch 9 scored 0.2346, Batch 2 at 380 K scored 0.2340, and Batch 11 at 375 K scored 0.2327. Batch 12’s lower score of 0.2292 at 371 K warned that local process or measurement variability was material.

Several choices relied more on unverified assumptions than on evidence. Using the maximum reagent, catalyst, and solvent allowances in every batch was an early heuristic, not a data-derived optimum. The fixed 600 rpm stirring speed was arbitrary. Batch 1’s selection of water and Catalyst A was exploratory rather than justified by the sparse initial packet. The initial 340 K/3600 s condition and later temperature increments were practical guesses. After Batch 2, the categorical screens were data-guided, while Batches 9–12 were explicitly guided by the observed water/Catalyst B performance.

3. Current competing mechanisms and what the experiments distinguish

The main competing explanations remain:

A. Reversible desired formation plus irreversible sinks:
R ⇌ P, R → B, and P → D.

B. Fully irreversible sequential/parallel chemistry:
R → P → D and R → B.

C. Time-dependent kinetics, such as catalyst activation/deactivation or a changing effective medium, with no chemically important reverse step.

D. Multiple unobserved intermediates whose instrument signals collapse into the public labels “target,” “byproduct,” and “degradation.”

The experiments distinguish these models from a simple irreversible R → P model with no important side chemistry. Batch 8 decisively showed that greater conversion and longer exposure need not improve target yield. Batches 5–7 showed that solvent category changes relative pathway rates rather than merely rescaling a single common rate. Batches 2–4 likewise showed catalyst-dependent selectivity, particularly the poorer selectivity of Catalyst D.

The experiments do not distinguish A from B. A falling target concentration accompanied by recovery of reactant would favor reversal, whereas a falling target concentration with monotonic reactant disappearance would favor sequential degradation. Only terminal assays were obtained for the decisive long-duration conditions, so that comparison is unavailable. Nor can the data separate P → D from B → D, identify whether degradation warning is a distinct mass pool, or establish whether the rate constants are constant over time.

The approximate relationships yield ≈ conversion × selectivity and byproduct ≈ conversion × (1 − selectivity) were useful bookkeeping observations, not proof of a unique network. Batch 12’s noticeable departure from the first relationship illustrates that assay channels, degradation, or process variability complicate this interpretation.

4. The single additional experiment I would choose

I would run one time-resolved water/Catalyst B batch at the recommended loading and 370 K, keeping 600 rpm, but divide the heating into segments. I would acquire HPLC measurements after cumulative heating times of approximately 1800 s and 7200 s, then continue to 14,400 s, terminate, and obtain the required final assay. The small destructive measurement volumes would be accounted for. This would be one complete batch, not three independent experiments.

The goal would be to observe the direction of movement of conversion, yield, selectivity, and byproduct within the same vessel as exposure increases. The final assay would add degradation warning at the longest time. Cross-instrument differences would remain a limitation, but the two HPLC points would be directly comparable.

Possible outcomes would change my judgment as follows:

• If yield rose initially and then fell while conversion also fell, that would provide meaningful evidence for net regeneration of reactant and would raise confidence in the reverse P → R channel.

• If yield fell after an initial maximum while conversion continued increasing, that would favor irreversible P → D and/or progressive diversion of remaining R into B over simple reversal.

• If conversion and yield plateaued together with stable selectivity, the severe Batch 8 outcome would look more like batch-specific variability or a condition-specific catalyst/medium change.

• If byproduct rose while target fell but conversion remained nearly constant, a direct P → B or P → D transformation would become more plausible.

• If the time course were non-monotonic or poorly reproducible, time-dependent catalyst state or process heterogeneity would deserve more weight.

Even this experiment would not uniquely identify all rate constants. It would, however, be more discriminating than another terminal-only temperature point.

5. Tradeoff between mechanistic identifiability and operating-score optimization

The research goal emphasized a strong safe score under a safety limit, and that substantially shaped the campaign. After the categorical screens identified water and Catalyst B as promising, most remaining batches were spent refining temperature near the apparent optimum. This improved sample-internal operating performance but sacrificed mechanistic breadth.

There were genuine identification-oriented choices. Batches 2–4 formed a matched catalyst comparison, and Batches 5–7 formed a matched solvent comparison. Batch 8 explored a distinct temperature/time combination and unexpectedly exposed strong time-dependent selectivity loss. Those batches sacrificed some immediate score potential to obtain comparative information.

Conversely, Batches 9–12 were largely optimization-oriented. Testing 365, 370, 371, and 375 K produced a useful local response map, but Batch 12 at 371 K was not an exact replicate and added less mechanistic information than a time course, a matched Catalyst A comparison, or a loading experiment would have added. The close scores of Batches 2, 9, and 11 suggest that some of this fine temperature allocation had diminishing informational returns.

Keeping all material amounts and stirring speed fixed made the comparisons clean within that slice of the design space, but it prevented identification of concentration, catalyst-order, scale, and mixing effects. Using only one nonfinal measurement, despite the larger allowance, was a particularly important tradeoff: it conserved procedural simplicity but forfeited the best opportunity to observe kinetics directly.

The campaign therefore found a reasonable sample-internal safe operating region, but it did not produce a strongly identifiable mechanistic model. That balance was defensible for the stated optimization goal, though not optimal for a mechanism-first study.

6. Underused evidence and weaknesses in the blind predictions

The public characterization artifacts contained richer synthetic signal information than the processed summaries I used. I relied mainly on processed conversion, yield, selectivity, byproduct, and degradation values rather than systematically analyzing peak shapes, assignments, mass-balance fields, or cross-channel consistency. Because the species mapping remained intentionally hidden, those signals would not have solved structural identification, but they could have revealed saturation, missingness, calibration inconsistencies, or additional evidence of overlapping channels.

The heat operations also reported actual temperature changes, not only target temperatures. I noted them during execution but did not incorporate them into a quantitative thermal-exposure model. Likewise, I did not formally fit uncertainty or the score response, even though the 12 completed batches could have supported a limited empirical sensitivity analysis. Such a fit would still have been fragile because catalyst, solvent, time, and temperature were partly confounded.

The blind predictions were weakest where they departed from K1’s stated applicability limits. K1 explicitly said that catalyst amount, reagent amount, solvent volume, stirring rate, reaction order, and scale dependence were unidentified. All blind queries used 0.005 L rather than 0.080 L, 0.003 mol rather than 0.040 mol, 400 rpm rather than 600 rpm, and catalyst amounts not directly studied. Nevertheless, the prediction rationale imposed an approximate catalyst-concentration exposure model. That was a necessary forecasting assumption, but it was not experimentally established.

Q06, Q08, and Q12 were especially unreliable because 465 K was 85 K above the highest campaign temperature. Their near-unity conversion estimates and very low selectivity estimates were mechanistic extrapolations, not interpolations. Q04 was also highly uncertain because it combined 410 K, high catalyst concentration, and 14,400 s. The conversion intervals for Q04, Q06, and Q08—such as 0.99–1.00 for Q08—were probably too narrow. Unknown catalyst deactivation, transport limitations, volatility, or a different high-temperature regime could prevent the assumed saturation.

Safety-risk intervals for the 465 K cases may also have been too narrow. Risk was extrapolated from a small 340–380 K range and from a different scale. K1 had only proposed a qualitative decomposition into loading and thermal contributions; it did not establish linear temperature extrapolation or scale invariance.

Q10 was weak for a different reason: quenching had never been tested. I predicted only a small chemical effect and no reduction of peak/accumulated risk because quenching followed the heating period. That is plausible but unsupported. Its interval should have allowed a larger divergence from Q09 if the benchmark’s quench operation changes product stability, assay state, or reported risk.

The score predictions were broadly the least identifiable metric because the exact scoring equation was not public and every completed batch displayed final cost as 1.0. Intervals such as Q08’s score range of 0–0.008 and Q06’s 0–0.02 were therefore overconfident even if the qualitative ranking was sensible.

There is also internal tension between K1’s warning that the exact local optimum was unresolved and the blind prediction model’s smooth exposure assumptions. Batch 9 at 370 K and Batch 12 at 371 K differed more than a deterministic one-degree response would suggest. The blind intervals acknowledged some uncertainty but did not consistently propagate that level of process variation, especially near saturated conversion.

7. Limitations of the sealed recommendation

The sealed recommendation was Batch 9: water, Catalyst B, 370 K, 7200 s at 600 rpm with the fixed campaign loadings. It was selected because its observed score of approximately 0.2346 was the highest among the 12 completed batches and its risk of approximately 0.1507 was comfortably below 0.35.

This means “sample-internal highest observed score,” not “proven optimum.” Its advantage was extremely small: Batch 2 scored about 0.2340 and Batch 11 about 0.2327. Those differences are comparable to plausible assay and process variability. There was no exact replicate of Batch 9, and Batch 12 at the nearby 371 K condition scored only 0.2292. Consequently, the evidence supports a broad favorable region around 370–380 K more strongly than it supports an exact 370 K optimum.

Repeatability should be tested with several independently prepared exact replicates of Batch 9, randomized among reference batches to detect drift. The distribution of score, risk, conversion, and selectivity—not merely the mean—should be compared with replicated 375 and 380 K alternatives.

Local robustness should be tested by small factorial perturbations around the recommendation: temperature, duration, catalyst loading, reagent concentration, solvent volume, and stirring rate. This would reveal whether the recommendation lies on a stable plateau or near a steep boundary. A robust condition with a slightly lower mean score could be preferable to a fragile nominal maximum.

Material robustness requires matched tests across catalysts and solvent categories. Catalyst A is a particularly important unresolved comparison because its only batch was much milder and showed high selectivity with very low degradation. It was never tested at the recommended temperature and duration. The recommendation therefore establishes Catalyst B only within the tested comparison set, not against all catalysts under optimized individual conditions.

Cross-world generalization is even more limited. Catalysts are anonymous benchmark formulations, solvent coupling is categorical, and hidden kinetic parameters may change between worlds. The recommendation should therefore be treated as specific to this public campaign world until independently validated in a new world under the same protocol.

Finally, safety robustness should be evaluated under plausible operating deviations and not inferred solely from the nominal margin. Batch 9’s measured risk was far below 0.35, which is reassuring, but the campaign did not test scale-up, mixing failure, temperature overshoot, or concentration variation. The sealed recommendation is a defensible empirical choice from the completed set, not a universal or formally optimized operating procedure.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 105.7 | none | 0 |
| Q | yes | 0 | 121.2 | none | 0 |
| K2 | yes | 0 | 136.4 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
