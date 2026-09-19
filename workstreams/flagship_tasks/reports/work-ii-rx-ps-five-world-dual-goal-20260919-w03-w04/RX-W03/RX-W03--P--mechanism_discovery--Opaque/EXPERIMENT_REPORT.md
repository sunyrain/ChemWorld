# RX-W03--P--mechanism_discovery--Opaque

## Run summary

- World: `RX-W03`
- Locus: `P`
- Goal: `mechanism_discovery`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `103`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `posttest-repair-v3`
- Recovery version: `unknown`
- Repaired stages: `Q, K2`
- Source experiments rerun: `False`
- Original source thread reused: `True`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `11`
- Rationale: Batch 11 gave the highest observed score and target yield while remaining below the safety limit; its 380 K boundary, 1800 s total heating, prompt quench, and Catalyst B also support the observed kinetic optimum before longer heating increased byproduct and degradation.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm → 350 K x 3600 s @ 600 rpm | no | 0.4854 | 0.5882 | 0.8187 | 0.3314 | 0.1023 | 0.1839 | 0.2403 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | yes | 0.3509 | 0.6565 | 0.5633 | 0.1874 | 0.0303 | 0.1579 | 0.1897 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 1800 s @ 600 rpm → 350 K x 1800 s @ 600 rpm | yes | 0.6188 | 0.7060 | 0.8693 | 0.2546 | 0.1778 | 0.1920 | 0.3246 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 1800 s @ 600 rpm → 350 K x 1800 s @ 600 rpm | yes | 0.5125 | 0.7296 | 0.7149 | 0.2038 | 0.0579 | 0.1754 | 0.2800 |
| 5 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 1800 s @ 600 rpm → 350 K x 1800 s @ 600 rpm | yes | 0.5013 | 0.7646 | 0.6520 | 0.1663 | 0.0531 | 0.1726 | 0.2792 |
| 6 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | yes | 0.5188 | 0.8076 | 0.6344 | 0.1145 | 0.0567 | 0.1308 | 0.3140 |
| 7 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | yes | 0.5591 | 0.7641 | 0.7359 | 0.1918 | 0.0830 | 0.1614 | 0.3156 |
| 8 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | yes | 0.4659 | 0.6103 | 0.7745 | 0.3082 | 0.1335 | 0.1891 | 0.2313 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 320 K x 1800 s @ 600 rpm → 320 K x 1800 s @ 600 rpm | yes | 0.4901 | 0.7623 | 0.6531 | 0.1594 | 0.0922 | 0.1717 | 0.2747 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 1800 s @ 600 rpm → 380 K x 1800 s @ 600 rpm | yes | 0.6189 | 0.6328 | 0.9705 | 0.3648 | 0.2894 | 0.2032 | 0.3114 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 900 s @ 600 rpm → 380 K x 900 s @ 600 rpm | yes | 0.6453 | 0.7972 | 0.7921 | 0.1551 | 0.1019 | 0.1916 | 0.3504 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.002500 mol) | 380 K x 900 s @ 600 rpm → 380 K x 900 s @ 600 rpm | yes | 0.4694 | 0.7757 | 0.6138 | 0.1337 | 0.0628 | 0.1717 | 0.2658 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `8`.

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
      "catalyst": 0,
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
      "duration_s": 3600,
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
    "byproduct_signal": 0.3313674032688141,
    "conversion": 0.8186890482902527,
    "cost": 1.0,
    "degradation_warning": 0.1023145243525505,
    "safety_risk": 0.18385985493659973,
    "score": 0.24034328758716583,
    "selectivity": 0.5881739258766174,
    "virtual_spectrum_summary": 0.22829359769821167,
    "yield": 0.4854195713996887
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
      "operation": "add_solvent",
      "solvent": 2,
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
  "end_step": 16,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.18739517033100128,
    "conversion": 0.5632662177085876,
    "cost": 1.0,
    "degradation_warning": 0.03032624162733555,
    "safety_risk": 0.15792322158813477,
    "score": 0.18974418938159943,
    "selectivity": 0.6564909219741821,
    "virtual_spectrum_summary": 0.11671414971351624,
    "yield": 0.35090070962905884
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `25`.

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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 25,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.25461381673812866,
    "conversion": 0.8693044781684875,
    "cost": 1.0,
    "degradation_warning": 0.1778077632188797,
    "safety_risk": 0.19201233983039856,
    "score": 0.3245568573474884,
    "selectivity": 0.706048846244812,
    "virtual_spectrum_summary": 0.2200510948896408,
    "yield": 0.6187993884086609
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `34`.

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
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 34,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2037682682275772,
    "conversion": 0.714941143989563,
    "cost": 1.0,
    "degradation_warning": 0.05794716253876686,
    "safety_risk": 0.17542245984077454,
    "score": 0.27995678782463074,
    "selectivity": 0.7295631766319275,
    "virtual_spectrum_summary": 0.13814876973628998,
    "yield": 0.5125299692153931
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `43`.

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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 43,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.16631625592708588,
    "conversion": 0.6519595980644226,
    "cost": 1.0,
    "degradation_warning": 0.05305597558617592,
    "safety_risk": 0.17260079085826874,
    "score": 0.2792040705680847,
    "selectivity": 0.7646327018737793,
    "virtual_spectrum_summary": 0.11534912884235382,
    "yield": 0.5013007521629333
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `51`.

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
  "end_step": 51,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.11452102661132812,
    "conversion": 0.6344358325004578,
    "cost": 1.0,
    "degradation_warning": 0.0567023940384388,
    "safety_risk": 0.13079240918159485,
    "score": 0.3140217363834381,
    "selectivity": 0.8075937628746033,
    "virtual_spectrum_summary": 0.08850264549255371,
    "yield": 0.5188407897949219
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `59`.

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
  "end_step": 59,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.19183249771595,
    "conversion": 0.7359191179275513,
    "cost": 1.0,
    "degradation_warning": 0.08296041190624237,
    "safety_risk": 0.16142907738685608,
    "score": 0.31562718749046326,
    "selectivity": 0.7641448974609375,
    "virtual_spectrum_summary": 0.14284005761146545,
    "yield": 0.5591053366661072
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `67`.

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
  "end_step": 67,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3081938922405243,
    "conversion": 0.7745090126991272,
    "cost": 1.0,
    "degradation_warning": 0.13347087800502777,
    "safety_risk": 0.18905970454216003,
    "score": 0.23133030533790588,
    "selectivity": 0.6103426814079285,
    "virtual_spectrum_summary": 0.22956854104995728,
    "yield": 0.46592649817466736
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `76`.

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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 320
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 320
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
  "end_step": 76,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.15939287841320038,
    "conversion": 0.653147280216217,
    "cost": 1.0,
    "degradation_warning": 0.0921579971909523,
    "safety_risk": 0.1716959923505783,
    "score": 0.27465906739234924,
    "selectivity": 0.7622930407524109,
    "virtual_spectrum_summary": 0.12913717329502106,
    "yield": 0.490085631608963
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `85`.

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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
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
  "end_step": 85,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3647531270980835,
    "conversion": 0.9704862833023071,
    "cost": 1.0,
    "degradation_warning": 0.28942322731018066,
    "safety_risk": 0.20323698222637177,
    "score": 0.3113531172275543,
    "selectivity": 0.6327643394470215,
    "virtual_spectrum_summary": 0.3308546841144562,
    "yield": 0.6189250349998474
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `94`.

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
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
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
  "end_step": 94,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.15509550273418427,
    "conversion": 0.7920975685119629,
    "cost": 1.0,
    "degradation_warning": 0.10186795890331268,
    "safety_risk": 0.19157640635967255,
    "score": 0.35043346881866455,
    "selectivity": 0.7971925735473633,
    "virtual_spectrum_summary": 0.13114310801029205,
    "yield": 0.6453373432159424
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `103`.

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
      "catalyst_amount_mol": 0.0025,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
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
  "end_step": 103,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.13373027741909027,
    "conversion": 0.6138455867767334,
    "cost": 1.0,
    "degradation_warning": 0.06276357173919678,
    "safety_risk": 0.17173995077610016,
    "score": 0.26577624678611755,
    "selectivity": 0.7756693363189697,
    "virtual_spectrum_summary": 0.1017952561378479,
    "yield": 0.4693933129310608
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

# Mechanistic report

## 1. Scope and evidence base

This report describes the bounded synthetic reaction world studied in 12 completed batches. The reagent and catalysts are anonymous benchmark materials, and the solvent effects are calibrated categorical effects; therefore, I do not assign a real chemical identity or named molecular mechanism. My claims concern the observed benchmark system only.

All batches used 0.040 mol reagent and 0.080 L solvent. Except for batch 12, they used 0.005 mol catalyst. Reported values are processed instrument estimates and therefore include instrument and process uncertainty. Intermediate values came from HPLC, while terminal values came from the final assay, so small pre-quench versus post-quench differences should not be interpreted as exact chemical changes.

## 2. Proposed process structure

The simplest account consistent with the observations is a catalyzed network with productive and competing conversion, followed by slower loss of accumulated target:

R --kP--> P
R --kB--> B
P --kD--> D and/or secondary byproducts

Here R is the public reactant, P the target, B primary competing product, and D degraded or secondary material. Catalyst identity and loading, solvent, temperature, and thermal history change the effective rate constants.

A useful phenomenological model is:

dR/dt = -a(t)[kP(T,s,c) + kB(T,s,c)]R

dP/dt = a(t)kP(T,s,c)R - kD(T,s,c)P

dB/dt = a(t)kB(T,s,c)R + alpha kD(T,s,c)P

da/dt = -kdeact(T,s,c)a

where c denotes catalyst identity, s solvent, and a(t) effective catalytic activity. Arrhenius-like temperature factors are plausible:

ki(T,s,c) = Ai,s,c exp[-Ei/(RT)].

This is not a uniquely fitted law. In particular, substrate depletion, catalyst deactivation, and product degradation cannot be separated cleanly with the available measurements. The data do, however, require at least two effective kinetic tendencies: productive formation and an increasingly important competing/degradation pathway at high thermal exposure.

For most final assays, yield was close to conversion multiplied by selectivity. For example, batch 11 gave conversion 0.7921 and selectivity 0.7972, whose product is approximately 0.631, close to the measured yield 0.6453. Thus conversion and branching selectivity provide a reasonable first-order decomposition of target yield, with remaining discrepancies attributable to calibration, noise, and the benchmark observation mapping.

## 3. Thermal history rather than nominal temperature alone

The vessel did not jump instantly to the requested temperature. At a 350 K target, the first 3600 s heating operation in batch 1 increased temperature by 48.71 K, whereas its second 3600 s segment increased it by only 1.48 K. At 380 K, batch 10 rose by 74.88 K in the first 1800 s and another 4.58 K in the second. In batch 11, two 900 s segments produced increases of 72.89 K and 6.63 K. At 320 K, batch 9 rose by 20.97 K in the first 1800 s and changed by only -0.02 K in the second.

Consequently, reaction progress should be related to the integral of temperature-dependent rates over the actual trajectory, not simply to requested temperature multiplied by elapsed time. A suitable exposure variable would be

Theta_i = integral exp[-Ei/(R Tactual(t))] dt.

Different reactions may have different activation energies, so increasing temperature can change selectivity as well as accelerate total conversion.

## 4. Evidence for target formation followed by competing conversion

Batch 1 used Catalyst A in acetonitrile at a 350 K target. After 3600 s, HPLC measured conversion 0.5510, yield 0.3746, selectivity 0.6731, and byproduct signal 0.1971. After another 3600 s without a prompt quench, the final assay measured conversion 0.8187 but yield only 0.4854; selectivity fell to 0.5882, byproduct signal rose to 0.3314, and degradation warning reached 0.1023.

Thus additional heating converted much more reactant, but a diminishing fraction became retained target. This observation caused me to reject a single irreversible R-to-P model. It supports parallel byproduct formation and possibly subsequent target degradation.

The same pattern was stronger with Catalyst B. In batch 10 at 380 K, the 1800 s HPLC measurement already showed conversion 0.7811, yield 0.6432, selectivity 0.7812, and byproduct signal 0.1438. Continuing to 3600 s raised terminal conversion to 0.9705, but terminal yield was only 0.6189. Selectivity fell to 0.6328, byproduct signal rose to 0.3648, and degradation warning rose to 0.2894. The target therefore has a finite thermal optimum: near-complete conversion is not the same as maximum target yield.

Batch 11 directly targeted the shorter high-temperature window. At 900 s and 380 K, HPLC measured conversion 0.4827, yield 0.4186, selectivity 0.8689, and byproduct signal 0.0906. After a second 900 s segment followed promptly by quench, the final assay measured conversion 0.7921, yield 0.6453, selectivity 0.7972, byproduct signal 0.1551, and degradation warning 0.1019. Its score, 0.35043, was the highest observed. Although batch 10 and batch 11 used different assays at the 1800 s point, their results agree that roughly 1800 s at the 380 K boundary is near the productive maximum and that another 1800 s mainly increases undesirable conversion.

## 5. Catalyst identity

Catalyst identity substantially changed both rate and selectivity. Batches 3–5 used acetonitrile, a 350 K target, 0.005 mol catalyst, and measurements after 1800 and 3600 s.

- Catalyst B, batch 3: at 1800 s, conversion 0.6038, yield 0.4906, selectivity 0.8254, and byproduct 0.0952. At 3600 s, the final values were conversion 0.8693, yield 0.6188, selectivity 0.7060, byproduct 0.2546, and degradation warning 0.1778.
- Catalyst C, batch 4: at 1800 s, conversion 0.4441, yield 0.3476, selectivity 0.7295, and byproduct 0.1242. Final values were conversion 0.7149, yield 0.5125, selectivity 0.7296, byproduct 0.2038, and degradation warning 0.0579.
- Catalyst D, batch 5: at 1800 s, conversion 0.4038, yield 0.3341, selectivity 0.8295, and byproduct 0.0634. Final values were conversion 0.6520, yield 0.5013, selectivity 0.7646, byproduct 0.1663, and degradation warning 0.0531.

Catalyst B is the fastest productive catalyst and produced the highest yield under these common conditions, but prolonged exposure also produced the greatest degradation warning. Catalyst D was slower but initially highly selective and cleaner. Catalyst C was intermediate in rate but less selective at the early point. Catalyst A was slower and less selective than B under comparable 350 K conditions: batch 2 at 3600 s gave terminal conversion 0.5633, yield 0.3509, and selectivity 0.6565.

I therefore model catalyst identity as changing both kP and kB, not merely multiplying all rates by one activity factor. The rise in degradation warning for Catalyst B could also mean that it accelerates secondary target loss, but it could instead be an indirect consequence of producing more target earlier and exposing that target to heat for longer. Those explanations are not separable here.

## 6. Catalyst loading

Batch 12 tested 0.0025 mol Catalyst B, half the usual loading, in acetonitrile at 380 K. At 900 s it gave conversion 0.3079 and yield 0.2515, compared with batch 11 at full loading, which gave conversion 0.4827 and yield 0.4186. After 1800 s, batch 12 gave conversion 0.6138, yield 0.4694, selectivity 0.7757, byproduct 0.1337, and degradation warning 0.0628; batch 11 at full loading gave conversion 0.7921 and yield 0.6453.

Thus the reaction rate depends strongly on catalyst amount. The effect is substantial but not demonstrably linear. A rough model could use initial activity proportional to catalyst amount, a(0) proportional to ncat, possibly with saturation at higher loading. Only two loadings were tested, and there was no catalyst-free control, so the existence and magnitude of an uncatalyzed background reaction remain unidentified.

## 7. Solvent coupling

Batches 3 and 6–8 compared Catalyst B at a 350 K target and 3600 s across solvents. The final assays showed:

- Water, batch 6: conversion 0.6344, yield 0.5188, selectivity 0.8076, byproduct 0.1145, degradation warning 0.0567, risk 0.1308.
- Ethanol, batch 7: conversion 0.7359, yield 0.5591, selectivity 0.7641, byproduct 0.1918, degradation warning 0.0830, risk 0.1614.
- Acetonitrile, batch 3: conversion 0.8693, yield 0.6188, selectivity 0.7060, byproduct 0.2546, degradation warning 0.1778, risk 0.1920.
- Toluene, batch 8: conversion 0.7745, yield 0.4659, selectivity 0.6103, byproduct 0.3082, degradation warning 0.1335, risk 0.1891.

The solvent therefore affects both total rate and branching. Water was slower but cleanest and most selective. Ethanol offered an intermediate rate/selectivity compromise. Acetonitrile gave the highest conversion and target yield in this 3600 s comparison, but also greater secondary damage. Toluene was especially unfavorable for selectivity: relatively high conversion produced poor yield and the largest byproduct signal among the solvent comparison.

These are categorical benchmark effects and should not be rationalized as real polarity, proticity, or solubility predictions. In the phenomenological model, solvent-specific multipliers are needed separately for productive formation, competing conversion, and degradation:

kP = mP(s)kP,reference,
kB = mB(s)kB,reference,
kD = mD(s)kD,reference.

A single solvent multiplier on overall rate would not reproduce the observed selectivity ordering.

## 8. Temperature dependence and the optimum window

With Catalyst B in acetonitrile:

- Batch 9 at 320 K: after 1800 s, conversion 0.3798, yield 0.3351, selectivity 0.8229, and byproduct 0.0442. At 3600 s, terminal conversion was 0.6531, yield 0.4901, selectivity 0.7623, byproduct 0.1594, and degradation warning 0.0922.
- Batch 3 at 350 K: after 1800 s, conversion 0.6038 and yield 0.4906; at 3600 s, conversion 0.8693 and yield 0.6188, with degradation warning 0.1778.
- Batch 10 at 380 K: after 1800 s, conversion 0.7811 and yield 0.6432; at 3600 s, conversion 0.9705 but yield 0.6189, with degradation warning 0.2894.

Higher temperature strongly accelerates conversion and early target formation. However, the benefit saturates because competing and degradation pathways accelerate too. The data are compatible with the undesirable pathways having equal or greater effective temperature sensitivity than target formation once substantial target has accumulated. Quantitative activation energies cannot be estimated reliably from only three requested temperatures, transient heating profiles, and non-identical assay timing.

The optimum is therefore a coupled temperature-time boundary rather than a universal best temperature. In this tested design space, 380 K for approximately 1800 s with prompt quench was superior to either 320 K for 3600 s or 380 K for 3600 s.

## 9. Quench and termination timing

The quench rapidly reduced temperature and risk. In batch 2, quenching after the 350 K heat step lowered temperature by 45 K, consumed about 56.1 s of process time, and reduced reported risk by 0.00676 before termination. The HPLC result immediately before quench was conversion 0.5502, yield 0.3698, selectivity 0.6617, and byproduct 0.1979. The final assay after quench measured conversion 0.5633, yield 0.3509, selectivity 0.6565, byproduct 0.1874, and degradation warning 0.0303.

Those changes are small relative to the use of different instruments and their stated uncertainties, so I do not claim that quench itself chemically increased or decreased any particular species. Its defensible role is to sharply reduce continuing thermal exposure. The contrast between batch 11, quenched at 1800 s, and batch 10, heated for another 1800 s, demonstrates why termination timing matters even though it does not isolate the microscopic quench chemistry.

Batch 1 lacked a prompt quench after 7200 s and accumulated much more byproduct than its 3600 s intermediate state. Most later batches were quenched promptly, so the independent effects of quench chemistry and shorter heating are confounded. A competing explanation is that termination alone would have stopped the chemistry equally well; that was not tested as a matched pair.

## 10. Safety coupling

All tested terminal risks remained below the specified 0.35 limit. Risk depended on solvent choice, temperature, duration, and quench. At otherwise comparable 350 K conditions, water in batch 6 ended at risk 0.1308, ethanol in batch 7 at 0.1614, acetonitrile in batch 3 at 0.1920, and toluene in batch 8 at 0.1891. The 380 K, 3600 s batch 10 reached a higher pre-quench risk of about 0.2389 and ended at 0.2032. The optimized shorter batch 11 ended at 0.1916.

Risk is therefore coupled to thermal exposure but is not simply conversion. Solvent-dependent baseline contributions and cooling during quench are also important. Because risk was reported as an aggregate metric, its physical components cannot be identified.

## 11. Predictive interpretation within the observed domain

Within 0.040 mol reagent, approximately 0.080 L solvent, 0.0025–0.005 mol Catalyst B, 320–380 K requested temperature, and 900–3600 s heating, I would predict behavior using the following pseudocode:

1. Propagate actual vessel temperature toward the requested set point rather than assuming an instantaneous step.
2. Compute temperature- and solvent-dependent productive, competing, and degradation rates.
3. Scale initial catalytic activity with catalyst identity and loading.
4. Integrate R, P, B, and D over time.
5. Quench when marginal target formation becomes smaller than marginal target loss/byproduct formation.

For Catalyst B in acetonitrile, the observed optimum lies near 380 K and 1800 s. Heating much longer should increase conversion toward unity while reducing selectivity and increasing byproduct and degradation. Reducing catalyst loading should slow both conversion and target formation, requiring longer exposure but potentially reducing degradation at a fixed time. Water or ethanol should improve selectivity relative to acetonitrile but give lower conversion at the same 350 K/3600 s schedule. Toluene should remain comparatively byproduct-prone.

These statements are interpolation-level conclusions. Predictions outside the studied temperature, time, loading, concentration, or solvent ranges would be extrapolations and are substantially less reliable.

## 12. Unidentified factors and competing explanations

Several important quantities remain unidentified:

- No catalyst-free batch was run, so background kinetics are unknown.
- Only one reagent concentration and nearly one catalyst loading were used; reaction orders cannot be established.
- Stirring was fixed at 600 rpm, so transport limitation was not tested.
- Solvent volume was fixed, preventing separation of dilution from solvent identity.
- Catalyst deactivation was not measured directly. Apparent slowing can also arise from reagent depletion, approach to a reversible state, or product inhibition.
- Product loss was inferred from yield/selectivity behavior and degradation warning, not from direct tracking of a purified target. A parallel late-forming byproduct could mimic sequential P-to-D degradation.
- Reversibility is possible. A reversible R-to-P step plus an irreversible byproduct sink could reproduce some plateaus without catalyst deactivation.
- Quench chemistry was not isolated from cooling and termination timing.
- Exact repeat batches were limited. Batch 10 and batch 11 provide a useful near-comparison at 1800 s, but their relevant measurements used HPLC and final assay respectively.
- The processed signals are synthetic proxies with known noise, and small cross-instrument differences should not be overinterpreted.
- Only aggregate temperature changes were observed, not a complete high-resolution temperature trace.

The strongest supported account is therefore not a unique molecular mechanism but a kinetic process model: catalyst-, solvent-, and temperature-dependent target formation competes with byproduct formation; prolonged high-temperature exposure increasingly favors undesirable channels and/or destroys accumulated target; actual heat-up dynamics and prompt quenching determine the effective exposure. Catalyst B provides the greatest productive rate, and the best tested balance was batch 11: Catalyst B, acetonitrile, 380 K requested temperature, 1800 s total heating, and prompt quench.

## Q — Blind predictions

### Overall rationale

The predictions extend the campaign model of parallel target and byproduct formation plus heat-dependent secondary target loss. They are anchored primarily to Catalyst B/acetonitrile batches 3, 9, 10, 11, and 12. The new batches have a higher reagent concentration, higher catalyst concentration, higher catalyst-to-reagent ratio, and lower stirring speed than the campaign batches; temperatures above 380 K are also extrapolations. Accordingly, uncertainty expands with temperature and duration, especially for Q04, Q06–Q08, and Q12. Quench pairs are predicted to differ mainly in safety risk because the campaign did not establish a large, instrument-resolved compositional effect of quenching itself.

### Q01

The higher catalyst-to-reagent ratio and 420 K exposure should drive nearly complete conversion, but 3300 s is expected to move well beyond the target-yield maximum observed near 380 K and 1800 s. The lack of quenching leaves comparatively high terminal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5700 | 0.3800 | 0.7600 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.3400 | 0.2500 | 0.4700 |
| score | 0.1100 | 0.0300 | 0.2300 |
| selectivity | 0.3700 | 0.2200 | 0.5500 |
| yield | 0.3600 | 0.2000 | 0.5300 |

### Q02

Chemistry at the end of heating should resemble Q01 because quenching occurs only afterward. Quenching is predicted mainly to reduce thermal risk and prevent residual post-heating evolution, with only a small possible improvement in retained target.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3600 | 0.7500 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.2700 | 0.1800 | 0.3900 |
| score | 0.1400 | 0.0400 | 0.2700 |
| selectivity | 0.3900 | 0.2300 | 0.5700 |
| yield | 0.3700 | 0.2100 | 0.5500 |

### Q03

At 390 K, the elevated catalyst concentration should still give very high conversion in 3300 s, while the lower temperature should preserve more target than Q01. This is a moderate extrapolation beyond the 380 K observations.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4100 | 0.2500 | 0.5900 |
| conversion | 0.9850 | 0.9200 | 1.0000 |
| safety_risk | 0.2400 | 0.1700 | 0.3400 |
| score | 0.2400 | 0.1100 | 0.3700 |
| selectivity | 0.5500 | 0.3900 | 0.7000 |
| yield | 0.5400 | 0.3700 | 0.6900 |

### Q04

A 450 K, 3300 s treatment is far outside the experimentally supported temperature range. I expect essentially complete conversion but extensive competing conversion or target degradation, together with a material chance of exceeding the stated safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7300 | 0.5100 | 0.9100 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.4800 | 0.3400 | 0.6500 |
| score | 0.0300 | 0.0000 | 0.1100 |
| selectivity | 0.1800 | 0.0500 | 0.3600 |
| yield | 0.1700 | 0.0400 | 0.3500 |

### Q05

Shortening the 420 K exposure to 1500 s should place this batch closer to the kinetic target maximum. Conversion should already be high because the catalyst concentration and catalyst-to-reagent ratio exceed those in the campaign, but selectivity loss should be less advanced than in Q01.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1500 | 0.4500 |
| conversion | 0.9600 | 0.8500 | 1.0000 |
| safety_risk | 0.2400 | 0.1600 | 0.3500 |
| score | 0.3300 | 0.1800 | 0.4600 |
| selectivity | 0.6500 | 0.4900 | 0.7900 |
| yield | 0.6200 | 0.4500 | 0.7600 |

### Q06

The prolonged 420 K exposure should exhaust reactant and then strongly favor secondary conversion. The prediction is uncertain because the campaign did not directly study this temperature or duration, but the deterioration from batch 11 to batch 10 supports a pronounced overreaction penalty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7700 | 0.5700 | 0.9300 |
| conversion | 1.0000 | 0.9850 | 1.0000 |
| safety_risk | 0.4300 | 0.3100 | 0.5900 |
| score | 0.0250 | 0.0000 | 0.0900 |
| selectivity | 0.2100 | 0.0600 | 0.3900 |
| yield | 0.2000 | 0.0500 | 0.3800 |

### Q07

The initial 390 K segment should accumulate target before the 450 K segment. That accumulated target is then exposed to severe secondary conversion, so final conversion should be nearly complete but retained yield and selectivity low.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6600 | 0.4400 | 0.8500 |
| conversion | 0.9970 | 0.9600 | 1.0000 |
| safety_risk | 0.4000 | 0.2800 | 0.5500 |
| score | 0.0650 | 0.0100 | 0.1700 |
| selectivity | 0.3100 | 0.1400 | 0.5000 |
| yield | 0.3000 | 0.1300 | 0.4900 |

### Q08

Starting at 450 K should create rapid conversion and substantial byproduct formation. The following 390 K segment may not immediately erase the high-temperature thermal state, so I predict slightly worse retention than for Q07, although the ordering effect is poorly identified and the intervals overlap broadly.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7100 | 0.4900 | 0.8900 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.4200 | 0.2900 | 0.5800 |
| score | 0.0450 | 0.0050 | 0.1400 |
| selectivity | 0.2600 | 0.1000 | 0.4500 |
| yield | 0.2500 | 0.0900 | 0.4400 |

### Q09

At 440 K, 1500 s should be sufficient for very high conversion but should pass the selectivity optimum more severely than Q05. Absence of quenching gives a relatively high safety-risk estimate.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4400 | 0.2500 | 0.6400 |
| conversion | 0.9850 | 0.9100 | 1.0000 |
| safety_risk | 0.3100 | 0.2100 | 0.4400 |
| score | 0.1900 | 0.0700 | 0.3400 |
| selectivity | 0.4800 | 0.3000 | 0.6600 |
| yield | 0.4600 | 0.2800 | 0.6400 |

### Q10

The chemical endpoint should be close to Q09, while quenching should lower terminal risk and prevent additional thermal evolution. The score is therefore predicted to improve chiefly through the safer closeout rather than a large composition change.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2400 | 0.6300 |
| conversion | 0.9850 | 0.9100 | 1.0000 |
| safety_risk | 0.2300 | 0.1400 | 0.3500 |
| score | 0.2300 | 0.0900 | 0.3800 |
| selectivity | 0.4900 | 0.3100 | 0.6700 |
| yield | 0.4700 | 0.2900 | 0.6500 |

### Q11

Although 370 K is comparatively mild, 5700 s at the higher catalyst concentration should produce near-complete conversion and substantial cumulative secondary loss. The outcome is expected to resemble an overextended moderate-temperature run rather than the 1800 s optimum.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4800 | 0.3000 | 0.6700 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.2600 | 0.1800 | 0.3700 |
| score | 0.1700 | 0.0700 | 0.3000 |
| selectivity | 0.4800 | 0.3200 | 0.6400 |
| yield | 0.4700 | 0.3000 | 0.6300 |

### Q12

This is the most extreme extrapolation: 460 K for 6300 s without quenching. Reactant conversion should be complete, while target retention is expected to be very poor and safety risk very high. The wide intervals acknowledge that neither the high-temperature degradation ceiling nor risk saturation was measured.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8500 | 0.6200 | 0.9800 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.7400 | 0.5000 | 0.9500 |
| score | 0.0020 | 0.0000 | 0.0250 |
| selectivity | 0.0500 | 0.0000 | 0.1800 |
| yield | 0.0400 | 0.0000 | 0.1600 |

## K2 — Retrospective analysis

## 1. Initial information: supported, contradicted, and untested claims

The initial packet contained almost no substantive kinetic or mechanistic prior. It explicitly said that no task-specific material dossier was supplied, that the catalysts were anonymous benchmark formulations, and that solvent effects were categorical benchmark effects rather than predictions from real solvent-property correlations. Thus there was no initial claim such as “Catalyst B is best,” “the reaction is first order,” or “acetonitrile should be optimal” to confirm or refute.

Several structural statements in the packet were respected but not experimentally tested. I treated the public species labels as proxies and did not infer a named synthesis or molecular catalyst. The results supported the practical importance of catalyst and solvent categories, but they did not validate any real-chemical explanation based on polarity, proticity, or catalyst identity. Likewise, the stated safety limit of 0.35 was not a mechanistic hypothesis. All campaign batches stayed below it, but that is only an absence of a violation in the tested domain, not proof that the broader system is safe.

The main empirical claims eventually made in K1 were supported as follows:

- K1’s claim that target formation competes with undesirable conversion was supported most clearly by batches 1 and 10. In batch 1, extending heating from 3600 to 7200 s raised conversion from 0.5510 to 0.8187 while selectivity fell from 0.6731 to 0.5882 and byproduct signal rose from 0.1971 to 0.3314. In batch 10, extending the 380 K treatment from 1800 to 3600 s raised conversion from 0.7811 to 0.9705 but did not improve yield; selectivity fell to 0.6328 and degradation warning rose to 0.2894.
- K1’s claim that catalyst identity affects branching rather than merely multiplying one common rate was supported by batches 3–5. Catalyst B was faster and higher-yielding, whereas Catalyst D was slower but initially cleaner and highly selective.
- K1’s solvent-specific branching claim was supported by batches 6–8: water was slower and cleaner, ethanol intermediate, and toluene comparatively byproduct-prone. A single solvent multiplier on total conversion could not readily explain those differences.
- K1’s conclusion that the 380 K/1800 s boundary was preferable to longer heating was supported by the contrast between batches 10 and 11.

Some K1 statements were plausible interpretations rather than uniquely demonstrated mechanisms. In particular, the proposed sequential P-to-D loss was not proven. The same evidence can be explained by a late-forming parallel byproduct, time-varying catalyst selectivity, or product inhibition. K1 did acknowledge this underdetermination, but its equations may visually suggest more mechanistic certainty than the data warrant.

There was no clear initial mechanistic claim for which counterevidence appeared and was knowingly ignored. There were, however, implicit working assumptions that were weakened during the campaign. I initially used acetonitrile, Catalyst A, maximum loading, and 350 K as a convenient baseline without evidence that this combination was privileged. Batch 3 showed that Catalyst B was materially better, while batches 6 and 7 showed that water and ethanol could provide cleaner, safer outcomes. I adapted subsequent experiments, so this was not counterevidence left wholly uncorrected. The remaining uncorrected assumption was that 600 rpm avoided transport limitations; stirring was never varied.

## 2. Experiments that actually formed or changed the interpretation

Batch 1 was the main hypothesis-forming experiment. Its intermediate and final measurements showed that additional heating increased conversion much more than retained target. Before that result, a simple monotonic R-to-P picture remained viable. After it, I began treating time as a selectivity variable and considered parallel or sequential undesirable channels.

Batch 2 was intended to provide a shorter, quenched comparison with batch 1. It supported the practical value of stopping earlier, but it was not a clean quench experiment because duration and quench status both differed from batch 1, and the pre-quench and final measurements used different instruments.

Batches 3–5 genuinely changed the catalyst interpretation. Batch 3 established Catalyst B as the fastest productive option: at 1800 s it already gave conversion 0.6038 and yield 0.4906. Batches 4 and 5 showed that lower rate did not imply uniformly worse selectivity. Catalyst D, for example, had selectivity 0.8295 and byproduct signal 0.0634 at 1800 s despite lower conversion. These results motivated separate catalyst effects on productive and competing rates in K1.

Batches 6–8 formed the solvent interpretation. The water/ethanol/acetonitrile/toluene ordering was empirical rather than derived from the real solvent names. Toluene’s final conversion of 0.7745 combined with yield 0.4659 and byproduct signal 0.3082 was especially important because it demonstrated that substantial conversion could coexist with poor target branching.

Batches 9 and 10 changed the temperature-time view from “hotter is faster” to “hotter has a shorter useful window.” Batch 10’s 1800 s intermediate yield of 0.6432 versus its 3600 s final yield of 0.6189 was the clearest evidence that more thermal exposure could become counterproductive.

Batch 11 was primarily an exploitation experiment informed by batch 10. It tested the inferred high-temperature optimum more directly and produced the sample-high score of 0.35043, yield 0.6453, and selectivity 0.7972. It strengthened the operational recommendation but added less structural discrimination than a catalyst-free control or an exact replicate would have.

Batch 12 was a deliberate return to identification. Halving Catalyst B lowered the 900 s conversion from batch 11’s 0.4827 to 0.3079 and the 1800 s final yield from 0.6453 to 0.4694. This supported a catalyst-loading effect, although two nonzero loadings cannot determine reaction order, saturation, or the uncatalyzed rate.

Several early choices depended mainly on unverified guesses: acetonitrile as the baseline solvent, 350 K as the initial temperature, 600 rpm as adequate mixing, maximum reagent and catalyst amounts, and equal allocation of stock over 12 vessels. Later choices depended increasingly on accumulated evidence: Catalyst B after batch 3, solvent comparisons after the catalyst screen, the 320/380 K contrast after observing time deterioration, and the 1800 s batch 11 design after batch 10.

## 3. Current competing mechanisms and what the experiments distinguish

The leading K1 model was a network containing productive and competing reactant conversion, with possible secondary target loss:

R → P, R → B, and possibly P → D/B.

The most important competing explanations are:

1. **Purely parallel formation with time-dependent branching.** R converts independently to P and B, but temperature, catalyst state, or composition changes the ratio kP/kB over time. Yield can peak without direct destruction of P.
2. **Sequential target degradation.** P forms first and is subsequently converted to degradation products. This naturally explains the declining yield or selectivity at long high-temperature exposure.
3. **Catalyst deactivation or catalyst-state evolution.** The catalyst may lose productive activity, change selectivity, or become inhibited by product. Apparent slowing need not be substrate depletion alone.
4. **Reversible target formation plus an irreversible sink.** R and P may approach a reversible state while byproduct formation slowly removes material. This can resemble both a yield plateau and degradation.
5. **Transport or thermal-lag effects.** The observed time dependence may partly reflect heat-up, cooling, or mixing rather than intrinsic chemical rate changes.
6. **Observation-model effects.** HPLC intermediate estimates and final-assay estimates are independently calibrated noisy proxies. Some apparent pre/post changes may be measurement differences rather than chemistry.

The experiments distinguish a single irreversible R-to-P pathway from a multi-channel process: the large byproduct and degradation signals and declining selectivity contradict the single-path model. They also distinguish catalyst and solvent categories empirically and show that nominal temperature and elapsed time jointly matter.

They do not distinguish direct P degradation from a late-forming parallel byproduct. No isolated target was reheated, and no common instrument repeatedly tracked the same vessel without perturbation. They also do not distinguish catalyst deactivation from substrate depletion or product inhibition. Batch 12 establishes loading sensitivity but not the uncatalyzed baseline. Stirring, concentration, and volume were effectively fixed, so transport and kinetic reaction order remain confounded. Finally, quench chemistry cannot be separated from cooling, altered thermal history, and cross-instrument measurement.

## 4. One additional complete experiment

If only one additional legal complete experiment were allowed, I would run a **catalyst-free matched control** under the batch 11 conditions:

- 0.080 L acetonitrile;
- 0.040 mol reagent;
- no catalyst addition, or a legal zero catalyst amount if an explicit addition were required;
- heat toward 380 K at 600 rpm for 900 s;
- measure by HPLC;
- heat for another 900 s;
- quench, terminate, and perform the required final assay.

This choice addresses the largest structural omission identified in K1 rather than trying to improve the score.

Possible outcomes would change the interpretation as follows:

- **Near-zero conversion at both times:** this would strongly support genuinely catalyst-dependent formation and make the batch 11 versus batch 12 loading trend more interpretable as catalytic activity scaling. It would disfavor a large thermal background reaction.
- **Substantial conversion with high selectivity:** Catalyst B would be primarily an accelerator, and the model would need a nonzero uncatalyzed productive term. Some of the apparent loading dependence could then reflect competition between background and catalytic pathways.
- **Substantial conversion dominated by byproduct:** Catalyst B would appear to suppress an uncatalyzed competing pathway as well as accelerate target formation. The catalyst-specific branching model would become more important.
- **Conversion comparable to batch 11:** the assumption that Catalyst B is mechanistically essential would be substantially undermined. Temperature, solvent, or a benchmark background process would dominate.
- **Large disagreement between the 900 s HPLC and 1800 s final assay without plausible kinetic progression:** that would increase concern about cross-instrument comparability and weaken quantitative rate inference.

An exact batch 11 replicate would be the best next experiment for operational validation, but the catalyst-free control offers greater mechanism discrimination from a single batch.

## 5. Tradeoff between identifiability and operational score

The stated research goal prioritized an explanatory and predictive account, with safe score explicitly secondary. The campaign therefore spent many batches on conditions that were unlikely to maximize score: Catalyst A in batches 1–2, Catalysts C and D in batches 4–5, all four solvents in batches 6–8, the low-temperature boundary in batch 9, the deliberately excessive 380 K exposure in batch 10, and the half-loading condition in batch 12. Those choices sacrificed immediate score to learn time, catalyst, solvent, temperature, and loading effects.

The design nevertheless shifted toward exploitation after Catalyst B emerged as favorable. Batch 11 was explicitly an optimization-oriented response to batch 10 and became the sealed recommendation. Choosing batch 11 instead of an exact replicate, catalyst-free control, or a randomized local factorial sacrificed identifiability and reproducibility for a higher observed score.

There was also a resource-driven compromise. One intermediate measurement per vessel gave useful within-batch timing information while respecting the 12-measurement limit. However, intermediate HPLC sampling and terminal final assays were not interchangeable. This design provided broad coverage but weak replication and complicated formal kinetic fitting.

The catalyst screen and solvent screen improved identifiability, but they were conducted at only one principal composition and temperature schedule. Conversely, the later focus on Catalyst B/acetonitrile improved local optimization while leaving interactions such as catalyst-by-solvent and loading-by-temperature largely untested. The campaign was therefore effective as sequential reconnaissance but not as a balanced factorial study.

## 6. Underused evidence and weakest blind predictions

Several acquired evidence streams were not fully exploited:

- I used processed estimates but did not analyze the full raw spectral artifacts. Peak areas and cross-channel structure might have helped assess whether “degradation” and “byproduct” behaved as distinct signals.
- Temperature increments were recorded, but I did not fit an explicit heat-transfer model. K1 correctly emphasized actual thermal history, yet the blind predictions were still based on qualitative exposure scaling rather than a calibrated temperature trajectory.
- Risk increments from additions, heating, and quenching were available operation by operation. I described their ordering but did not fit a quantitative risk model.
- The data could have supported a small hierarchical or nonlinear fit with separate observation errors for HPLC and final assay. Instead, both K1 and the blind predictions remained largely heuristic.
- The destructive intermediate samples slightly changed vessel volume. The effect was probably small at 0.080 L, but it was not explicitly propagated.
- Cost and the exact score mapping were not identified. Blind score predictions were consequently less grounded than conversion or yield predictions.

The least reliable sealed predictions are Q12, Q04, Q06, Q07, and Q08. Q12 extrapolates to 460 K for 6300 s, far beyond the campaign’s maximum 380 K tested boundary and longer than the best-supported high-temperature duration. Q04 and Q06 similarly combine untested temperatures with prolonged exposure. Q07 and Q08 require prediction of order-dependent thermal history, yet the campaign never reversed temperature segments or fitted heating and cooling dynamics.

The quench pairs Q01/Q02 and Q09/Q10 are also weak in a different way. K1 explicitly said that quench chemistry was not isolated and that the defensible role of quench was reduction of continuing thermal exposure. The sealed predictions nevertheless assigned modest compositional improvements to the quenched members. Those differences were plausible but not strongly identified.

Some prediction intervals were probably too narrow. In particular:

- Q12 assigned conversion an 80% interval of 0.99–1.00 despite extreme extrapolation and unknown high-temperature deactivation. That is overconfident.
- Q04 and Q06 also used narrow near-unity conversion intervals while the catalyst’s high-temperature stability was never tested.
- Q05 and Q09 extrapolated target-yield optima to 420–440 K with intervals that may not fully cover uncertainty in heat-up rate, catalyst concentration scaling, and the lower 400 rpm stirring speed.
- Safety-risk and score intervals throughout are vulnerable because neither response law was identified mechanistically.

These weaknesses are partly inconsistent with K1’s explicit statement that predictions outside the studied temperature, time, loading, concentration, or solvent ranges were “substantially less reliable.” The narrative rationales acknowledged the extrapolation, and the yield/selectivity intervals were often broad, but the near-saturated conversion forecasts did not always propagate that warning adequately.

The new blind batches also used 0.003 mol reagent in 0.005 L and 0.000525 mol catalyst, rather than the campaign’s 0.040 mol in 0.080 L with 0.005 mol catalyst. Both concentration and catalyst-to-reagent ratio changed, while stirring decreased from 600 to 400 rpm. K1 explicitly listed concentration, stirring, and broader loading ranges as unidentified. Therefore, all blind predictions—not merely the highest-temperature cases—contain a scale-transfer uncertainty that should arguably have widened their intervals.

## 7. Limitations of the sealed recommendation

The sealed recommendation selected batch 11 because it had the highest observed score, 0.35043, while remaining below the safety limit. Its observed final values were yield 0.6453, selectivity 0.7972, conversion 0.7921, byproduct signal 0.1551, degradation warning 0.1019, and safety risk 0.1916.

This establishes only that batch 11 was the **sample-highest result among the 12 tested batches**. It does not prove a global optimum, a local mathematical optimum, or even that the same recipe has the highest expected score under replication. There was only one exact realization of batch 11. The comparison with batch 10 is informative but not an exact replicate because batch 10 continued heating after its 1800 s HPLC measurement, whereas batch 11 was quenched and assessed by the final assay.

Repeatability should first be tested through several exact batch 11 replicates, including the same operation order and quench timing. The distribution of yield, selectivity, risk, and score would determine whether 0.35043 was typical or a favorable realization.

Local robustness should then be tested with a compact response-surface design around the recommendation, for example 370, 380, and 390 K; 1500, 1800, and 2100 s; and modest variations in Catalyst B loading. Stirring and quench delay should also be perturbed. A robust operating point should retain acceptable performance under small deviations rather than merely maximize one nominal run.

Cross-material scope requires repeating the local time-temperature study in water and ethanol and, if relevant, with Catalysts C and D. The campaign showed strong solvent and catalyst interactions, so the batch 11 optimum cannot be transferred across materials by changing only a rate constant.

Cross-scale scope requires varying reagent concentration, solvent volume, and catalyst-to-reagent ratio. The blind queries expose this limitation directly: they use a much smaller volume and different concentrations than the campaign. Heat-transfer behavior and mixing may also change with scale.

Finally, cross-world generalization is especially limited because the catalysts and kinetic effects are anonymous latent benchmark categories. Evidence that Catalyst B is best in this world is not evidence that an identically labeled category will be best in another world unless the world definition guarantees shared latent parameters. The defensible claim is therefore narrow: batch 11 was the best observed member of this campaign and is a reasonable incumbent for local follow-up, not a demonstrated universal optimum.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 105.8 | none | 0 |
| Q | yes | 0 | 65.6 | none | 0 |
| K2 | yes | 0 | 109.9 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
