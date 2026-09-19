# RX-W04--P--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W04`
- Locus: `P`
- Goal: `safety_constrained_optimization`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `84`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `11`
- Rationale: Highest observed final-assay safe score (0.4516) among completed batches, with safety risk 0.1531 well below the 0.35 limit; water, Catalyst B, 390 K target, 3300 s, and 350 rpm balanced yield/selectivity against byproduct and degradation.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.7636 | 0.7953 | 0.9646 | 0.1848 | 0.1147 | 0.2858 | 0.4065 |
| 2 | S0 (0.0050 L) | 0.003000 mol | C0 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.5993 | 0.7083 | 0.8396 | 0.2509 | 0.1183 | 0.2847 | 0.3281 |
| 3 | S0 (0.0050 L) | 0.003000 mol | C2 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6201 | 0.7238 | 0.8566 | 0.2559 | 0.0487 | 0.2845 | 0.3337 |
| 4 | S0 (0.0050 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6940 | 0.7729 | 0.8747 | 0.1994 | 0.0904 | 0.2851 | 0.3561 |
| 5 | S1 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6500 | 0.6708 | 0.9650 | 0.3515 | 0.2018 | 0.3088 | 0.3195 |
| 6 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6545 | 0.6427 | 1.0000 | 0.3676 | 0.2966 | 0.3271 | 0.3092 |
| 7 | S3 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.7039 | 0.7136 | 0.9935 | 0.2985 | 0.2207 | 0.3399 | 0.3405 |
| 8 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 430 K x 3300 s @ 350 rpm | no | 0.7669 | 0.7833 | 0.9789 | 0.2069 | 0.1324 | 0.3287 | 0.3869 |
| 9 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 410 K x 3300 s @ 350 rpm | no | 0.7523 | 0.8027 | 0.9353 | 0.1933 | 0.1068 | 0.2362 | 0.4233 |
| 10 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 400 K x 3300 s @ 350 rpm | no | 0.7570 | 0.8220 | 0.9066 | 0.1754 | 0.0965 | 0.1894 | 0.4482 |
| 11 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 390 K x 3300 s @ 350 rpm | no | 0.7265 | 0.8289 | 0.8820 | 0.1606 | 0.0780 | 0.1531 | 0.4516 |
| 12 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 390 K x 4500 s @ 350 rpm | no | 0.7384 | 0.7632 | 0.9427 | 0.2073 | 0.1181 | 0.1535 | 0.4448 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.18478119373321533,
    "conversion": 0.9646226167678833,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.11470863223075867,
    "safety_risk": 0.2858142554759979,
    "score": 0.40653717517852783,
    "selectivity": 0.7953085899353027,
    "virtual_spectrum_summary": 0.15324853360652924,
    "yield": 0.7635854482650757
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.25090497732162476,
    "conversion": 0.8395981788635254,
    "cost": 0.4456999897956848,
    "degradation_warning": 0.11833897233009338,
    "safety_risk": 0.28465357422828674,
    "score": 0.328100323677063,
    "selectivity": 0.7082961201667786,
    "virtual_spectrum_summary": 0.1912502646446228,
    "yield": 0.5993264317512512
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.25588399171829224,
    "conversion": 0.8565864562988281,
    "cost": 0.529699981212616,
    "degradation_warning": 0.0486820712685585,
    "safety_risk": 0.28448230028152466,
    "score": 0.333673357963562,
    "selectivity": 0.7237963080406189,
    "virtual_spectrum_summary": 0.16264311969280243,
    "yield": 0.6201316714286804
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.19935549795627594,
    "conversion": 0.8747285008430481,
    "cost": 0.7397000193595886,
    "degradation_warning": 0.09037529677152634,
    "safety_risk": 0.28508272767066956,
    "score": 0.3560502231121063,
    "selectivity": 0.772925078868866,
    "virtual_spectrum_summary": 0.15031440556049347,
    "yield": 0.6940082907676697
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
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.3515353202819824,
    "conversion": 0.9650211334228516,
    "cost": 0.6577000021934509,
    "degradation_warning": 0.20180575549602509,
    "safety_risk": 0.30880019068717957,
    "score": 0.3194904625415802,
    "selectivity": 0.6708351373672485,
    "virtual_spectrum_summary": 0.28415700793266296,
    "yield": 0.6500241160392761
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
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.3676076829433441,
    "conversion": 1.0,
    "cost": 0.6608999967575073,
    "degradation_warning": 0.2966390550136566,
    "safety_risk": 0.3271262049674988,
    "score": 0.30917030572891235,
    "selectivity": 0.6426653265953064,
    "virtual_spectrum_summary": 0.3356718122959137,
    "yield": 0.6545019149780273
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
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.2984684705734253,
    "conversion": 0.993524432182312,
    "cost": 0.6589000225067139,
    "degradation_warning": 0.22074781358242035,
    "safety_risk": 0.3398732542991638,
    "score": 0.34049272537231445,
    "selectivity": 0.713607668876648,
    "virtual_spectrum_summary": 0.2634941637516022,
    "yield": 0.7039282917976379
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 430
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
    "byproduct_signal": 0.20686277747154236,
    "conversion": 0.9788593053817749,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.13235528767108917,
    "safety_risk": 0.3287447988986969,
    "score": 0.38694390654563904,
    "selectivity": 0.7832675576210022,
    "virtual_spectrum_summary": 0.17333440482616425,
    "yield": 0.766865611076355
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 410
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
    "byproduct_signal": 0.19329452514648438,
    "conversion": 0.935325026512146,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.10681770741939545,
    "safety_risk": 0.2361977994441986,
    "score": 0.42326152324676514,
    "selectivity": 0.8027111887931824,
    "virtual_spectrum_summary": 0.1543799638748169,
    "yield": 0.7522755861282349
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 400
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
    "byproduct_signal": 0.17535452544689178,
    "conversion": 0.9066276550292969,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.09648122638463974,
    "safety_risk": 0.1894015669822693,
    "score": 0.4481692314147949,
    "selectivity": 0.8220101594924927,
    "virtual_spectrum_summary": 0.13986153900623322,
    "yield": 0.7570115923881531
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.16063004732131958,
    "conversion": 0.8820390701293945,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.07795053720474243,
    "safety_risk": 0.1531040370464325,
    "score": 0.4515570402145386,
    "selectivity": 0.8289002180099487,
    "virtual_spectrum_summary": 0.12342426925897598,
    "yield": 0.7264872193336487
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `84`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 4500,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 84,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.20728643238544464,
    "conversion": 0.9427127242088318,
    "cost": 0.6657000184059143,
    "degradation_warning": 0.11807996034622192,
    "safety_risk": 0.153461292386055,
    "score": 0.444795697927475,
    "selectivity": 0.7632227540016174,
    "virtual_spectrum_summary": 0.16714352369308472,
    "yield": 0.7383658289909363
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

# Mechanistic report

## 1. Scope and evidence base

This report concerns the bounded synthetic reaction-and-thermal benchmark studied in 12 completed batches. Catalyst identities are anonymous benchmark formulations, and even the named solvents have task-specific categorical effects. Consequently, references to “Catalyst B” or “water” describe observed benchmark behavior, not a claim about a real catalyst or a transferable real-world synthesis.

Every batch used 0.003 mol reagent, 0.005 L solvent, 0.000525 mol catalyst, and 350 rpm stirring. Unless stated otherwise, heating lasted 3300 s. These fixed conditions correspond nominally to 0.6 mol/L reagent and a catalyst/reagent molar ratio of 0.175. Each batch had one HPLC measurement followed by termination and a final assay. The final-assay observations are the main basis for comparisons because they determine the completed-batch score.

## 2. Principal empirical findings

The final-assay results were:

| Batch | Solvent | Catalyst | Temperature | Time | Risk | Score | Conversion | Yield | Selectivity | Byproduct | Degradation |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Water | B | 420 K | 3300 s | 0.2858 | 0.4065 | 0.9646 | 0.7636 | 0.7953 | 0.1848 | 0.1147 |
| 2 | Water | A | 420 K | 3300 s | 0.2847 | 0.3281 | 0.8396 | 0.5993 | 0.7083 | 0.2509 | 0.1183 |
| 3 | Water | C | 420 K | 3300 s | 0.2845 | 0.3337 | 0.8566 | 0.6201 | 0.7238 | 0.2559 | 0.0487 |
| 4 | Water | D | 420 K | 3300 s | 0.2851 | 0.3561 | 0.8747 | 0.6940 | 0.7729 | 0.1994 | 0.0904 |
| 5 | Ethanol | B | 420 K | 3300 s | 0.3088 | 0.3195 | 0.9650 | 0.6500 | 0.6708 | 0.3515 | 0.2018 |
| 6 | Acetonitrile | B | 420 K | 3300 s | 0.3271 | 0.3092 | 1.0000 | 0.6545 | 0.6427 | 0.3676 | 0.2966 |
| 7 | Toluene | B | 420 K | 3300 s | 0.3399 | 0.3405 | 0.9935 | 0.7039 | 0.7136 | 0.2985 | 0.2207 |
| 8 | Water | B | 430 K | 3300 s | 0.3287 | 0.3869 | 0.9789 | 0.7669 | 0.7833 | 0.2069 | 0.1324 |
| 9 | Water | B | 410 K | 3300 s | 0.2362 | 0.4233 | 0.9353 | 0.7523 | 0.8027 | 0.1933 | 0.1068 |
| 10 | Water | B | 400 K | 3300 s | 0.1894 | 0.4482 | 0.9066 | 0.7570 | 0.8220 | 0.1754 | 0.0965 |
| 11 | Water | B | 390 K | 3300 s | 0.1531 | 0.4516 | 0.8820 | 0.7265 | 0.8289 | 0.1606 | 0.0780 |
| 12 | Water | B | 390 K | 4500 s | 0.1535 | 0.4448 | 0.9427 | 0.7384 | 0.7632 | 0.2073 | 0.1181 |

All reported risks remained below the declared limit of 0.35. Batch 11 had the highest observed final score, 0.4516, and was therefore selected as the recommendation.

## 3. Proposed reaction network

The simplest model consistent with the results is a productive reaction competing with one or more unproductive pathways, followed by possible secondary degradation of the desired product:

R --k_p--> P
R --k_s--> B
P --k_d--> D

Here R is the limiting reactant, P is the desired public product, B represents primary byproducts, and D represents degradation products or signals. A minimal kinetic description is:

-dR/dt = (k_p + k_s)R

dP/dt = k_p R - k_d P

dB/dt = k_s R + beta*k_d P

The rate constants likely depend on temperature, catalyst, and solvent:

k_j(T,c,s) = A_j * exp[-E_j/(R_gas*T)] * alpha_j(catalyst) * gamma_j(solvent)

This is a mechanistic hypothesis rather than an identified law. The data do not determine individual rate constants or activation energies. Nevertheless, the network explains several observations:

1. High conversion did not guarantee high yield or score. Batch 6 reached reported conversion 1.0000 but had yield 0.6545, selectivity 0.6427, byproduct 0.3676, degradation 0.2966, and score only 0.3092. Substrate disappearance therefore includes substantial nonproductive chemistry.
2. Raising temperature increased conversion but generally worsened selectivity, byproduct formation, degradation, safety risk, and total score. This is consistent with side-reaction or degradation rates having stronger effective temperature dependence than the productive advantage gained at high temperature.
3. Extending residence time at 390 K increased conversion but harmed selectivity. Relative to Batch 11, Batch 12 increased time from 3300 to 4500 s. Conversion rose from 0.8820 to 0.9427 and yield from 0.7265 to 0.7384, but selectivity fell from 0.8289 to 0.7632, byproduct rose from 0.1606 to 0.2073, degradation rose from 0.0780 to 0.1181, and score fell from 0.4516 to 0.4448. This is direct evidence for increasing secondary or parallel side chemistry with prolonged exposure.

A competing model in which temperature merely shifts an equilibrium could also explain part of the conversion trend. However, the simultaneous growth of byproduct and degradation signals with temperature and time makes a purely reversible single-reaction equilibrium model insufficient by itself.

## 4. Catalyst effects

Batches 1–4 isolated the catalyst category at water/420 K/3300 s. Catalyst B clearly gave the strongest balanced outcome: score 0.4065 versus 0.3281 for A, 0.3337 for C, and 0.3561 for D. Its final yield was 0.7636, compared with 0.5993, 0.6201, and 0.6940, respectively.

The catalysts do more than uniformly multiply the overall reaction rate. For example, Catalyst C had relatively low degradation warning, 0.0487, but still poor yield and score because conversion and selectivity were weak. Catalyst D gave intermediate conversion and substantially better yield/selectivity than A or C. Thus catalyst-specific factors probably act differently on k_p, k_s, and possibly k_d rather than through one common activity coefficient.

Safety risk at fixed solvent and temperature was almost catalyst-independent: 0.2845–0.2858 across Batches 1–4. I therefore infer that catalyst identity strongly affects kinetic partitioning but contributes little to the benchmark’s dominant thermal safety term at this tested loading.

No catalyst-free batch or catalyst-loading series was performed. Catalyst order, saturation behavior, deactivation, and the possibility of catalyst-dependent assay response remain unidentified.

## 5. Solvent coupling

Batches 1 and 5–7 compared solvents using Catalyst B at 420 K. Water was decisively best for the safe-score objective. The three alternative solvents all retained very high conversion but produced substantially more byproduct and degradation and lower selectivity:

- Water: score 0.4065, selectivity 0.7953, byproduct 0.1848, degradation 0.1147.
- Ethanol: score 0.3195, selectivity 0.6708, byproduct 0.3515, degradation 0.2018.
- Acetonitrile: score 0.3092, selectivity 0.6427, byproduct 0.3676, degradation 0.2966.
- Toluene: score 0.3405, selectivity 0.7136, byproduct 0.2985, degradation 0.2207.

Risk also followed solvent category: water 0.2858, ethanol 0.3088, acetonitrile 0.3271, and toluene 0.3399. The initial solvent-addition risks already differed: approximately 0.0364 for water, 0.0598 for ethanol, 0.0778 for acetonitrile, and 0.0904 for toluene. This supports a model with a solvent-dependent baseline hazard plus a thermal contribution.

Because the task explicitly defines solvent behavior as categorical benchmark coupling, it would be unjustified to explain these rankings solely from real-world boiling point, polarity, flammability, or other tabulated properties. Matrix-dependent analytical response is also a reasonable alternative explanation for some signal differences, although the coordinated changes in conversion, selectivity, byproduct, degradation, risk, and score suggest that the solvent effects are not purely instrumental.

## 6. Temperature and safety behavior

With water, Catalyst B, and 3300 s, the observed risk rose strongly with temperature:

390 K: 0.1531
400 K: 0.1894
410 K: 0.2362
420 K: 0.2858
430 K: 0.3287

Over this local region, risk can be represented empirically as

risk ≈ r_setup(solvent,reagent) + f_thermal(T) + epsilon,

where f_thermal is increasing and mildly nonlinear. Duration had very little effect on the reported peak risk at 390 K: increasing time by 1200 s changed risk only from 0.1531 to 0.1535. This suggests that the public safety metric is dominated by peak thermal state or target severity rather than accumulated exposure. That interpretation is limited to the two tested durations at one temperature.

The actual thermal state did not simply jump exactly to the requested setpoint. Public state deltas showed approximate temperature increases of 85.45 K at a 390 K target, 94.23 K at 400 K, 102.91 K at 410 K, and 119.92 K at 430 K. These observations are consistent with a dynamic heating model starting near ambient, possibly with incomplete or noisy approach to target.

The supplied initial incomplete model suggested that the higher-temperature side of the 420 K reference region would retain safe balanced performance more reliably. The campaign modified that belief. Higher temperature did improve conversion and approximately preserved yield, but it consistently increased risk and worsened selectivity, byproduct, degradation, and total safe score between 390 and 430 K. The initial claim may have described conversion robustness, may have been shifted relative to this instance, or may simply have been unreliable outside a narrow reference interpretation.

## 7. Why the optimum occurred near 390–400 K

The measured score reflects a compromise rather than maximization of conversion alone. Cooling from 430 to 390 K reduced conversion from 0.9789 to 0.8820 and yield from 0.7669 to 0.7265, but improved selectivity from 0.7833 to 0.8289, reduced byproduct from 0.2069 to 0.1606, reduced degradation from 0.1324 to 0.0780, and more than halved the excess risk above the setup baseline. The resulting score improved from 0.3869 to 0.4516.

Batch 10 at 400 K had almost the same performance as Batch 11: score 0.4482 versus 0.4516. Given single-batch noise, I would not claim that 390 K is a sharply identified global optimum. The supported conclusion is a broad favorable local region around 390–400 K for the fixed formulation and residence time. Temperatures below 390 K were not tested, so the lower-temperature side of the optimum is unobserved. Extrapolating the kinetic trend suggests that sufficiently low temperature would eventually lose too much conversion and yield, but the location of that turnover is unknown.

## 8. Measurement interpretation

HPLC and final-assay values were broadly consistent but not identical. For example, Batch 11 HPLC reported conversion 0.8642, yield 0.7109, selectivity 0.8292, and byproduct 0.1578; the final assay reported 0.8820, 0.7265, 0.8289, and 0.1606. In Batch 1, HPLC selectivity was 0.8378 while the final assay gave 0.7953. These differences should not automatically be interpreted as reaction progression after sampling. They can arise from instrument noise, calibration differences, sampling, matrix effects, or elapsed-time behavior. The agreement in major trends is more informative than small cross-instrument numerical differences.

There were no replicate batches at precisely identical conditions, so process variation cannot be separated from assay noise. The small score differences among Batches 10–12 should therefore be treated less confidently than the large catalyst and solvent contrasts.

## 9. Recommended operating procedure

The sealed recommendation is Batch 11:

1. Charge 0.005 L water.
2. Add 0.003 mol limiting reagent.
3. Add 0.000525 mol Catalyst B.
4. Heat toward 390 K for 3300 s at 350 rpm.
5. Terminate and assay according to the campaign lifecycle.

Observed final performance was score 0.4516, risk 0.1531, conversion 0.8820, yield 0.7265, selectivity 0.8289, byproduct signal 0.1606, and degradation warning 0.0780. These are observations from this benchmark batch, not guaranteed predictions for a physical system.

## 10. Applicability limits and unresolved factors

The interpretation is local to the tested reagent amount, solvent volume, catalyst amount, stirring rate, addition sequence, temperature range of 390–430 K for systematic temperature comparisons, and duration range of 3300–4500 s. The campaign did not identify effects of concentration, dilution, catalyst loading, reagent loading, stirring, staged addition, quenching, multiple heating segments, temperatures below 390 K, or substantially shorter times.

The public species mapping is hidden, so “product,” “byproduct,” and “degradation” remain operational signal classes rather than identified molecules. The exact score equation and exact risk equation were not exposed and cannot be reconstructed uniquely from 12 observations. Likewise, individual activation energies and rate constants are not identifiable.

Reasonable competing explanations include parallel irreversible reactions, desired-product decomposition, catalyst deactivation, temperature-dependent equilibrium, mass-transfer limitations, and solvent-dependent analytical response. The current evidence most strongly favors a combination of productive conversion plus parallel/secondary side reactions whose relative importance increases with temperature and prolonged exposure. It does not uniquely distinguish whether the added byproduct at long time originates mainly from residual reactant or from degradation of already formed product.

## Q — Blind predictions

### Overall rationale

Predictions are anchored to Batch 6, the direct acetonitrile/Catalyst B/420 K/3300 s observation, and adjusted using the campaign's water-based temperature and duration trends. The model treats conversion as productive plus competing substrate consumption, with secondary byproduct formation increasing with thermal exposure. Safety risk is modeled mainly as a solvent-dependent baseline plus peak thermal severity. Extrapolated 440–460 K acetonitrile actions are predicted to encounter the declared safety boundary and roll back; uncertainty intervals are deliberately wider for those actions, multi-stage schedules, quenching, and the untested 370 K condition.

### Q01

This nearly replicates observed Batch 6, apart from the modest stirring increase from 350 to 400 rpm. I assume stirring is not rate-limiting in this range and center the prediction on Batch 6.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3680 | 0.3300 | 0.4100 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.3270 | 0.3100 | 0.3450 |
| score | 0.3090 | 0.2700 | 0.3500 |
| selectivity | 0.6430 | 0.5900 | 0.6900 |
| yield | 0.6550 | 0.6100 | 0.7000 |

### Q02

The chemistry before quenching matches Q01. I expect quenching to arrest residual hot-state chemistry but not erase peak safety risk; because termination follows immediately, its incremental benefit should be small.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3600 | 0.3200 | 0.4000 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.3270 | 0.3100 | 0.3450 |
| score | 0.3150 | 0.2750 | 0.3600 |
| selectivity | 0.6500 | 0.6000 | 0.7000 |
| yield | 0.6570 | 0.6100 | 0.7050 |

### Q03

Cooling from 420 to 390 K should lower conversion but improve selectivity, byproduct formation, and safety. This extrapolates the temperature trends observed with water while retaining the adverse categorical acetonitrile effect.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.2700 | 0.3900 |
| conversion | 0.9100 | 0.8200 | 0.9700 |
| safety_risk | 0.1950 | 0.1700 | 0.2250 |
| score | 0.3500 | 0.2900 | 0.4100 |
| selectivity | 0.6800 | 0.6100 | 0.7500 |
| yield | 0.6350 | 0.5600 | 0.7000 |

### Q04

Extrapolation from the measured acetonitrile risk at 420 K indicates that a 450 K target would exceed the 0.35 safety boundary. I therefore predict a temperature-bound rollback, leaving mainly setup-state material. The wide upper bounds acknowledge uncertainty about whether partial heating occurs before rollback.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.0250 | 0.0000 | 0.2000 |
| conversion | 0.0400 | 0.0000 | 0.3500 |
| safety_risk | 0.1320 | 0.1150 | 0.3500 |
| score | 0.0200 | 0.0000 | 0.1600 |
| selectivity | 0.1800 | 0.0000 | 0.6500 |
| yield | 0.0200 | 0.0000 | 0.2000 |

### Q05

The shorter 1500 s exposure should give incomplete conversion but substantially less secondary byproduct formation than Q01. Peak risk is expected to remain largely temperature-controlled, although incomplete thermal approach may reduce it slightly.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1600 | 0.3100 |
| conversion | 0.7900 | 0.6700 | 0.8900 |
| safety_risk | 0.3220 | 0.2950 | 0.3450 |
| score | 0.3400 | 0.2700 | 0.4100 |
| selectivity | 0.7200 | 0.6400 | 0.7900 |
| yield | 0.5700 | 0.4800 | 0.6500 |

### Q06

Longer exposure should maintain complete conversion while shifting more material into side products and degradation. Batch 11 versus Batch 12 supplied direct evidence that added residence time can reduce selectivity even when yield changes only modestly.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4700 | 0.4000 | 0.5500 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.3290 | 0.3100 | 0.3470 |
| score | 0.2450 | 0.1800 | 0.3100 |
| selectivity | 0.5400 | 0.4600 | 0.6200 |
| yield | 0.5800 | 0.4900 | 0.6500 |

### Q07

I expect the initial 390 K segment to react successfully but the subsequent 450 K request to trigger a safety rollback. The estimate therefore resembles an approximately 1800 s exposure at 390 K. Intervals also cover partial execution of the hotter segment.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.1100 | 0.2900 |
| conversion | 0.6900 | 0.5000 | 0.8500 |
| safety_risk | 0.1940 | 0.1650 | 0.3500 |
| score | 0.3500 | 0.2400 | 0.4300 |
| selectivity | 0.7400 | 0.6200 | 0.8300 |
| yield | 0.5100 | 0.3600 | 0.6300 |

### Q08

The first 450 K request is predicted to roll back atomically, after which the 390 K segment proceeds. Under that interpretation Q07 and Q08 converge to similar final states; the broad intervals reflect uncertainty about rollback atomicity and thermal memory.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.1100 | 0.2800 |
| conversion | 0.6900 | 0.5000 | 0.8500 |
| safety_risk | 0.1940 | 0.1650 | 0.3500 |
| score | 0.3500 | 0.2400 | 0.4300 |
| selectivity | 0.7400 | 0.6200 | 0.8300 |
| yield | 0.5100 | 0.3600 | 0.6300 |

### Q09

Although the duration is short, the projected acetonitrile thermal risk near a 440 K target is close to or above the safety boundary. I assign greatest probability to rollback, while the wide intervals cover a partially heated, moderately converted alternative.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.0200 | 0.0000 | 0.1800 |
| conversion | 0.0400 | 0.0000 | 0.3800 |
| safety_risk | 0.1320 | 0.1150 | 0.3500 |
| score | 0.0200 | 0.0000 | 0.1800 |
| selectivity | 0.1800 | 0.0000 | 0.6800 |
| yield | 0.0200 | 0.0000 | 0.2200 |

### Q10

This shares the predicted rollback behavior of Q09. A subsequent quench should have little effect if the heat operation was rejected, though it could modestly improve the outcome in the less likely partial-heating case.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.0180 | 0.0000 | 0.1700 |
| conversion | 0.0400 | 0.0000 | 0.3800 |
| safety_risk | 0.1300 | 0.1100 | 0.3500 |
| score | 0.0220 | 0.0000 | 0.1900 |
| selectivity | 0.1900 | 0.0000 | 0.6900 |
| yield | 0.0210 | 0.0000 | 0.2300 |

### Q11

A long, low-temperature exposure should recover substantial conversion while avoiding the high thermal risk and severe degradation of hotter conditions. This is an extrapolation below the campaign's lowest tested temperature, so kinetic uncertainty remains appreciable.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2700 | 0.1900 | 0.3600 |
| conversion | 0.8600 | 0.7300 | 0.9500 |
| safety_risk | 0.1500 | 0.1200 | 0.1900 |
| score | 0.3900 | 0.3100 | 0.4600 |
| selectivity | 0.7200 | 0.6300 | 0.8000 |
| yield | 0.6300 | 0.5300 | 0.7100 |

### Q12

A 460 K target in acetonitrile is far beyond the locally inferred safety boundary, and the long duration does not make acceptance more plausible. I therefore predict rollback and negligible reaction; the asymmetric upper bounds acknowledge the low-probability alternative of partial heating with extensive side-product formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.0200 | 0.0000 | 0.4500 |
| conversion | 0.0300 | 0.0000 | 0.3500 |
| safety_risk | 0.1320 | 0.1150 | 0.3500 |
| score | 0.0150 | 0.0000 | 0.1400 |
| selectivity | 0.1500 | 0.0000 | 0.5500 |
| yield | 0.0150 | 0.0000 | 0.1800 |

## K2 — Retrospective analysis

## 1. Assessment of the initial information

The initial packet contained one substantive directional claim: near the 420 K reference region, the higher-temperature side was expected to retain safe, balanced performance more reliably than the lower-temperature side. It was explicitly labeled an incomplete, potentially shifted model rather than authoritative truth.

That claim was contradicted locally. With water, Catalyst B, and 3300 s, Batch 8 at 430 K had a final score of 0.3869 and risk of 0.3287, compared with Batch 1 at 420 K at 0.4065 and 0.2858. Moving downward produced Batch 9 at 410 K with score 0.4233, Batch 10 at 400 K with 0.4482, and Batch 11 at 390 K with 0.4516. Higher temperature did preserve conversion and yield reasonably well, but it did not preserve the combined safe-score objective: selectivity deteriorated and byproduct, degradation, and risk increased. K1 explicitly revised the initial view rather than merely noting an absence of support.

The initial 420 K, 3300 s reference region itself was useful: Batch 1 confirmed that it was an active, feasible region with conversion 0.9646 and risk below the 0.35 limit. This supports its use as a reference condition, but not the directional claim attached to it.

The packet also warned that a temperature-bound rollback should be treated as evidence rather than missing output. No campaign experiment actually crossed the safety boundary or produced an observed rollback. Therefore rollback behavior remained untested. In the sealed blind predictions, I nevertheless made strong rollback assumptions for Q04, Q09, Q10, and Q12 and partial/order-dependent rollback assumptions for Q07 and Q08. Those were extrapolations from the risk trend, not findings from the campaign.

The anonymous-catalyst and categorical-solvent scope statements were respected. The experiments supported the practical importance of both categories, but they could not validate any real chemical identity or real-solvent property mechanism. The claim that experimental evidence should dominate the supplied model was supported operationally: following the data downward from 420 K produced better observed scores.

## 2. Experiments that formed or changed the interpretation

Batch 1 was chosen principally from the supplied reference context. It established an active baseline for water and Catalyst B at 420 K, but the choice was not yet data-driven within this campaign.

Batches 2–4 were the first genuinely diagnostic block. Holding water, 420 K, and 3300 s fixed while changing catalyst showed that Catalyst B was superior locally. Final scores were 0.3281 for A, 0.3337 for C, 0.3561 for D, and 0.4065 for B. This changed the catalyst question from an open categorical uncertainty into a local ranking, although without replication or loading dependence.

Batches 5–7 formed the solvent interpretation. At the same Catalyst B/420 K condition, ethanol, acetonitrile, and toluene all gave lower selectivity, more byproduct and degradation, higher risk, and lower scores than water. Batch 6 was especially informative: acetonitrile reached reported conversion 1.0000 but only yield 0.6545, selectivity 0.6427, and score 0.3092. This strongly changed my view from “conversion is the main limitation” to “partitioning after or alongside reactant disappearance is central.”

Batches 8–11 most directly overturned the initial temperature direction. The monotonic improvement in safe score from 430 K down to 390 K, accompanied by declining conversion but improving selectivity and safety, created the trade-off model described in K1. Batch 11 became the recommendation because it had the highest observed final score, not because 390 K had been predicted in advance.

Batch 12 was the only deliberate residence-time perturbation. Relative to Batch 11, extending 390 K operation from 3300 to 4500 s raised conversion from 0.8820 to 0.9427 but reduced selectivity from 0.8289 to 0.7632 and raised byproduct from 0.1606 to 0.2073. This was the strongest evidence behind K1’s proposed secondary or time-dependent side chemistry. It did not, by itself, prove product degradation.

Several choices rested on weakly tested assumptions. I kept reagent amount, catalyst loading, solvent volume, addition order, and 350 rpm constant because the supplied reference context made them convenient, not because they had been optimized. The exact temperature ladder, the decision not to test below 390 K, and the selection of 4500 s for Batch 12 were judgment calls. No-quench operation was also an unverified default. In the blind questions, assuming that 400 rpm was equivalent to 350 rpm was another unsupported extrapolation.

## 3. Important competing mechanisms and explanations

The leading kinetic interpretation remains a productive reaction competing with side reactions, possibly followed by degradation of desired product. A schematic version is R→P, R→B, and P→D. It explains why high conversion can coexist with modest yield and why longer or hotter exposure can worsen selectivity.

The principal competing explanations are:

- **Parallel reaction only:** R may partition directly between desired product and byproduct, with no significant P→D step. Batch 12 does not distinguish this from product degradation because unreacted R was still present at 3300 s.
- **Sequential product degradation:** Desired product accumulates and then degrades during prolonged exposure. The Batch 11–12 change is consistent with this, but no isolated-product or within-batch species trajectory was measured.
- **Temperature-dependent equilibrium:** Cooling could favor the desired species or reduce reversal. Equilibrium alone cannot readily explain all byproduct and degradation signals, but it could contribute.
- **Catalyst deactivation or selectivity drift:** The time effect could arise because Catalyst B changes state during prolonged heating rather than because product itself decomposes.
- **Transport or thermal-lag effects:** Setpoint temperature was not identical to instantaneous liquid temperature. Apparent kinetics may partly reflect approach to temperature rather than intrinsic rate constants.
- **Solvent-dependent assay response:** Some solvent ranking could come from matrix effects. Coordinated changes across several metrics argue for real benchmark-state differences, but the campaign did not independently validate response factors.
- **Peak-risk versus accumulated-risk models:** Batch 11 and Batch 12 had nearly identical reported risks despite different durations, favoring a peak-state interpretation. Only one temperature/time pair tested that question, so accumulated exposure cannot be excluded generally.

The experiments distinguish local categorical performance reasonably well: Catalyst B outperformed A, C, and D at the tested formulation, and water outperformed the other solvents at 420 K. They also establish that lower temperature improved the observed objective between 390 and 430 K. They do not identify rate constants, activation energies, the molecular origin of byproduct signals, or whether the time penalty is parallel reaction, sequential degradation, catalyst change, or some combination.

## 4. One additional complete experiment

If only one additional legal complete experiment were allowed, I would run the Batch 11 formulation at 380 K for 3300 s and 350 rpm: 0.005 L water, 0.003 mol reagent, and 0.000525 mol Catalyst B. I would take one HPLC measurement after heating, terminate, and obtain the required final assay.

This experiment addresses the most important untested boundary in both the recommendation and K1: every systematic temperature result ended at 390 K, so the lower side of the apparent optimum was never observed.

Possible interpretations would be:

- If the final score exceeded 0.4516 while risk, byproduct, and degradation continued to fall without a severe yield loss, I would move the favorable region below 390 K and reject the suggestion that 390–400 K brackets the optimum.
- If conversion and yield fell enough that score dropped materially despite higher selectivity, it would support a genuine turnover near 390–400 K.
- If conversion remained unexpectedly high, the effective kinetics would be less temperature-sensitive than inferred, or thermal history rather than nominal setpoint would require more emphasis.
- If byproduct or degradation rose at 380 K, the monotonic thermal-side-reaction explanation would be inadequate; equilibrium, catalyst state, or measurement effects would become more competitive.
- A large disagreement between HPLC and the final assay would strengthen concern about measurement or post-sampling effects rather than clean kinetic interpretation.

An exact Batch 11 replicate would be better for estimating repeatability, but the 380 K experiment provides more decision-relevant information about whether the selected point lies near an optimum or merely at the edge of the explored grid.

## 5. Trade-off between identifiability and score optimization

The first seven batches devoted substantial resources to identifiability. Catalyst A, C, and D and the three non-water solvents were expected to risk lower scores, but they established which categorical choices mattered. Batches 2–7 therefore sacrificed immediate score optimization for a one-factor-at-a-time map.

After water and Catalyst B emerged, the design shifted strongly toward optimization. Batches 8–11 concentrated on a temperature ladder using the best observed formulation. This was appropriate for the stated safe-score goal and efficiently found better operating points. It also narrowed mechanistic coverage: catalyst loading, concentration, stirring, addition order, quenching, and catalyst–solvent interactions were left unexplored.

Batch 12 partially restored mechanistic content through a duration perturbation, but it remained close to the best formulation. Its lower score of 0.4448 was a modest optimization sacrifice that yielded evidence about residence-time penalties.

The largest sacrifice of identifiability was the absence of replication. Because all 12 final assays were spent on distinct conditions, I could not separate process variability from true differences. That matters especially for Batch 10 versus Batch 11, whose scores differed by only about 0.0034. The design also used only one nonfinal HPLC per batch; this aided monitoring but did not provide a genuine time course.

Conversely, some identification effort was broader than necessary for maximizing score. Once Catalyst B and water looked strong, additional catalyst and solvent categories were unlikely to beat the baseline, yet they consumed six batches. This was defensible research exploration, but a purely optimization-oriented campaign would have moved earlier into temperature, time, or loading refinement.

## 6. Underused evidence and weaknesses in the blind predictions

The public characterization artifacts contained richer raw signals than I used. I relied mainly on processed estimates and did not inspect spectral shapes, peak assignments, calibration flags, or mass-balance details. Those data might have clarified whether solvent effects were chemical or analytical and whether degradation represented a distinct signal population.

I also underused the differences between HPLC and final assay. K1 acknowledged them qualitatively, but I did not quantify cross-instrument bias or propagate it into comparisons. Actual temperature-state deltas were recorded for several later batches, yet I did not fit a thermal response model. Likewise, I did not attempt to infer even an approximate score function from yield, selectivity, byproduct, degradation, cost, and risk.

The least reliable blind predictions are Q04, Q09, Q10, and Q12. Their point estimates depended on a temperature-bound rollback that was never observed during the campaign. For Q04 and Q12, I predicted nearly unreacted final states after presumed rollback; if the environment instead accepts the heat with a violation, clips temperature, or commits partial heating, the outcomes could be close to the opposite end of the intervals. The distributions are plausibly multimodal, which a single central interval represents poorly.

Q07 and Q08 are also highly uncertain. I assumed atomic rollback of the 450 K segment and therefore predicted almost identical results for the two orders. The campaign never tested rollback atomicity, thermal memory, or order dependence. Their conversion and yield intervals may be too narrow if partial high-temperature execution is possible.

Q02 and Q10 rely on an untested assumption that quenching has little effect beyond arresting residual chemistry. No campaign batch included a quench. Their intervals should have allowed a larger effect on risk or final composition.

Q11 extrapolates below the tested temperature range to 370 K and combines that with a longer 5700 s duration in acetonitrile. Its score interval of 0.31–0.46 and conversion interval of 0.73–0.95 may be overconfident because both temperature and duration are out of the directly observed local domain.

Q05 and Q06 extrapolate the time response in acetonitrile using only the water comparison between Batches 11 and 12. Solvent–time interactions were not measured. Even Q01, the strongest prediction because it resembles Batch 6, assumes that raising stirring from 350 to 400 rpm is negligible.

These weaknesses are consistent with K1’s stated applicability limits: quenching, stirring effects, temperatures below 390 K, high-temperature rollback, and broad duration dependence were explicitly unidentified. The inconsistency lies not in failing to mention those uncertainties, but in sometimes assigning narrow or strongly one-sided blind intervals despite them.

## 7. Limitations of the sealed recommendation

Batch 11 was the sample-in highest scorer among the 12 completed batches. It was not proved globally optimal, locally optimal, or even statistically superior to Batch 10. The score difference between Batch 11 at 390 K and Batch 10 at 400 K was only 0.0034, smaller than a prudent estimate of combined process and assay uncertainty. Batch 12 also showed that modest changes in duration can shift selectivity and score.

The recommendation has several specific limitations:

- It rests on a single realization of the exact condition.
- The lower-temperature side was not explored.
- Time was tested only at 3300 and 4500 s at 390 K.
- Catalyst and reagent loading, dilution, stirring, addition order, and quenching were not optimized.
- Catalyst–solvent and catalyst–temperature interactions were not mapped.
- The safety margin was favorable in Batch 11, but robustness to thermal overshoot and formulation variation was not tested.
- Anonymous benchmark categories prevent transfer to a named real catalyst or real synthesis.

Repeatability should first be tested with multiple independent exact replicates of Batch 11, using the same final assay and at least occasional intermediate HPLC. Local robustness should then be assessed with a small design around approximately 385–405 K, 3000–3600 s, and nearby stirring rates and catalyst loadings. Replication at the center is essential to distinguish curvature from noise.

Material robustness requires repeating the local design across solvent and catalyst categories rather than assuming additive effects. Cross-world robustness would require independent benchmark worlds or seeds because hidden categorical activity and thermal-response parameters may shift. Real-world transfer would require empirical chemical identification, physical safety characterization, and calibrated analytical methods; nothing in this synthetic benchmark establishes that transfer.

The defensible conclusion is therefore: Batch 11 was the best observed member of the tested set and had a substantial observed safety margin. The stronger claim that it is the true optimum, a robust optimum, or transferable beyond this local benchmark is unsupported.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 106.2 | none | 0 |
| Q | yes | 0 | 115.8 | none | 0 |
| K2 | yes | 0 | 107.9 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1781 | 0.4167 | 0.1750 | 0.8665 |
| conversion | 0.4016 | 0.2500 | 0.2375 | 2.6808 |
| safety_risk | 0.1125 | 0.5833 | 0.1331 | 0.5019 |
| score | 0.1176 | 0.6000 | 0.1463 | 0.6118 |
| selectivity | 0.1924 | 0.5833 | 0.3175 | 0.5327 |
| yield | 0.2512 | 0.5667 | 0.1837 | 1.6793 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3680 | 0.3300 | 0.4100 | 0.3661 | 0.3711, 0.3582, 0.3829, 0.3546, 0.3637 |
| conversion | 0.9950 | 0.9600 | 1.0000 | 0.9983 | 1.0000, 1.0000, 1.0000, 0.9986, 0.9928 |
| safety_risk | 0.3270 | 0.3100 | 0.3450 | 0.3271 | 0.3271, 0.3271, 0.3271, 0.3271, 0.3271 |
| score | 0.3090 | 0.2700 | 0.3500 | 0.3117 | 0.3089, 0.3133, 0.3128, 0.3125, 0.3110 |
| selectivity | 0.6430 | 0.5900 | 0.6900 | 0.6454 | 0.6395, 0.6416, 0.6482, 0.6527, 0.6453 |
| yield | 0.6550 | 0.6100 | 0.7000 | 0.6395 | 0.6358, 0.6456, 0.6401, 0.6368, 0.6391 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3600 | 0.3200 | 0.4000 | 0.3678 | 0.3770, 0.3726, 0.3588, 0.3768, 0.3536 |
| conversion | 0.9950 | 0.9600 | 1.0000 | 0.9992 | 1.0000, 1.0000, 0.9960, 1.0000, 1.0000 |
| safety_risk | 0.3270 | 0.3100 | 0.3450 | 0.1558 | 0.1558, 0.1558, 0.1558, 0.1558, 0.1558 |
| score | 0.3150 | 0.2750 | 0.3600 | 0.3843 | 0.3838, 0.3841, 0.3876, 0.3844, 0.3815 |
| selectivity | 0.6500 | 0.6000 | 0.7000 | 0.6378 | 0.6410, 0.6229, 0.6441, 0.6452, 0.6359 |
| yield | 0.6570 | 0.6100 | 0.7050 | 0.6412 | 0.6377, 0.6497, 0.6463, 0.6367, 0.6353 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.2700 | 0.3900 | 0.3044 | 0.3118, 0.2995, 0.2990, 0.3073, 0.3044 |
| conversion | 0.9100 | 0.8200 | 0.9700 | 0.9949 | 1.0000, 0.9882, 0.9993, 0.9868, 1.0000 |
| safety_risk | 0.1950 | 0.1700 | 0.2250 | 0.1950 | 0.1950, 0.1950, 0.1950, 0.1950, 0.1950 |
| score | 0.3500 | 0.2900 | 0.4100 | 0.4036 | 0.4011, 0.4007, 0.4038, 0.4111, 0.4016 |
| selectivity | 0.6800 | 0.6100 | 0.7500 | 0.6944 | 0.6873, 0.6875, 0.6946, 0.7114, 0.6911 |
| yield | 0.6350 | 0.5600 | 0.7000 | 0.6910 | 0.6879, 0.6895, 0.6901, 0.7010, 0.6867 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.0250 | 0.0000 | 0.2000 | 0.4313 | 0.4386, 0.4318, 0.4285, 0.4243, 0.4336 |
| conversion | 0.0400 | 0.0000 | 0.3500 | 0.9955 | 1.0000, 0.9995, 1.0000, 1.0000, 0.9781 |
| safety_risk | 0.1320 | 0.1150 | 0.3500 | 0.4212 | 0.4212, 0.4212, 0.4212, 0.4212, 0.4212 |
| score | 0.0200 | 0.0000 | 0.1600 | 0.2325 | 0.2360, 0.2291, 0.2318, 0.2346, 0.2309 |
| selectivity | 0.1800 | 0.0000 | 0.6500 | 0.5807 | 0.5940, 0.5696, 0.5798, 0.5793, 0.5809 |
| yield | 0.0200 | 0.0000 | 0.2000 | 0.5884 | 0.5878, 0.5859, 0.5861, 0.5936, 0.5887 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1600 | 0.3100 | 0.1919 | 0.1999, 0.1936, 0.1956, 0.1847, 0.1857 |
| conversion | 0.7900 | 0.6700 | 0.8900 | 0.9641 | 0.9653, 0.9636, 0.9659, 0.9650, 0.9609 |
| safety_risk | 0.3220 | 0.2950 | 0.3450 | 0.3273 | 0.3273, 0.3273, 0.3273, 0.3273, 0.3273 |
| score | 0.3400 | 0.2700 | 0.4100 | 0.4064 | 0.4049, 0.4081, 0.4049, 0.4106, 0.4033 |
| selectivity | 0.7200 | 0.6400 | 0.7900 | 0.8032 | 0.8034, 0.8204, 0.7967, 0.8219, 0.7738 |
| yield | 0.5700 | 0.4800 | 0.6500 | 0.7825 | 0.7786, 0.7763, 0.7826, 0.7812, 0.7941 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4700 | 0.4000 | 0.5500 | 0.5074 | 0.5074, 0.5103, 0.5024, 0.5104, 0.5064 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9997 | 1.0000, 1.0000, 0.9987, 1.0000, 1.0000 |
| safety_risk | 0.3290 | 0.3100 | 0.3470 | 0.3268 | 0.3268, 0.3268, 0.3268, 0.3268, 0.3268 |
| score | 0.2450 | 0.1800 | 0.3100 | 0.2221 | 0.2215, 0.2177, 0.2267, 0.2202, 0.2244 |
| selectivity | 0.5400 | 0.4600 | 0.6200 | 0.5033 | 0.4978, 0.4899, 0.5120, 0.5071, 0.5098 |
| yield | 0.5800 | 0.4900 | 0.6500 | 0.5074 | 0.5094, 0.5047, 0.5138, 0.5001, 0.5090 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1900 | 0.1100 | 0.2900 | 0.4056 | 0.3992, 0.4027, 0.3978, 0.4203, 0.4080 |
| conversion | 0.6900 | 0.5000 | 0.8500 | 0.9957 | 1.0000, 0.9892, 1.0000, 0.9894, 1.0000 |
| safety_risk | 0.1940 | 0.1650 | 0.3500 | 0.4329 | 0.4329, 0.4329, 0.4329, 0.4329, 0.4329 |
| score | 0.3500 | 0.2400 | 0.4300 | 0.2409 | 0.2417, 0.2395, 0.2409, 0.2380, 0.2446 |
| selectivity | 0.7400 | 0.6200 | 0.8300 | 0.6144 | 0.6243, 0.6129, 0.6092, 0.6034, 0.6225 |
| yield | 0.5100 | 0.3600 | 0.6300 | 0.6023 | 0.5969, 0.6014, 0.6043, 0.6034, 0.6053 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1900 | 0.1100 | 0.2800 | 0.3999 | 0.4150, 0.4019, 0.3945, 0.4007, 0.3876 |
| conversion | 0.6900 | 0.5000 | 0.8500 | 0.9967 | 1.0000, 0.9900, 0.9935, 1.0000, 1.0000 |
| safety_risk | 0.1940 | 0.1650 | 0.3500 | 0.2015 | 0.2015, 0.2015, 0.2015, 0.2015, 0.2015 |
| score | 0.3500 | 0.2400 | 0.4300 | 0.3495 | 0.3550, 0.3465, 0.3441, 0.3457, 0.3562 |
| selectivity | 0.7400 | 0.6200 | 0.8300 | 0.6174 | 0.6125, 0.6215, 0.6070, 0.6070, 0.6390 |
| yield | 0.5100 | 0.3600 | 0.6300 | 0.6112 | 0.6271, 0.6029, 0.6049, 0.6074, 0.6138 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.0200 | 0.0000 | 0.1800 | 0.2157 | 0.2139, 0.2192, 0.2065, 0.2248, 0.2142 |
| conversion | 0.0400 | 0.0000 | 0.3800 | 0.9822 | 0.9779, 0.9743, 0.9871, 0.9816, 0.9901 |
| safety_risk | 0.1320 | 0.1150 | 0.3500 | 0.4014 | 0.4014, 0.4014, 0.4014, 0.4014, 0.4014 |
| score | 0.0200 | 0.0000 | 0.1800 | 0.3688 | 0.3704, 0.3654, 0.3661, 0.3703, 0.3717 |
| selectivity | 0.1800 | 0.0000 | 0.6800 | 0.7845 | 0.7914, 0.7629, 0.7803, 0.7954, 0.7923 |
| yield | 0.0200 | 0.0000 | 0.2200 | 0.7792 | 0.7799, 0.7863, 0.7739, 0.7764, 0.7795 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.0180 | 0.0000 | 0.1700 | 0.2145 | 0.2078, 0.2005, 0.2088, 0.2291, 0.2264 |
| conversion | 0.0400 | 0.0000 | 0.3800 | 0.9863 | 0.9887, 0.9803, 0.9816, 0.9811, 1.0000 |
| safety_risk | 0.1300 | 0.1100 | 0.3500 | 0.1883 | 0.1883, 0.1883, 0.1883, 0.1883, 0.1883 |
| score | 0.0220 | 0.0000 | 0.1900 | 0.4623 | 0.4647, 0.4590, 0.4625, 0.4649, 0.4606 |
| selectivity | 0.1900 | 0.0000 | 0.6900 | 0.7874 | 0.7957, 0.7843, 0.7856, 0.7886, 0.7828 |
| yield | 0.0210 | 0.0000 | 0.2300 | 0.7789 | 0.7791, 0.7741, 0.7815, 0.7858, 0.7740 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2700 | 0.1900 | 0.3600 | 0.4056 | 0.3998, 0.4141, 0.4004, 0.4077, 0.4058 |
| conversion | 0.8600 | 0.7300 | 0.9500 | 0.9898 | 0.9902, 0.9783, 0.9875, 1.0000, 0.9929 |
| safety_risk | 0.1500 | 0.1200 | 0.1900 | 0.1568 | 0.1568, 0.1568, 0.1568, 0.1568, 0.1568 |
| score | 0.3900 | 0.3100 | 0.4600 | 0.3583 | 0.3600, 0.3543, 0.3578, 0.3581, 0.3614 |
| selectivity | 0.7200 | 0.6300 | 0.8000 | 0.6037 | 0.6056, 0.6084, 0.6044, 0.5914, 0.6089 |
| yield | 0.6300 | 0.5300 | 0.7100 | 0.5977 | 0.6005, 0.5876, 0.5965, 0.6024, 0.6014 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.0200 | 0.0000 | 0.4500 | 0.6871 | 0.6912, 0.6734, 0.6842, 0.7000, 0.6867 |
| conversion | 0.0300 | 0.0000 | 0.3500 | 0.9967 | 0.9995, 0.9953, 0.9901, 1.0000, 0.9987 |
| safety_risk | 0.1320 | 0.1150 | 0.3500 | 0.4328 | 0.4328, 0.4328, 0.4328, 0.4328, 0.4328 |
| score | 0.0150 | 0.0000 | 0.1400 | 0.0681 | 0.0730, 0.0656, 0.0644, 0.0697, 0.0677 |
| selectivity | 0.1500 | 0.0000 | 0.5500 | 0.3424 | 0.3558, 0.3442, 0.3324, 0.3403, 0.3390 |
| yield | 0.0150 | 0.0000 | 0.1800 | 0.3454 | 0.3486, 0.3383, 0.3441, 0.3500, 0.3460 |

## Recommendation retest

- Selected source batch: `11`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1606 | 0.1602 | -0.0004 |
| conversion | 0.8820 | 0.8853 | 0.0033 |
| cost | 0.6557 | 0.6557 | 0.0000 |
| degradation_warning | 0.0780 | 0.0853 | 0.0074 |
| safety_risk | 0.1531 | 0.1531 | 0.0000 |
| score | 0.4516 | 0.4475 | -0.0041 |
| selectivity | 0.8289 | 0.8200 | -0.0089 |
| virtual_spectrum_summary | 0.1234 | 0.1265 | 0.0031 |
| yield | 0.7265 | 0.7211 | -0.0054 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
