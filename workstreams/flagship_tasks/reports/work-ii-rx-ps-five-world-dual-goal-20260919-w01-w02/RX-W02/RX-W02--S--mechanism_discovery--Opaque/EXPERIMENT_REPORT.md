# RX-W02--S--mechanism_discovery--Opaque

## Run summary

- World: `RX-W02`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay: `{'checked_steps': 85, 'max_abs_error': 0.0, 'mismatches': [], 'verified': True}`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `9`
- Rationale: Batch 9 gave the highest observed final yield and campaign score, with strong conversion while remaining below the safety-risk limit.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.2161 | 0.5402 | 0.4029 | 0.1868 | 0.0207 | 0.1464 | 0.0959 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.2361 | 0.5724 | 0.4183 | 0.1874 | 0.0362 | 0.1502 | 0.1118 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.2198 | 0.5843 | 0.3643 | 0.1583 | 0.0321 | 0.1463 | 0.1046 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.2102 | 0.5235 | 0.3967 | 0.1908 | 0.0407 | 0.1457 | 0.0891 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.1948 | 0.6053 | 0.3199 | 0.1214 | 0.0132 | 0.1009 | 0.1158 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.1976 | 0.4884 | 0.4057 | 0.2103 | 0.0298 | 0.1267 | 0.0847 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | no | 0.2120 | 0.5225 | 0.4303 | 0.2121 | 0.0202 | 0.1594 | 0.0867 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 300 K × 3600 s @ 600 rpm | no | 0.0939 | 0.4638 | 0.1893 | 0.1003 | 0.0104 | 0.1263 | 0.0156 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 380 K × 3600 s @ 600 rpm | no | 0.3523 | 0.5611 | 0.6194 | 0.2795 | 0.0569 | 0.1885 | 0.1583 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 1200 s @ 600 rpm | no | 0.1036 | 0.5764 | 0.1440 | 0.0790 | 0.0007 | 0.1289 | 0.0420 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 7200 s @ 600 rpm | no | 0.3175 | 0.4786 | 0.6570 | 0.3582 | 0.0671 | 0.1622 | 0.1393 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 3600 s @ 600 rpm | yes | 0.2123 | 0.5237 | 0.4005 | 0.1919 | 0.0233 | 0.1418 | 0.0921 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

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
    "byproduct_signal": 0.18675775825977325,
    "conversion": 0.4028644561767578,
    "cost": 1.0,
    "degradation_warning": 0.02074926719069481,
    "safety_risk": 0.14642088115215302,
    "score": 0.09587715566158295,
    "selectivity": 0.5401735305786133,
    "virtual_spectrum_summary": 0.11205393821001053,
    "yield": 0.2160918116569519
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `14`.

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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.18738043308258057,
    "conversion": 0.4183264970779419,
    "cost": 1.0,
    "degradation_warning": 0.03619616851210594,
    "safety_risk": 0.1502189338207245,
    "score": 0.11175815761089325,
    "selectivity": 0.57237708568573,
    "virtual_spectrum_summary": 0.11934751272201538,
    "yield": 0.23607438802719116
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `21`.

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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.15832604467868805,
    "conversion": 0.3642897605895996,
    "cost": 1.0,
    "degradation_warning": 0.0320940837264061,
    "safety_risk": 0.1463121771812439,
    "score": 0.10458352416753769,
    "selectivity": 0.5843055248260498,
    "virtual_spectrum_summary": 0.10152166336774826,
    "yield": 0.21979659795761108
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `28`.

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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.1907794177532196,
    "conversion": 0.39673247933387756,
    "cost": 1.0,
    "degradation_warning": 0.04068201035261154,
    "safety_risk": 0.14567112922668457,
    "score": 0.08907239884138107,
    "selectivity": 0.5234901905059814,
    "virtual_spectrum_summary": 0.12323558330535889,
    "yield": 0.21019652485847473
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `35`.

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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.12135493755340576,
    "conversion": 0.31991273164749146,
    "cost": 1.0,
    "degradation_warning": 0.013154769316315651,
    "safety_risk": 0.10094886273145676,
    "score": 0.11580417305231094,
    "selectivity": 0.6053281426429749,
    "virtual_spectrum_summary": 0.07266486436128616,
    "yield": 0.19476965069770813
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `42`.

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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.21025720238685608,
    "conversion": 0.4056757390499115,
    "cost": 1.0,
    "degradation_warning": 0.02979656681418419,
    "safety_risk": 0.12665700912475586,
    "score": 0.08469521254301071,
    "selectivity": 0.4883957505226135,
    "virtual_spectrum_summary": 0.12904991209506989,
    "yield": 0.1975608766078949
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `49`.

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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.21207129955291748,
    "conversion": 0.43030020594596863,
    "cost": 1.0,
    "degradation_warning": 0.020171210169792175,
    "safety_risk": 0.15940353274345398,
    "score": 0.08671856671571732,
    "selectivity": 0.5225152969360352,
    "virtual_spectrum_summary": 0.12571625411510468,
    "yield": 0.21197830140590668
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `56`.

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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 300
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.10031848400831223,
    "conversion": 0.18928827345371246,
    "cost": 1.0,
    "degradation_warning": 0.010441740043461323,
    "safety_risk": 0.1262885481119156,
    "score": 0.015584169887006283,
    "selectivity": 0.4637523889541626,
    "virtual_spectrum_summary": 0.059873949736356735,
    "yield": 0.093867726624012
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `63`.

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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2795443534851074,
    "conversion": 0.6194243431091309,
    "cost": 1.0,
    "degradation_warning": 0.0568508505821228,
    "safety_risk": 0.1885319948196411,
    "score": 0.1582971215248108,
    "selectivity": 0.5610752105712891,
    "virtual_spectrum_summary": 0.17933227121829987,
    "yield": 0.35231319069862366
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `70`.

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
      "duration_s": 1200,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.07901936769485474,
    "conversion": 0.14396122097969055,
    "cost": 1.0,
    "degradation_warning": 0.0007280842401087284,
    "safety_risk": 0.12888416647911072,
    "score": 0.04195176810026169,
    "selectivity": 0.5764049291610718,
    "virtual_spectrum_summary": 0.04378828778862953,
    "yield": 0.10363071411848068
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `77`.

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
      "duration_s": 7200,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.358213871717453,
    "conversion": 0.6569579839706421,
    "cost": 1.0,
    "degradation_warning": 0.0670924261212349,
    "safety_risk": 0.1622140109539032,
    "score": 0.13934583961963654,
    "selectivity": 0.4785938858985901,
    "virtual_spectrum_summary": 0.22720922529697418,
    "yield": 0.3174946904182434
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `85`.

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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.19189545512199402,
    "conversion": 0.40045005083084106,
    "cost": 1.0,
    "degradation_warning": 0.023256709799170494,
    "safety_risk": 0.14175249636173248,
    "score": 0.09211904555559158,
    "selectivity": 0.5237399339675903,
    "virtual_spectrum_summary": 0.11600801348686218,
    "yield": 0.21231921017169952
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Experimental scope

I completed 12 batches using 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring in every batch. Thus, the conclusions apply to this composition and agitation regime; reagent concentration, catalyst loading, solvent volume, and stirring effects were not independently identified. The catalysts are anonymous benchmark formulations, and solvent effects are categorical benchmark effects rather than claims about real-solvent physical chemistry.

The study sequence was:
- Batch 1: Catalyst A/acetonitrile, 340 K target, 3600 s baseline.
- Batches 2–4: Catalysts B, C, and D under the Batch 1 conditions.
- Batches 5–7: water, ethanol, and toluene with Catalyst A at 340 K for 3600 s.
- Batches 8–9: 300 and 380 K targets with Catalyst A/acetonitrile for 3600 s.
- Batches 10–11: 1200 and 7200 s at a 340 K target with Catalyst A/acetonitrile.
- Batch 12: matched to Batch 1 but quenched after heating and before analysis.

Each batch received an HPLC measurement near the end of processing and a required post-termination final assay. Numerical comparisons below primarily use final assays; HPLC is treated as corroborating evidence rather than silently pooled with the final assay.

2. Proposed reaction network

The simplest account consistent with the observations is a parallel reaction network followed by slower degradation:

R -> P, desired target formation
R -> B, competing byproduct formation
P -> D and/or B -> D, accumulated thermal degradation

A useful minimal model is

dR/dt = -[kP(T,S,C,a) + kB(T,S,C,a)]R

dP/dt = kP(T,S,C,a)R - kDP(T,S,C)P

dB/dt = kB(T,S,C,a)R - kDB(T,S,C)B

dD/dt = kDP P + kDB B

Here S is solvent category, C is catalyst category, T is the actual temperature history, and a is an optional catalyst-activity state. If deactivation is included, a possible equation is da/dt = -kd(T,S,C)a. The present data do not require strong deactivation, however; this term should remain optional rather than asserted as established.

For approximately constant activity and temperature,

X(t) approximately equals 1 - exp[-(kP + kB)t].

The data also support the measurement-level relation

yield approximately equals conversion × selectivity.

For example, Batch 1 gives 0.4029 × 0.5402 = approximately 0.2176, close to the measured yield of 0.2161. Batch 9 gives approximately 0.3476 versus a measured 0.3523, and Batch 11 gives approximately 0.3144 versus 0.3175. Small disagreements are expected from independent noisy assay channels and possible degradation/mass-balance effects.

The rate constants can be represented by categorical multipliers and an Arrhenius term:

ki(T,S,C) = Ai × fS,i(S) × fC,i(C) × exp[-Ei/(RT)].

The experiments show that solvent and catalyst can affect desired and competing channels differently, so a single common multiplier for all rates would be inadequate.

3. Time dependence and apparent kinetics

The 340 K time series strongly supports progressive conversion with a fairly stable apparent first-order total rate:

- Batch 10, 1200 s: conversion 0.1440, yield 0.1036, selectivity 0.5764, byproduct 0.0790, degradation warning 0.0007.
- Batch 1, 3600 s: conversion 0.4029, yield 0.2161, selectivity 0.5402, byproduct 0.1868, degradation warning 0.0207.
- Batch 11, 7200 s: conversion 0.6570, yield 0.3175, selectivity 0.4786, byproduct 0.3582, degradation warning 0.0671.

Using k_app = -ln(1-X)/t gives approximately 1.30×10^-4, 1.43×10^-4, and 1.49×10^-4 s^-1 for Batches 10, 1, and 11. Their agreement is notable given single-batch noise and thermal transients. It supports pseudo-first-order depletion over this interval and provides no positive evidence for severe catalyst deactivation.

However, selectivity falls from 0.576 at 1200 s to 0.540 at 3600 s and 0.479 at 7200 s, while byproduct and degradation signals rise. Therefore extended residence time increases target amount but progressively favors undesirable material. This can arise from a slower competing R -> B channel, secondary P -> D degradation, catalyst-state evolution, or a combination. The current measurements cannot uniquely separate those explanations.

Batch 11 had more target yield than Batch 1, so the target was not yet undergoing catastrophic net loss at 7200 s. Nevertheless, its declining selectivity and increasing degradation warning imply that indefinite heating should not be extrapolated as beneficial.

4. Temperature dependence and thermal history

Temperature was the strongest rate-control variable tested:

- Batch 8, 300 K target for 3600 s: conversion 0.1893, yield 0.0939, selectivity 0.4638, byproduct 0.1003, degradation warning 0.0104.
- Batch 1, 340 K target for 3600 s: conversion 0.4029, yield 0.2161, selectivity 0.5402, byproduct 0.1868, degradation warning 0.0207.
- Batch 9, 380 K target for 3600 s: conversion 0.6194, yield 0.3523, selectivity 0.5611, byproduct 0.2795, degradation warning 0.0569.

The recorded temperature changes were +1.94 K in Batch 8, about +40.14 K in Batch 1, and +75.22 K in Batch 9. These values demonstrate that requested setpoint is not identical to realized thermal history. In particular, the high-temperature run did not simply exhibit an exact +80 K endpoint change. A suitable process layer is therefore

dT/dt = [Tset - T]/tauT - Qloss(T, solvent) + reaction-heat terms,

rather than assuming instantaneous isothermal operation. Only aggregate temperature changes were observed, not the full trajectory, so tauT and heat-generation terms are unidentifiable.

Apparent first-order constants calculated from final conversion are 5.83×10^-5 s^-1 at the 300 K target, 1.43×10^-4 s^-1 at 340 K, and 2.68×10^-4 s^-1 at the 380 K target. Treating approximately 300, 340, and 375 K as representative realized temperatures gives pairwise apparent activation energies near 19 kJ mol^-1. This is a useful local empirical descriptor, not a precise elementary-step activation energy, because heating ramps, solvent effects, degradation, and measurement noise are folded into it.

Higher temperature accelerated desired formation but also increased byproduct and degradation. Batch 9 delivered the highest observed yield and score, but its degradation warning was nearly three times that of Batch 1. Thus temperature changes total rate and the balance among channels; it is not merely a uniform clock-speed multiplier.

5. Catalyst effects

At the common acetonitrile/340 K/3600 s condition:

- Batch 1, Catalyst A: conversion 0.4029, yield 0.2161, selectivity 0.5402, byproduct 0.1868.
- Batch 2, Catalyst B: conversion 0.4183, yield 0.2361, selectivity 0.5724, byproduct 0.1874.
- Batch 3, Catalyst C: conversion 0.3643, yield 0.2198, selectivity 0.5843, byproduct 0.1583.
- Batch 4, Catalyst D: conversion 0.3967, yield 0.2102, selectivity 0.5235, byproduct 0.1908.

Catalyst B gave the largest yield and conversion in this screen. Catalyst C gave the highest selectivity and lowest byproduct signal, but at lower conversion. Catalyst D was the least favorable of the four by yield and selectivity. This pattern supports catalyst-specific control of both productive and competing rates: Catalyst B appears to increase productive throughput, whereas Catalyst C appears relatively more selective but slower.

These effects are modest and each catalyst was tested only once. Some pairwise differences are comparable to assay uncertainty, so the exact ranking is provisional. Moreover, there was no catalyst-free control and no catalyst-loading series. Consequently, I cannot determine the absolute catalytic acceleration, reaction order in catalyst, saturation behavior, or whether any catalyst merely changes induction/heating behavior.

6. Solvent effects

With Catalyst A at 340 K for 3600 s:

- Batch 5, water: conversion 0.3199, yield 0.1948, selectivity 0.6053, byproduct 0.1214, degradation 0.0132, risk 0.1009.
- Batch 6, ethanol: conversion 0.4057, yield 0.1976, selectivity 0.4884, byproduct 0.2103, degradation 0.0298, risk 0.1267.
- Batch 1, acetonitrile: conversion 0.4029, yield 0.2161, selectivity 0.5402, byproduct 0.1868, degradation 0.0207, risk 0.1464.
- Batch 7, toluene: conversion 0.4303, yield 0.2120, selectivity 0.5225, byproduct 0.2121, degradation 0.0202, risk 0.1594.

Water produced lower conversion but the highest selectivity, lowest byproduct signal, lowest degradation warning, and lowest safety risk. Ethanol and toluene favored more competing material. Acetonitrile provided the highest measured yield of this solvent screen, though toluene had slightly greater conversion.

This is consistent with solvent-specific multipliers that suppress or enhance productive and side pathways by different amounts. Because runtime solvent effects are categorical benchmarks, it would be inappropriate to attribute these differences specifically to real-world polarity, boiling point, or proticity without additional evidence.

7. Quench and termination

Batch 12 reproduced the Batch 1 nominal reaction and then quenched before measurement. Its final conversion, yield, selectivity, byproduct, and degradation warning were 0.4005, 0.2123, 0.5237, 0.1919, and 0.0233. These are close to Batch 1 values of 0.4029, 0.2161, 0.5402, 0.1868, and 0.0207. The chemical differences are small enough to be compatible with assay noise and ordinary batch variation.

The observed safety risk was lower after quenching: 0.1418 in Batch 12 versus 0.1464 in Batch 1. Thus the evidence supports quench as a way to reduce thermal-state risk and freeze composition, without a demonstrated large instantaneous yield penalty. It does not establish whether quenching at substantially earlier times would improve selectivity; only one post-3600-s quench was tested.

Termination itself appears to halt further reaction. HPLC and final assays generally agreed qualitatively, although individual channels differed. For example, Batch 1 HPLC gave conversion 0.4072 and yield 0.2160, versus final values 0.4029 and 0.2161. Larger discrepancies occurred in some batches, notably Batch 10 yield, so instrument/process uncertainty should be retained rather than interpreting every difference as chemistry.

8. Safety coupling and recommended operating point

All observed risks remained below the 0.35 limit. Risk depended on both recipe and thermal exposure. Among the 3600-s solvent runs, risk ranged from 0.1009 in water to 0.1594 in toluene. At the standard acetonitrile recipe, it increased from 0.1289 at 1200 s to 0.1464 at 3600 s and 0.1622 at 7200 s; the high-temperature Batch 9 reached 0.1885.

Batch 9 was the sealed recommendation because it had the highest final yield (0.3523), conversion (0.6194), campaign score (0.1583), and remained well below the risk constraint. This is an empirical recommendation within the tested domain, not a claim that still higher temperature would improve the process. Its elevated byproduct and degradation signals indicate an approaching tradeoff.

If selectivity and risk were prioritized over absolute target yield, Batch 5 would be a defensible alternative: its score was 0.1158, selectivity 0.6053, and risk only 0.1009. If catalyst choice could be changed while retaining the standard solvent, Catalyst B in Batch 2 was the best tested catalyst for yield at 340 K.

9. How the evidence changed the explanation

Batch 1 established that target and byproduct form together at moderate conversion. Batches 2–4 changed the initial simple idea of catalysts acting only as uniform rate multipliers: Catalyst C's higher selectivity but lower conversion implies differential effects on productive and competing channels. Batches 5–7 produced the same conclusion for solvent category, especially the water result.

Batches 8 and 9 established strong thermal acceleration and showed that degradation also rises with temperature. The close-to-Arrhenius change in apparent total rate motivated the temperature-dependent kinetic form.

Batches 10 and 11 were especially diagnostic. Their nearly constant apparent total first-order rate argues against strong deactivation over 1200–7200 s, while declining selectivity and increasing degradation require time-dependent accumulation of undesirable material. I therefore favor parallel formation plus secondary degradation over a model consisting only of R -> P.

Batch 12 showed that quenching after the standard reaction time mainly changes thermal risk, with no resolved large chemical discontinuity. This makes quench a process-state intervention rather than evidence for a new reaction branch.

10. Limits, unidentified factors, and competing explanations

The model is locally supported only for 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, 600 rpm, 300–380 K requested temperature, and 1200–7200 s. Extrapolation outside these bounds is speculative.

The following remain unidentified:
- Reaction orders in reagent and catalyst.
- Absolute catalyst-free rates and the magnitude of catalytic acceleration.
- Heating time constant and full temperature trajectory.
- Whether degradation consumes target, byproduct, or both.
- Whether catalyst deactivation, activation, or induction occurs.
- Effects of stirring and mass transfer.
- Interactions between catalyst and solvent, because only Catalyst A received a full solvent screen.
- Repeatability and true between-batch variance, because most conditions had one replicate.
- Exact chemical identities, which are deliberately hidden.

Reasonable competing explanations include: two parallel primary pathways with no secondary degradation; a sequential R -> P -> B mechanism; catalyst activation followed by deactivation; or temperature-dependent measurement/process bias. The rising degradation warning and falling selectivity with time favor a degradation-containing network, but they do not uniquely identify its topology. A sequential P -> B model could also reproduce declining selectivity, while the fact that target yield continues to rise through 7200 s would require formation still to exceed loss over the tested interval.

Accordingly, the strongest defensible conclusion is that total conversion follows an approximately first-order, thermally activated process in the tested domain, while catalyst, solvent, temperature, and residence time independently alter the competition between target formation and undesirable-product accumulation. The data support this predictive structure, but not a unique microscopic mechanism.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported parallel target/byproduct model with approximately first-order reactant depletion, Arrhenius-like thermal acceleration, declining selectivity with accumulated hot residence, and a modest Catalyst B selectivity advantage. Catalyst concentration was scaled from the campaign concentration of approximately 0.0625 mol/L; the medium query loading is close to that value, whereas the low and high loadings require extrapolation. Yield and byproduct were constrained approximately by yield = conversion × selectivity and byproduct signal = conversion × (1 - selectivity). Scores were computed from the public outcomes' inferred exact linear relationship: score = max(0, -0.1 + 0.4·yield + 0.25·selectivity + 0.1·conversion - 0.45·safety_risk). The 80% intervals include assay noise, uncertain thermal trajectories, unmeasured catalyst-loading response, and especially large model uncertainty at 410–465 K and 14400 s.

### Q01

The low catalyst concentration offsets much of the acceleration expected at 410 K. The short exposure should retain moderate Catalyst B selectivity and limit degradation, but temperature and catalyst-loading extrapolation make the interval wider than assay noise alone.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.0900 | 0.3100 |
| conversion | 0.4200 | 0.2500 | 0.6000 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 |
| score | 0.0800 | 0.0100 | 0.1800 |
| selectivity | 0.5500 | 0.4100 | 0.6800 |
| yield | 0.2300 | 0.1300 | 0.3500 |

### Q02

Four hours at 410 K should drive nearly complete conversion even at low catalyst loading. Long hot residence is predicted to shift converted material toward byproduct or degradation, lower selectivity, and bring safety risk close to the stated limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6800 | 0.4900 | 0.8400 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.3300 | 0.2400 | 0.4500 |
| score | 0.0440 | 0.0000 | 0.1600 |
| selectivity | 0.3000 | 0.1400 | 0.4700 |
| yield | 0.3000 | 0.1400 | 0.4700 |

### Q03

The high Catalyst B loading should give substantially more conversion than Q01 during the same short heat. Short residence preserves the favorable selectivity observed for Catalyst B, making this one of the stronger predicted outcomes.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2900 | 0.1500 | 0.4400 |
| conversion | 0.7000 | 0.5000 | 0.8500 |
| safety_risk | 0.2050 | 0.1400 | 0.2900 |
| score | 0.1890 | 0.0800 | 0.3100 |
| selectivity | 0.5900 | 0.4600 | 0.7100 |
| yield | 0.4100 | 0.2700 | 0.5500 |

### Q04

High catalyst loading and four hours at 410 K should exhaust almost all reactant. The long post-formation thermal exposure is expected to erase much of the initial selectivity advantage through competing conversion and degradation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6800 | 0.5000 | 0.8500 |
| conversion | 0.9990 | 0.9600 | 1.0000 |
| safety_risk | 0.3400 | 0.2500 | 0.4700 |
| score | 0.0550 | 0.0000 | 0.1800 |
| selectivity | 0.3200 | 0.1500 | 0.4900 |
| yield | 0.3200 | 0.1500 | 0.4900 |

### Q05

At 350 K, the low catalyst concentration should produce only moderate conversion over two hours. Selectivity is expected to decline somewhat with residence time but degradation and safety risk should remain milder than in the 410–465 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1600 | 0.4100 |
| conversion | 0.5600 | 0.4000 | 0.7000 |
| safety_risk | 0.1700 | 0.1200 | 0.2400 |
| score | 0.1170 | 0.0400 | 0.2100 |
| selectivity | 0.5000 | 0.3800 | 0.6200 |
| yield | 0.2800 | 0.1800 | 0.4000 |

### Q06

Two hours at 465 K is far outside the measured temperature range and should give nearly complete conversion despite low catalyst loading. Severe competing conversion, degradation, and likely safety-limit pressure lead to low predicted selectivity and a score at the clipping floor.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7900 | 0.6100 | 0.9400 |
| conversion | 0.9800 | 0.8900 | 1.0000 |
| safety_risk | 0.3800 | 0.2700 | 0.5400 |
| score | 0.0000 | 0.0000 | 0.1000 |
| selectivity | 0.2000 | 0.0500 | 0.3800 |
| yield | 0.2000 | 0.0500 | 0.3800 |

### Q07

High Catalyst B loading at the comparatively moderate 350 K target should provide strong conversion without the extreme degradation expected at higher temperatures. This balance gives the highest predicted score among the queries.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3900 | 0.2700 | 0.5200 |
| conversion | 0.8400 | 0.7000 | 0.9300 |
| safety_risk | 0.1750 | 0.1200 | 0.2500 |
| score | 0.2220 | 0.1200 | 0.3300 |
| selectivity | 0.5400 | 0.4200 | 0.6600 |
| yield | 0.4500 | 0.3200 | 0.5800 |

### Q08

High catalyst loading combined with two hours at 465 K should rapidly reach complete conversion and then accumulate extensive byproduct or degradation. Both the temperature and loading are extrapolations, so the interval is broad, but a safety-limit violation and near-zero score are plausible.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6500 | 0.9600 |
| conversion | 0.9990 | 0.9600 | 1.0000 |
| safety_risk | 0.4000 | 0.2900 | 0.5700 |
| score | 0.0000 | 0.0000 | 0.0800 |
| selectivity | 0.1800 | 0.0400 | 0.3500 |
| yield | 0.1800 | 0.0400 | 0.3500 |

### Q09

The medium catalyst concentration is close to the catalyst concentration used in the campaign. At 410 K for two hours, nearly complete conversion is expected, but the time trend indicates substantial loss of selectivity to competing material.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4200 | 0.7400 |
| conversion | 0.9700 | 0.8800 | 1.0000 |
| safety_risk | 0.2700 | 0.2000 | 0.3800 |
| score | 0.1300 | 0.0200 | 0.2500 |
| selectivity | 0.4000 | 0.2500 | 0.5500 |
| yield | 0.3900 | 0.2300 | 0.5500 |

### Q10

The quench occurs only after the full heat treatment, so composition should remain close to Q09. Based on the matched campaign quench comparison, it is predicted to give a small risk reduction and at most a minor apparent improvement in retained selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5700 | 0.4100 | 0.7300 |
| conversion | 0.9700 | 0.8800 | 1.0000 |
| safety_risk | 0.2500 | 0.1800 | 0.3500 |
| score | 0.1460 | 0.0300 | 0.2700 |
| selectivity | 0.4100 | 0.2600 | 0.5600 |
| yield | 0.4000 | 0.2400 | 0.5600 |

### Q11

Four hours at 350 K should approach high conversion at the medium catalyst concentration. The lower temperature moderates degradation relative to 410 K, but the very long residence still predicts lower selectivity than the shorter 350 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5400 | 0.3800 | 0.7000 |
| conversion | 0.9300 | 0.8000 | 0.9900 |
| safety_risk | 0.2300 | 0.1600 | 0.3300 |
| score | 0.1500 | 0.0400 | 0.2700 |
| selectivity | 0.4200 | 0.2700 | 0.5700 |
| yield | 0.3900 | 0.2400 | 0.5500 |

### Q12

The short duration limits degradation relative to Q06 and Q08, while 465 K still produces rapid conversion. The result should retain moderate target yield, but the large temperature extrapolation creates substantial uncertainty in both selectivity and safety.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2700 | 0.5900 |
| conversion | 0.8100 | 0.6200 | 0.9200 |
| safety_risk | 0.2700 | 0.1800 | 0.3900 |
| score | 0.1290 | 0.0200 | 0.2500 |
| selectivity | 0.4700 | 0.3200 | 0.6100 |
| yield | 0.3800 | 0.2300 | 0.5300 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial material packet did not provide a substantive task-specific kinetic mechanism, nominal rate constants, catalyst ranking, solvent ranking, or preferred operating window. It explicitly said that no task-specific property dossier was supplied and that experimental evidence was authoritative. Consequently, most of K1 was constructed from the campaign rather than tested against an initial mechanistic theory.

Several limited initial claims were consistent with the observations:

- The catalysts were described as anonymous formulations with latent categorical activity profiles. Batches 1–4 were consistent with catalyst-category effects: Catalyst B gave the highest yield in that screen, while Catalyst C gave higher selectivity at lower conversion. This is support for categorical differences, but not definitive proof because each catalyst condition was run only once.
- Solvent effects were declared to be categorical benchmark effects rather than predictions from real-solvent properties. Batches 1 and 5–7 clearly differed by solvent category. Nothing in the results justified assigning those differences to physical concepts such as polarity or proticity, so K1 correctly avoided doing so.
- The instrument packet stated that measurements contained instrument noise plus a process proxy. HPLC and final assays usually agreed qualitatively, which supports their use as bounded observations. Their differences, especially the relatively large Batch 10 yield discrepancy, show why they should not be treated as exact replicates.
- The 0.35 safety limit was respected in all campaign batches. This confirms compliance, not a mechanistic safety law.

Several statements remained untested rather than supported. The anonymous catalyst identities, precise calibration behavior, detection-limit behavior, and mapping from hidden species to public channels could not be independently verified. Likewise, I found no evidence bearing on whether the benchmark solvent categories reproduce any real chemical system.

It is important to distinguish absence of contrary evidence from positive confirmation. K1 stated that the 340 K apparent rate constants provided “no positive evidence for severe catalyst deactivation.” That was deliberately weaker than claiming stable catalyst activity. The campaign lacked a catalyst-free control, catalyst-loading series, or direct catalyst-state measurement, so deactivation remained unresolved.

There was also evidence that challenged overly simple interpretations. K1 used an approximately first-order model, but the apparent constants increased from about 1.30×10^-4 s^-1 in Batch 10 to 1.49×10^-4 s^-1 in Batch 11. That spread is not large enough to refute the approximation, but it is counterevidence to an exact constant-rate law. Similarly, some HPLC/final differences were larger than the nominal channel noise alone might suggest. I acknowledged process uncertainty in K1, but I did not quantitatively revise the kinetic fit to include it.

2. Experiments that formed or changed my judgments

Batch 1 was the empirical anchor. It established that the selected Catalyst A/acetonitrile condition produced moderate conversion together with substantial byproduct, motivating at least two outcome channels rather than a target-only reaction.

Batches 2–4 materially changed the interpretation of catalyst action. A uniform catalyst multiplier would tend to preserve selectivity, but Catalyst B increased both yield and selectivity relative to Batch 1, while Catalyst C gave higher selectivity with lower conversion. This led to K1’s judgment that catalyst category probably changes productive and competing rates differently. The evidence was suggestive rather than conclusive because there were no replicates.

Batches 5–7 were similarly important for solvent effects. Batch 5, with water, combined lower conversion with markedly higher selectivity and lower byproduct and risk. This made a single solvent multiplier on total rate inadequate and supported pathway-specific solvent factors.

Batches 8 and 9 created the strongest evidence for thermal acceleration. Conversion rose from 0.1893 at the 300 K target to 0.4029 at 340 K and 0.6194 at 380 K for the same nominal duration. Their recorded temperature changes also forced me to distinguish requested setpoint from realized thermal history. The approximately 19 kJ mol^-1 apparent activation estimate in K1 came from these observations and was explicitly described as local and composite rather than elementary.

Batches 10 and 11 most strongly shaped the reaction-network interpretation. Conversion increased with time while selectivity declined and both byproduct and degradation warning rose. This caused me to reject a target-only R→P account and favor parallel target/byproduct formation plus possible secondary degradation. These batches did not uniquely establish that topology.

Batch 12 addressed quench timing. Its composition was close to Batch 1, while risk was slightly lower. That supported the limited judgment that a quench after 3600 s mainly changes thermal state and arrests further evolution; it did not establish the effect of earlier quenching.

Some design choices were not evidence-led. Catalyst A and acetonitrile were chosen as an initial benchmark without prior proof that they were optimal or mechanistically special. The 340 K, 3600 s baseline was likewise a pragmatic middle condition. Using the maximum per-batch reagent, solvent, and catalyst allocations made the 12-batch resource accounting simple, but it sacrificed any direct information about concentration or catalyst order. The later selection of Batch 9 was data-driven by its observed yield and score, whereas the initial choice to test 380 K was an unvalidated but reasonable guess that temperature would increase rate.

3. Principal competing mechanisms and what can be distinguished

K1 favored this family:

R→P; R→B; followed by P→D and/or B→D.

The most important competitor is a sequential network such as R→P→B or R→P→D, possibly accompanied by a smaller direct R→B channel. Both families can produce increasing conversion, declining selectivity, rising byproduct, and rising degradation warning.

A second competition concerns catalyst state. The time dependence could reflect ordinary substrate depletion plus product degradation, or it could include catalyst activation, inhibition, or deactivation. The near-constant apparent total rate argues against very strong deactivation but cannot exclude moderate or pathway-selective activity changes.

A third competition is intrinsic kinetics versus thermal-history effects. The apparent Arrhenius trend could arise from true temperature-dependent chemistry, differing heating ramps, temperature-dependent side reactions, or all three. Only aggregate temperature changes were observed, so the chemical and thermal submodels cannot be cleanly separated.

The experiments can distinguish several broad claims:

- A target-only model is inadequate because byproduct and degradation signals systematically accumulate.
- Temperature strongly affects total conversion.
- Solvent and catalyst category probably affect the balance of pathways, not just the common reaction clock.
- Longer hot residence worsens selectivity within the tested standard recipe.

They cannot determine whether byproduct is formed directly from reactant or secondarily from target, whether degradation consumes target or byproduct, or whether catalyst-state evolution is responsible for part of the time dependence. They also cannot separate catalyst–solvent interactions because only Catalyst A received the full solvent screen.

An alternative measurement explanation remains possible: some apparent channel changes could reflect state-dependent assay bias or process-proxy uncertainty. The consistency of yield≈conversion×selectivity and byproduct≈conversion×(1−selectivity) makes a real competing-channel interpretation plausible, but those algebraic relationships may also be partly imposed by the public observation mapping.

4. One additional complete experiment

If one additional legal complete experiment were available, I would run the standard Catalyst B/acetonitrile composition at the campaign concentrations, 340 K target, and 600 rpm, but use a within-vessel time course extending to 14,400 s. I would heat for 3600 s, take an HPLC measurement, continue to 7200 s and take another HPLC measurement, continue to 14,400 s, take a final pre-termination HPLC measurement, terminate, and obtain the required final assay.

This design is preferable to another isolated endpoint because it reduces between-batch variation and observes the same reacting inventory over time. The small HPLC sample losses would need to be accounted for.

Possible outcomes would change the interpretation as follows:

- If conversion continued to rise while target yield first rose and then fell, with byproduct rising, that would strongly favor sequential target loss such as P→B or P→D.
- If yield continued to rise but selectivity fell because byproduct accumulated alongside it, parallel R→P and R→B formation would remain the better minimal explanation.
- If conversion approached a plateau much earlier than first-order depletion predicts while substantial reactant remained, catalyst deactivation, reversible inhibition, or equilibrium limitation would become more credible.
- If all three HPLC observations followed one constant apparent rate and stable selectivity, much of the prior selectivity drift would have to be reassigned to between-batch or instrument variation.
- If the final assay disagreed systematically with the last HPLC observation, instrument/process-state effects would require explicit modeling before stronger mechanistic conclusions.

A catalyst-free control would also be valuable, but the proposed time course better targets the central unresolved topology and deactivation questions simultaneously.

5. Tradeoff between identifiability and operational score

The research goal emphasized explanation rather than pure score optimization, and the design reflected that. Batches 8 and 10 deliberately used conditions expected to give relatively low conversion and score because low-temperature and short-time anchors were necessary for estimating thermal and temporal response. Batch 11 used a long residence despite expected selectivity loss to test competing conversion and degradation. Batch 12 spent an entire batch on a matched quench comparison rather than on another optimization candidate. These were sacrifices in expected score for identifiability.

Conversely, identifiability was sacrificed in several ways. After Batch 9 produced the best result, I did not use later batches to map a dense neighborhood around it. No conditions between 340 and 380 K, and no times between 3600 and 7200 s, were tested. Therefore the recommendation was not locally optimized. Using full catalyst loading in every campaign batch also prevented identification of catalyst order, saturation, or uncatalyzed background.

The catalyst and solvent screens were efficient for broad comparison but lacked replication. With only 12 batches, I chose coverage of catalyst, solvent, temperature, time, and quench over replicate-based uncertainty estimation. That improved breadth but weakened causal confidence in the smaller catalyst differences.

The final recommendation itself prioritized the observed safe score and yield: Batch 9 was selected because it had the highest observed conversion, yield, and score while remaining below the safety limit. That selection did not alter K1’s mechanistic conclusions, but it did favor a high-throughput condition despite its elevated degradation warning.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts were underused. I relied almost entirely on processed estimates and did not perform a systematic comparison of peak areas, peak shapes, assignments, or spectral residuals across batches. Such a comparison might have revealed whether the degradation channel represented a distinct accumulating species or merely a correlated proxy.

The paired HPLC and final-assay results were also not fully exploited. Twelve pairs could have been used to estimate cross-instrument bias and excess process variance. Instead, K1 discussed selected agreements and discrepancies qualitatively. Batch 10, in particular, had HPLC yield 0.0777 and final yield 0.1036, a difference large enough to influence a short-time kinetic fit.

I also did not fit the safety-risk trajectory quantitatively, even though risk was observed after operations and varied with solvent, time, and temperature. Nor did I use the later-inferred exact score relationship during campaign planning. In the sealed predictions, I inferred the score equation from campaign outcomes, but uncertainty in score was still handled heuristically rather than propagated from a joint predictive distribution.

The least reliable blind predictions are Q06 and Q08. Both use 465 K for 7200 s, far above the campaign’s highest 380 K target. Their predicted near-complete conversion, severe selectivity loss, and high risk depend on extrapolating the Arrhenius-like model and degradation trend far outside K1’s stated range. Q02 and Q04 are also weak because 14,400 s doubles the longest campaign exposure and combines that extrapolation with 410 K. Q04 and Q08 additionally use the high catalyst loading, which was never studied.

Q01 and Q03 are somewhat less extreme in duration but still combine 410 K with untested catalyst concentrations. Q09 and Q10 use a catalyst concentration close to the campaign concentration and are therefore better grounded, but their 410 K/7200 s condition remains an extrapolation. The Q09–Q10 quench difference is especially uncertain because the only campaign quench comparison was at 340 K after 3600 s.

Several intervals were probably too narrow. In Q04 and Q08 I assigned conversion intervals of 0.96–1.00 despite simultaneously acknowledging large uncertainty in catalyst loading, thermal history, and degradation at extreme conditions. The saturation boundary made the interval look artificially confident. The low score intervals for Q06 and Q08 may also be too narrow because a different high-temperature selectivity law could move the score materially above the clipping floor. Safety-risk intervals at 465 K may understate uncertainty in thermal runaway or risk accumulation because the campaign never approached that temperature.

This is partly inconsistent with K1’s explicit scope statement, which limited support to fixed catalyst loading, 300–380 K requested temperature, and 1200–7200 s. The prediction rationale acknowledged extrapolation and widened intervals, but not always enough. A more internally consistent treatment would have used heavier-tailed or substantially wider intervals for every query outside those bounds, particularly when multiple extrapolations were combined.

The new queries also changed addition order and used a smaller, more concentrated recipe at 400 rpm. My prediction model concentrated mainly on catalyst concentration and temperature and did not explicitly represent order-of-addition, scale-dependent thermal response, or the change from 600 to 400 rpm. K1 had already identified concentration and stirring as unmeasured factors, so failing to give them stronger uncertainty weight was another weakness.

7. Limitations of the sealed recommendation

Batch 9 is the sample-internal winner, not a proven optimum. Its final values—conversion 0.6194, yield 0.3523, selectivity 0.5611, score 0.1583, and risk 0.1885—were the best observed throughput result among the 12 chosen conditions. That establishes only that it outperformed the other sampled endpoints in this single campaign realization.

It was run once. Therefore its advantage could contain batch variation or favorable assay noise. It also used one specific material combination: Catalyst A, acetonitrile, fixed concentrations, 600 rpm, a 380 K target, and 3600 s. The recorded temperature change was about 75.22 K rather than an exact realization of the nominal setpoint, so even reproducing the action list may not reproduce an identical thermal path.

Repeatability should be tested with independent replicates of Batch 9, including replicate final assays where allowed and consistent recording of the realized thermal trajectory. A matched Batch 1 replicate series would provide a useful reference for estimating between-batch variance.

Local robustness should be tested with a neighborhood design around Batch 9: temperatures such as 365, 380, and 395 K; times such as 2700, 3600, and 4500 s; and modest catalyst-loading changes. This would reveal whether the observed maximum lies on a broad plateau or a narrow tradeoff boundary. Quenching at several nearby times would test whether the high-temperature target yield can be retained while reducing degradation and risk.

Cross-material robustness requires repeating that neighborhood with at least Catalyst B and the other solvent categories. The catalyst and solvent screens show that pathway balance is material-dependent, so there is no basis for assuming Batch 9’s operating point transfers unchanged. Catalyst–solvent interactions should be tested directly rather than inferred from separate one-factor screens.

Finally, cross-world generalization would require independent worlds or seeds with the same public contract, followed by external validation of both rank ordering and calibrated prediction intervals. Until those tests are performed, the correct statement is: Batch 9 was the highest observed safe-scoring batch in this sampled campaign. It is not: Batch 9 has been proven globally optimal, universally robust, or transferable to other materials or worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 125.6 | none | 0 |
| Q | yes | 0 | 134.5 | none | 0 |
| K2 | yes | 0 | 118.3 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
