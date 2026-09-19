# RX-W02--S--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W02`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `96`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `10`
- Rationale: Batch 10 gave the strongest observed safe score and highest target yield among the tested conditions while remaining below the safety limit; its quench also reduced terminal risk.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 900 s @ 600 rpm → 350 K x 900 s @ 600 rpm | no | 0.1669 | 0.5805 | 0.2495 | 0.1048 | 0.0000 | 0.1398 | 0.0739 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.4065 | 0.5627 | 0.7012 | 0.3078 | 0.1251 | 0.1725 | 0.1957 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.3683 | 0.5773 | 0.6481 | 0.2660 | 0.1163 | 0.1678 | 0.1810 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.3415 | 0.5274 | 0.6494 | 0.3176 | 0.1138 | 0.1661 | 0.1586 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.4059 | 0.6729 | 0.6139 | 0.1949 | 0.0683 | 0.1272 | 0.2348 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.3902 | 0.5828 | 0.6797 | 0.3013 | 0.0859 | 0.1517 | 0.2015 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.4060 | 0.5618 | 0.7210 | 0.3079 | 0.0998 | 0.1851 | 0.1916 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | yes | 0.2707 | 0.6667 | 0.3966 | 0.1488 | 0.0307 | 0.1049 | 0.1674 |
| 9 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 430 K x 1800 s @ 600 rpm | yes | 0.3417 | 0.7510 | 0.4574 | 0.1354 | 0.0345 | 0.1327 | 0.2105 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 7200 s @ 600 rpm | yes | 0.4894 | 0.5501 | 0.8750 | 0.3791 | 0.1921 | 0.1447 | 0.2557 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 430 K x 900 s @ 600 rpm → 430 K x 900 s @ 600 rpm | yes | 0.3861 | 0.7591 | 0.5265 | 0.1301 | 0.0434 | 0.1638 | 0.2232 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 7200 s @ 600 rpm | no | 0.4781 | 0.5459 | 0.8521 | 0.3897 | 0.1938 | 0.1888 | 0.2280 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `8`.

```json
{
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 8,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.10484933108091354,
    "conversion": 0.24948954582214355,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.13983897864818573,
    "score": 0.07389984279870987,
    "selectivity": 0.5805301070213318,
    "virtual_spectrum_summary": 0.05766713246703148,
    "yield": 0.1668647676706314
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `16`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 16,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.30780696868896484,
    "conversion": 0.7011922597885132,
    "cost": 1.0,
    "degradation_warning": 0.1251259595155716,
    "safety_risk": 0.17253726720809937,
    "score": 0.19574947655200958,
    "selectivity": 0.5626872777938843,
    "virtual_spectrum_summary": 0.22560052573680878,
    "yield": 0.4065004885196686
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `24`.

```json
{
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
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 24,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.26597198843955994,
    "conversion": 0.6481273174285889,
    "cost": 1.0,
    "degradation_warning": 0.11629007011651993,
    "safety_risk": 0.16776880621910095,
    "score": 0.18096615374088287,
    "selectivity": 0.5773290991783142,
    "virtual_spectrum_summary": 0.19861511886119843,
    "yield": 0.36829280853271484
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `32`.

```json
{
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 32,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3175828754901886,
    "conversion": 0.649358332157135,
    "cost": 1.0,
    "degradation_warning": 0.11382739245891571,
    "safety_risk": 0.16607676446437836,
    "score": 0.1586323082447052,
    "selectivity": 0.5274010300636292,
    "virtual_spectrum_summary": 0.22589290142059326,
    "yield": 0.3414519131183624
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `40`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 40,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.194887176156044,
    "conversion": 0.6139461994171143,
    "cost": 1.0,
    "degradation_warning": 0.06831832975149155,
    "safety_risk": 0.12719471752643585,
    "score": 0.234758660197258,
    "selectivity": 0.6729416847229004,
    "virtual_spectrum_summary": 0.1379311978816986,
    "yield": 0.40591561794281006
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `48`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 48,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3012526035308838,
    "conversion": 0.6797363758087158,
    "cost": 1.0,
    "degradation_warning": 0.08592242002487183,
    "safety_risk": 0.1517392098903656,
    "score": 0.20146188139915466,
    "selectivity": 0.5827729105949402,
    "virtual_spectrum_summary": 0.20435401797294617,
    "yield": 0.3901941776275635
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `56`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 56,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3078871965408325,
    "conversion": 0.7209770679473877,
    "cost": 1.0,
    "degradation_warning": 0.09976564347743988,
    "safety_risk": 0.1851278841495514,
    "score": 0.19162045419216156,
    "selectivity": 0.5617890954017639,
    "virtual_spectrum_summary": 0.21423248946666718,
    "yield": 0.40595754981040955
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `64`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 64,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.14882218837738037,
    "conversion": 0.39660343527793884,
    "cost": 1.0,
    "degradation_warning": 0.030665675178170204,
    "safety_risk": 0.10491098463535309,
    "score": 0.1673962026834488,
    "selectivity": 0.6667296290397644,
    "virtual_spectrum_summary": 0.09565175324678421,
    "yield": 0.2706584632396698
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `72`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 430
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 72,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.1353815346956253,
    "conversion": 0.4573681950569153,
    "cost": 1.0,
    "degradation_warning": 0.03452064469456673,
    "safety_risk": 0.1326719969511032,
    "score": 0.21047188341617584,
    "selectivity": 0.7509600520133972,
    "virtual_spectrum_summary": 0.08999413251876831,
    "yield": 0.3417436182498932
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `80`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 80,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3790753185749054,
    "conversion": 0.875022292137146,
    "cost": 1.0,
    "degradation_warning": 0.19213518500328064,
    "safety_risk": 0.144650399684906,
    "score": 0.2556743621826172,
    "selectivity": 0.5500970482826233,
    "virtual_spectrum_summary": 0.29495227336883545,
    "yield": 0.4893513321876526
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `89`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 430
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 430
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 89,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.1301267147064209,
    "conversion": 0.5265121459960938,
    "cost": 1.0,
    "degradation_warning": 0.04335889592766762,
    "safety_risk": 0.16376672685146332,
    "score": 0.2231549173593521,
    "selectivity": 0.7590824365615845,
    "virtual_spectrum_summary": 0.09108119457960129,
    "yield": 0.3860703110694885
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `96`.

```json
{
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
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
  "end_step": 96,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3897470533847809,
    "conversion": 0.8520711660385132,
    "cost": 1.0,
    "degradation_warning": 0.19376280903816223,
    "safety_risk": 0.1887592375278473,
    "score": 0.22798596322536469,
    "selectivity": 0.5458962917327881,
    "virtual_spectrum_summary": 0.3015541434288025,
    "yield": 0.47811609506607056
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

# Mechanistic report

## 1. Scope and evidence base

This report concerns the bounded synthetic reaction world studied in twelve completed batches. Every batch used 0.040 mol of the anonymous limiting reagent, 0.080 L of one solvent, 0.005 mol of one anonymous catalyst, and 600 rpm stirring. Consequently, the conclusions apply only near those loadings and should not be interpreted as claims about a named real reaction.

The principal measurements were an HPLC result immediately before termination or quenching and a destructive final assay after termination. Numerical differences of a few hundredths can reflect measurement noise, sampling, or run-to-run process variation. Larger, systematic changes across controlled comparisons are more persuasive.

## 2. Proposed process model

The simplest model consistent with the observations has at least four kinetic pools:

- R: unconverted limiting reagent;
- P: desired target;
- B: competing byproduct;
- D: thermally degraded material, partially reflected by `degradation_warning`.

A useful provisional reaction network is:

R ⇌ P
R → B
P → D

The reverse P → R step is plausible and was part of the initial structural prior, but the present experiments do not uniquely establish it. Product inhibition, catalyst deactivation, and irreversible consecutive degradation can produce similar late-time behavior.

One mathematical representation is:

- dR/dt = −a·kf(T,C,S)·R + kr(T,C,S)·P − kb(T,C,S)·R
- dP/dt = a·kf(T,C,S)·R − kr(T,C,S)·P − kd(T,S)·P
- dB/dt = kb(T,C,S)·R + fD·kd(T,S)·P
- da/dt = −kdeact(T,S)·a

Here C denotes catalyst identity, S solvent identity, and a is active catalyst fraction. Each rate constant can be represented locally by an Arrhenius-like form, for example

k(T,C,S) = A(C,S) exp[−E(C,S)/(RT)].

The reported conversion is approximately total disappearance of R, whereas yield is associated with P. Accordingly, yield/conversion broadly tracks measured selectivity. For example, in batch 5 the final yield/conversion ratio was 0.4059/0.6139 = 0.661, close to the measured selectivity of 0.6729. The quantities are not exactly identical because they are independently calibrated noisy channels.

The data indicate two coupled regimes:

1. **Early target-forming regime:** Heating accelerates conversion and target formation. In water, high temperature also initially favors target selectivity.
2. **Late competing regime:** Continued hot exposure raises conversion but increasingly produces byproduct and degradation, so selectivity declines even while absolute target yield can continue increasing.

## 3. Thermal history is a state variable

The world does not behave as if nominal setpoint multiplied by nominal time were the only thermal descriptor. A reasonable thermal model is

dT/dt = (Tset − T)/τ,

with reaction rates depending on the resulting T(t), not merely Tset. Operational segmentation may also change the effective ramp behavior.

Evidence includes batch 1, where the first 900 s heat operation toward 350 K increased temperature by 48.91 K, while the second nominally identical 900 s segment increased it by only another 1.83 K. The material therefore experienced a ramp followed by a near-setpoint hold.

The strongest indication that operation history matters comes from batches 9 and 11. Both used Catalyst B, water, and a nominal total of 1800 s at 430 K:

- Batch 9 used one continuous 1800 s heat operation. Its recorded temperature increment was 113.97 K and its pre-quench safety risk was 0.3102.
- Batch 11 used two 900 s operations. The recorded increments were 102.28 K and 25.57 K, and risk rose from 0.2198 after the first segment to 0.3764 after the second.

Thus, batch 11 crossed the 0.35 safety limit even though batch 9 did not. Batch 11 also ended with greater final conversion and yield than batch 9. These differences are too consequential to treat segmented and continuous heat commands as interchangeable. A predictive implementation should integrate the actual temperature history and preserve temperature between operations.

A useful exposure variable would be

Θj = ∫ exp[−Ej/(R·T(t))] dt,

calculated separately for target formation, competition, degradation, and safety accumulation. A single universal “thermal dose” is probably insufficient because the pathways have different temperature sensitivities.

## 4. Catalyst effects

Batches 2–4 provide the cleanest catalyst comparison: all used acetonitrile, 390 K, and 3600 s.

- **Batch 2, Catalyst B:** final conversion 0.7012, yield 0.4065, selectivity 0.5627, byproduct 0.3078.
- **Batch 3, Catalyst C:** final conversion 0.6481, yield 0.3683, selectivity 0.5773, byproduct 0.2660.
- **Batch 4, Catalyst D:** final conversion 0.6494, yield 0.3415, selectivity 0.5274, byproduct 0.3176.

Catalyst B gave the greatest conversion and target yield. Catalyst C was somewhat slower but retained similar or slightly better selectivity. Catalyst D showed no conversion advantage over C and gave distinctly poorer target yield and selectivity. This suggests that catalyst identity affects both the target-forming rate and the branching ratio, rather than merely scaling all reaction rates together.

Catalyst A was tested only in batch 1 at 350 K and 1800 s, so it cannot be ranked directly against B–D. Batch 1 ended at conversion 0.2495 and yield 0.1669, but its milder and shorter thermal program is a major confounder.

I therefore used Catalyst B for the subsequent solvent and thermal comparisons. The evidence supports B as the best observed catalyst for absolute target production in the tested region, not as universally optimal under untested loadings or temperatures.

## 5. Solvent effects

Batches 2, 5, 6, and 7 compared solvents with Catalyst B at 390 K for 3600 s.

- **Acetonitrile, batch 2:** conversion 0.7012, yield 0.4065, selectivity 0.5627, byproduct 0.3078, degradation warning 0.1251, final risk 0.1725.
- **Water, batch 5:** conversion 0.6139, yield 0.4059, selectivity 0.6729, byproduct 0.1949, degradation warning 0.0683, final risk 0.1272.
- **Ethanol, batch 6:** conversion 0.6797, yield 0.3902, selectivity 0.5828, byproduct 0.3013, degradation warning 0.0859, final risk 0.1517.
- **Toluene, batch 7:** conversion 0.7210, yield 0.4060, selectivity 0.5618, byproduct 0.3079, degradation warning 0.0998, final risk 0.1851.

Water reduced total conversion relative to the other solvents but strongly suppressed the competing channel. It therefore delivered almost the same absolute yield as acetonitrile and toluene while providing substantially higher selectivity and lower risk and degradation. This is consistent with water lowering both productive and competing rates, but lowering the competing rate more strongly.

Toluene gave the greatest conversion at this condition, but the extra conversion did not improve final target yield because selectivity was lower. Acetonitrile behaved similarly. Ethanol was intermediate in conversion but did not show the selective advantage of water.

This solvent comparison caused an important revision to the working model: maximizing conversion is not equivalent to maximizing target formation. Solvent chiefly controls pathway partitioning and degradation as well as overall rate.

## 6. Temperature and time effects in the Catalyst B/water system

The most informative temperature/time series consists of batches 5, 8, 9, 10, 11, and 12.

### 350 K for 3600 s — batch 8

Final conversion was 0.3966, yield 0.2707, selectivity 0.6667, byproduct 0.1488, degradation warning 0.0307, and final risk 0.1049. This was mild and relatively selective but kinetically incomplete.

### 390 K for 3600 s — batch 5

Final conversion rose to 0.6139 and yield to 0.4059. Selectivity remained useful at 0.6729, with byproduct 0.1949 and degradation warning 0.0683. This shows strong acceleration relative to 350 K without a major selectivity penalty at 3600 s.

### 390 K for 7200 s — batches 10 and 12

Batch 10, followed by quenching, gave final conversion 0.8750, yield 0.4894, selectivity 0.5501, byproduct 0.3791, and degradation warning 0.1921.

Batch 12, terminated without quenching, gave conversion 0.8521, yield 0.4781, selectivity 0.5459, byproduct 0.3897, and degradation warning 0.1938.

Relative to batch 5, doubling the hot time caused a large increase in conversion and a more modest increase in target yield, while selectivity fell by approximately 0.12 and both byproduct and degradation warning nearly doubled. Target formation therefore continued, but its marginal benefit declined because the competing and degradation pathways became increasingly important.

This behavior is consistent with either depletion of R combined with continued P degradation, approach to a reversible equilibrium, catalyst-state evolution, or some combination. A purely irreversible, parallel first-order model with fixed branching fractions would not naturally explain such a strong time-dependent loss of selectivity.

### 430 K for 1800 s — batches 9 and 11

Batch 9 gave final conversion 0.4574, yield 0.3417, selectivity 0.7510, byproduct 0.1354, and degradation warning 0.0345. The HPLC result before quenching was conversion 0.4860, yield 0.3483, selectivity 0.7714, and byproduct 0.1195.

In batch 11, after the first 900 s, HPLC showed conversion 0.2285, yield 0.1446, selectivity 0.7459, and byproduct 0.0580. After a second 900 s heat segment and quench, the final assay showed conversion 0.5265, yield 0.3861, selectivity 0.7591, byproduct 0.1301, and degradation warning 0.0434.

The 430 K experiments indicate that, over short exposure, the productive pathway has a strong temperature response and can achieve selectivity near 0.75. This suggests a larger effective activation energy for productive formation than for the principal early competing route. However, the operationally segmented batch 11 accumulated excessive peak risk, so the high-temperature advantage is coupled tightly to the thermal control protocol.

## 7. Evidence for late competition, reversal, or deactivation

The clearest late-time comparison is batch 5 versus batches 10 and 12 at 390 K:

- Conversion increased from about 0.614 at 3600 s to 0.85–0.88 at 7200 s.
- Yield increased only from about 0.406 to 0.478–0.489.
- Selectivity declined from 0.673 to about 0.546–0.550.
- Byproduct increased from 0.195 to about 0.38–0.39.
- Degradation warning increased from 0.068 to about 0.193.

This establishes that prolonged heating activates an increasingly important non-target sink. It does not, by itself, identify the sink.

Three mechanistic explanations remain viable:

1. **Consecutive degradation:** R forms P, and P subsequently degrades to D or to material contributing to the byproduct channel.
2. **Reversible target formation plus trapping:** P reverses to R, after which R is gradually diverted to B.
3. **Catalyst evolution or product inhibition:** catalyst activity or branching selectivity changes with time or accumulated products.

The rising degradation-warning channel favors some real thermal degradation component. Nevertheless, no experiment directly followed a preformed high-P mixture during an isothermal hold or cooling interval, so the reverse rate and deactivation rate are not separately identifiable.

## 8. Quench and termination behavior

Most later batches were measured by HPLC, quenched, terminated, and then assayed. Batch 12 instead went directly from HPLC to termination and final assay, making it the best available comparison with quenched batch 10.

The chemical results of batches 10 and 12 were close relative to the scale of the responses: final yields differed by 0.0112, conversions by 0.0230, selectivities by 0.0042, and degradation warnings by 0.0016. These differences could be ordinary process and measurement variation. I therefore do not claim that quenching chemically improved the isolated composition in a large way.

The risk difference was clearer. Batch 10 had pre-quench risk 0.1888 and final risk 0.1447, whereas unquenched batch 12 remained at 0.1888. Similar reductions occurred in other quenched runs. The quench appears primarily to cool or deactivate the reactive state, arresting further evolution and lowering terminal risk.

Quench does not erase earlier peak risk. Batch 11 reached 0.3764 before quenching and thus exceeded the 0.35 constraint, even though its post-quench final risk was only 0.1638. Safe control must therefore consider the full trajectory, not merely the final readout.

## 9. Safety model

Observed safety risk depends on solvent, actual temperature, duration, and operation history. A provisional dynamic representation is

dH/dt = qheat(T,S) + qrxn(T,R,a) − qcool(T,S),

with reported risk a bounded function of H, temperature, and reactive inventory. Quenching sharply increases qcool or removes reactive capacity.

At 390 K for 3600 s, pre-quench risks were approximately 0.1715 in water, 0.1960 in ethanol, 0.2168 in acetonitrile, and 0.2294 in toluene. This solvent ordering broadly accompanies the observed byproduct and degradation burden, although solvent-specific baseline risk is also likely.

The segmented 430 K batch demonstrates that safety cannot be predicted reliably from final composition alone. Thermal transients must be represented explicitly.

## 10. Why batch 10 was recommended

Batch 10 used Catalyst B, water, 390 K, 7200 s, followed by quenching. It gave the highest measured final target yield, 0.4894, and the highest observed safe score, approximately 0.2557, among the completed batches. Its pre-quench risk of 0.1888 remained below the 0.35 limit, and quenching reduced final risk to 0.1447.

This recommendation is empirical rather than a claim that 7200 s is the true optimum. The declining selectivity and increasing degradation warning indicate that an optimum in yield or utility may occur near this region, and potentially before much longer exposure. Batch 11 achieved high selectivity but was not recommendable because its segmented high-temperature trajectory crossed the safety limit.

## 11. Limits of identification and competing explanations

Several important quantities remain unidentifiable from this campaign:

- No catalyst-loading series was performed, so reaction order in catalyst is unknown.
- Reagent concentration and solvent volume were fixed, preventing identification of concentration dependence or reaction order in R.
- Stirring was fixed at 600 rpm, so mass-transfer limitations cannot be excluded.
- Catalyst A was not tested under the common 390 K/3600 s condition.
- There was no catalyst-free control, so uncatalyzed background rates are unknown.
- There was no direct measurement during cooling, no long isothermal wait without heating, and no reheat experiment. Reversibility, product inhibition, and catalyst deactivation therefore cannot be separated.
- The byproduct signal may combine more than one chemical pool. Likewise, `degradation_warning` is an indicator rather than a direct material balance for D.
- Actual temperature was inferred only from operation deltas, not a continuous trace. The precise thermal time constant and any batch-to-batch initial-temperature variation cannot be fitted uniquely.
- HPLC and final assay values came from different samples and calibrations. Small pre/post-quench changes should not be overinterpreted.
- All conclusions are local to the tested categorical benchmark identities and recipe scale. Extrapolation beyond 350–430 K, 1800–7200 s, or the tested loadings is speculative.

A simpler competing model—irreversible parallel formation of P and B with temperature- and time-varying effective rate constants—could fit much of the dataset without explicit reversibility. Conversely, a reversible R ⇌ P model with irreversible B formation could explain declining late selectivity even without P degradation. The increase in degradation warning argues that degradation should be retained, but the current observations do not fix its stoichiometric relationship to the byproduct signal.

## 12. Consolidated interpretation

Within the tested domain, Catalyst B is the strongest target-producing catalyst. Water sacrifices some conversion rate but improves pathway selectivity, suppresses byproduct and degradation, and lowers risk. Temperature strongly accelerates target formation: short high-temperature exposure can be highly selective, but the thermal trajectory and operation segmentation strongly affect safety. At 390 K, extending time from 3600 to 7200 s raises target yield while causing a pronounced shift toward byproduct and degradation, consistent with late competition, target degradation, reversible target formation, catalyst evolution, or a combination of these processes. Quenching mainly arrests the reactive thermal state and lowers terminal risk; it does not undo prior peak exposure.

The most defensible predictive model is therefore a temperature-history-dependent, catalyst- and solvent-specific network with productive, competing, reversible, and degradative terms—not a static mapping from nominal setpoint and time to yield.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-derived picture of catalyst-dependent target formation in parallel with competing conversion and later target loss. Conversion was extrapolated with a temperature- and catalyst-loading-dependent effective first-order rate, while selectivity was reduced for accumulated hot exposure. Yield was constrained to remain approximately conversion multiplied by selectivity, and byproduct signal was treated as approximately converted material not appearing as target. Safety was modeled from actual thermal severity, solvent, duration, and quench state; its intervals are deliberately wide because all blind batches use a smaller scale, 400 rpm stirring, catalyst loadings not directly calibrated in the campaign, and temperatures up to 465 K. Scores were estimated from the observed empirical relationship among yield, selectivity, and the safety penalty. The largest uncertainties apply to the 14400 s and 465 K cases, which extrapolate beyond the measured time or temperature domain.

### Q01

A short 410 K exposure with low catalyst loading should give partial conversion. I expect moderately favorable early selectivity, but acetonitrile should produce more competing material than water.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1500 | 0.0900 | 0.2300 |
| conversion | 0.3670 | 0.2600 | 0.4900 |
| safety_risk | 0.1800 | 0.1000 | 0.2800 |
| score | 0.1050 | 0.0550 | 0.1700 |
| selectivity | 0.5900 | 0.4900 | 0.6900 |
| yield | 0.2170 | 0.1400 | 0.3000 |

### Q02

The long exposure should largely exhaust the reagent even at low catalyst loading. Extrapolation from the 390 K time series predicts severe late competition and degradation, leaving low target selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7400 | 0.6000 | 0.8800 |
| conversion | 0.9740 | 0.9000 | 1.0000 |
| safety_risk | 0.2900 | 0.1600 | 0.4600 |
| score | 0.0400 | 0.0100 | 0.0900 |
| selectivity | 0.2400 | 0.1200 | 0.3800 |
| yield | 0.2340 | 0.1100 | 0.3600 |

### Q03

The higher catalyst concentration should substantially accelerate productive conversion during the short heat period. Selectivity should remain relatively high because the exposure is not long enough for the late competing regime to dominate.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2210 | 0.1400 | 0.3100 |
| conversion | 0.5980 | 0.4700 | 0.7200 |
| safety_risk | 0.2000 | 0.1100 | 0.3100 |
| score | 0.1900 | 0.1100 | 0.2800 |
| selectivity | 0.6300 | 0.5300 | 0.7200 |
| yield | 0.3770 | 0.2800 | 0.4700 |

### Q04

High catalyst loading and 14400 s at 410 K should drive conversion to its ceiling. The prolonged hot hold is expected to divert or degrade much of the target, so nearly complete conversion does not imply high yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7990 | 0.6500 | 0.9100 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.3400 | 0.1900 | 0.5400 |
| score | 0.0260 | 0.0050 | 0.0750 |
| selectivity | 0.2000 | 0.0800 | 0.3400 |
| yield | 0.2000 | 0.0800 | 0.3400 |

### Q05

At 350 K the low catalyst loading should produce moderate conversion over 7200 s. Thermal competition should be milder than at 410 K, preserving useful selectivity and low risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2310 | 0.1500 | 0.3200 |
| conversion | 0.5500 | 0.4200 | 0.6800 |
| safety_risk | 0.0550 | 0.0250 | 0.1100 |
| score | 0.1750 | 0.1100 | 0.2400 |
| selectivity | 0.5800 | 0.4800 | 0.6700 |
| yield | 0.3190 | 0.2300 | 0.4100 |

### Q06

This is a large extrapolation beyond the studied 430 K boundary. Even with low catalyst loading, 7200 s at 465 K should give near-complete conversion, extensive competing or degradative chemistry, and very high unquenched risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8620 | 0.7800 | 0.9600 |
| conversion | 0.9580 | 0.9000 | 1.0000 |
| safety_risk | 0.7800 | 0.5500 | 0.9800 |
| score | 0.0020 | 0.0000 | 0.0150 |
| selectivity | 0.1000 | 0.0300 | 0.2200 |
| yield | 0.0960 | 0.0300 | 0.2000 |

### Q07

Higher catalyst loading should make the mild 350 K program substantially more productive than Q05 while retaining moderate selectivity. This is predicted to be one of the strongest safe outcomes.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3180 | 0.2200 | 0.4100 |
| conversion | 0.7960 | 0.6800 | 0.8900 |
| safety_risk | 0.0650 | 0.0300 | 0.1300 |
| score | 0.2680 | 0.1800 | 0.3600 |
| selectivity | 0.6000 | 0.5000 | 0.6900 |
| yield | 0.4780 | 0.3700 | 0.5900 |

### Q08

High catalyst loading should rapidly consume the reagent, but the extreme 465 K, 7200 s history should strongly favor late degradation and byproduct formation. The unquenched thermal risk is predicted to be extreme.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9080 | 0.8000 | 0.9700 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.9000 | 0.6800 | 1.0000 |
| score | 0.0010 | 0.0000 | 0.0100 |
| selectivity | 0.0900 | 0.0200 | 0.2000 |
| yield | 0.0900 | 0.0200 | 0.2000 |

### Q09

The catalyst concentration is close to the concentration used in the campaign. At 410 K for 7200 s, conversion should be high, while prolonged exposure should lower selectivity through the late competing regime.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5920 | 0.4600 | 0.7200 |
| conversion | 0.9400 | 0.8700 | 0.9800 |
| safety_risk | 0.2500 | 0.1400 | 0.4100 |
| score | 0.0970 | 0.0400 | 0.1700 |
| selectivity | 0.3700 | 0.2400 | 0.5000 |
| yield | 0.3480 | 0.2300 | 0.4700 |

### Q10

Chemistry immediately before quenching should resemble Q09. Based on the paired campaign runs, quenching should have only a small compositional effect but should substantially reduce terminal safety risk and therefore improve score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5830 | 0.4500 | 0.7100 |
| conversion | 0.9400 | 0.8700 | 0.9800 |
| safety_risk | 0.1100 | 0.0550 | 0.2100 |
| score | 0.1210 | 0.0550 | 0.2000 |
| selectivity | 0.3800 | 0.2500 | 0.5100 |
| yield | 0.3570 | 0.2400 | 0.4800 |

### Q11

The long 350 K exposure should eventually reach high conversion without the severe thermal penalty expected at 410–465 K. Selectivity should nevertheless decline relative to a shorter mild run because competing chemistry has 14400 s to accumulate.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4840 | 0.3600 | 0.6100 |
| conversion | 0.9140 | 0.8400 | 0.9700 |
| safety_risk | 0.0700 | 0.0300 | 0.1400 |
| score | 0.1880 | 0.1200 | 0.2700 |
| selectivity | 0.4700 | 0.3400 | 0.5900 |
| yield | 0.4300 | 0.3100 | 0.5500 |

### Q12

A short 465 K exposure should create substantial conversion and retain more target than the long 465 K batches, but both selectivity and unquenched safety are highly uncertain because this temperature lies beyond the experimental range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3380 | 0.2300 | 0.4500 |
| conversion | 0.7050 | 0.5700 | 0.8200 |
| safety_risk | 0.5500 | 0.3600 | 0.7800 |
| score | 0.0860 | 0.0300 | 0.1600 |
| selectivity | 0.5200 | 0.3900 | 0.6400 |
| yield | 0.3670 | 0.2500 | 0.4900 |

## K2 — Retrospective analysis

## 1. Reassessment of the initial information

The only substantive mechanistic prior in the initial packet was: **“The target pathway may have an appreciable reverse channel on the public support,”** with moderate confidence. The material catalog otherwise supplied identities and interpretation constraints, not a task-specific kinetic dossier. In particular, it explicitly warned that the catalysts were anonymous benchmark formulations and that solvent effects were categorical benchmark effects rather than predictions from real solvent chemistry. I respected that restriction and did not assign a real chemical identity to the reaction.

The reverse-channel claim was **not directly demonstrated**. The strongest relevant evidence was the comparison between batch 5 and batches 10/12. At 390 K with Catalyst B in water, extending heating from 3600 to 7200 s increased conversion from 0.6139 to about 0.85–0.88, but yield increased only from 0.4059 to about 0.48–0.49, while selectivity fell from 0.6729 to about 0.55 and degradation warning rose from 0.0683 to about 0.193. Those changes are compatible with P reverting to R and the regenerated R being trapped as byproduct, but they are equally compatible with irreversible P degradation, changing catalyst selectivity, or product inhibition.

There is also limited evidence against a **strongly dominant** reverse channel over the observed interval: neither conversion nor target yield visibly declined between 3600 and 7200 s at 390 K. Conversion continued to increase substantially, and absolute yield also rose. Thus, if the initial claim were interpreted as saying that reversal dominates the observable dynamics, the data weigh against that interpretation. If interpreted merely as an appreciable secondary pathway, it remains unresolved.

K1 appropriately stated that reversal was “plausible” and “not uniquely establish[ed],” and listed irreversible degradation and catalyst evolution as alternatives. However, placing `R ⇌ P` in the headline network may still have given the initial prior more visual prominence than the evidence warranted. The more evidence-led core is `R → P`, `R → B`, and a late loss or diversion process affecting P or selectivity; reversibility is an optional extension.

I did not encounter a clear contradiction to an initial empirical dossier because no such dossier was supplied. This is therefore not a case where strong contrary evidence appeared and was ignored. Rather, the initial reverse-channel claim remained incompletely tested, with some evidence limiting how strong it could be.

## 2. Experiments that formed or changed my judgments

Several experiments genuinely changed the working account:

- **Batch 1** established that commanded heating did not represent an instantaneous isothermal hold. The first 900 s toward 350 K produced a 48.91 K temperature increment, while the second 900 s added only 1.83 K. This was the first reason to treat actual thermal history as a state variable.
- **Batches 2–4** produced the principal catalyst ranking under matched acetonitrile/390 K/3600 s conditions. Catalyst B gave final conversion 0.7012 and yield 0.4065, Catalyst C gave 0.6481 and 0.3683, and Catalyst D gave 0.6494 and 0.3415. This shifted subsequent work toward Catalyst B.
- **Batches 5–7**, compared with batch 2, changed the interpretation of solvent effects. Water in batch 5 gave lower conversion than acetonitrile or toluene but almost the same yield, because selectivity was much higher and byproduct was lower. This directly motivated the K1 judgment that “maximizing conversion is not equivalent to maximizing target formation.”
- **Batch 8** showed that 350 K was kinetically mild: final conversion 0.3966 and yield 0.2707 after 3600 s, with low degradation warning of 0.0307.
- **Batches 9 and 11** established the importance of command segmentation. Their nominal recipe and total 430 K heating time were similar, but the continuous and split thermal programs produced materially different temperature increments, conversion, yield, and peak risk. Batch 11 reached risk 0.3764 and crossed the constraint. This was stronger evidence for thermal-history dependence than any fitted rate equation.
- **Batches 10 and 12** established the late-time selectivity loss at 390 K and provided the best available quench comparison. Their close chemical results, combined with the clear risk reduction in quenched batch 10, led to the judgment that quenching mainly arrested the reactive thermal state rather than dramatically improving composition.

Some choices were less evidentially grounded:

- The first use of Catalyst A and acetonitrile in batch 1 was essentially an exploratory guess, not a consequence of the weak reverse-channel prior.
- The common 390 K/3600 s condition for the catalyst and solvent screens was a pragmatic middle condition, not an identified mechanistic optimum.
- Moving to Catalyst B after batches 2–4 was data-driven, but abandoning a matched test of Catalyst A left the catalyst comparison incomplete.
- Moving from acetonitrile to water after batch 5 was strongly data-driven and aligned with both mechanistic selectivity and safe score.
- The 430 K experiments were motivated by a hypothesis that high temperature might favor productive formation over early competition. Batch 9 supported that hypothesis, but batch 11 exposed an underestimated safety and command-history coupling.
- Batch 10 was partly an optimization experiment, extending the most promising Catalyst B/water condition. Batch 12 was more diagnostic because omitting the quench tested termination behavior at the expense of expected score.

## 3. Current competing mechanisms and what the data distinguish

The most important alternatives are:

1. **Parallel formation plus consecutive target degradation**
   
   `R → P`, `R → B`, and `P → D`.

2. **Reversible target formation plus irreversible trapping**
   
   `R ⇌ P` and `R → B`, possibly with additional degradation.

3. **Time-dependent catalyst state or product inhibition**
   
   Catalyst activity or branching selectivity changes as products accumulate or as the catalyst thermally deactivates.

4. **A simpler effective model with no distinct mechanistic pools**
   
   Product and byproduct are generated by time-, solvent-, and temperature-dependent effective branching fractions. Such a model can reproduce the observed outputs without uniquely assigning molecular steps.

The experiments do distinguish several broader relationships:

- Catalyst identity affects more than a common rate multiplier, because B, C, and D changed both conversion and selectivity under matched conditions.
- Solvent affects branching and safety as well as total rate. The water/acetonitrile/toluene comparison cannot be explained by a uniform rate scaling alone.
- A constant irreversible branching fraction is inadequate across time: selectivity at 390 K fell markedly between 3600 and 7200 s.
- Nominal setpoint and total duration are insufficient descriptors; the segmented 430 K result requires operational or actual-temperature history.
- Quenching clearly affects terminal risk, while its compositional effect was small relative to the observed variability.

The experiments cannot determine whether the late target loss is reversal, degradation, or evolving catalyst selectivity. They also cannot determine reaction orders, catalyst-loading dependence, whether byproduct signal represents one or several pools, or whether mixing contributes. K1’s equations should therefore be read as one generative family, not an identified kinetic law.

## 4. The single additional experiment I would choose

I would run one complete trajectory using the established Catalyst B/water recipe: 0.040 mol reagent, 0.080 L water, 0.005 mol Catalyst B, and 600 rpm. I would heat at 390 K for 7200 s, measure by HPLC, then continue at 350 K for 7200 s, terminate without quenching, and perform the final assay.

The first stage recreates the high-conversion, high-target state observed in batches 10 and 12. The second, cooler stage asks what happens to an already product-rich mixture when productive formation from residual reagent should be slower but catalyst, product, and byproducts remain present.

Possible interpretations would be:

- **Conversion decreases while target yield decreases:** This would be the clearest available support for appreciable P → R reversal, because reactant-like material would be regenerated. Instrument differences would still require caution.
- **Conversion remains nearly constant while yield decreases and byproduct or degradation warning rises:** This would favor irreversible target degradation or conversion of P into secondary material.
- **Conversion and yield both continue to increase, but more slowly:** This would indicate that residual forward conversion still dominates and would weaken the case for a kinetically important reverse channel in this range.
- **Almost no change:** This would favor catalyst deactivation, near-freezing of the network at 350 K, or approach to a stationary composition. Those possibilities would remain partly confounded.
- **Selectivity changes without a clear material-balance trend:** This would raise concern that the public channels or cross-instrument calibration are insufficient for mechanistic discrimination.

This is not a perfect experiment because the intermediate HPLC and final assay are different instruments and because lowering temperature changes all rates simultaneously. Nevertheless, it directly targets the largest unresolved claim in K1 and is more discriminating than another optimization replicate.

## 5. Tradeoff between identifiability and operational score

The campaign mixed mechanistic exploration with adaptive optimization.

Early catalyst and solvent screens favored identifiability: batches 2–4 held solvent, temperature, and time fixed while changing catalyst, and batches 2/5/6/7 approximately held catalyst and thermal program fixed while changing solvent. These experiments provided more explanatory value than simply repeating the best current condition.

After batch 5, the design increasingly concentrated on Catalyst B in water. That improved the chance of finding a strong safe result, culminating in batch 10, but sacrificed identification of catalyst–solvent interactions. For example, Catalyst C might have behaved differently in water, and Catalyst A was never compared under the standard 390 K/3600 s condition.

Batch 10 was chiefly optimization-oriented. It extended the favorable Catalyst B/water condition to 7200 s and produced the sample-in best score. In contrast:

- Batch 8 sacrificed likely yield to characterize a mild-temperature regime.
- Batch 9 tested a short, high-temperature regime with greater safety uncertainty.
- Batch 11 sacrificed safety and score robustness to probe a segmented thermal history; the constraint violation was not intended, but it revealed an important coupling.
- Batch 12 omitted quenching, knowingly giving up expected risk reduction to obtain a quench/termination comparison.

The research goal explicitly prioritized an explanatory and predictive account over the public safe score. That justified the temperature, timing, segmentation, and no-quench tests. Nevertheless, optimization pressure influenced the repeated use of Catalyst B/water and the choice of batch 10 as the recommendation. A more purely mechanistic design would have included a catalyst-free control, a matched Catalyst A run, catalyst-loading variation, and a deliberate reversal/deactivation test instead of so many conditions near the emerging optimum.

## 6. Underused evidence and weaknesses in the blind predictions

Several evidence sources were underused or intrinsically difficult to use:

- I relied mainly on processed estimates and did not exploit raw spectral peak shapes or artifact-level uncertainty. Those might have indicated whether the byproduct channel represented one or multiple components.
- The paired HPLC/final-assay observations could have been used to estimate systematic cross-instrument offsets, but quenching, sampling, and assay noise were confounded with instrument identity.
- Actual thermal information was reduced to operation-level temperature increments. I did not have a continuous trace, and I did not quantitatively fit a thermal time constant.
- I did not formally fit competing kinetic models or propagate parameter uncertainty. K1 presented plausible equations, but the blind forecasts used a much simpler effective first-order conversion approximation plus heuristic selectivity decay.
- The cost channel saturated at 1 in the useful experiments and therefore contributed little discrimination; I did not attempt to reconstruct its latent scale.
- Batch 11’s segmentation effect was recognized qualitatively but not converted into a calibrated operational-history term for prediction.

The least reliable blind predictions are **Q06 and Q08** at 465 K for 7200 s, followed by **Q12** at 465 K for 1800 s. K1 explicitly limited the empirical temperature range to 350–430 K, yet these predictions extrapolated far beyond it. Their selectivity, yield, and especially safety estimates depend on unknown high-temperature degradation and on whether risk scales with absolute inventory, concentration, or vessel temperature. The safety intervals for Q06 and Q08—0.55–0.98 and 0.68–1.00—may be too narrow because they largely exclude a strong absolute-scale reduction in risk.

**Q02 and Q04** are also weak because 14400 s at 410 K exceeds the campaign’s maximum observed 7200 s exposure. Their conversion intervals were particularly overconfident: Q04 used 0.97–1.00 even though catalyst deactivation, reversible equilibrium, or an alternative conversion plateau could prevent near-complete conversion. The corresponding yield and byproduct estimates inherit that overconfidence.

**Q11** extrapolates to 14400 s at 350 K. It is less thermally extreme, but the long-duration selectivity loss was not calibrated at that temperature. Its interval should have allowed a wider range of late competition and catalyst deactivation.

All twelve predictions changed catalyst loading, scale, reagent concentration, and stirring speed relative to the campaign. K1 explicitly stated that catalyst-loading order, concentration dependence, and stirring effects were unidentified. Nevertheless, the forecasts imposed a square-root-like catalyst scaling and only a modest stirring correction. The contrast between low-loading Q01/Q02/Q05/Q06 and high-loading Q03/Q04/Q07/Q08 is therefore more speculative than the numerical intervals suggest.

**Q09 and Q10** are comparatively better anchored in catalyst concentration and duration, but the solvent, scale, 410 K temperature, and 400 rpm stirring still require extrapolation. Q10’s predicted quench benefit assumes that the risk reduction seen at the larger campaign scale transfers to the smaller acetonitrile system. That interval may also be too narrow.

These weaknesses are partly inconsistent with K1’s stated scope. K1 correctly warned that extrapolation beyond 350–430 K, 1800–7200 s, fixed loading, and 600 rpm was speculative. The blind-prediction rationale repeated that warning, but several numerical intervals—especially conversion near one and high-temperature safety—did not fully embody it. A more consistent forecast would have used broader, more asymmetric intervals and stronger correlations among conversion, byproduct, degradation, and safety.

## 7. Limitations of the sealed recommendation

Batch 10 was selected because it had the highest observed final target yield, 0.4894, and the highest observed safe score, about 0.2557, while remaining below the safety limit and benefiting from quenching. That makes it the **sample-in highest observed condition**, not a demonstrated optimum.

Its limitations include:

- It was observed only once under the exact quenched condition.
- Batch 12 provided a useful near-replicate of the chemistry without quenching, but it did not replicate the full recommended operation. Its yield of 0.4781 supports rough reproducibility of the chemical region, not exact reproducibility of batch 10.
- No local temperature or time grid tightly bracketed 390 K and 7200 s. Yield might peak earlier or later, and a shorter run might offer a better score after accounting for selectivity and degradation.
- Catalyst amount, reagent concentration, solvent volume, and stirring speed were fixed.
- Catalyst B/water was not compared against every catalyst–solvent interaction.
- The recommendation depends on actual thermal execution. Batch 11 showed that apparently similar nominal commands can produce different peak risks.
- The score advantage is subject to final-assay noise and process variability.

To test repeatability, I would first run independent exact replicates of batch 10 and report distributions for peak risk, conversion, yield, selectivity, degradation warning, and score—not just final averages. Continuous or more detailed temperature records would be essential.

To test local robustness, I would vary one factor at a time or use a compact response-surface design around approximately 380–400 K and 5400–9000 s, while also perturbing stirring and catalyst loading. A robust recommendation should remain favorable under small command and process deviations and should not rely on a narrow safety margin.

To test material generality, the same local design would need to be repeated with the other catalyst and solvent categories. The current recommendation is specifically for anonymous Catalyst B in water; it does not establish a universal solvent or catalyst rule.

To test cross-world generality, the model and policy would need prospective evaluation in independently initialized worlds with potentially different latent kinetic and thermal parameters. The categorical benchmark identities do not guarantee invariant behavior across worlds.

Accordingly, the sealed recommendation should be described as: **the best observed completed batch in this twelve-run campaign, with one nearby chemical corroboration and plausible safety benefit from quenching**. It has not been proven globally optimal, locally optimal, or universally transferable.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 116.2 | none | 0 |
| Q | yes | 0 | 107.1 | none | 0 |
| K2 | yes | 0 | 129.0 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0909 | 0.5833 | 0.2125 | 0.3379 |
| conversion | 0.0231 | 1.0000 | 0.1508 | 0.1508 |
| safety_risk | 0.1227 | 0.5833 | 0.2433 | 0.5965 |
| score | 0.0422 | 0.7833 | 0.1104 | 0.1546 |
| selectivity | 0.1082 | 0.5667 | 0.2233 | 0.4168 |
| yield | 0.0921 | 0.4833 | 0.2142 | 0.3394 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1500 | 0.0900 | 0.2300 | 0.1782 | 0.1719, 0.1927, 0.1713, 0.1761, 0.1792 |
| conversion | 0.3670 | 0.2600 | 0.4900 | 0.3787 | 0.3890, 0.3691, 0.3786, 0.3815, 0.3753 |
| safety_risk | 0.1800 | 0.1000 | 0.2800 | 0.2482 | 0.2482, 0.2482, 0.2482, 0.2482, 0.2482 |
| score | 0.1050 | 0.0550 | 0.1700 | 0.1113 | 0.1107, 0.1150, 0.1139, 0.1108, 0.1061 |
| selectivity | 0.5900 | 0.4900 | 0.6900 | 0.5342 | 0.5285, 0.5428, 0.5404, 0.5432, 0.5159 |
| yield | 0.2170 | 0.1400 | 0.3000 | 0.1981 | 0.1977, 0.2044, 0.2007, 0.1906, 0.1973 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7400 | 0.6000 | 0.8800 | 0.8680 | 0.8628, 0.8805, 0.8748, 0.8604, 0.8614 |
| conversion | 0.9740 | 0.9000 | 1.0000 | 0.9713 | 0.9732, 0.9617, 0.9777, 0.9684, 0.9755 |
| safety_risk | 0.2900 | 0.1600 | 0.4600 | 0.2504 | 0.2504, 0.2504, 0.2504, 0.2504, 0.2504 |
| score | 0.0400 | 0.0100 | 0.0900 | 0.0223 | 0.0226, 0.0237, 0.0181, 0.0255, 0.0215 |
| selectivity | 0.2400 | 0.1200 | 0.3800 | 0.1167 | 0.1044, 0.1305, 0.1151, 0.1180, 0.1155 |
| yield | 0.2340 | 0.1100 | 0.3600 | 0.1171 | 0.1251, 0.1144, 0.1059, 0.1252, 0.1148 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2210 | 0.1400 | 0.3100 | 0.2009 | 0.2003, 0.1949, 0.1960, 0.2082, 0.2050 |
| conversion | 0.5980 | 0.4700 | 0.7200 | 0.6928 | 0.6944, 0.6860, 0.6802, 0.7078, 0.6957 |
| safety_risk | 0.2000 | 0.1100 | 0.3100 | 0.2508 | 0.2508, 0.2508, 0.2508, 0.2508, 0.2508 |
| score | 0.1900 | 0.1100 | 0.2800 | 0.2732 | 0.2736, 0.2726, 0.2729, 0.2680, 0.2788 |
| selectivity | 0.6300 | 0.5300 | 0.7200 | 0.7132 | 0.7147, 0.7062, 0.7182, 0.6935, 0.7334 |
| yield | 0.3770 | 0.2800 | 0.4700 | 0.4874 | 0.4870, 0.4919, 0.4867, 0.4831, 0.4881 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7990 | 0.6500 | 0.9100 | 0.9222 | 0.9358, 0.9360, 0.9159, 0.9147, 0.9085 |
| conversion | 0.9990 | 0.9700 | 1.0000 | 0.9978 | 1.0000, 0.9958, 1.0000, 0.9931, 1.0000 |
| safety_risk | 0.3400 | 0.1900 | 0.5400 | 0.2514 | 0.2514, 0.2514, 0.2514, 0.2514, 0.2514 |
| score | 0.0260 | 0.0050 | 0.0750 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.2000 | 0.0800 | 0.3400 | 0.1116 | 0.1207, 0.1187, 0.1061, 0.1146, 0.0981 |
| yield | 0.2000 | 0.0800 | 0.3400 | 0.1152 | 0.1099, 0.1171, 0.1206, 0.1122, 0.1165 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2310 | 0.1500 | 0.3200 | 0.3580 | 0.3663, 0.3430, 0.3585, 0.3549, 0.3671 |
| conversion | 0.5500 | 0.4200 | 0.6800 | 0.5450 | 0.5461, 0.5383, 0.5449, 0.5515, 0.5443 |
| safety_risk | 0.0550 | 0.0250 | 0.1100 | 0.1399 | 0.1399, 0.1399, 0.1399, 0.1399, 0.1399 |
| score | 0.1750 | 0.1100 | 0.2400 | 0.1240 | 0.1268, 0.1238, 0.1222, 0.1240, 0.1233 |
| selectivity | 0.5800 | 0.4800 | 0.6700 | 0.3503 | 0.3610, 0.3467, 0.3378, 0.3526, 0.3533 |
| yield | 0.3190 | 0.2300 | 0.4100 | 0.1927 | 0.1927, 0.1961, 0.1959, 0.1895, 0.1892 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8620 | 0.7800 | 0.9600 | 0.7622 | 0.7621, 0.7660, 0.7721, 0.7664, 0.7444 |
| conversion | 0.9580 | 0.9000 | 1.0000 | 0.9635 | 0.9596, 0.9586, 0.9801, 0.9618, 0.9574 |
| safety_risk | 0.7800 | 0.5500 | 0.9800 | 0.4248 | 0.4248, 0.4248, 0.4248, 0.4248, 0.4248 |
| score | 0.0020 | 0.0000 | 0.0150 | 0.0116 | 0.0027, 0.0143, 0.0140, 0.0161, 0.0108 |
| selectivity | 0.1000 | 0.0300 | 0.2200 | 0.2224 | 0.1987, 0.2343, 0.2303, 0.2341, 0.2145 |
| yield | 0.0960 | 0.0300 | 0.2000 | 0.2074 | 0.2010, 0.2081, 0.2043, 0.2118, 0.2120 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3180 | 0.2200 | 0.4100 | 0.4182 | 0.4188, 0.4236, 0.4141, 0.4110, 0.4234 |
| conversion | 0.7960 | 0.6800 | 0.8900 | 0.8317 | 0.8297, 0.8404, 0.8394, 0.8293, 0.8196 |
| safety_risk | 0.0650 | 0.0300 | 0.1300 | 0.1423 | 0.1423, 0.1423, 0.1423, 0.1423, 0.1423 |
| score | 0.2680 | 0.1800 | 0.3600 | 0.2552 | 0.2548, 0.2547, 0.2606, 0.2520, 0.2539 |
| selectivity | 0.6000 | 0.5000 | 0.6900 | 0.5081 | 0.5162, 0.5026, 0.5107, 0.5022, 0.5089 |
| yield | 0.4780 | 0.3700 | 0.5900 | 0.4251 | 0.4196, 0.4250, 0.4351, 0.4214, 0.4242 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9080 | 0.8000 | 0.9700 | 0.8136 | 0.8039, 0.8190, 0.8162, 0.8189, 0.8103 |
| conversion | 0.9980 | 0.9700 | 1.0000 | 0.9972 | 1.0000, 0.9961, 0.9898, 1.0000, 1.0000 |
| safety_risk | 0.9000 | 0.6800 | 1.0000 | 0.4257 | 0.4257, 0.4257, 0.4257, 0.4257, 0.4257 |
| score | 0.0010 | 0.0000 | 0.0100 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0900 | 0.0200 | 0.2000 | 0.2151 | 0.2198, 0.2201, 0.2127, 0.2197, 0.2030 |
| yield | 0.0900 | 0.0200 | 0.2000 | 0.2196 | 0.2080, 0.2292, 0.2229, 0.2200, 0.2176 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5920 | 0.4600 | 0.7200 | 0.6412 | 0.6468, 0.6526, 0.6308, 0.6450, 0.6309 |
| conversion | 0.9400 | 0.8700 | 0.9800 | 0.9603 | 0.9542, 0.9623, 0.9671, 0.9597, 0.9582 |
| safety_risk | 0.2500 | 0.1400 | 0.4100 | 0.2514 | 0.2514, 0.2514, 0.2514, 0.2514, 0.2514 |
| score | 0.0970 | 0.0400 | 0.1700 | 0.1563 | 0.1611, 0.1557, 0.1566, 0.1521, 0.1560 |
| selectivity | 0.3700 | 0.2400 | 0.5000 | 0.3491 | 0.3682, 0.3369, 0.3532, 0.3389, 0.3485 |
| yield | 0.3480 | 0.2300 | 0.4700 | 0.3309 | 0.3325, 0.3366, 0.3274, 0.3269, 0.3310 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5830 | 0.4500 | 0.7100 | 0.6416 | 0.6430, 0.6534, 0.6375, 0.6335, 0.6407 |
| conversion | 0.9400 | 0.8700 | 0.9800 | 0.9574 | 0.9629, 0.9531, 0.9508, 0.9623, 0.9580 |
| safety_risk | 0.1100 | 0.0550 | 0.2100 | 0.1449 | 0.1449, 0.1449, 0.1449, 0.1449, 0.1449 |
| score | 0.1210 | 0.0550 | 0.2000 | 0.1985 | 0.2001, 0.1935, 0.2037, 0.1991, 0.1961 |
| selectivity | 0.3800 | 0.2500 | 0.5100 | 0.3414 | 0.3470, 0.3397, 0.3535, 0.3365, 0.3301 |
| yield | 0.3570 | 0.2400 | 0.4800 | 0.3305 | 0.3295, 0.3202, 0.3377, 0.3337, 0.3315 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4840 | 0.3600 | 0.6100 | 0.6839 | 0.6840, 0.6827, 0.6839, 0.6823, 0.6867 |
| conversion | 0.9140 | 0.8400 | 0.9700 | 0.9229 | 0.9302, 0.9186, 0.9241, 0.9175, 0.9240 |
| safety_risk | 0.0700 | 0.0300 | 0.1400 | 0.1421 | 0.1421, 0.1421, 0.1421, 0.1421, 0.1421 |
| score | 0.1880 | 0.1200 | 0.2700 | 0.1471 | 0.1415, 0.1447, 0.1532, 0.1432, 0.1530 |
| selectivity | 0.4700 | 0.3400 | 0.5900 | 0.2754 | 0.2586, 0.2864, 0.2814, 0.2556, 0.2947 |
| yield | 0.4300 | 0.3100 | 0.5500 | 0.2553 | 0.2500, 0.2434, 0.2664, 0.2592, 0.2577 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3380 | 0.2300 | 0.4500 | 0.2756 | 0.2779, 0.2906, 0.2640, 0.2722, 0.2734 |
| conversion | 0.7050 | 0.5700 | 0.8200 | 0.7780 | 0.7710, 0.7746, 0.7904, 0.7802, 0.7737 |
| safety_risk | 0.5500 | 0.3600 | 0.7800 | 0.4251 | 0.4251, 0.4251, 0.4251, 0.4251, 0.4251 |
| score | 0.0860 | 0.0300 | 0.1600 | 0.2070 | 0.2049, 0.2009, 0.2080, 0.2099, 0.2113 |
| selectivity | 0.5200 | 0.3900 | 0.6400 | 0.6441 | 0.6530, 0.6267, 0.6386, 0.6481, 0.6540 |
| yield | 0.3670 | 0.2500 | 0.4900 | 0.5031 | 0.4939, 0.4996, 0.5059, 0.5073, 0.5087 |

## Recommendation retest

- Selected source batch: `10`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.3791 | 0.3929 | 0.0138 |
| conversion | 0.8750 | 0.8558 | -0.0192 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1921 | 0.1878 | -0.0043 |
| safety_risk | 0.1447 | 0.1447 | 0.0000 |
| score | 0.2557 | 0.2503 | -0.0054 |
| selectivity | 0.5501 | 0.5527 | 0.0026 |
| virtual_spectrum_summary | 0.2950 | 0.3006 | 0.0057 |
| yield | 0.4894 | 0.4791 | -0.0103 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
