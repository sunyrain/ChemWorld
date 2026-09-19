# RX-W03--S--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W03`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v9`
- Recovery version: `recovery-v9-parallel4`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 gave the strongest observed endpoint yield and campaign score while staying below the safety limit; its Catalyst B/acetonitrile, 350 K for 3600 s, followed by prompt quench also directly controls the elevated-temperature residence time.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.0838 | 0.5945 | 0.1548 | 0.0812 | 0.0007 | 0.0856 | 0.0591 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.2464 | 0.8493 | 0.2844 | 0.0516 | 0.0000 | 0.1011 | 0.1938 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.1437 | 0.6914 | 0.2083 | 0.0609 | 0.0055 | 0.0916 | 0.1099 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.1258 | 0.7632 | 0.1795 | 0.0316 | 0.0040 | 0.0898 | 0.1187 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.2830 | 0.8050 | 0.3513 | 0.0703 | 0.0180 | 0.1306 | 0.1908 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.3929 | 0.8351 | 0.4799 | 0.0827 | 0.0253 | 0.1606 | 0.2417 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.2681 | 0.6965 | 0.3807 | 0.1134 | 0.0254 | 0.1613 | 0.1468 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 310 K x 1800 s @ 600 rpm | no | 0.2691 | 0.8406 | 0.3394 | 0.0518 | 0.0135 | 0.1446 | 0.1867 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 600 s @ 600 rpm | no | 0.2018 | 0.8874 | 0.2310 | 0.0302 | 0.0000 | 0.1421 | 0.1617 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.5108 | 0.8114 | 0.6110 | 0.1147 | 0.0567 | 0.1778 | 0.2883 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6155 | 0.6994 | 0.8576 | 0.2413 | 0.1636 | 0.1983 | 0.3176 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | yes | 0.6209 | 0.7258 | 0.8499 | 0.2461 | 0.1884 | 0.1915 | 0.3286 |

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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 330
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
    "byproduct_signal": 0.08120311796665192,
    "conversion": 0.15475726127624512,
    "cost": 1.0,
    "degradation_warning": 0.00074405298801139,
    "safety_risk": 0.08562304824590683,
    "score": 0.05908169224858284,
    "selectivity": 0.594473659992218,
    "virtual_spectrum_summary": 0.044996537268161774,
    "yield": 0.08379480242729187
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
      "target_temperature_K": 330
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
    "byproduct_signal": 0.05155857652425766,
    "conversion": 0.2843819558620453,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.10112175345420837,
    "score": 0.1938353329896927,
    "selectivity": 0.8493396639823914,
    "virtual_spectrum_summary": 0.028357217088341713,
    "yield": 0.24641753733158112
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
      "target_temperature_K": 330
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
    "byproduct_signal": 0.060921989381313324,
    "conversion": 0.20832312107086182,
    "cost": 1.0,
    "degradation_warning": 0.0055262623354792595,
    "safety_risk": 0.0916384682059288,
    "score": 0.10992903262376785,
    "selectivity": 0.6914199590682983,
    "virtual_spectrum_summary": 0.03599391132593155,
    "yield": 0.1436976045370102
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
      "target_temperature_K": 330
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
    "byproduct_signal": 0.03162132576107979,
    "conversion": 0.17948226630687714,
    "cost": 1.0,
    "degradation_warning": 0.00404302217066288,
    "safety_risk": 0.08977891504764557,
    "score": 0.11866015195846558,
    "selectivity": 0.7632351517677307,
    "virtual_spectrum_summary": 0.019211089238524437,
    "yield": 0.12575912475585938
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
      "target_temperature_K": 330
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
    "byproduct_signal": 0.07031460106372833,
    "conversion": 0.3512974679470062,
    "cost": 1.0,
    "degradation_warning": 0.017998185008764267,
    "safety_risk": 0.13058242201805115,
    "score": 0.19083666801452637,
    "selectivity": 0.8050225377082825,
    "virtual_spectrum_summary": 0.04677221179008484,
    "yield": 0.28303343057632446
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
      "target_temperature_K": 330
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
    "byproduct_signal": 0.0827295184135437,
    "conversion": 0.4799017012119293,
    "cost": 1.0,
    "degradation_warning": 0.02534300647675991,
    "safety_risk": 0.16062650084495544,
    "score": 0.241663858294487,
    "selectivity": 0.8351427316665649,
    "virtual_spectrum_summary": 0.056905586272478104,
    "yield": 0.39292481541633606
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
      "target_temperature_K": 330
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
    "byproduct_signal": 0.11335616558790207,
    "conversion": 0.3806855380535126,
    "cost": 1.0,
    "degradation_warning": 0.025350509211421013,
    "safety_risk": 0.16129063069820404,
    "score": 0.1468474119901657,
    "selectivity": 0.6964609622955322,
    "virtual_spectrum_summary": 0.07375361770391464,
    "yield": 0.268110990524292
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
      "target_temperature_K": 310
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
    "byproduct_signal": 0.05176897346973419,
    "conversion": 0.3394482135772705,
    "cost": 1.0,
    "degradation_warning": 0.013514013960957527,
    "safety_risk": 0.14455068111419678,
    "score": 0.18666799366474152,
    "selectivity": 0.8405748009681702,
    "virtual_spectrum_summary": 0.034554243087768555,
    "yield": 0.2690682113170624
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
      "duration_s": 600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
    "byproduct_signal": 0.03016888163983822,
    "conversion": 0.23102730512619019,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.14208269119262695,
    "score": 0.16173045337200165,
    "selectivity": 0.8874207139015198,
    "virtual_spectrum_summary": 0.016592884436249733,
    "yield": 0.20177438855171204
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
    "byproduct_signal": 0.11474378407001495,
    "conversion": 0.6109775304794312,
    "cost": 1.0,
    "degradation_warning": 0.056708455085754395,
    "safety_risk": 0.17780271172523499,
    "score": 0.28827324509620667,
    "selectivity": 0.8114346861839294,
    "virtual_spectrum_summary": 0.088627889752388,
    "yield": 0.5108200907707214
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "gc",
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
    "byproduct_signal": 0.24131342768669128,
    "conversion": 0.857618510723114,
    "cost": 1.0,
    "degradation_warning": 0.1635638326406479,
    "safety_risk": 0.1983037292957306,
    "score": 0.3175692856311798,
    "selectivity": 0.6993818283081055,
    "virtual_spectrum_summary": 0.20632611215114594,
    "yield": 0.6154966354370117
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.24613524973392487,
    "conversion": 0.8499048352241516,
    "cost": 1.0,
    "degradation_warning": 0.18840131163597107,
    "safety_risk": 0.19154542684555054,
    "score": 0.32858553528785706,
    "selectivity": 0.7257913947105408,
    "virtual_spectrum_summary": 0.22015497088432312,
    "yield": 0.6208566427230835
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

I completed 12 batches using a common charge of 0.040 mol limiting reagent, 0.080 L solvent, and 0.005 mol catalyst, with stirring at 600 rpm. Every batch received a terminal final assay. The study varied catalyst identity, solvent identity, temperature, duration, and—in the final paired comparison—whether the hot mixture was quenched before termination. The catalyst labels are anonymous benchmark formulations, so this report assigns functional roles but does not claim real chemical identities.

The assay quantities are dimensionless processed estimates. I interpret conversion as disappearance of the public reactant, yield as target formation relative to the initial reactant, selectivity as the target fraction of converted material, and the byproduct and degradation channels as aggregate proxies. This interpretation is supported by the approximate relationship yield ≈ conversion × selectivity, although noise and channel calibration prevent exact equality.

2. Observed batch results

Final-assay results were:

- Batch 1: water, Catalyst A, 330 K, 1800 s. Conversion 0.1548, selectivity 0.5945, yield 0.0838, byproduct 0.0812, degradation 0.0007, safety risk 0.0856.
- Batch 2: water, Catalyst B, 330 K, 1800 s. Conversion 0.2844, selectivity 0.8493, yield 0.2464, byproduct 0.0516, degradation 0, risk 0.1011.
- Batch 3: water, Catalyst C, 330 K, 1800 s. Conversion 0.2083, selectivity 0.6914, yield 0.1437, byproduct 0.0609, degradation 0.0055, risk 0.0916.
- Batch 4: water, Catalyst D, 330 K, 1800 s. Conversion 0.1795, selectivity 0.7632, yield 0.1258, byproduct 0.0316, degradation 0.0040, risk 0.0898.
- Batch 5: ethanol, Catalyst B, 330 K, 1800 s. Conversion 0.3513, selectivity 0.8050, yield 0.2830, byproduct 0.0703, degradation 0.0180, risk 0.1306.
- Batch 6: acetonitrile, Catalyst B, 330 K, 1800 s. Conversion 0.4799, selectivity 0.8351, yield 0.3929, byproduct 0.0827, degradation 0.0253, risk 0.1606.
- Batch 7: toluene, Catalyst B, 330 K, 1800 s. Conversion 0.3807, selectivity 0.6965, yield 0.2681, byproduct 0.1134, degradation 0.0254, risk 0.1613.
- Batch 8: acetonitrile, Catalyst B, 310 K, 1800 s. Conversion 0.3394, selectivity 0.8406, yield 0.2691, byproduct 0.0518, degradation 0.0135, risk 0.1446.
- Batch 9: acetonitrile, Catalyst B, 350 K, 600 s. Conversion 0.2310, selectivity 0.8874, yield 0.2018, byproduct 0.0302, degradation 0, risk 0.1421.
- Batch 10: acetonitrile, Catalyst B, 350 K, 1800 s. Conversion 0.6110, selectivity 0.8114, yield 0.5108, byproduct 0.1147, degradation 0.0567, risk 0.1778.
- Batch 11: acetonitrile, Catalyst B, 350 K, 3600 s, no quench. Conversion 0.8576, selectivity 0.6994, yield 0.6155, byproduct 0.2413, degradation 0.1636, risk 0.1983.
- Batch 12: the same nominal reaction conditions as Batch 11, followed by quenching. Conversion 0.8499, selectivity 0.7258, yield 0.6209, byproduct 0.2461, degradation 0.1884, risk 0.1915.

All observed risks remained below the task limit of 0.35.

3. Proposed reaction network

The smallest network consistent with the observations is a reversible target-forming reaction combined with parallel and consecutive side reactions:

R ⇌ P
R → B
P → B and/or D

Here R is the limiting reactant, P is the desired target, B is the aggregate competing-product channel, and D is the material responsible for the degradation warning. I retain the reverse P → R channel because the supplied structural prior stated that it may be appreciable, but the campaign did not isolate it experimentally. The observed rise in conversion through 3600 s does not itself prove reversibility.

A useful kinetic representation is:

r1 = a·k1,c,s(T)·R
r−1 = a·k−1,c,s(T)·P
rb = a·kb,c,s(T)·R
rp = kp,s(T)·P
rd = kd,s(T)·P

dR/dt = −r1 + r−1 − rb
dP/dt = r1 − r−1 − rp − rd
dB/dt = rb + rp
dD/dt = rd

da/dt = −kdeact,s(T)·a

The variable a is the fraction of active catalyst. Catalyst and solvent labels enter as categorical multipliers because their real molecular properties are unknown. The rate constants can be written in Arrhenius form, for example k(T) = A·exp(−E/RT), but the present data do not justify separate numerical A and E values for every channel.

The deactivation equation is included as a plausible mechanism, not as an identified fact. A model with constant a fits the observed direction of change equally well over the measured durations. Likewise, B may represent several chemically distinct products rather than one species.

4. Catalyst effects

Batches 1–4 form a controlled catalyst comparison in water at 330 K for 1800 s. Catalyst B was clearly the most active and target-selective formulation: its conversion was 0.2844 and yield 0.2464, compared with conversions of 0.1548–0.2083 and yields of 0.0838–0.1437 for A, C, and D. Catalyst B also had selectivity 0.8493, much higher than Catalyst A at 0.5945.

This changed my initial explanation from one in which temperature and equilibrium might dominate to one in which catalyst identity strongly controls both the desired and competing activation barriers. Catalyst B is not merely faster: its selectivity advantage over A and C indicates preferential acceleration of target formation or suppression of a competing channel. Catalyst D produced the lowest observed byproduct signal in this comparison, 0.0316, but its low conversion limited target yield.

Only one loading, 0.005 mol, was tested. Consequently, the catalyst order, saturation behavior, turnover frequency, and loading dependence are not identifiable. No uncatalyzed control was run. Catalyst deactivation is also not directly measured.

5. Solvent effects and coupling to catalyst

Batches 2, 5, 6, and 7 compared all four solvents with Catalyst B at 330 K for 1800 s. The observed activity order was acetonitrile > toluene > ethanol > water by conversion. Acetonitrile gave the largest conversion, 0.4799, and largest yield, 0.3929. Toluene gave appreciable conversion, 0.3807, but poorer selectivity, 0.6965, and the largest byproduct signal in this solvent comparison, 0.1134. Ethanol was intermediate. Water preserved good selectivity but reacted more slowly.

I therefore treat solvent as coupled to both the target-forming rate and the side-reaction rates, rather than as a single multiplicative acceleration factor. In the proposed equations this appears as separate solvent factors on k1, kb, kp, and kd. Acetonitrile favors productive conversion under the studied conditions, whereas toluene appears to favor competing conversion more strongly.

Risk was also solvent-dependent: the water/Catalyst B batch had risk 0.1011, while acetonitrile and toluene were near 0.16. Thus the same solvent variable couples reaction performance to the thermal/safety response. These are benchmark categorical effects; I do not infer polarity, boiling point, or a real molecular solvation mechanism from them.

6. Temperature and thermal history

With Catalyst B in acetonitrile for 1800 s, conversion increased monotonically with target temperature:

- 310 K, Batch 8: 0.3394 conversion and 0.2691 yield.
- 330 K, Batch 6: 0.4799 conversion and 0.3929 yield.
- 350 K, Batch 10: 0.6110 conversion and 0.5108 yield.

A deliberately crude irreversible first-order reduction, kapp = −ln(1−X)/t, gives 2.30×10⁻⁴, 3.63×10⁻⁴, and 5.25×10⁻⁴ s⁻¹ at 310, 330, and 350 K. Treating those values as isothermal Arrhenius rates gives an apparent activation energy of about 18.6 kJ mol⁻¹ from the 310–350 K endpoints. This is an empirical local summary, not an identified elementary barrier: it assumes equilibrium conversion of one, ignores reverse reaction and side reactions, and compresses the heat-up trajectory into the target temperature.

The thermal operations recorded temperature changes of about +11.2 K for Batch 8, +30.4 to +30.5 K for the 330 K runs, and +47.5 to +48.8 K for the 350 K runs. The 600 s operation in Batch 9 recorded a slightly smaller rise than the longer 350 K operations. This implies that actual integrated thermal exposure, rather than nominal set point alone, matters. A suitable process model is

dT/dt = (Tset−T)/τheat + Qreaction/(mCp),

with every kinetic rate integrated over T(t). The data are insufficient to separate heat-transfer lag from reaction heat, and no full temperature trace was exposed.

7. Reaction time, competing conversion, and degradation

Batches 9–11 provide the clearest time series at nominally 350 K in acetonitrile with Catalyst B:

- 600 s: conversion 0.2310, selectivity 0.8874, yield 0.2018, byproduct 0.0302, degradation 0.
- 1800 s: conversion 0.6110, selectivity 0.8114, yield 0.5108, byproduct 0.1147, degradation 0.0567.
- 3600 s: conversion 0.8576, selectivity 0.6994, yield 0.6155, byproduct 0.2413, degradation 0.1636.

Longer thermal exposure therefore increases target yield but with sharply diminishing selectivity. Between 1800 and 3600 s, conversion rose by about 0.247 and yield by only about 0.105, while the byproduct and degradation channels increased substantially. This is strong evidence that the competing network accumulates with thermal dose.

The nonzero byproduct signal at 600 s supports a parallel R → B path. The increasingly prominent degradation warning at longer times additionally supports a consecutive P → D or reactive-intermediate → D path. A purely parallel two-product model could reproduce declining selectivity if its rates changed with time or temperature, but the delayed degradation signal makes a consecutive thermally activated channel more natural.

The data do not show a decrease in target yield by 3600 s, so I cannot locate the yield maximum. Extrapolation beyond 3600 s is hazardous: yield might continue rising slowly, plateau because of equilibrium or catalyst deactivation, or eventually decline as P is consumed by degradation.

8. Reverse reaction, equilibrium, and deactivation

The initial structural prior suggested an appreciable reverse channel. A reversible R ⇌ P step is compatible with the saturation-like curvature of conversion, but it is not uniquely demonstrated. Conversion was still increasing at the longest time, and no experiment began from isolated product or perturbed an apparent equilibrium.

At least four explanations remain observationally confounded:

1. A true reversible approach to an equilibrium conversion.
2. Ordinary irreversible kinetics approaching reagent exhaustion.
3. Catalyst deactivation that slows late conversion.
4. Growing competition that diverts remaining reactant or product.

The declining selectivity and rising degradation strongly establish growing competition, but they do not quantify k−1 or kdeact. The slightly increasing first-order kapp inferred from the 600, 1800, and 3600 s conversions at 350 K is more consistent with heat-up lag in the short batch than with severe early catalyst deactivation, but this is only qualitative evidence.

9. Quench and termination behavior

Batches 11 and 12 were nominal replicate reactions at 350 K for 3600 s, differing in that Batch 12 was quenched before termination. The quench recorded a 45 K temperature decrease over 56.1 s and reduced reported risk by 0.00676, from 0.1983 immediately before quench to 0.1915 afterward.

Relative to unquenched Batch 11, the final assay of Batch 12 differed by +0.0054 yield, +0.0264 selectivity, −0.0077 conversion, +0.0048 byproduct signal, and +0.0248 degradation warning. Because these are two separate batches and several differences are comparable to assay or process variability, I do not interpret the apparent selectivity increase as a proven chemical benefit of quenching.

Within Batch 12, the pre-quench HPLC reported conversion 0.8709, selectivity 0.7240, yield 0.6139, and byproduct 0.2426. The post-quench final assay reported 0.8499, 0.7258, 0.6209, and 0.2461. Cross-instrument calibration prevents assigning those small differences to quench chemistry. The defensible conclusion is that prompt quenching rapidly reduced temperature and observed safety risk while approximately preserving the chemical endpoint. Whether substantial reaction continues during a slow quench remains unresolved.

10. Compact predictive process description

Within the tested region, my working simulator would be:

initialize R = 1, P = B = D = 0, catalyst activity a = 1
choose categorical catalyst factors fc and solvent factors fs
for each short time increment dt:
    update T from the heat-transfer equation
    calculate target, reverse, parallel-side, and degradation rates using T, fc, fs, and a
    integrate R, P, B, D
    optionally reduce a through thermal deactivation
on quench:
    lower T according to the observed quench trajectory and continue integrating during the finite quench time
report:
    conversion ≈ 1−R
    yield ≈ P
    selectivity ≈ P/(1−R)
    byproduct signal = calibrated proxy for B
    degradation warning = calibrated proxy for D

This description predicts the observed qualitative couplings: Catalyst B raises productive rate; acetonitrile raises overall conversion; increasing temperature raises conversion; increasing time first raises target yield and then increasingly sacrifices selectivity to side products and degradation; quenching limits subsequent hot residence and lowers risk.

11. Applicability and uncertainty

The model is supported only near 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm. Temperature evidence spans 310–350 K, and time evidence spans 600–3600 s. Catalyst and solvent comparisons were performed only at 330 K for 1800 s, so interactions outside that point are extrapolations. No catalyst-loading, reagent-concentration, solvent-volume, stirring-rate, staged-addition, or uncatalyzed experiments were performed.

Each condition was ordinarily run once. Final-assay noise is smaller than many of the large catalyst, solvent, temperature, and time effects, but unmeasured batch-to-batch process variation remains. Intermediate HPLC and GC estimates use different calibration and noise models from the final assay. Sampling also removed small volumes before the endpoint. The anonymous byproduct and degradation channels do not reveal molecular identities or distinguish multiple products.

Consequently, the catalyst ranking, solvent ranking, positive temperature dependence, and time-dependent selectivity loss are well supported within the studied domain. The precise rate law, equilibrium constant, reverse rate, deactivation constant, number of byproducts, molecular mechanism, and behavior beyond 3600 s are not identified. The principal competing explanation is an irreversible parallel-plus-consecutive network without any reverse reaction; it explains the measured observations nearly as well as the reversible model. Product-spiking, denser time courses, matched quenched/unquenched replicates, catalyst-loading variation, and direct catalyst-activity measurements would be needed to distinguish those alternatives, but no such additional experiments were performed.

## Q — Blind predictions

### Overall rationale

Predictions use the Catalyst B/acetonitrile mechanism inferred from the completed campaign: catalyst-dependent reactant disappearance, approximately Arrhenius temperature acceleration, an initially high target branch, and a higher-temperature consecutive target-loss channel. Catalyst effects were scaled primarily by catalyst concentration. The score was calculated from the empirically identified public scoring relation: score = max(0, −0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion − 0.45·safety_risk). Intervals include assay noise, batch variability, uncertainty in catalyst scaling, and especially model-form uncertainty when extrapolating from the studied 310–350 K and 600–3600 s domain to 410–465 K and 14400 s.

### Q01

At 410 K the low catalyst concentration should still give substantial conversion in 1800 s, but the extrapolated thermally activated secondary loss lowers target selectivity relative to short 350 K batches.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2500 | 0.1000 | 0.5000 |
| conversion | 0.6100 | 0.4000 | 0.8000 |
| safety_risk | 0.1040 | 0.0700 | 0.1600 |
| score | 0.2060 | 0.0500 | 0.3700 |
| selectivity | 0.5900 | 0.3400 | 0.7900 |
| yield | 0.3600 | 0.1800 | 0.5600 |

### Q02

The long 410 K residence should nearly exhaust reactant even at low catalyst loading, while prolonged hot exposure is predicted to convert most initially formed target into competing or degraded material.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9900 | 0.7800 | 1.0000 |
| conversion | 0.9990 | 0.9300 | 1.0000 |
| safety_risk | 0.1400 | 0.0900 | 0.2300 |
| score | 0.0000 | 0.0000 | 0.1200 |
| selectivity | 0.0100 | 0.0000 | 0.1800 |
| yield | 0.0100 | 0.0000 | 0.1800 |

### Q03

The high Catalyst B concentration should drive almost complete conversion within 1800 s. Faster target formation competes with substantial 410 K degradation, producing a moderate endpoint yield rather than quantitative target accumulation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4900 | 0.2500 | 0.7200 |
| conversion | 0.9830 | 0.9000 | 1.0000 |
| safety_risk | 0.1190 | 0.0800 | 0.1800 |
| score | 0.2660 | 0.0800 | 0.4300 |
| selectivity | 0.5000 | 0.2700 | 0.7100 |
| yield | 0.4900 | 0.2500 | 0.7000 |

### Q04

High catalyst loading should form target rapidly, but 14400 s at 410 K leaves ample time for the consecutive loss channel. Conversion remains complete while little target is expected to survive.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9980 | 0.8500 | 1.0000 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.1400 | 0.0900 | 0.2400 |
| score | 0.0000 | 0.0000 | 0.0800 |
| selectivity | 0.0020 | 0.0000 | 0.1200 |
| yield | 0.0020 | 0.0000 | 0.1200 |

### Q05

At 350 K the low catalyst concentration slows reactant disappearance. The 7200 s duration nevertheless gives appreciable conversion, with moderate target loss and a predicted yield near that of the shorter, more highly catalyzed research batches.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3100 | 0.1400 | 0.5500 |
| conversion | 0.7750 | 0.5800 | 0.9100 |
| safety_risk | 0.0890 | 0.0600 | 0.1400 |
| score | 0.2740 | 0.1100 | 0.4100 |
| selectivity | 0.6010 | 0.3600 | 0.8000 |
| yield | 0.4660 | 0.2700 | 0.6500 |

### Q06

The 465 K condition is a major temperature extrapolation. Even low catalyst loading should give nearly complete conversion, while the higher-activation competing and degradation channels are expected to remove almost all target during 7200 s.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9970 | 0.8400 | 1.0000 |
| conversion | 0.9990 | 0.9400 | 1.0000 |
| safety_risk | 0.1780 | 0.1100 | 0.3000 |
| score | 0.0000 | 0.0000 | 0.0800 |
| selectivity | 0.0020 | 0.0000 | 0.1200 |
| yield | 0.0020 | 0.0000 | 0.1200 |

### Q07

High Catalyst B loading should essentially complete the reaction at 350 K. Target is formed early and then partly lost during the remaining residence time, leading to roughly equal target and non-target fractions.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4970 | 0.2800 | 0.7300 |
| conversion | 0.9990 | 0.9600 | 1.0000 |
| safety_risk | 0.0980 | 0.0600 | 0.1500 |
| score | 0.2830 | 0.1000 | 0.4300 |
| selectivity | 0.5030 | 0.2800 | 0.7200 |
| yield | 0.5020 | 0.2700 | 0.7000 |

### Q08

At 465 K with high catalyst loading, conversion should occur very early. The remaining high-temperature residence is predicted to destroy or divert essentially all target; uncertainty is wide because this temperature lies far outside the studied range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 1.0000 | 0.9000 | 1.0000 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.1780 | 0.1100 | 0.3100 |
| score | 0.0000 | 0.0000 | 0.0500 |
| selectivity | 0.0001 | 0.0000 | 0.0800 |
| yield | 0.0001 | 0.0000 | 0.0800 |

### Q09

The intermediate catalyst concentration should give virtually complete conversion at 410 K. Over 7200 s, the consecutive thermal-loss channel is expected to dominate, leaving a small but highly uncertain amount of target.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9470 | 0.6500 | 1.0000 |
| conversion | 1.0000 | 0.9600 | 1.0000 |
| safety_risk | 0.1400 | 0.0900 | 0.2300 |
| score | 0.0000 | 0.0000 | 0.1600 |
| selectivity | 0.0530 | 0.0000 | 0.2800 |
| yield | 0.0530 | 0.0000 | 0.2800 |

### Q10

Because quenching occurs only after the 7200 s heat operation, it should not reverse the accumulated chemical damage. I predict chemistry close to Q09, with a modestly lower final safety risk from rapid cooling.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9470 | 0.6200 | 1.0000 |
| conversion | 1.0000 | 0.9400 | 1.0000 |
| safety_risk | 0.1330 | 0.0800 | 0.2200 |
| score | 0.0000 | 0.0000 | 0.1800 |
| selectivity | 0.0530 | 0.0000 | 0.3000 |
| yield | 0.0530 | 0.0000 | 0.3000 |

### Q11

At 350 K and intermediate catalyst loading, 14400 s should produce essentially complete conversion but allow extensive consecutive target loss. Some target is expected to remain because degradation is slower than at 410–465 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7340 | 0.4500 | 0.9200 |
| conversion | 1.0000 | 0.9600 | 1.0000 |
| safety_risk | 0.0980 | 0.0600 | 0.1600 |
| score | 0.1290 | 0.0000 | 0.3000 |
| selectivity | 0.2660 | 0.0800 | 0.5200 |
| yield | 0.2660 | 0.0800 | 0.5200 |

### Q12

The intermediate catalyst loading and very high temperature should give near-complete conversion in 1800 s. The shorter residence preserves more target than Q06 or Q08, but degradation is still predicted to dominate the endpoint.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8280 | 0.5200 | 0.9700 |
| conversion | 0.9910 | 0.8800 | 1.0000 |
| safety_risk | 0.1490 | 0.0900 | 0.2500 |
| score | 0.0380 | 0.0000 | 0.2500 |
| selectivity | 0.1640 | 0.0300 | 0.4200 |
| yield | 0.1630 | 0.0300 | 0.4200 |

## K2 — Retrospective analysis

1. Initial claims: supported, challenged, or untested

The only substantive mechanistic prior in the initial material was: “The target pathway may have an appreciable reverse channel on the public support,” with moderate confidence. My sealed K1 report retained an R ⇌ P step, but explicitly stated that the reverse channel was “compatible with” rather than demonstrated by the data.

That prior remains untested, not supported. None of my experiments started from target-enriched material, perturbed an established equilibrium, or measured relaxation in both directions. Conversion continued to rise through 3600 s at 350 K: 0.2310 in Batch 9 at 600 s, 0.6110 in Batch 10 at 1800 s, and 0.8576 in Batch 11 at 3600 s. This monotonic trend does not provide evidence for reverse flux. It creates mild tension with a low equilibrium ceiling, but it does not refute a reverse reaction whose equilibrium lies above the measured conversion or whose reverse rate is small on this timescale. I did not overlook definite contrary evidence; rather, I correctly described the issue in K1 as unresolved.

The initial information also warned that catalysts were anonymous benchmark formulations and that named solvents had categorical benchmark effects rather than validated real-material kinetic correlations. I respected that limitation in K1 by declining to assign molecular catalyst identities or infer solvent effects from real-world polarity or boiling-point arguments. That claim was a boundary condition on interpretation, not an experimentally testable mechanism.

No task-specific property dossier, nominal kinetic constants, or species mapping was supplied. Therefore, there were no other substantive initial mechanistic claims to confirm or reject. The statement that experimental evidence should be authoritative was procedural rather than scientific.

2. Experiments that formed or changed my judgment

Batch 1 established that water/Catalyst A at 330 K for 1800 s produced little target: conversion 0.1548, selectivity 0.5945, and yield 0.0838. This was not enough to define a mechanism, but it motivated a controlled catalyst comparison rather than immediate temperature optimization.

Batches 2–4 genuinely changed the working model. At otherwise matched conditions, Catalyst B produced conversion 0.2844, selectivity 0.8493, and yield 0.2464, substantially exceeding Catalysts A, C, and D. This supported the K1 judgment that catalyst identity affected both the productive and competing activation channels, rather than merely multiplying all rates equally.

Batches 5–7 then established a solvent-dependent activity/selectivity tradeoff for Catalyst B. Acetonitrile in Batch 6 gave the largest yield, 0.3929, whereas toluene in Batch 7 gave lower selectivity, 0.6965, and higher byproduct signal, 0.1134. These results caused me to represent solvent with separate effects on productive and side-reaction rates rather than with one common rate multiplier.

Batches 8, 6, and 10 formed the local temperature series at 310, 330, and 350 K for 1800 s. Conversion rose from 0.3394 to 0.4799 to 0.6110. This supported positive thermal activation and led to the crude local apparent activation estimate of about 18.6 kJ mol⁻¹ quoted in K1. That estimate depended on an irreversible first-order reduction and was not an elementary activation energy.

Batches 9–11 had the greatest mechanistic value. At 350 K, extending time from 600 to 1800 to 3600 s raised conversion and yield, but selectivity fell from 0.8874 to 0.8114 to 0.6994, while byproduct signal rose from 0.0302 to 0.1147 to 0.2413 and degradation warning rose from 0 to 0.0567 to 0.1636. These data were the main basis for changing from a simple target-formation model to the parallel-plus-consecutive network described in K1. They show increasing competition with thermal residence, although they do not uniquely prove that isolated target is the precursor of the degradation channel.

Batch 12 was chosen as a paired quench comparison with Batch 11. It showed a 45 K cooling step over 56.1 s and a risk reduction of 0.00676. Its chemical endpoint was close to Batch 11. This supported only the limited K1 conclusion that quenching reduced temperature and risk while approximately preserving the endpoint. It did not demonstrate a selectivity improvement.

Several choices were driven more by strategy than by evidence. The initial catalyst screen was a broad factorial choice made before catalyst rankings were known. The solvent screen followed the observed superiority of Catalyst B. The later concentration on Catalyst B/acetonitrile relied on accumulated evidence but also served optimization. The assumption that 600 rpm was adequate, the use of a single catalyst amount, and the decision not to run an uncatalyzed control were unvalidated. The reverse reaction was retained mainly because of the initial prior, not because a particular batch revealed it.

3. Most important competing mechanisms

The principal competition is between the reversible network used in K1,

R ⇌ P, R → B, and P → B or D,

and an irreversible network,

R → P and R → B,

with time-dependent rates caused by heat-up, catalyst-state changes, or multiple parallel pathways. The irreversible alternative can explain nearly all measured trends without invoking P → R.

A second competition concerns the source of declining selectivity. My preferred explanation is consecutive target loss because degradation warning was delayed and increased strongly with time. However, a parallel reaction can mimic this behavior if its activation energy is higher than that of target formation, if the catalyst changes state during heating, or if the thermal trajectory changes the branching ratio. Because the degradation channel was only an aggregate calibrated signal, the experiments cannot prove that the measured target itself was converted into the degradation products.

A third competition is equilibrium versus catalyst deactivation versus ordinary kinetic exhaustion as the cause of slowing conversion. The data can distinguish these from neither one another nor mixtures of them. Monotonic conversion and the absence of a target-yield downturn by 3600 s argue against extremely rapid deactivation or a low equilibrium ceiling, but they do not estimate a reverse rate or deactivation constant.

The experiments do distinguish several broader facts: Catalyst B was superior at the tested loading and reference condition; solvent altered selectivity as well as conversion; increasing temperature accelerated conversion between 310 and 350 K; and longer hot residence increased non-target signals. They do not identify molecular intermediates, individual byproducts, reaction orders, catalyst saturation, or the separate temperature dependences of productive, reverse, and damaging channels.

4. One additional complete experiment I would choose

I would repeat the standard Catalyst B/acetonitrile charge used in Batches 9–12—0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm—and heat it at 350 K for 3600 s. I would take the permitted nonfinal HPLC measurement at 3600 s, then continue heating at 350 K for another 10800 s, terminate without a chemical quench, and perform the required final assay. This would provide a within-batch observation near the known Batch 11 endpoint followed by a much longer total residence of 14400 s.

If conversion remained near 0.86 while target yield and selectivity fell sharply, that would strongly favor consecutive target loss or continuing degradation with little additional reactant consumption. If conversion and yield both continued to increase while selectivity remained roughly stable, the 3600 s curvature would be better explained by incomplete forward reaction than by severe degradation. If conversion approached a stable plateau and target yield remained stable, reversible equilibrium or catalyst deactivation would become more plausible, though those two would remain confounded. If conversion decreased while reactant signal returned, that would be unusually strong evidence for reverse reaction. If all signals changed little, either the system had reached a stable endpoint or the catalyst had become inactive; a separate catalyst-rescue experiment would then be needed to distinguish them.

The cross-instrument comparison between the intermediate HPLC and final assay would remain a weakness. Nevertheless, the large extension in residence time should produce changes much larger than instrument noise if the consecutive-loss model used in the blind predictions is approximately correct.

5. Tradeoff between identifiability and operational score

The design began with an identifiability emphasis: four catalysts at matched conditions and four solvents with the best catalyst consumed seven of the twelve batches. Those screens reduced categorical uncertainty but did not maximize score in every batch. Batch 1, for example, was knowingly retained as a low-performing baseline once its result was known.

The later design increasingly favored the promising Catalyst B/acetonitrile combination. This improved operational performance and enabled a clean local time/temperature study, but it narrowed material coverage. Batches 9–11 traded some selectivity for mechanistic information about thermal residence. Batch 11 deliberately extended the reaction into a region with byproduct signal 0.2413 and degradation warning 0.1636; its purpose was more diagnostic than purely optimal, although its high conversion also raised its score.

Batch 12 combined optimization and process diagnosis. It reproduced the highest-yield region and added a quench. Its score of 0.3286 was the highest observed, but that outcome does not mean the design was an unbiased optimization campaign.

The largest sacrifice of identifiability was using the same maximum reagent, solvent, and catalyst charges in every batch. That exhausted the available stocks neatly and maintained comparability, but it left reaction orders, catalyst-loading dependence, concentration effects, and catalyst saturation unidentified. I also spent most nonfinal measurements at endpoints rather than using multiple timed samples from fewer batches. Endpoint HPLC often repeated information later obtained from the final assay; those uses could have been more informative if allocated to within-batch kinetic transitions.

Conversely, I did not pursue very high temperatures because the research goal included safety and because all batches had to be completed. This protected the campaign from unsafe outcomes but limited identification of high-temperature degradation—the exact region later required by several blind queries.

6. Underused evidence and reliability of the blind predictions

The raw characterization artifacts were underused. I relied primarily on processed estimates and selected peak summaries. A more systematic comparison of reactant, target, byproduct, and degradation proxy peak areas across HPLC, GC, and final-assay channels might have clarified whether discrepancies were calibration effects or real process variation. Batch 11’s GC measurement, which gave byproduct 0.2766 and degradation 0.1879 before its final assay, was useful corroboration but was not quantitatively integrated with the HPLC and final-assay observations.

The measured temperature changes were also only partially used. K1 correctly noted heat-up effects, especially the smaller +47.5 K change in the 600 s Batch 9 compared with about +48.7 to +48.8 K in longer 350 K batches. However, my blind-prediction model compressed this into simple temperature multipliers. I did not have a full temperature trace and therefore could not reliably extrapolate thermal dose.

The most reliable blind predictions are comparatively Q05 and Q07 because they remain at 350 K, although their catalyst concentrations and scale differ from the training batches. Q01 and Q03 are less reliable because 410 K was outside the 310–350 K research range, but their 1800 s durations at least remain within the observed time scale.

The least reliable predictions are Q02, Q04, Q06, Q08, Q09, Q10, Q11, and Q12. Q02 and Q04 combine 410 K with 14400 s. Q06 and Q08 use 465 K for 7200 s. Q09 and Q10 use 410 K for 7200 s, Q11 extends 350 K to 14400 s, and Q12 uses 465 K. Their predicted collapse of yield depended on an unmeasured activation law for consecutive degradation. No experiment established that law.

Several intervals were probably too narrow. Q08 predicted conversion 1.00 with an 80% interval of 0.98–1.00 and yield 0.0001 with an interval of 0–0.08, despite being far outside both the temperature and catalyst-loading support. Similar boundary-concentrated intervals were assigned to Q04 and Q06. Q02’s yield interval of 0–0.18 and Q09/Q10 intervals extending only to about 0.28–0.30 may also understate uncertainty about equilibrium, deactivation, and target stability. Safety intervals were based on an unvalidated scaling of setup risk with quantity and a simple extrapolation of thermal risk; Q06 and Q08 especially could have required wider upper bounds.

This is partly inconsistent with K1, which explicitly said that evidence was supported only over 310–350 K and 600–3600 s and that extrapolation beyond 3600 s was hazardous. The rationales acknowledged extrapolation, but some numerical intervals conveyed more confidence than the report justified. The point predictions near zero or one were consequences of a particular kinetic model, not robust consequences of the data.

The score predictions were structurally better grounded because the observed scores fit the public relation used in the prediction rationale: score = max(0, −0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion − 0.45·safety risk). Nevertheless, score uncertainty inherits all uncertainty in chemistry and risk; clipping many extrapolated scores to zero concealed model uncertainty rather than eliminating it.

7. Limitations of the sealed recommendation

Batch 12 was the sample-in highest-scoring batch, not a demonstrated optimum. It produced the highest observed score, 0.3286, and yield, 0.6209, among the twelve completed experiments. The recommendation therefore had an empirical basis, but it was selected from a sparse, adaptive design with one realization per nominal condition.

The apparent advantage over Batch 11 was small: yield differed by only +0.0054 and score by about +0.0110. Batch 12 also differed by the inclusion of a quench and by ordinary between-batch variation. The campaign did not establish that quenching caused the higher score, only that it lowered the reported risk and left a broadly similar chemical endpoint.

Repeatability should first be tested with several exact independent replicates of Batch 12, reporting distributions of yield, selectivity, degradation, risk, and score rather than only means. Batch 11 should be replicated in parallel to estimate the causal effect of the quench.

Local robustness should be tested with a neighborhood around 350 K and 3600 s—for example modest changes in temperature, duration, catalyst amount, concentration, and stirring speed. A useful recommendation should not fail sharply under small execution errors. A response-surface or sequential design could determine whether the observed condition lies near a broad plateau, on an increasing-yield boundary, or beyond the true selectivity optimum.

Material transfer is especially limited. “Catalyst B” is an anonymous benchmark formulation, and acetonitrile’s effect is a world-specific categorical coupling. The recommendation cannot be transferred to a named real catalyst or synthesis without new evidence. Even within ChemWorld, another hidden world could assign different categorical activities, reverse rates, or thermal degradation. Cross-world validity would require repeating a compact calibration set—at minimum a catalyst comparison, solvent comparison, and short time series—in each new world.

Accordingly, the sealed recommendation should be described as the best observed completed batch under this campaign’s sampled conditions. It was not proven globally optimal, locally stationary, repeatable, robust to perturbations, or portable across materials or worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 129.9 | none | 0 |
| Q | yes | 0 | 206.8 | none | 0 |
| K2 | yes | 0 | 119.5 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1553 | 0.6833 | 0.3342 | 0.5507 |
| conversion | 0.0174 | 1.0000 | 0.1092 | 0.1092 |
| safety_risk | 0.1294 | 0.2500 | 0.1317 | 0.6696 |
| score | 0.0738 | 0.9167 | 0.2100 | 0.2516 |
| selectivity | 0.1692 | 0.5500 | 0.3067 | 0.7057 |
| yield | 0.1634 | 0.5833 | 0.2958 | 0.6775 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2500 | 0.1000 | 0.5000 | 0.1848 | 0.1918, 0.1819, 0.1704, 0.1891, 0.1908 |
| conversion | 0.6100 | 0.4000 | 0.8000 | 0.7137 | 0.7023, 0.7224, 0.7188, 0.7145, 0.7107 |
| safety_risk | 0.1040 | 0.0700 | 0.1600 | 0.2518 | 0.2518, 0.2518, 0.2518, 0.2518, 0.2518 |
| score | 0.2060 | 0.0500 | 0.3700 | 0.3274 | 0.3246, 0.3325, 0.3231, 0.3272, 0.3293 |
| selectivity | 0.5900 | 0.3400 | 0.7900 | 0.7446 | 0.7346, 0.7507, 0.7388, 0.7478, 0.7514 |
| yield | 0.3600 | 0.1800 | 0.5600 | 0.5270 | 0.5292, 0.5340, 0.5188, 0.5246, 0.5285 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9900 | 0.7800 | 1.0000 | 0.9165 | 0.9241, 0.9159, 0.9222, 0.9177, 0.9027 |
| conversion | 0.9990 | 0.9300 | 1.0000 | 0.9982 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9911 |
| safety_risk | 0.1400 | 0.0900 | 0.2300 | 0.2522 | 0.2522, 0.2522, 0.2522, 0.2522, 0.2522 |
| score | 0.0000 | 0.0000 | 0.1200 | 0.0065 | 0.0068, 0.0060, 0.0124, 0.0037, 0.0034 |
| selectivity | 0.0100 | 0.0000 | 0.1800 | 0.0907 | 0.0810, 0.0943, 0.1061, 0.0782, 0.0938 |
| yield | 0.0100 | 0.0000 | 0.1800 | 0.0891 | 0.0956, 0.0852, 0.0939, 0.0896, 0.0814 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4900 | 0.2500 | 0.7200 | 0.2439 | 0.2551, 0.2405, 0.2456, 0.2377, 0.2404 |
| conversion | 0.9830 | 0.9000 | 1.0000 | 0.9840 | 0.9910, 0.9798, 0.9883, 0.9778, 0.9833 |
| safety_risk | 0.1190 | 0.0800 | 0.1800 | 0.2538 | 0.2538, 0.2538, 0.2538, 0.2538, 0.2538 |
| score | 0.2660 | 0.0800 | 0.4300 | 0.4127 | 0.4149, 0.4118, 0.4145, 0.4127, 0.4096 |
| selectivity | 0.5000 | 0.2700 | 0.7100 | 0.7564 | 0.7525, 0.7577, 0.7556, 0.7640, 0.7520 |
| yield | 0.4900 | 0.2500 | 0.7000 | 0.7398 | 0.7460, 0.7376, 0.7438, 0.7366, 0.7348 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9980 | 0.8500 | 1.0000 | 0.9599 | 0.9591, 0.9620, 0.9651, 0.9593, 0.9539 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9956 | 1.0000, 0.9911, 1.0000, 0.9919, 0.9949 |
| safety_risk | 0.1400 | 0.0900 | 0.2400 | 0.2525 | 0.2525, 0.2525, 0.2525, 0.2525, 0.2525 |
| score | 0.0000 | 0.0000 | 0.0800 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0020 | 0.0000 | 0.1200 | 0.0756 | 0.0716, 0.0733, 0.0668, 0.0853, 0.0810 |
| yield | 0.0020 | 0.0000 | 0.1200 | 0.0734 | 0.0697, 0.0765, 0.0699, 0.0811, 0.0700 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3100 | 0.1400 | 0.5500 | 0.4087 | 0.4217, 0.4103, 0.4022, 0.3956, 0.4138 |
| conversion | 0.7750 | 0.5800 | 0.9100 | 0.8430 | 0.8392, 0.8436, 0.8392, 0.8386, 0.8545 |
| safety_risk | 0.0890 | 0.0600 | 0.1400 | 0.1426 | 0.1426, 0.1426, 0.1426, 0.1426, 0.1426 |
| score | 0.2740 | 0.1100 | 0.4100 | 0.2913 | 0.2939, 0.2886, 0.2971, 0.2898, 0.2871 |
| selectivity | 0.6010 | 0.3600 | 0.8000 | 0.5173 | 0.5216, 0.5049, 0.5338, 0.5106, 0.5157 |
| yield | 0.4660 | 0.2700 | 0.6500 | 0.4350 | 0.4399, 0.4358, 0.4401, 0.4365, 0.4227 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9970 | 0.8400 | 1.0000 | 0.8233 | 0.8278, 0.8247, 0.8136, 0.8315, 0.8191 |
| conversion | 0.9990 | 0.9400 | 1.0000 | 0.9952 | 0.9988, 0.9901, 0.9926, 0.9947, 1.0000 |
| safety_risk | 0.1780 | 0.1100 | 0.3000 | 0.4261 | 0.4261, 0.4261, 0.4261, 0.4261, 0.4261 |
| score | 0.0000 | 0.0000 | 0.0800 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0020 | 0.0000 | 0.1200 | 0.1871 | 0.1941, 0.1683, 0.1953, 0.1894, 0.1884 |
| yield | 0.0020 | 0.0000 | 0.1200 | 0.1849 | 0.1885, 0.1877, 0.1865, 0.1781, 0.1839 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4970 | 0.2800 | 0.7300 | 0.5161 | 0.5192, 0.5183, 0.5198, 0.5114, 0.5117 |
| conversion | 0.9990 | 0.9600 | 1.0000 | 0.9945 | 0.9933, 1.0000, 0.9913, 0.9970, 0.9911 |
| safety_risk | 0.0980 | 0.0600 | 0.1500 | 0.1438 | 0.1438, 0.1438, 0.1438, 0.1438, 0.1438 |
| score | 0.2830 | 0.1000 | 0.4300 | 0.2970 | 0.2948, 0.2939, 0.2935, 0.3014, 0.3012 |
| selectivity | 0.5030 | 0.2800 | 0.7200 | 0.4950 | 0.4950, 0.4901, 0.4932, 0.4948, 0.5021 |
| yield | 0.5020 | 0.2700 | 0.7000 | 0.4986 | 0.4935, 0.4928, 0.4919, 0.5092, 0.5058 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 1.0000 | 0.9000 | 1.0000 | 0.8563 | 0.8570, 0.8322, 0.8629, 0.8565, 0.8729 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9973 | 1.0000, 0.9919, 1.0000, 1.0000, 0.9945 |
| safety_risk | 0.1780 | 0.1100 | 0.3100 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0000 | 0.0000 | 0.0500 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0001 | 0.0000 | 0.0800 | 0.1701 | 0.1633, 0.1704, 0.1715, 0.1742, 0.1709 |
| yield | 0.0001 | 0.0000 | 0.0800 | 0.1738 | 0.1784, 0.1766, 0.1728, 0.1716, 0.1699 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9470 | 0.6500 | 1.0000 | 0.7196 | 0.7083, 0.7133, 0.7299, 0.7153, 0.7310 |
| conversion | 1.0000 | 0.9600 | 1.0000 | 0.9933 | 1.0000, 0.9804, 1.0000, 0.9986, 0.9875 |
| safety_risk | 0.1400 | 0.0900 | 0.2300 | 0.2529 | 0.2529, 0.2529, 0.2529, 0.2529, 0.2529 |
| score | 0.0000 | 0.0000 | 0.1600 | 0.1314 | 0.1360, 0.1316, 0.1277, 0.1341, 0.1277 |
| selectivity | 0.0530 | 0.0000 | 0.2800 | 0.3006 | 0.3108, 0.3002, 0.2918, 0.3038, 0.2963 |
| yield | 0.0530 | 0.0000 | 0.2800 | 0.2924 | 0.2957, 0.2963, 0.2868, 0.2958, 0.2873 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9470 | 0.6200 | 1.0000 | 0.7130 | 0.7267, 0.7023, 0.7206, 0.7129, 0.7025 |
| conversion | 1.0000 | 0.9400 | 1.0000 | 0.9922 | 1.0000, 0.9941, 0.9958, 0.9831, 0.9878 |
| safety_risk | 0.1330 | 0.0800 | 0.2200 | 0.1456 | 0.1456, 0.1456, 0.1456, 0.1456, 0.1456 |
| score | 0.0000 | 0.0000 | 0.1800 | 0.1737 | 0.1786, 0.1673, 0.1736, 0.1726, 0.1762 |
| selectivity | 0.0530 | 0.0000 | 0.3000 | 0.2959 | 0.3124, 0.2771, 0.2873, 0.3050, 0.2977 |
| yield | 0.0530 | 0.0000 | 0.3000 | 0.2889 | 0.2891, 0.2842, 0.2933, 0.2828, 0.2953 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7340 | 0.4500 | 0.9200 | 0.7775 | 0.7826, 0.7700, 0.7824, 0.7723, 0.7800 |
| conversion | 1.0000 | 0.9600 | 1.0000 | 0.9975 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9875 |
| safety_risk | 0.0980 | 0.0600 | 0.1600 | 0.1432 | 0.1432, 0.1432, 0.1432, 0.1432, 0.1432 |
| score | 0.1290 | 0.0000 | 0.3000 | 0.1414 | 0.1452, 0.1394, 0.1458, 0.1449, 0.1317 |
| selectivity | 0.2660 | 0.0800 | 0.5200 | 0.2451 | 0.2573, 0.2426, 0.2622, 0.2561, 0.2075 |
| yield | 0.2660 | 0.0800 | 0.5200 | 0.2426 | 0.2439, 0.2387, 0.2423, 0.2439, 0.2444 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8280 | 0.5200 | 0.9700 | 0.3277 | 0.3364, 0.3157, 0.3327, 0.3236, 0.3300 |
| conversion | 0.9910 | 0.8800 | 1.0000 | 0.9933 | 0.9929, 0.9900, 1.0000, 0.9984, 0.9854 |
| safety_risk | 0.1490 | 0.0900 | 0.2500 | 0.4273 | 0.4273, 0.4273, 0.4273, 0.4273, 0.4273 |
| score | 0.0380 | 0.0000 | 0.2500 | 0.3000 | 0.3025, 0.2997, 0.3014, 0.2990, 0.2971 |
| selectivity | 0.1640 | 0.0300 | 0.4200 | 0.6713 | 0.6755, 0.6797, 0.6646, 0.6644, 0.6722 |
| yield | 0.1630 | 0.0300 | 0.4200 | 0.6671 | 0.6710, 0.6621, 0.6732, 0.6677, 0.6612 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2461 | 0.2436 | -0.0025 |
| conversion | 0.8499 | 0.8510 | 0.0011 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1884 | 0.1762 | -0.0122 |
| safety_risk | 0.1915 | 0.1915 | 0.0000 |
| score | 0.3286 | 0.3218 | -0.0068 |
| selectivity | 0.7258 | 0.7149 | -0.0108 |
| virtual_spectrum_summary | 0.2202 | 0.2133 | -0.0069 |
| yield | 0.6209 | 0.6104 | -0.0105 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
