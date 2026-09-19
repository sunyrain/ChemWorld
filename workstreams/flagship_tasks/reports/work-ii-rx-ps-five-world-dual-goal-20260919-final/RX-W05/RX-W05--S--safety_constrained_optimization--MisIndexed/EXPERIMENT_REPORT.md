# RX-W05--S--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W05`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `97`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v11`
- Recovery version: `recovery-v11-parallel4-transport-repair`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 delivered the highest observed public safe score (0.4095) while its safety risk (0.1703) remained well below the 0.35 limit; it also combined high yield and conversion with favorable selectivity.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm → 350 K x 3600 s @ 600 rpm | yes | 0.5370 | 0.7495 | 0.7212 | 0.1831 | 0.0451 | 0.1351 | 0.3135 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | yes | 0.5993 | 0.7260 | 0.8249 | 0.2314 | 0.1092 | 0.1445 | 0.3387 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | yes | 0.4083 | 0.5929 | 0.6797 | 0.2656 | 0.0285 | 0.1219 | 0.2246 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | yes | 0.6650 | 0.7417 | 0.8734 | 0.2153 | 0.1113 | 0.1518 | 0.3705 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | yes | 0.5832 | 0.6339 | 0.8752 | 0.3100 | 0.2305 | 0.1738 | 0.3011 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | yes | 0.6271 | 0.6908 | 0.9366 | 0.3248 | 0.2493 | 0.1981 | 0.3280 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | yes | 0.4793 | 0.5407 | 0.8806 | 0.4228 | 0.2570 | 0.1976 | 0.2260 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 330 K x 7200 s @ 600 rpm | yes | 0.5725 | 0.7850 | 0.7297 | 0.1651 | 0.0861 | 0.1393 | 0.3355 |
| 9 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 7200 s @ 600 rpm | yes | 0.6870 | 0.7329 | 0.9404 | 0.2622 | 0.1860 | 0.1601 | 0.3800 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 10800 s @ 600 rpm | yes | 0.6507 | 0.6701 | 0.9593 | 0.3073 | 0.2141 | 0.1571 | 0.3530 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 390 K x 5400 s @ 600 rpm | yes | 0.7204 | 0.7651 | 0.9495 | 0.2321 | 0.1480 | 0.1638 | 0.4006 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 410 K x 4500 s @ 600 rpm | yes | 0.7472 | 0.7692 | 0.9492 | 0.2243 | 0.1590 | 0.1703 | 0.4095 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `9`.

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
  "end_step": 9,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.1830957531929016,
    "conversion": 0.7212240695953369,
    "cost": 1.0,
    "degradation_warning": 0.04505213722586632,
    "safety_risk": 0.13509097695350647,
    "score": 0.31351807713508606,
    "selectivity": 0.7495027780532837,
    "virtual_spectrum_summary": 0.12097612023353577,
    "yield": 0.5370272397994995
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `17`.

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
  "end_step": 17,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.23140229284763336,
    "conversion": 0.8248629570007324,
    "cost": 1.0,
    "degradation_warning": 0.10916347801685333,
    "safety_risk": 0.1445450484752655,
    "score": 0.33866509795188904,
    "selectivity": 0.7260002493858337,
    "virtual_spectrum_summary": 0.17639482021331787,
    "yield": 0.5993099808692932
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
  "end_step": 25,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.26556137204170227,
    "conversion": 0.6796935200691223,
    "cost": 1.0,
    "degradation_warning": 0.028474444523453712,
    "safety_risk": 0.12190769612789154,
    "score": 0.2246474176645279,
    "selectivity": 0.5929386019706726,
    "virtual_spectrum_summary": 0.15887224674224854,
    "yield": 0.4082546830177307
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `33`.

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
  "end_step": 33,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.21529661118984222,
    "conversion": 0.8734263777732849,
    "cost": 1.0,
    "degradation_warning": 0.11130143702030182,
    "safety_risk": 0.1517837643623352,
    "score": 0.3704519271850586,
    "selectivity": 0.7416552305221558,
    "virtual_spectrum_summary": 0.16849878430366516,
    "yield": 0.6649954915046692
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `41`.

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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 41,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.31000858545303345,
    "conversion": 0.8751581311225891,
    "cost": 1.0,
    "degradation_warning": 0.23051635921001434,
    "safety_risk": 0.17380227148532867,
    "score": 0.3010610342025757,
    "selectivity": 0.6339414715766907,
    "virtual_spectrum_summary": 0.27423709630966187,
    "yield": 0.5831772089004517
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `49`.

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
      "duration_s": 7200,
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
  "end_step": 49,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.32476502656936646,
    "conversion": 0.9366410970687866,
    "cost": 1.0,
    "degradation_warning": 0.2492712438106537,
    "safety_risk": 0.19810765981674194,
    "score": 0.3280350863933563,
    "selectivity": 0.6907939314842224,
    "virtual_spectrum_summary": 0.2907928228378296,
    "yield": 0.627052366733551
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `57`.

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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 57,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.4228084981441498,
    "conversion": 0.8805835247039795,
    "cost": 1.0,
    "degradation_warning": 0.2570146918296814,
    "safety_risk": 0.1976403295993805,
    "score": 0.22602374851703644,
    "selectivity": 0.5406860709190369,
    "virtual_spectrum_summary": 0.34820127487182617,
    "yield": 0.47933006286621094
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `65`.

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
      "target_temperature_K": 330
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
  "end_step": 65,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.16511887311935425,
    "conversion": 0.7296611666679382,
    "cost": 1.0,
    "degradation_warning": 0.08612223714590073,
    "safety_risk": 0.1393386870622635,
    "score": 0.3354940116405487,
    "selectivity": 0.7849993109703064,
    "virtual_spectrum_summary": 0.1295703798532486,
    "yield": 0.5724512338638306
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `73`.

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
      "target_temperature_K": 370
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
  "end_step": 73,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.26221880316734314,
    "conversion": 0.9404193162918091,
    "cost": 1.0,
    "degradation_warning": 0.18597231805324554,
    "safety_risk": 0.16006967425346375,
    "score": 0.38001278042793274,
    "selectivity": 0.7328662872314453,
    "virtual_spectrum_summary": 0.22790789604187012,
    "yield": 0.6869640350341797
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `81`.

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
      "duration_s": 10800,
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
  "end_step": 81,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3073047399520874,
    "conversion": 0.9592718482017517,
    "cost": 1.0,
    "degradation_warning": 0.21408997476100922,
    "safety_risk": 0.15710504353046417,
    "score": 0.35302895307540894,
    "selectivity": 0.6700581908226013,
    "virtual_spectrum_summary": 0.2653580904006958,
    "yield": 0.650711178779602
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
      "duration_s": 5400,
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
  "end_step": 89,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.23205126821994781,
    "conversion": 0.9494689702987671,
    "cost": 1.0,
    "degradation_warning": 0.1479617804288864,
    "safety_risk": 0.16382203996181488,
    "score": 0.40064510703086853,
    "selectivity": 0.7651056051254272,
    "virtual_spectrum_summary": 0.1942109912633896,
    "yield": 0.7203543186187744
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `97`.

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
      "duration_s": 4500,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 410
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
  "end_step": 97,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.22425809502601624,
    "conversion": 0.9491588473320007,
    "cost": 1.0,
    "degradation_warning": 0.1590414047241211,
    "safety_risk": 0.17031095921993256,
    "score": 0.40946197509765625,
    "selectivity": 0.7692126631736755,
    "virtual_spectrum_summary": 0.19491058588027954,
    "yield": 0.7472071647644043
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidentiary basis

This report concerns only the bounded synthetic reaction-and-thermal benchmark studied in the completed 12-batch campaign. The reagent, target, impurities, degradation products, and catalysts are anonymous benchmark entities. Although the selectable solvents have real names, their kinetic effects were explicitly defined as categorical benchmark effects. I therefore make no claim that this behavior describes a named real reaction or catalyst.

Every batch used 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, and 600 rpm stirring. Consequently, the campaign identifies categorical catalyst and solvent effects and a limited temperature-time response, but it does not identify concentration, catalyst-loading, dilution, or mixing laws.

2. Proposed reaction network

My most useful working model is a reversible target-forming pathway coupled to at least two undesirable channels:

R ⇌ P
R → B
P → D

Here R is the public reactant, P the target product, B a primary or parallel byproduct pool, and D a thermally promoted degradation pool. More complicated variants, such as B also degrading or several unresolved byproducts contributing to each signal, remain possible.

A minimal kinetic representation is:

r_f = k_f(T, catalyst, solvent)·[R]
r_r = k_r(T, catalyst, solvent)·[P]
r_B = k_B(T, catalyst, solvent)·[R]
r_D = k_D(T, catalyst, solvent)·[P]

d[R]/dt = -r_f + r_r - r_B
d[P]/dt = r_f - r_r - r_D
d[B]/dt = r_B
d[D]/dt = r_D

Each rate constant can be represented locally by an Arrhenius-like temperature factor multiplied by categorical catalyst and solvent factors, for example k_j = A_j·f_j(catalyst)·g_j(solvent)·exp(-E_j/RT). The data do not justify numerical values for these parameters.

The structural prior supplied before experimentation stated that an appreciable reverse target channel might exist. The campaign is consistent with that possibility, particularly because target yield saturates while conversion continues to rise, but it does not uniquely demonstrate reversibility. Irreversible product degradation plus a parallel byproduct pathway can reproduce the same qualitative observations.

3. Relationship among public assay variables

Across the campaign, target yield was approximately conversion multiplied by selectivity. For example, batch 11 gave conversion 0.9495 and selectivity 0.7651, whose product is about 0.726, close to its measured yield of 0.7204. Batch 10 gave 0.9593 × 0.6701 ≈ 0.643, close to yield 0.6507. Deviations of a few percent are compatible with the declared assay noise and the fact that these processed channels need not be algebraically constrained.

I interpret conversion as reactant disappearance, selectivity as the fraction of converted material associated with target formation, byproduct_signal as an unresolved side-product proxy, and degradation_warning as a proxy for thermally or temporally accumulated damage. These latter two quantities should not be treated as exact mole fractions or summed into a strict mass balance.

The public score behaved as an aggregate quality measure rather than a direct kinetic observable. It generally improved with target yield and favorable selectivity and declined with side products, degradation, and safety risk. I did not infer an exact scoring equation.

4. Thermal dynamics and exposure

The vessel does not jump instantaneously to the requested setpoint. In batch 1, the first 3600 s heat operation targeting 350 K increased the reported temperature by 49.17 K, while a second identical operation increased it by only another 1.53 K. This is consistent with first-order thermal relaxation:

dT/dt = (T_set - T)/τ_heat,

with reaction proceeding throughout the warm-up. Quenching batch 1 lowered temperature by 45 K over approximately 54.7 s and reduced the displayed instantaneous safety risk slightly, but did not erase accumulated exposure.

Thus both requested temperature and residence time matter. A useful process abstraction is that desired formation depends strongly on the time integral of k_f(T), whereas degradation and risk depend on their own cumulative thermal-exposure integrals. Because the activation sensitivities can differ, a hotter but shorter operation can outperform a cooler, longer one.

5. Evidence from catalyst screening

The closest catalyst comparison used water, a nominal 350 K target, and 7200 s total heating:

• Batch 1, Catalyst A: conversion 0.7212, selectivity 0.7495, yield 0.5370, byproduct 0.1831, degradation 0.0451, safety risk 0.1351, score 0.3135.
• Batch 2, Catalyst B: conversion 0.8249, selectivity 0.7260, yield 0.5993, byproduct 0.2314, degradation 0.1092, risk 0.1445, score 0.3387.
• Batch 3, Catalyst C: conversion 0.6797, selectivity 0.5929, yield 0.4083, byproduct 0.2656, degradation 0.0285, risk 0.1219, score 0.2246.
• Batch 4, Catalyst D: conversion 0.8734, selectivity 0.7417, yield 0.6650, byproduct 0.2153, degradation 0.1113, risk 0.1518, score 0.3705.

Catalyst D therefore supplied the best observed balance of target-pathway rate and selectivity. Catalyst B was active but somewhat less target-favoring. Catalyst C was clearly poor for target production under these conditions: its lower conversion alone does not explain its much lower selectivity. Catalyst A appeared cleaner but slower.

Batch 1 was not perfectly protocol-identical because its 7200 s exposure was divided into two 3600 s heat operations with an intermediate HPLC measurement. At 3600 s, that HPLC measurement showed conversion 0.4799, selectivity 0.7842, yield 0.3704, and byproduct 0.1043. After the second heating period, final conversion and yield increased, while selectivity declined and byproduct increased. This time evolution directly supports progressive target formation accompanied by increasing competition from side reactions. The catalyst ranking is nevertheless somewhat confounded by batch 1's segmented protocol.

6. Evidence from solvent screening

With Catalyst D, a 350 K target, and 7200 s heating, batches 4-7 compared the four solvents:

• Batch 4, water: conversion 0.8734, selectivity 0.7417, yield 0.6650, byproduct 0.2153, degradation 0.1113, risk 0.1518, score 0.3705.
• Batch 5, ethanol: conversion 0.8752, selectivity 0.6339, yield 0.5832, byproduct 0.3100, degradation 0.2305, risk 0.1738, score 0.3011.
• Batch 6, acetonitrile: conversion 0.9366, selectivity 0.6908, yield 0.6271, byproduct 0.3248, degradation 0.2493, risk 0.1981, score 0.3280.
• Batch 7, toluene: conversion 0.8806, selectivity 0.5407, yield 0.4793, byproduct 0.4228, degradation 0.2570, risk 0.1976, score 0.2260.

Water was not simply the fastest medium—acetonitrile produced higher conversion—but it most strongly favored useful target production relative to undesirable channels and had the lowest risk in this comparison. Acetonitrile appears to accelerate overall disappearance of reactant while also promoting byproduct and degradation channels. Toluene gave high conversion but very poor partitioning into target. Ethanol was intermediate. These are categorical benchmark conclusions, not deductions from real solvent polarity, boiling point, or chemical compatibility.

7. Temperature-time optimization with Catalyst D in water

The later batches explored the best catalyst-solvent pair:

• Batch 8, 330 K for 7200 s: conversion 0.7297, selectivity 0.7850, yield 0.5725, byproduct 0.1651, degradation 0.0861, risk 0.1393, score 0.3355.
• Batch 4, 350 K for 7200 s: conversion 0.8734, selectivity 0.7417, yield 0.6650, byproduct 0.2153, degradation 0.1113, risk 0.1518, score 0.3705.
• Batch 9, 370 K for 7200 s: conversion 0.9404, selectivity 0.7329, yield 0.6870, byproduct 0.2622, degradation 0.1860, risk 0.1601, score 0.3800.
• Batch 10, 350 K for 10800 s: conversion 0.9593, selectivity 0.6701, yield 0.6507, byproduct 0.3073, degradation 0.2141, risk 0.1571, score 0.3530.
• Batch 11, 390 K for 5400 s: conversion 0.9495, selectivity 0.7651, yield 0.7204, byproduct 0.2321, degradation 0.1480, risk 0.1638, score 0.4006.
• Batch 12, 410 K for 4500 s: conversion 0.9492, selectivity 0.7692, yield 0.7472, byproduct 0.2243, degradation 0.1590, risk 0.1703, score 0.4095.

Several mechanistic conclusions follow.

First, increasing temperature from 330 to 370 K at fixed nominal time greatly increased conversion, indicating a strongly temperature-activated target-forming process. Selectivity decreased moderately and degradation increased, showing that side pathways are also thermally activated.

Second, merely extending time was counterproductive after high conversion was reached. Relative to batch 4, batch 10's longer 350 K residence raised conversion from 0.8734 to 0.9593 but lowered selectivity from 0.7417 to 0.6701, increased byproduct from 0.2153 to 0.3073 and degradation from 0.1113 to 0.2141, and slightly reduced yield from 0.6650 to 0.6507. This is strong evidence for cumulative secondary chemistry. It is compatible with P degradation, increasing parallel conversion to B, approach to a reversible equilibrium, or a combination.

Third, hotter and shorter schedules were superior within the tested region. Batches 11 and 12 reached approximately 0.95 conversion without the selectivity loss observed in batch 10. This suggests that the desired formation rate benefits more from the high-temperature pulse than the dominant undesirable processes benefit from additional residence time. It does not mean arbitrarily high temperatures would continue to improve performance; batch 12 already showed degradation warning 0.1590, and no points above 410 K were tested.

The intermediate HPLC result in batch 12 was conversion 0.9540, selectivity 0.7752, yield 0.7368, and byproduct 0.2300. The final assay after quenching gave nearby but nonidentical values. I interpret the discrepancy mainly as instrument/channel noise and sampling differences, not as evidence for a large post-quench reaction.

8. Safety behavior

All completed batches remained below the declared safety limit of 0.35. Final observed risks ranged from 0.1219 to 0.1981 in the main screens; the selected batch 12 had risk 0.1703. Risk was affected by material additions, solvent identity, temperature, and exposure. Water consistently gave lower risk than the other solvents in the matched screen. Within the Catalyst D/water series, risk generally increased with more severe thermal operation, but it was not a simple function of conversion or setpoint alone.

A plausible state model is:

risk_state = material/solvent contribution + thermal contribution,
thermal contribution ∝ integral h(T(t), solvent, composition) dt,

with quenching reducing the current thermal component while accumulated or peak-risk accounting remains path dependent. The experiment does not reveal the exact safety equation. The observed margin below 0.35 is specific to the tested scale and benchmark rules and should not be extrapolated to a physical reactor.

9. Interpretation of the preferred operating region

Within the measured design space, the best observed procedure was batch 12: Catalyst D in water, 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, 600 rpm, a 410 K target for 4500 s, followed by quenching, termination, and final assay. It produced the campaign's highest observed score, 0.4095, with risk 0.1703.

This is an empirical recommendation, not proof of a global optimum. A local optimum may lie near the high-temperature/short-time edge explored in batches 11 and 12, but behavior above 410 K, at durations below 4500 s, or under different loadings is unmeasured. Because batch 12 was chosen after adaptive searching and was not replicated, its apparent advantage over batch 11 could be partly inflated by measurement noise.

10. Non-identifiable factors and competing explanations

The following remain unresolved:

• Reversibility versus degradation: the prior proposed an appreciable reverse channel, and yield saturation is consistent with it, but there was no direct reversal experiment such as isolated product exposure or a temperature-downshift hold. An irreversible R → P → D network could explain the same data.
• Parallel versus consecutive byproduct formation: byproduct_signal increased with residence time, but the data do not show whether B forms directly from R, from P, or through both routes.
• Catalyst mechanism: Catalyst D may increase k_f, suppress k_B/k_D, alter the forward/reverse equilibrium, or combine these effects. Fixed catalyst loading prevents separation of activity from selectivity changes.
• Solvent mechanism: the matched screen establishes categorical effects but cannot distinguish kinetic stabilization, equilibrium shifts, heat-transfer differences, or synthetic instrument-response effects.
• Thermal parameters: only setpoints and public state changes were observed. Heat capacity, transfer coefficient, and exact temperature trajectories are not identifiable from the limited telemetry.
• Concentration and mass transfer: reagent amount, catalyst amount, solvent volume, and stirring speed were fixed, so reaction order, catalyst saturation, and mixing limitations are unknown.
• Assay noise and batch variability: each condition had one final assay and no true replicate. Small differences, especially between batches 11 and 12, should not be overinterpreted.
• Score law: the exact transformation from yield, selectivity, side-product indicators, degradation, and risk to score was not identified.

11. Final world model

The simplest coherent explanation is a thermally activated, catalyst- and solvent-dependent network in which target formation competes with byproduct formation and subsequent degradation, with a possible appreciable reverse target channel. Catalyst D and water jointly provide the most favorable rate/selectivity balance. Conversion can be increased by either time or temperature, but long residence after high conversion disproportionately increases byproduct and degradation signals. Because the vessel warms gradually, a high setpoint combined with a shorter residence can deliver rapid target formation while limiting cumulative secondary chemistry. Safety risk is path dependent and coupled to solvent choice and thermal exposure, but all tested schedules remained within the declared limit. This model is well supported inside the tested categorical choices and approximately 330-410 K, 4500-10800 s operating window; beyond that window it is a reasoned extrapolation rather than an observation.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-derived model R ⇌ P with parallel byproduct formation and consecutive target degradation. Conversion was treated as increasing with catalyst-to-reagent ratio, temperature-dependent effective exposure, and time, while selectivity was reduced by cumulative thermal exposure and the acetonitrile categorical effect. The new batches use Catalyst B in acetonitrile at a smaller, slightly more concentrated scale and at 400 rpm; these conditions were not jointly observed. The closest anchors were batch 2 for Catalyst B at 350 K for 7200 s and batch 6 for the acetonitrile effect, while batches 8-12 informed temperature-time behavior. Intervals include final-assay noise, uncertainty in catalyst-loading scaling, thermal lag, scale transfer, and substantial extrapolation at 465 K. Quenching in Q10 was assumed to affect safety risk more than chemical composition. All bounds are clipped to the public 0-1 metric range.

### Q01

The low catalyst loading and short residence should limit conversion despite the 410 K setpoint and acetonitrile acceleration. Thermal lag during only 1800 s further reduces effective exposure. Moderate selectivity and limited accumulated byproduct are expected.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1200 | 0.3100 |
| conversion | 0.5300 | 0.3800 | 0.6800 |
| safety_risk | 0.0850 | 0.0550 | 0.1250 |
| score | 0.2500 | 0.1500 | 0.3400 |
| selectivity | 0.6900 | 0.5700 | 0.7900 |
| yield | 0.3600 | 0.2400 | 0.4900 |

### Q02

The eightfold longer residence should drive nearly complete reactant disappearance even at low catalyst loading. However, the campaign showed that prolonged exposure after high conversion sharply increases secondary chemistry, so selectivity and safe score are predicted to deteriorate.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.4000 | 0.7000 |
| conversion | 0.9800 | 0.9100 | 1.0000 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 |
| score | 0.1800 | 0.0800 | 0.2800 |
| selectivity | 0.4300 | 0.2700 | 0.5800 |
| yield | 0.4100 | 0.2500 | 0.5700 |

### Q03

The high catalyst-to-reagent ratio should produce rapid conversion during the short 410 K treatment. Short exposure should preserve substantially better selectivity than the corresponding 14400 s batch, making this one of the stronger predicted procedures.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2500 | 0.1600 | 0.3600 |
| conversion | 0.9300 | 0.8400 | 0.9800 |
| safety_risk | 0.0900 | 0.0600 | 0.1300 |
| score | 0.4600 | 0.3400 | 0.5600 |
| selectivity | 0.7200 | 0.6300 | 0.8000 |
| yield | 0.6700 | 0.5500 | 0.7700 |

### Q04

High catalyst loading and very long heating should exhaust the reactant, but the same combination is expected to maximize parallel and consecutive side chemistry. Conversion therefore remains high while target yield, selectivity, and score fall.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6700 | 0.5200 | 0.8200 |
| conversion | 0.9900 | 0.9600 | 1.0000 |
| safety_risk | 0.2100 | 0.1600 | 0.2800 |
| score | 0.1000 | 0.0200 | 0.2100 |
| selectivity | 0.3200 | 0.1700 | 0.4800 |
| yield | 0.3100 | 0.1600 | 0.4700 |

### Q05

At 350 K, low catalyst loading should leave the reaction kinetically limited even after 7200 s. Acetonitrile is expected to increase conversion relative to an inert medium but also produce a meaningful byproduct burden.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 |
| conversion | 0.5500 | 0.4000 | 0.7000 |
| safety_risk | 0.1000 | 0.0650 | 0.1450 |
| score | 0.2500 | 0.1500 | 0.3500 |
| selectivity | 0.6900 | 0.5800 | 0.7900 |
| yield | 0.3800 | 0.2600 | 0.5000 |

### Q06

A 465 K setpoint sustained for 7200 s should overcome the low catalyst loading and produce nearly complete disappearance. This temperature is outside the explored range and is expected to accelerate degradation and byproduct formation strongly, with a material chance of approaching or exceeding the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7200 | 0.5600 | 0.8700 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.2800 | 0.2000 | 0.3800 |
| score | 0.0700 | 0.0100 | 0.1700 |
| selectivity | 0.2800 | 0.1300 | 0.4400 |
| yield | 0.2700 | 0.1200 | 0.4300 |

### Q07

High catalyst loading at 350 K should provide high conversion without the extreme thermal damage expected at 465 K. Acetonitrile should still depress selectivity relative to water, so the result is predicted to be good but not exceptionally clean.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3600 | 0.2500 | 0.4800 |
| conversion | 0.9600 | 0.9000 | 0.9900 |
| safety_risk | 0.1050 | 0.0700 | 0.1500 |
| score | 0.3900 | 0.2800 | 0.4900 |
| selectivity | 0.6600 | 0.5600 | 0.7500 |
| yield | 0.6300 | 0.5200 | 0.7300 |

### Q08

This combines the highest catalyst loading, highest temperature, and a long residence. Reactant disappearance should be complete, but extensive parallel reaction and product degradation are expected to dominate. The safety interval crosses the declared 0.35 limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6700 | 0.9400 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.3000 | 0.2200 | 0.4100 |
| score | 0.0300 | 0.0000 | 0.1100 |
| selectivity | 0.1800 | 0.0600 | 0.3400 |
| yield | 0.1800 | 0.0500 | 0.3400 |

### Q09

The intermediate catalyst loading and 7200 s at 410 K should drive conversion close to completion. Compared with the short high-temperature schedules, the longer exposure should substantially increase byproduct formation and lower selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4800 | 0.3500 | 0.6100 |
| conversion | 0.9800 | 0.9300 | 1.0000 |
| safety_risk | 0.1600 | 0.1150 | 0.2200 |
| score | 0.2500 | 0.1400 | 0.3600 |
| selectivity | 0.5300 | 0.4000 | 0.6500 |
| yield | 0.5200 | 0.3900 | 0.6400 |

### Q10

The chemical state at termination should be almost the same as Q09. Quenching is predicted mainly to reduce the final thermal-risk state, with only a small possible benefit from suppressing residual post-heating chemistry; the expected score is therefore slightly higher.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4700 | 0.3400 | 0.6000 |
| conversion | 0.9800 | 0.9300 | 1.0000 |
| safety_risk | 0.1450 | 0.1000 | 0.2000 |
| score | 0.2600 | 0.1500 | 0.3700 |
| selectivity | 0.5300 | 0.4000 | 0.6500 |
| yield | 0.5200 | 0.3900 | 0.6400 |

### Q11

Long heating at 350 K should eventually generate high conversion at the intermediate catalyst loading. The campaign's 10800 s experiment showed that extra time can trade selectivity for conversion, so 14400 s is predicted to give substantial accumulated byproduct and only moderate target yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4900 | 0.3600 | 0.6300 |
| conversion | 0.9800 | 0.9200 | 1.0000 |
| safety_risk | 0.1700 | 0.1200 | 0.2300 |
| score | 0.2400 | 0.1300 | 0.3500 |
| selectivity | 0.5200 | 0.3900 | 0.6500 |
| yield | 0.5100 | 0.3800 | 0.6400 |

### Q12

Although 465 K is an extrapolation beyond the campaign, the residence is only 1800 s and much of it should occur during thermal ramp-up. Rapid target formation is expected before the long-exposure degradation seen in Q06 and Q08, but uncertainty is wide because the temperature is untested.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3400 | 0.2200 | 0.4900 |
| conversion | 0.9700 | 0.8800 | 1.0000 |
| safety_risk | 0.1300 | 0.0850 | 0.1900 |
| score | 0.3900 | 0.2600 | 0.5000 |
| selectivity | 0.6400 | 0.5100 | 0.7500 |
| yield | 0.6200 | 0.4800 | 0.7400 |

## K2 — Retrospective analysis

1. Assessment of the initial claims

The only substantive mechanistic claim in the initial packet was: “The target pathway may have an appreciable reverse channel on the public support,” with moderate confidence. The remaining initial information mainly established material identities, anonymity, benchmark status, and instrument rules; it did not provide a task-specific property dossier or quantitative kinetic claims.

The reverse-channel claim was not directly tested. In K1 I said that the campaign was “consistent with that possibility” but did not uniquely demonstrate it. That remains the correct distinction. Batch 10 reached conversion 0.9593 after 10800 s at 350 K, compared with 0.8734 for batch 4 after 7200 s, while selectivity fell from 0.7417 to 0.6701 and yield fell slightly from 0.6650 to 0.6507. This supports cumulative secondary chemistry, but it does not specifically support reversal: conversion continued to rise rather than fall. Product degradation or increasingly important parallel conversion can explain the same observation without any reverse reaction.

There was therefore no decisive refutation of an appreciable reverse channel, but neither was there positive identification of one. The lack of a conversion reversal is weak evidence against reversal being dominant over the tested interval, not evidence that its rate is zero. K1 appropriately retained an irreversible R → P → D alternative, although the wording about yield saturation being consistent with reversibility could have been more guarded.

The categorical nature of the materials was strongly respected by the data. For example, water outperformed the other named solvents under the matched Catalyst D screen, but nothing in the observations supports interpreting that through real-world polarity, boiling point, or named-chemical reactivity. No empirical observation contradicted the initial warning against such inference.

2. Experiments that formed or changed the interpretation

Batch 1 provided the first genuinely mechanistic update because it contained an intermediate HPLC measurement. After the first 3600 s segment at a 350 K setpoint, conversion was 0.4799, selectivity 0.7842, yield 0.3704, and byproduct signal 0.1043. After another 3600 s, the final assay gave conversion 0.7212, selectivity 0.7495, yield 0.5370, and byproduct 0.1831. This changed the initial vague picture into a time-dependent competition model: target accumulated, but selectivity deteriorated and byproduct accumulated with additional exposure. The reported temperature increments of 49.17 K and then 1.53 K also established that the thermal state approached the setpoint gradually rather than instantaneously.

Batches 2-4 materially changed the catalyst ranking. Under approximately matched water/350 K/7200 s conditions, Catalyst D in batch 4 produced the best score, 0.3705, and yield, 0.6650. Catalyst C in batch 3 had both lower conversion, 0.6797, and much lower selectivity, 0.5929, ruling out an explanation based only on slower kinetics. These batches motivated using Catalyst D thereafter.

Batches 4-7 established the solvent effect. Batch 6 with acetonitrile had higher conversion than water, 0.9366 versus 0.8734, but worse selectivity, byproduct, degradation, risk, and score. Batch 7 with toluene was especially informative: conversion remained high at 0.8806, while selectivity fell to 0.5407 and byproduct rose to 0.4228. This separated reactant disappearance from useful target formation and strengthened the competing-pathway interpretation.

Batches 8-10 formed the main exposure argument. Batch 8 at 330 K retained high selectivity, 0.7850, but had only 0.7297 conversion. Batch 9 at 370 K increased conversion to 0.9404 and yield to 0.6870, with more degradation. Most importantly, the longer batch 10 increased conversion but lost yield and score relative to batch 4. That comparison was the strongest evidence for an optimum in residence time rather than a monotonic “more conversion is always better” rule.

Batches 11 and 12 changed the operational conclusion. Their hotter, shorter schedules gave approximately 0.95 conversion while preserving selectivity near 0.77. Batch 12 reached the sample-high score of 0.4095 at risk 0.1703. These results supported the high-temperature/short-time operating hypothesis within the observed window.

Several design choices were not grounded in prior evidence. The initial 350 K and 7200 s baseline was a reasonable but unvalidated guess. Using the maximum reagent, solvent, and catalyst allocations in every batch was primarily a campaign-resource strategy, not a mechanistic conclusion. Fixing 600 rpm assumed that mixing was adequate without testing it. Dividing batch 1 into two heat segments and then switching to single heat operations was pragmatic rather than part of a prespecified kinetic design. The later 390 K/5400 s and 410 K/4500 s schedules were data-driven extrapolations from batches 8-10, while the exact temperature-time combinations remained heuristic.

3. Principal competing mechanisms and what the data distinguish

The most important competition remains between:

A. R ⇌ P, with parallel R → B and possibly P → D; and
B. an entirely irreversible network, such as R → P, R → B, and P → D.

The experiments establish that target formation competes with undesirable chemistry and that additional exposure can lower final target yield after conversion is already high. They do not determine whether loss of P regenerates R. No batch deliberately created a high-P state and then looked for renewed reactant formation under conditions favoring reversal.

A second unresolved distinction is whether the byproduct proxy mainly represents direct R → B formation or consecutive P → B/D chemistry. Batch 1 and the batch 4 versus batch 10 comparison show that the byproduct signal grows with time, but both direct and consecutive pathways predict that. The separate degradation-warning channel helps, yet it does not provide a stoichiometric assignment.

A third competition concerns catalyst function. Catalyst D could increase the forward target rate, suppress competing rates, change the forward/reverse ratio, or do all three. The fixed catalyst loading prevents separation of rate acceleration from catalyst-dependent selectivity. Similarly, the solvent screen establishes performance differences but cannot distinguish kinetic effects, equilibrium effects, heat-transfer changes, or synthetic observation-response differences.

The data do distinguish simple one-dimensional explanations. Conversion alone cannot explain score because batches 6, 7, and 10 had high conversion but poorer selectivity and score. Temperature alone cannot explain performance because residence time changed the tradeoff substantially. A model in which every reaction channel scales identically with temperature is also inadequate: the hotter, shorter batches 11 and 12 preserved better selectivity than the longer batch 10.

4. One additional complete experiment

If allowed exactly one additional legal experiment, I would prioritize discrimination between reversibility and irreversible degradation rather than another score search. I would reproduce the batch 12 preparation—0.080 L water, 0.040 mol reagent, and 0.005 mol Catalyst D at 600 rpm—and heat toward 410 K for 4500 s. I would then take an HPLC measurement, quench, hold the quenched mixture with stirring for a substantial legal interval such as 7200 s, terminate, and obtain the final assay.

The key comparison would be the within-batch change between the post-heating HPLC state and the final state after the cool hold:

• If target yield and conversion both decreased, with a corresponding recovery of the reactant proxy and little increase in degradation or byproduct proxies, that would strongly increase confidence in a reverse P → R channel.
• If target yield decreased while conversion remained approximately constant and degradation warning increased, that would favor irreversible product degradation.
• If conversion increased further while selectivity declined and byproduct increased, residual forward and parallel chemistry would dominate even after quenching.
• If all channels remained stable within uncertainty, the cool-state reverse and degradation rates would both be constrained to be small on that timescale, but high-temperature reversibility would remain unresolved.

This would still not be perfect because HPLC and final assay are different observation platforms, and the quench itself changes the state. Ideally one would want matched repeated measurements or an isolated-product experiment, neither of which was available in the completed design. Nevertheless, the direction of conversion change would be more discriminating than another endpoint-only temperature screen.

5. Tradeoff between identifiability and score optimization

The research goal explicitly prioritized strong safe-score performance under a risk limit. The design therefore moved from broad screening to exploitation: four catalyst conditions, four solvent conditions with the leading catalyst, and then five increasingly focused temperature-time trials using Catalyst D in water. That sequence was effective for finding a better observed score, rising from 0.3135 in batch 1 to 0.4095 in batch 12.

This optimization focus sacrificed identifiability. All batches used the same maximum material amounts, so reaction order, catalyst-loading dependence, dilution effects, and scale dependence were not studied. Stirring was fixed at 600 rpm. There were no replicates, no randomized repeats, and no direct reverse-channel challenge. Temperature and time were deliberately co-adjusted in batches 11 and 12 to improve performance, making their individual contributions difficult to separate.

The early Catalyst C and non-water solvent batches sacrificed likely score in exchange for categorical identification. Batch 3 scored only 0.2246 and batch 7 only 0.2260, but they were valuable in ruling out those options and showing that high conversion need not imply useful selectivity. Conversely, batches 11 and 12 were principally exploitation experiments: they improved the score but added less clean mechanistic information than a factorial temperature-time pair or a replicated kinetic trajectory would have.

The use of one intermediate HPLC measurement in every batch was not fully optimized for identifiability. In most batches it occurred immediately after the sole heat operation, so it largely duplicated the endpoint chemical state on a different platform. A more informative design would have measured halfway through heating and then continued, as happened in batch 1.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts contained peak areas, assignments, spectra, and calibration metadata that were not quantitatively integrated into a joint model. I relied mainly on processed estimates. The action receipts also contained temperature changes, process times, risk increments, and quench behavior. Apart from batch 1, I did not fit those thermal observations to estimate a heating time constant or reconstruct temperature-time integrals. That limited the later extrapolations.

The systematic difference between intermediate HPLC and final-assay values was acknowledged but not modeled. Batch 12, for example, had intermediate HPLC conversion 0.9540, selectivity 0.7752, yield 0.7368, and byproduct 0.2300, followed by a final assay with nearby but distinct values. A hierarchical instrument-bias model could have separated process uncertainty from measurement uncertainty. Cost information was also difficult to use because the visible cost saturated at 1.0 after catalyst addition.

The least reliable blind predictions are Q06, Q08, and Q12 because they use 465 K, beyond K1's stated empirical range of approximately 330-410 K. Q08 is especially uncertain because it combines 465 K, 7200 s, and the highest catalyst loading. I predicted conversion 0.995 with an 80% interval of 0.97-1.00 and score 0.03 with an interval of 0.00-0.11. Those intervals were probably too narrow for such a compounded extrapolation. The direction—high conversion with severe selectivity loss—was mechanistically motivated, but its magnitude was weakly constrained.

Q02 and Q04 are also unreliable because 14400 s at 410 K exceeds the observed joint temperature-time exposure. Their near-complete conversion intervals may be overly confident, and the degree of selectivity collapse depends on whether degradation is catalyst-coupled, purely thermal, or equilibrium-limited.

All 12 blind queries changed scale, concentration, catalyst loading, and stirring simultaneously relative to the campaign. The campaign fixed the catalyst/reagent ratio at 0.125, whereas the queries used ratios of about 0.04, 0.105, or 0.173. No catalyst-loading law was measured. The predictions treated activity approximately as loading-scaled, which was an explicit but unvalidated modeling choice. Q01, Q03, Q05, and Q07 therefore also had intervals that should arguably have been wider.

Q09 versus Q10 is comparatively more reliable as a directional comparison: I predicted nearly unchanged chemistry with a modest risk reduction from quenching. Even there, the absolute risk estimates were uncertain because the campaign did not establish how risk scales from 0.080 L to 0.005 L or from 600 to 400 rpm.

These weaknesses are partly consistent with K1, which explicitly said that catalyst loading, concentration, mixing, behavior above 410 K, and transfer beyond the tested scale were unidentified. The blind-prediction rationale also acknowledged those extrapolations. However, several numerical intervals—especially Q08 conversion, Q06 conversion, and the high-temperature score intervals—were more precise than those caveats justified. The prose recognized model uncertainty better than the intervals did.

7. Limitations of the sealed recommendation

Batch 12 is the sample-in highest observed result, not a proven optimum. It had the highest measured score, 0.4095, among the 12 completed batches and remained below the risk limit at 0.1703. That justifies selecting it from the observed campaign. It does not establish global optimality, or even local optimality, because the search ended at 410 K and 4500 s and did not independently vary neighboring temperatures and times.

The recommendation has not been replicated. Final-assay noise, process variability, and adaptive winner selection can make the largest observed score optimistic. Batch 11 scored 0.4006, close enough that their ordering could change under replication. Moreover, batch 12's higher temperature and shorter time were changed together, so its advantage cannot be assigned uniquely to either factor.

Repeatability should first be tested with several exact independent replicates of batch 12, reporting the distribution of score, risk, yield, selectivity, byproduct, and degradation rather than only their means. Local robustness should then be examined with a small neighborhood design around the recommendation—for example temperatures near 390, 410, and 430 K crossed with durations near 3600, 4500, and 5400 s—plus modest perturbations in catalyst amount and stirring. A robust operating region with a stable lower-tail score and risk margin would be more valuable than a sharp nominal maximum.

Material robustness requires repeating the local comparison with at least the next-best catalyst and solvent categories. The campaign suggests that water and Catalyst D are favorable, but it does not show that the same temperature-time optimum applies to Catalyst B or to another solvent. Scale robustness would require varying reagent concentration and vessel fill while monitoring the actual thermal trajectory. Cross-world generalization would require repetition across independent benchmark worlds or seeds; nothing in one campaign proves that the same anonymous catalyst category retains its latent profile elsewhere.

Finally, the safety margin is benchmark-specific. The fact that batch 12 had observed risk 0.1703 below a limit of 0.35 does not establish physical process safety, scale-up safety, or tolerance to heating-control failure. The sealed recommendation is therefore best described as the highest-scoring observed batch within one bounded synthetic campaign, with promising but unverified local structure around it.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 102.8 | none | 0 |
| Q | yes | 0 | 100.4 | none | 0 |
| K2 | yes | 0 | 92.2 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0897 | 0.6833 | 0.2550 | 0.3294 |
| conversion | 0.0237 | 0.9167 | 0.1150 | 0.1209 |
| safety_risk | 0.0992 | 0.5000 | 0.1108 | 0.5929 |
| score | 0.0382 | 0.9833 | 0.1983 | 0.1987 |
| selectivity | 0.0902 | 0.7333 | 0.2500 | 0.3725 |
| yield | 0.0771 | 0.8333 | 0.2642 | 0.3186 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2000 | 0.1200 | 0.3100 | 0.1394 | 0.1397, 0.1462, 0.1413, 0.1384, 0.1316 |
| conversion | 0.5300 | 0.3800 | 0.6800 | 0.5419 | 0.5369, 0.5361, 0.5497, 0.5430, 0.5438 |
| safety_risk | 0.0850 | 0.0550 | 0.1250 | 0.2496 | 0.2496, 0.2496, 0.2496, 0.2496, 0.2496 |
| score | 0.2500 | 0.1500 | 0.3400 | 0.2633 | 0.2655, 0.2652, 0.2643, 0.2587, 0.2626 |
| selectivity | 0.6900 | 0.5700 | 0.7900 | 0.7421 | 0.7503, 0.7451, 0.7464, 0.7401, 0.7288 |
| yield | 0.3600 | 0.2400 | 0.4900 | 0.4090 | 0.4107, 0.4134, 0.4068, 0.3985, 0.4152 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5500 | 0.4000 | 0.7000 | 0.7361 | 0.7397, 0.7292, 0.7492, 0.7245, 0.7377 |
| conversion | 0.9800 | 0.9100 | 1.0000 | 0.9894 | 0.9940, 0.9820, 0.9971, 0.9889, 0.9850 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 | 0.2515 | 0.2515, 0.2515, 0.2515, 0.2515, 0.2515 |
| score | 0.1800 | 0.0800 | 0.2800 | 0.1240 | 0.1282, 0.1246, 0.1241, 0.1240, 0.1192 |
| selectivity | 0.4300 | 0.2700 | 0.5800 | 0.2740 | 0.2821, 0.2767, 0.2785, 0.2713, 0.2612 |
| yield | 0.4100 | 0.2500 | 0.5700 | 0.2699 | 0.2741, 0.2715, 0.2653, 0.2716, 0.2669 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2500 | 0.1600 | 0.3600 | 0.1516 | 0.1469, 0.1490, 0.1465, 0.1682, 0.1471 |
| conversion | 0.9300 | 0.8400 | 0.9800 | 0.9045 | 0.9126, 0.8934, 0.9063, 0.9038, 0.9066 |
| safety_risk | 0.0900 | 0.0600 | 0.1300 | 0.2526 | 0.2526, 0.2526, 0.2526, 0.2526, 0.2526 |
| score | 0.4600 | 0.3400 | 0.5600 | 0.4366 | 0.4406, 0.4357, 0.4386, 0.4338, 0.4345 |
| selectivity | 0.7200 | 0.6300 | 0.8000 | 0.8453 | 0.8629, 0.8401, 0.8425, 0.8499, 0.8314 |
| yield | 0.6700 | 0.5500 | 0.7700 | 0.7624 | 0.7594, 0.7661, 0.7686, 0.7528, 0.7653 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6700 | 0.5200 | 0.8200 | 0.7894 | 0.7706, 0.7875, 0.8048, 0.7903, 0.7936 |
| conversion | 0.9900 | 0.9600 | 1.0000 | 0.9959 | 1.0000, 0.9907, 1.0000, 0.9890, 1.0000 |
| safety_risk | 0.2100 | 0.1600 | 0.2800 | 0.2519 | 0.2519, 0.2519, 0.2519, 0.2519, 0.2519 |
| score | 0.1000 | 0.0200 | 0.2100 | 0.0871 | 0.0917, 0.0894, 0.0841, 0.0875, 0.0830 |
| selectivity | 0.3200 | 0.1700 | 0.4800 | 0.2562 | 0.2603, 0.2645, 0.2443, 0.2601, 0.2517 |
| yield | 0.3100 | 0.1600 | 0.4700 | 0.2596 | 0.2675, 0.2614, 0.2583, 0.2597, 0.2510 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 | 0.2859 | 0.2874, 0.2976, 0.2794, 0.2754, 0.2894 |
| conversion | 0.5500 | 0.4000 | 0.7000 | 0.7070 | 0.7056, 0.7061, 0.7105, 0.7038, 0.7091 |
| safety_risk | 0.1000 | 0.0650 | 0.1450 | 0.1416 | 0.1416, 0.1416, 0.1416, 0.1416, 0.1416 |
| score | 0.2500 | 0.1500 | 0.3500 | 0.2914 | 0.2937, 0.2855, 0.2896, 0.2953, 0.2931 |
| selectivity | 0.6900 | 0.5800 | 0.7900 | 0.6004 | 0.6055, 0.5865, 0.5961, 0.6143, 0.5996 |
| yield | 0.3800 | 0.2600 | 0.5000 | 0.4163 | 0.4191, 0.4105, 0.4134, 0.4182, 0.4204 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7200 | 0.5600 | 0.8700 | 0.6099 | 0.6123, 0.6066, 0.6036, 0.6193, 0.6079 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9947 | 1.0000, 0.9837, 0.9990, 0.9934, 0.9973 |
| safety_risk | 0.2800 | 0.2000 | 0.3800 | 0.4259 | 0.4259, 0.4259, 0.4259, 0.4259, 0.4259 |
| score | 0.0700 | 0.0100 | 0.1700 | 0.1323 | 0.1345, 0.1397, 0.1227, 0.1333, 0.1313 |
| selectivity | 0.2800 | 0.1300 | 0.4400 | 0.3927 | 0.3842, 0.4258, 0.3714, 0.4011, 0.3809 |
| yield | 0.2700 | 0.1200 | 0.4300 | 0.3962 | 0.4056, 0.3968, 0.3843, 0.3939, 0.4005 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3600 | 0.2500 | 0.4800 | 0.3215 | 0.3256, 0.3232, 0.3132, 0.3178, 0.3278 |
| conversion | 0.9600 | 0.9000 | 0.9900 | 0.9676 | 0.9735, 0.9585, 0.9756, 0.9696, 0.9610 |
| safety_risk | 0.1050 | 0.0700 | 0.1500 | 0.1439 | 0.1439, 0.1439, 0.1439, 0.1439, 0.1439 |
| score | 0.3900 | 0.2800 | 0.4900 | 0.4053 | 0.4066, 0.4069, 0.4029, 0.4048, 0.4054 |
| selectivity | 0.6600 | 0.5600 | 0.7500 | 0.6857 | 0.6945, 0.6952, 0.6796, 0.6717, 0.6874 |
| yield | 0.6300 | 0.5200 | 0.7300 | 0.6572 | 0.6533, 0.6575, 0.6531, 0.6640, 0.6580 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8200 | 0.6700 | 0.9400 | 0.6400 | 0.6433, 0.6384, 0.6379, 0.6363, 0.6440 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9930 | 0.9781, 0.9871, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.3000 | 0.2200 | 0.4100 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0300 | 0.0000 | 0.1100 | 0.1053 | 0.1049, 0.1045, 0.0992, 0.1060, 0.1120 |
| selectivity | 0.1800 | 0.0600 | 0.3400 | 0.4013 | 0.4087, 0.3948, 0.3933, 0.3967, 0.4131 |
| yield | 0.1800 | 0.0500 | 0.3400 | 0.3962 | 0.3944, 0.3998, 0.3842, 0.3991, 0.4038 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4800 | 0.3500 | 0.6100 | 0.4912 | 0.4900, 0.4852, 0.4940, 0.4841, 0.5025 |
| conversion | 0.9800 | 0.9300 | 1.0000 | 0.9974 | 1.0000, 0.9923, 1.0000, 1.0000, 0.9946 |
| safety_risk | 0.1600 | 0.1150 | 0.2200 | 0.2523 | 0.2523, 0.2523, 0.2523, 0.2523, 0.2523 |
| score | 0.2500 | 0.1400 | 0.3600 | 0.2752 | 0.2725, 0.2767, 0.2744, 0.2725, 0.2800 |
| selectivity | 0.5300 | 0.4000 | 0.6500 | 0.5164 | 0.5050, 0.5198, 0.5199, 0.5132, 0.5241 |
| yield | 0.5200 | 0.3900 | 0.6400 | 0.5154 | 0.5150, 0.5181, 0.5106, 0.5099, 0.5231 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4700 | 0.3400 | 0.6000 | 0.4949 | 0.4892, 0.4966, 0.4999, 0.5047, 0.4842 |
| conversion | 0.9800 | 0.9300 | 1.0000 | 0.9942 | 0.9991, 0.9998, 1.0000, 0.9939, 0.9781 |
| safety_risk | 0.1450 | 0.1000 | 0.2000 | 0.1459 | 0.1459, 0.1459, 0.1459, 0.1459, 0.1459 |
| score | 0.2600 | 0.1500 | 0.3700 | 0.3201 | 0.3218, 0.3178, 0.3232, 0.3200, 0.3179 |
| selectivity | 0.5300 | 0.4000 | 0.6500 | 0.5173 | 0.5167, 0.5191, 0.5235, 0.5115, 0.5160 |
| yield | 0.5200 | 0.3900 | 0.6400 | 0.5165 | 0.5199, 0.5082, 0.5188, 0.5198, 0.5156 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4900 | 0.3600 | 0.6300 | 0.5489 | 0.5697, 0.5532, 0.5308, 0.5504, 0.5403 |
| conversion | 0.9800 | 0.9200 | 1.0000 | 0.9903 | 0.9833, 0.9865, 0.9912, 0.9955, 0.9949 |
| safety_risk | 0.1700 | 0.1200 | 0.2300 | 0.1434 | 0.1434, 0.1434, 0.1434, 0.1434, 0.1434 |
| score | 0.2400 | 0.1300 | 0.3500 | 0.2810 | 0.2783, 0.2768, 0.2825, 0.2819, 0.2854 |
| selectivity | 0.5200 | 0.3900 | 0.6500 | 0.4585 | 0.4538, 0.4471, 0.4607, 0.4561, 0.4750 |
| yield | 0.5100 | 0.3800 | 0.6400 | 0.4602 | 0.4583, 0.4578, 0.4625, 0.4628, 0.4597 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3400 | 0.2200 | 0.4900 | 0.2069 | 0.2063, 0.2058, 0.1964, 0.2129, 0.2132 |
| conversion | 0.9700 | 0.8800 | 1.0000 | 0.9513 | 0.9555, 0.9519, 0.9512, 0.9428, 0.9552 |
| safety_risk | 0.1300 | 0.0850 | 0.1900 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.3900 | 0.2600 | 0.5000 | 0.3582 | 0.3619, 0.3582, 0.3617, 0.3502, 0.3588 |
| selectivity | 0.6400 | 0.5100 | 0.7500 | 0.7886 | 0.7934, 0.7801, 0.8111, 0.7735, 0.7849 |
| yield | 0.6200 | 0.4800 | 0.7400 | 0.7491 | 0.7543, 0.7544, 0.7438, 0.7407, 0.7521 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2243 | 0.2115 | -0.0128 |
| conversion | 0.9492 | 0.9604 | 0.0112 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1590 | 0.1671 | 0.0080 |
| safety_risk | 0.1703 | 0.1703 | 0.0000 |
| score | 0.4095 | 0.4092 | -0.0002 |
| selectivity | 0.7692 | 0.7654 | -0.0039 |
| virtual_spectrum_summary | 0.1949 | 0.1915 | -0.0034 |
| yield | 0.7472 | 0.7463 | -0.0009 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
