# RX-W05--S--mechanism_discovery--Opaque

## Run summary

- World: `RX-W05`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `86`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `posttest-repair-v11`
- Recovery version: `recovery-v11-parallel4-transport-repair`
- Repaired stages: `K1, Q, K2`
- Source experiments rerun: `False`
- Original source thread reused: `True`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `10`
- Rationale: Batch 10 gave the highest observed safe score (about 0.364) with strong yield (about 0.677) at lower risk and degradation than the hotter Batch 11 or prolonged Batch 12.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.2604 | 0.7608 | 0.3507 | 0.0808 | 0.0157 | 0.1047 | 0.1823 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.3485 | 0.7611 | 0.4352 | 0.1120 | 0.0192 | 0.1139 | 0.2219 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.1865 | 0.6000 | 0.3052 | 0.1258 | 0.0161 | 0.0979 | 0.1110 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.4171 | 0.8395 | 0.4805 | 0.0835 | 0.0325 | 0.1204 | 0.2706 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.4082 | 0.8020 | 0.5062 | 0.1044 | 0.0403 | 0.1451 | 0.2491 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.4975 | 0.8151 | 0.5987 | 0.0986 | 0.0626 | 0.1733 | 0.2847 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.3534 | 0.6750 | 0.5186 | 0.1637 | 0.0648 | 0.1725 | 0.1843 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 300 K x 3600 s @ 600 rpm | no | 0.2976 | 0.8349 | 0.3533 | 0.0519 | 0.0000 | 0.1459 | 0.1974 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6040 | 0.8113 | 0.7476 | 0.1597 | 0.0831 | 0.1913 | 0.3331 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.6769 | 0.8053 | 0.8689 | 0.2036 | 0.1289 | 0.2121 | 0.3635 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | no | 0.7110 | 0.7739 | 0.9585 | 0.2296 | 0.1673 | 0.2486 | 0.3619 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 1800 s @ 600 rpm → 370 K x 5400 s @ 600 rpm | yes | 0.5898 | 0.5956 | 0.9890 | 0.3937 | 0.3402 | 0.2026 | 0.2926 |

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
    "byproduct_signal": 0.08080356568098068,
    "conversion": 0.35070133209228516,
    "cost": 1.0,
    "degradation_warning": 0.01568787544965744,
    "safety_risk": 0.10473736375570297,
    "score": 0.18230389058589935,
    "selectivity": 0.760772705078125,
    "virtual_spectrum_summary": 0.05150150507688522,
    "yield": 0.2604309916496277
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
      "duration_s": 3600,
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
    "byproduct_signal": 0.11203674972057343,
    "conversion": 0.43523791432380676,
    "cost": 1.0,
    "degradation_warning": 0.019175972789525986,
    "safety_risk": 0.1139422357082367,
    "score": 0.22190456092357635,
    "selectivity": 0.7610607743263245,
    "virtual_spectrum_summary": 0.07024940103292465,
    "yield": 0.3484739661216736
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
      "duration_s": 3600,
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
    "byproduct_signal": 0.1258397400379181,
    "conversion": 0.30519235134124756,
    "cost": 1.0,
    "degradation_warning": 0.01609247736632824,
    "safety_risk": 0.09790848195552826,
    "score": 0.1110491082072258,
    "selectivity": 0.5999793410301208,
    "virtual_spectrum_summary": 0.07645346969366074,
    "yield": 0.18648463487625122
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
      "duration_s": 3600,
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
    "byproduct_signal": 0.08347683399915695,
    "conversion": 0.4805450439453125,
    "cost": 1.0,
    "degradation_warning": 0.032524656504392624,
    "safety_risk": 0.12037037312984467,
    "score": 0.27061378955841064,
    "selectivity": 0.8395208120346069,
    "virtual_spectrum_summary": 0.06054835394024849,
    "yield": 0.41711437702178955
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
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
    "byproduct_signal": 0.10441241413354874,
    "conversion": 0.5061932802200317,
    "cost": 1.0,
    "degradation_warning": 0.04026622697710991,
    "safety_risk": 0.14510904252529144,
    "score": 0.24908261001110077,
    "selectivity": 0.8019636869430542,
    "virtual_spectrum_summary": 0.07554662972688675,
    "yield": 0.4081785976886749
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
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
    "byproduct_signal": 0.09861430525779724,
    "conversion": 0.5986753702163696,
    "cost": 1.0,
    "degradation_warning": 0.06257688999176025,
    "safety_risk": 0.17325925827026367,
    "score": 0.28468057513237,
    "selectivity": 0.8150506615638733,
    "virtual_spectrum_summary": 0.0823974683880806,
    "yield": 0.4975425601005554
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
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
    "byproduct_signal": 0.16367842257022858,
    "conversion": 0.5186305642127991,
    "cost": 1.0,
    "degradation_warning": 0.0647878348827362,
    "safety_risk": 0.17251096665859222,
    "score": 0.1843414008617401,
    "selectivity": 0.6749697923660278,
    "virtual_spectrum_summary": 0.11917766183614731,
    "yield": 0.3534145653247833
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
      "catalyst": 3,
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
    "byproduct_signal": 0.05192244052886963,
    "conversion": 0.3532595634460449,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.14589081704616547,
    "score": 0.19743302464485168,
    "selectivity": 0.8348643779754639,
    "virtual_spectrum_summary": 0.028557341545820236,
    "yield": 0.29760462045669556
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
      "catalyst": 3,
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
    "byproduct_signal": 0.15968020260334015,
    "conversion": 0.7475559711456299,
    "cost": 1.0,
    "degradation_warning": 0.0830821618437767,
    "safety_risk": 0.19127100706100464,
    "score": 0.3331200182437897,
    "selectivity": 0.8113022446632385,
    "virtual_spectrum_summary": 0.12521108984947205,
    "yield": 0.6040270328521729
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
    "byproduct_signal": 0.20362012088298798,
    "conversion": 0.8688533902168274,
    "cost": 1.0,
    "degradation_warning": 0.1288665533065796,
    "safety_risk": 0.2120669037103653,
    "score": 0.3635319769382477,
    "selectivity": 0.8052789568901062,
    "virtual_spectrum_summary": 0.16998101770877838,
    "yield": 0.6768925189971924
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
    "byproduct_signal": 0.22959913313388824,
    "conversion": 0.9584770798683167,
    "cost": 1.0,
    "degradation_warning": 0.16733209788799286,
    "safety_risk": 0.24855758249759674,
    "score": 0.36186280846595764,
    "selectivity": 0.7738931179046631,
    "virtual_spectrum_summary": 0.20157897472381592,
    "yield": 0.7109817862510681
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `86`.

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
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 86,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.39370930194854736,
    "conversion": 0.9890400767326355,
    "cost": 1.0,
    "degradation_warning": 0.3401808738708496,
    "safety_risk": 0.20256921648979187,
    "score": 0.2925613224506378,
    "selectivity": 0.5956034064292908,
    "virtual_spectrum_summary": 0.36962148547172546,
    "yield": 0.5897815227508545
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Evidential basis and scope

The material packet supplied no task-specific kinetic or thermodynamic dossier. It identified four anonymous catalyst formulations, four solvent categories, and an anonymous limiting reagent, while explicitly warning that the solvent effects were benchmark categorical effects rather than predictions from real solvent properties. Consequently, the account below is empirical and benchmark-specific. It should not be interpreted as a mechanism for a named chemical reaction.

All twelve batches used 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, and 600 rpm stirring, except that temperature, duration, solvent, catalyst identity, and quench history were varied as described below. Thus, concentration, catalyst loading, and mixing-rate effects were not independently identified. Final-assay values are the principal endpoint evidence; intermediate HPLC results provide limited time-course information. Small HPLC/final-assay discrepancies are consistent with their stated measurement noise and should not automatically be treated as real chemical changes.

2. Proposed process structure

My preferred minimal explanation is a catalyst- and solvent-dependent network with productive conversion, competing byproduct formation, and slower thermal degradation:

R -> P  (productive path)
R -> B  (parallel competing path)
P -> D and/or B -> D  (secondary thermal degradation)

Here R is the public reactant, P the target product, B the measured byproduct class, and D the degradation class. A useful provisional kinetic form is:

dR/dt = -a(t)[kP(T,catalyst,solvent) + kB(T,catalyst,solvent)]R

dP/dt = a(t)kP R - kPD(T,solvent)P

dB/dt = a(t)kB R + fB kPD P - kBD B

dD/dt = (1-fB)kPD P + kBD B

da/dt = -kd(T,solvent,R,B)a

The activity variable a(t) allows catalyst deactivation or inhibition, but deactivation was not directly measured. A simpler model with constant catalyst activity and only substrate depletion plus sequential degradation remains viable.

For each elementary or effective rate constant, an Arrhenius-like dependence is plausible within the explored range:

kj = Aj Fcat,j Fsolv,j exp[-Ej/(RT(t))].

The factors Fcat,j and Fsolv,j are categorical benchmark coefficients, not inferred physical-property correlations. Temperature should be represented by the actual vessel history T(t), rather than merely the requested set point. For example, Batch 12’s first 1,800 s heat step increased temperature by about 66.83 K, its subsequent 5,400 s step added only about 3.37 K, and quenching lowered it by 45 K. This shows substantial initial thermal approach followed by near-set-point residence. Batch 1 similarly recorded a 30.89 K rise during its 330 K heat operation. A first-order thermal approximation, dT/dt = [Tset - T]/tau, is therefore more defensible than assuming an instantaneous temperature jump, although tau was not estimated reliably.

The approximate relationship yield ≈ conversion × selectivity is broadly useful. It is not exact because the three channels have independent calibration and noise, and because the public observables may represent bounded proxy quantities rather than a perfectly closed mole balance.

3. Catalyst effects

Batches 1–4 compared catalysts A–D in water at a nominal 330 K for 3,600 s. Their final-assay results were:

Batch 1, Catalyst A: conversion 0.351, selectivity 0.761, yield 0.260, byproduct 0.081, degradation 0.016.
Batch 2, Catalyst B: conversion 0.435, selectivity 0.761, yield 0.348, byproduct 0.112, degradation 0.019.
Batch 3, Catalyst C: conversion 0.305, selectivity 0.600, yield 0.186, byproduct 0.126, degradation 0.016.
Batch 4, Catalyst D: conversion 0.481, selectivity 0.840, yield 0.417, byproduct 0.083, degradation 0.033.

This screen strongly changed the working account. Catalyst identity affects both overall rate and pathway partitioning; it cannot be represented merely as a common multiplier on all reaction rates. Catalyst D increased conversion while retaining the best selectivity in this comparison, suggesting a favorable increase in kP relative to kB. Catalyst C was inferior in both rate and pathway partitioning. Catalyst B improved conversion relative to A but did not improve final selectivity and produced a larger byproduct signal.

These are single observations in one solvent and at one temperature. Catalyst-by-solvent and catalyst-by-temperature interactions remain unidentified. Catalyst D is therefore the best observed catalyst under the screen conditions, not a universally dominant catalyst.

4. Solvent effects

Batches 4–7 held Catalyst D, nominal temperature, duration, loading, and stirring fixed while changing solvent. Final yields were 0.417 in water (Batch 4), 0.408 in ethanol (Batch 5), 0.498 in acetonitrile (Batch 6), and 0.353 in toluene (Batch 7). The corresponding final conversions were 0.481, 0.506, 0.599, and 0.519; selectivities were 0.840, 0.802, 0.815, and 0.675.

Acetonitrile produced the largest target yield principally through greater conversion while maintaining reasonably high selectivity. Water had slightly better observed selectivity but substantially less conversion. Toluene’s lower selectivity and higher byproduct signal, 0.164, indicate unfavorable pathway partitioning rather than simply a slower productive reaction. Ethanol was intermediate.

This supports solvent-specific effects on both effective activation rates and selectivity. It does not identify whether those effects arise from solvation, catalyst speciation, transport, or an encoded categorical benchmark coefficient. Because only Catalyst D received a complete solvent comparison, a solvent effect common to all catalysts is an extrapolation rather than an observation.

5. Temperature, conversion, and degradation

Batches 8, 6, 9, 10, and 11 form the most informative temperature series for Catalyst D in acetonitrile after 3,600 s at nominal targets of 300, 330, 350, 370, and 390 K:

Batch 8, 300 K: conversion 0.353, selectivity 0.835, yield 0.298, byproduct 0.052, degradation 0.000, risk 0.146, score 0.197.
Batch 6, 330 K: conversion 0.599, selectivity 0.815, yield 0.498, byproduct 0.099, degradation 0.063, risk 0.173, score 0.285.
Batch 9, 350 K: conversion 0.748, selectivity 0.811, yield 0.604, byproduct 0.160, degradation 0.083, risk 0.191, score 0.333.
Batch 10, 370 K: conversion 0.869, selectivity 0.805, yield 0.677, byproduct 0.204, degradation 0.129, risk 0.212, score 0.364.
Batch 11, 390 K: conversion 0.958, selectivity 0.774, yield 0.711, byproduct 0.230, degradation 0.167, risk 0.249, score 0.362.

Raising temperature strongly accelerates reagent conversion. However, byproduct and degradation signals also rise, while selectivity gradually falls. This is consistent with the unwanted pathways having equal or greater effective temperature sensitivity than the productive pathway. Target yield was still increasing at 390 K over a one-hour residence, but the safe score ceased improving: Batch 10 had the highest observed score, while Batch 11 had a slightly greater yield but lower selectivity and higher risk and degradation.

Thus there are two different empirical optima in the observed range: the highest measured final yield occurred in Batch 11, whereas the highest safe score occurred in Batch 10. Nothing in the data proves that either is the global optimum.

6. Time dependence, thermal history, and quenching

Batch 12 is the primary evidence that prolonged hot residence changes the network qualitatively. It used Catalyst D in acetonitrile at a nominal 370 K, with 1,800 s followed by another 5,400 s of heating. At 1,800 s, HPLC estimated conversion 0.598, selectivity 0.864, yield 0.525, and byproduct 0.081. After 7,200 s total heating, quenching, termination, and final assay, conversion was 0.989, selectivity 0.596, yield 0.590, byproduct 0.394, and degradation 0.340.

The additional hot residence drove conversion almost to completion, but most of the incremental reaction burden went into byproduct and degradation rather than durable target. Final yield was lower than the 0.677 observed after 3,600 s in Batch 10, despite higher conversion. This observation caused me to reject a simple one-step model in which longer time merely approaches a fixed product/selectivity plateau. A parallel-plus-sequential network, or a time-dependent loss of catalyst selectivity, is needed.

Batch 12 does not isolate quench chemistry because time and quench were changed together relative to Batch 10. Quenching did have a directly observed physical effect: it reduced temperature by 45 K and visible safety risk from approximately 0.222 immediately before quench to 0.203 afterward. There was no pre-quench final assay at 7,200 s, so the chemical effect of the quench cannot be separated from prolonged heating or assay noise. Termination without quench and quenching before termination should therefore not be assigned distinct compositional effects from these data alone.

7. Safety and score coupling

Observed safety risk increased with hotter operation and was reduced by quenching. In the acetonitrile temperature series, final risk rose from 0.146 at 300 K to 0.249 at 390 K. The score therefore reflects a coupling among yield, selectivity, degradation/byproduct burden, and risk rather than conversion alone. The public scoring formula was not identified, so I do not claim a quantitative score equation.

The recommended Batch 10 condition was chosen because it had the largest observed safe score, about 0.364, and a strong yield of about 0.677 at lower risk and degradation than Batch 11. This was an empirical operating recommendation, not proof of mechanistic or global optimality.

8. Measurement interpretation

Intermediate HPLC and final assay generally agreed in direction but not exactly. For Batch 10, HPLC gave conversion 0.867, selectivity 0.784, yield 0.669, and byproduct 0.201, whereas the final assay gave 0.869, 0.805, 0.677, and 0.204. This is good agreement. Larger differences in some other batches, such as Batch 2’s HPLC yield of 0.317 versus final-assay yield of 0.348, should be treated as a combination of instrument noise, sampling, and potentially minor state evolution, not as definitive kinetics. There were no replicates, so process variance cannot be separated from assay variance.

9. Alternative explanations and identifiability limits

Several competing explanations remain plausible:

• The loss of selectivity at high temperature or long time could be direct parallel formation of B from R, sequential destruction of P, or both. Batch 12 supports a secondary-time effect but does not determine whether P or B is the immediate degradation precursor.
• Apparent time-dependent selectivity could reflect catalyst deactivation, catalyst transformation into a less selective form, product inhibition, substrate depletion exposing a slower side reaction, or ordinary sequential degradation with constant catalyst activity.
• Solvent effects could act through intrinsic kinetic coefficients, catalyst activation/speciation, heat transfer, or encoded categorical response. The experiments do not distinguish these.
• The fall in score above 370 K could be caused by the explicit risk penalty, worsening chemistry, or both. The individual observed channels establish that both changed, but the hidden numerical score mapping was not fitted.
• Stirring was fixed, so transport limitation was not tested. The apparently smooth temperature response does not prove kinetic control.

10. Applicability and uncertainty

The most defensible empirical domain is Catalyst D in acetonitrile, 0.040 mol reagent in 0.080 L solvent with 0.005 mol catalyst, 600 rpm, nominal targets of 300–390 K, and residence times of 1,800–7,200 s. Predictions within that neighborhood may reasonably use interpolation of conversion and degradation versus integrated thermal exposure. Predictions outside it—different loadings, concentrations, mixing speeds, catalysts at high temperature, other catalyst-solvent combinations, temperatures above 390 K, or much longer times—would be extrapolations with substantially wider uncertainty.

The main evidential weaknesses are the lack of replication, sparse time sampling, confounding of prolonged heating with quenching in Batch 12, absence of direct catalyst-state measurements, and use of only one intermediate measurement per batch. Accordingly, the proposed equations are a compact explanatory scaffold rather than an identified kinetic law. The robust qualitative conclusions are that catalyst and solvent affect both rate and selectivity, conversion rises strongly with thermal exposure, unwanted conversion and degradation become increasingly important at high temperature and long residence, and rapid termination near an intermediate exposure can outperform driving the reagent to complete conversion.

## Q — Blind predictions

### Overall rationale

Predictions use the sealed report's parallel productive/byproduct pathways plus secondary thermal degradation. Conversion was scaled qualitatively with temperature, residence time, and catalyst-to-reagent ratio; selectivity and retained yield were reduced with prolonged high-temperature exposure. Catalyst B was only observed in water at 330 K, whereas every query uses acetonitrile, different concentrations, 400 rpm, and catalyst loadings outside the campaign design. Therefore the intervals include structural extrapolation uncertainty in addition to final-assay noise. Q06, Q08, and Q12 are particularly uncertain because 465 K exceeds the highest researched target by 75 K. Scores were estimated from the observed joint behavior of yield, selectivity, byproduct burden, and safety rather than from an identified scoring equation.

### Q01

Low Catalyst B loading limits conversion despite the high set point and short residence. The interval is wide because Catalyst B was never tested in acetonitrile or at 410 K, and the thermal ramp occupies an appreciable part of 1,800 s.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1800 | 0.0700 | 0.3400 |
| conversion | 0.5000 | 0.2900 | 0.7300 |
| safety_risk | 0.1100 | 0.0500 | 0.1900 |
| score | 0.2300 | 0.1000 | 0.3900 |
| selectivity | 0.6800 | 0.4700 | 0.8400 |
| yield | 0.3400 | 0.1600 | 0.5400 |

### Q02

Four hours at 410 K should compensate for low catalyst loading and nearly exhaust the reagent, but prolonged hot residence is expected to divert or degrade much of the target. This is a major time extrapolation beyond the research campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6200 | 0.3800 | 0.8500 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.2200 | 0.1300 | 0.3400 |
| score | 0.1800 | 0.0400 | 0.3500 |
| selectivity | 0.3000 | 0.1000 | 0.5300 |
| yield | 0.2900 | 0.0900 | 0.5100 |

### Q03

The high catalyst-to-reagent ratio should give rapid conversion during the short 410 K treatment. Catalyst B is expected to remain less selective than Catalyst D, and uncertainty in catalyst-loading response remains substantial.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1300 | 0.4700 |
| conversion | 0.9200 | 0.7800 | 0.9900 |
| safety_risk | 0.1200 | 0.0600 | 0.2000 |
| score | 0.3800 | 0.2100 | 0.5400 |
| selectivity | 0.6600 | 0.4700 | 0.8000 |
| yield | 0.6100 | 0.4000 | 0.7600 |

### Q04

High catalyst loading and four hours at 410 K should produce essentially complete conversion early, followed by extensive competing reaction or target degradation. The precise balance between residual target, byproduct, and degradation is poorly identified.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7200 | 0.4800 | 0.9300 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.2300 | 0.1400 | 0.3500 |
| score | 0.1100 | 0.0100 | 0.2900 |
| selectivity | 0.2000 | 0.0400 | 0.4300 |
| yield | 0.2000 | 0.0300 | 0.4200 |

### Q05

At 350 K, two hours should give moderate conversion at low Catalyst B loading while retaining better selectivity than the hotter cases. This is closer to the measured temperature domain but still extrapolates catalyst identity, loading, concentration, and solvent jointly.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1800 | 0.0700 | 0.3300 |
| conversion | 0.5700 | 0.3600 | 0.7600 |
| safety_risk | 0.0900 | 0.0400 | 0.1600 |
| score | 0.2800 | 0.1400 | 0.4300 |
| selectivity | 0.7200 | 0.5400 | 0.8500 |
| yield | 0.4100 | 0.2300 | 0.5800 |

### Q06

Even at low catalyst loading, two hours at 465 K is expected to force nearly complete conversion but severely erode target retention. Both chemistry and safety are far outside the measured temperature range, so these intervals are especially wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8400 | 0.5900 | 0.9900 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.3300 | 0.2100 | 0.4900 |
| score | 0.0350 | 0.0000 | 0.1500 |
| selectivity | 0.0800 | 0.0100 | 0.2500 |
| yield | 0.0800 | 0.0000 | 0.2400 |

### Q07

High catalyst loading at 350 K should approach complete conversion in two hours without the extreme degradation expected at 410–465 K. The point estimate assumes catalyst loading mainly accelerates both primary pathways rather than changing Catalyst B's intrinsic pathway preference.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1300 | 0.4700 |
| conversion | 0.9700 | 0.8700 | 1.0000 |
| safety_risk | 0.1000 | 0.0500 | 0.1700 |
| score | 0.3900 | 0.2200 | 0.5500 |
| selectivity | 0.6700 | 0.4900 | 0.8100 |
| yield | 0.6500 | 0.4500 | 0.7900 |

### Q08

High catalyst loading plus two hours at 465 K is predicted to exhaust the reagent rapidly and leave extensive time for secondary loss. This is the strongest extrapolation in the set, and the endpoint could instead plateau at a materially larger residual yield if degradation saturates.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9000 | 0.6800 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.3500 | 0.2200 | 0.5200 |
| score | 0.0150 | 0.0000 | 0.0900 |
| selectivity | 0.0400 | 0.0000 | 0.1600 |
| yield | 0.0400 | 0.0000 | 0.1600 |

### Q09

At the intermediate loading, two hours at 410 K should give nearly complete conversion but appreciable time-dependent loss of selectivity. The estimate interpolates catalyst loading but extrapolates Catalyst B's high-temperature degradation behavior.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.2800 | 0.7300 |
| conversion | 0.9950 | 0.9400 | 1.0000 |
| safety_risk | 0.1800 | 0.1000 | 0.2900 |
| score | 0.2700 | 0.1000 | 0.4400 |
| selectivity | 0.4300 | 0.2200 | 0.6400 |
| yield | 0.4300 | 0.2100 | 0.6300 |

### Q10

Because quench follows the entire heating period immediately before termination, I predict little compositional difference from Q09 but a lower reported risk. The campaign did not isolate a chemical quench effect, so the near-equality of chemical endpoints is an assumption rather than an established result.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4900 | 0.2700 | 0.7200 |
| conversion | 0.9950 | 0.9400 | 1.0000 |
| safety_risk | 0.1500 | 0.0700 | 0.2600 |
| score | 0.2900 | 0.1100 | 0.4700 |
| selectivity | 0.4400 | 0.2300 | 0.6500 |
| yield | 0.4400 | 0.2200 | 0.6400 |

### Q11

Four hours at 350 K should eventually approach complete conversion at intermediate catalyst loading, but extended residence is expected to reduce target retention. Lower temperature should make this less destructive than Q09 despite the longer duration.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4500 | 0.2300 | 0.6800 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.1400 | 0.0700 | 0.2400 |
| score | 0.3000 | 0.1300 | 0.4700 |
| selectivity | 0.4900 | 0.2800 | 0.6800 |
| yield | 0.4800 | 0.2700 | 0.6700 |

### Q12

The 465 K set point creates very fast conversion, but the short operation includes a thermal ramp and therefore less high-temperature residence than the two-hour cases. The balance between rapid target formation and equally rapid degradation is highly uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.2000 | 0.6900 |
| conversion | 0.9800 | 0.8600 | 1.0000 |
| safety_risk | 0.2000 | 0.1100 | 0.3400 |
| score | 0.3000 | 0.1200 | 0.4800 |
| selectivity | 0.5200 | 0.2900 | 0.7200 |
| yield | 0.5100 | 0.2800 | 0.7000 |

## K2 — Retrospective analysis

1. Initial information: supported, contradicted, and untested claims

The initial material packet made almost no substantive reaction-specific mechanistic claims. It explicitly said that no task-specific property dossier was available, that catalysts and reaction species were anonymous, and that solvent effects were categorical benchmark effects rather than real-chemistry predictions from solvent properties. Therefore there was no initial claim such as “Catalyst D is best,” “acetonitrile is fastest,” or “the reaction follows an Arrhenius law” to confirm or refute.

Several framework-level claims were consistent with the observations:

• Catalyst identity was described as coupled to a latent categorical activity profile. Batches 1–4 supported the importance of catalyst category: under the same water/330 K/3,600 s conditions, final yields ranged from 0.186 for Catalyst C to 0.417 for Catalyst D, with substantial selectivity differences as well. This supports categorical catalyst effects, although it does not validate any particular hidden profile.
• Solvent identity was described as a categorical benchmark input. Batches 4–7 supported a real solvent-category effect within this world: with Catalyst D, yield ranged from 0.353 in toluene to 0.498 in acetonitrile. This is evidence for a categorical effect, not evidence that the effect follows known physical properties of those real solvents.
• The public packet stated that instruments have independent calibration and noise. Differences between intermediate HPLC and final assay, such as Batch 2’s yields of 0.317 and 0.348, were compatible with that statement. Compatibility is only “no counterevidence”; without replicates or paired simultaneous assays, the experiment did not independently prove the stated noise model.
• The thermal observations supported K1’s later judgment that actual T(t), rather than only the requested set point, matters. Batch 12 recorded a 66.83 K rise during the first 1,800 s, only another 3.37 K during the following 5,400 s, and a 45 K fall on quenching.

No important initial mechanistic claim was clearly refuted because none was supplied. Several matters remained untested: the hidden catalyst profile itself, the mechanism-to-species mapping, whether mixing was kinetically limiting, and whether the named solvents’ real physical properties had any relevance beyond their categorical labels.

There was, however, an important early working assumption that did encounter counterevidence: a simple monotonic picture in which more thermal exposure merely increased target formation. Batch 12 contradicted that picture because conversion rose to 0.989 after 7,200 s while selectivity fell to 0.596, byproduct rose to 0.394, degradation reached 0.340, and yield was only 0.590. I did revise this in K1 by rejecting a simple one-step plateau model. Thus this is not a case where counterevidence was observed but left uncorrected. A weaker unresolved issue is that I continued to use Arrhenius-like language in K1 despite never measuring enough temperatures, especially for Catalyst B, to establish Arrhenius behavior. I labeled it “plausible” and “provisional,” but the mathematical form still risks sounding better supported than it was.

2. Experiments that formed or changed the account

Batch 1 was an exploratory baseline rather than a deduction from prior evidence. Water, Catalyst A, 330 K, and 3,600 s were chosen largely as moderate, safe-seeming conditions. The choice relied on unverified intuition; the initial packet supplied no reason to privilege them.

Batches 2–4 genuinely formed the catalyst judgment. They showed that catalyst identity affected both conversion and selectivity, not merely a common rate multiplier. In particular, Batch 4’s conversion of 0.481 and selectivity of 0.840 with Catalyst D contrasted with Batch 3’s 0.305 and 0.600 with Catalyst C. This evidence motivated carrying Catalyst D forward.

Batches 5–7 formed the solvent judgment. Batch 6, using Catalyst D in acetonitrile, produced conversion 0.599 and yield 0.498, versus yield 0.417 in water, 0.408 in ethanol, and 0.353 in toluene. That result motivated using acetonitrile for the temperature series. Selecting only the currently best catalyst for the solvent screen was data-driven, but it also assumed—without testing—that catalyst–solvent interactions would not reverse the catalyst ranking.

Batches 8–11 produced the clearest systematic relation in the campaign. From nominal 300 to 390 K, conversion increased from 0.353 to 0.958 and yield from 0.298 to 0.711, while byproduct increased from 0.052 to 0.230, degradation from 0.000 to 0.167, and selectivity declined from 0.835 to 0.774. This series formed the thermal-exposure account and the distinction in K1 between the highest observed yield, Batch 11, and the highest observed safe score, Batch 10.

Batch 12 most strongly changed the mechanistic account. Its 1,800 s HPLC result—conversion 0.598, selectivity 0.864, yield 0.525, and byproduct 0.081—followed by the degraded 7,200 s endpoint made a parallel-plus-sequential network more credible than a single productive conversion. It also demonstrated that almost complete conversion is not equivalent to a good target endpoint.

Some key choices remained guesses rather than consequences of data. I used full stock allocations per batch, fixed 600 rpm, chose 20 K temperature increments, and used one intermediate measurement per batch without having identified their optimal information value. The jump to 390 K was motivated partly by optimization after the rising yield trend, while the 7,200 s Batch 12 was motivated by the need to test residence-time damage. Quenching only Batch 12 was an especially consequential design choice: it gave useful safety information but confounded chemical residence-time effects with the quench operation.

3. Current competing mechanisms and what can be distinguished

K1’s preferred minimal account was R→P in parallel with R→B, followed by P→D and/or B→D, optionally modified by catalyst deactivation. That remains my preferred qualitative account, but several alternatives are still viable.

The main competition is among:

A. Parallel side reaction plus sequential product degradation: R→P, R→B, and P→D.
B. Parallel reactions only, with the product fraction determined by changing substrate composition or temperature history rather than destruction of P.
C. Catalyst-state evolution: an initially selective catalyst becomes less selective or less active through deactivation, poisoning, or transformation.
D. Product or byproduct inhibition, causing rates and apparent selectivity to change with accumulated composition.
E. Transport or thermal-history effects that mimic kinetic changes, especially during the initial ramp.

The experiments can distinguish a constant-selectivity, single irreversible conversion from all of these richer accounts. Batch 12 is incompatible with a model in which time only raises conversion while preserving a fixed target fraction. The temperature series also establishes that unwanted signals grow more strongly with thermal exposure than a simple conversion-only model predicts.

The experiments cannot cleanly distinguish A from C or D. A falling target fraction during extended heating would support sequential degradation, but only one late final assay was taken and no catalyst-state observable was available. Nor can the data establish whether degradation arises mainly from P or B. The similar qualitative temperature trends are consistent with higher activation sensitivity of side reactions, but catalyst transformation at high temperature would generate a similar pattern.

Transport limitation was not tested because stirring stayed at 600 rpm. Catalyst–solvent interactions were also not identified: only Catalyst D received the solvent and temperature studies. The apparent superiority of Catalyst D could therefore be conditional rather than universal.

Finally, K1’s first-order thermal approximation, dT/dt=(Tset−T)/τ, was an explanatory convenience. The recorded deltas show thermal lag, but they are insufficient to identify τ, heat-generation terms, or solvent-dependent heat transfer.

4. The single additional experiment I would choose

I would run one complete Batch-12-matched experiment with Catalyst D, acetonitrile, 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, and 600 rpm. I would heat at a nominal 370 K for 3,600 s, measure HPLC, continue heating at 370 K for another 3,600 s, omit the quench, terminate immediately, and obtain the required final assay.

This would be legal and would address two major gaps simultaneously. The 3,600 s HPLC point would give a within-vessel bridge to Batch 10’s 3,600 s endpoint, while the unquenched 7,200 s final assay would be directly comparable to Batch 12’s quenched 7,200 s endpoint.

Interpretation of possible outcomes:

• If target yield falls substantially between 3,600 and 7,200 s while conversion changes little, that would strongly favor sequential target loss over a purely parallel competition model.
• If conversion continues rising and target yield also rises, but selectivity falls because byproduct rises faster, parallel side conversion would appear more important than direct product destruction.
• If both conversion and all product signals largely stop changing after 3,600 s, catalyst deactivation, inhibition, or an equilibrium-like limitation would become more plausible.
• If the unquenched 7,200 s endpoint closely matches Batch 12, the most economical conclusion would be that quench chiefly reduced temperature and reported risk without materially changing composition.
• If it differs greatly from Batch 12, quench chemistry would become plausible, but batch variability and instrument noise would still need replication before assigning causality.

This one experiment would not fully separate catalyst deactivation from product inhibition, but it would reduce the largest time/quench confounding in the existing campaign.

5. Tradeoff between identifiability and operating score

The catalyst screen, solvent screen, and temperature series served both goals. They identified major categorical and thermal effects while progressively moving toward better observed performance. The research goal’s emphasis on explanation led me to retain intermediate HPLC measurements and to spend Batch 12 on prolonged exposure rather than simply repeating the best condition.

There were nevertheless important optimization-driven sacrifices. After Batch 4, I screened solvents only with Catalyst D. After Batch 6, I explored temperature only with the Catalyst D/acetonitrile combination. This efficiently located high-scoring conditions but sacrificed identification of catalyst×solvent and catalyst×temperature interactions. Likewise, Batches 9–11 concentrated around the rising-performance region rather than adding replicates, zero-catalyst controls, stirring-rate tests, or catalyst-loading variation.

Conversely, Batch 12 knowingly sacrificed expected score for mechanism. Its prolonged residence was likely to worsen degradation, but it tested whether conversion and target yield remained aligned. That experiment was scientifically valuable even though its score, 0.293, was below Batch 10’s 0.364.

Using all batches at maximum reagent, solvent, and catalyst amounts simplified comparisons and used the stock budget symmetrically, but it prevented concentration and catalyst-order identification. The absence of replicates was the largest identifiability sacrifice: it maximized condition coverage, yet made small differences—especially Batch 10 versus Batch 11—difficult to distinguish from process and assay variation.

6. Underused evidence and weaknesses of the blind predictions

The raw characterization artifacts were not deeply exploited. I relied mainly on processed estimates rather than fitting peak areas, checking baseline or saturation flags, or comparing full spectral structure across batches. The recorded temperature changes were recognized qualitatively but not used to fit a thermal time constant or integrated-temperature exposure. Operation-level risk increments and cost increments were also not modeled quantitatively.

The paired HPLC/final-assay observations were underused. A hierarchical error model could have estimated cross-instrument bias and process variance, although the lack of replication would still limit it. Instead, K1 treated discrepancies mostly as compatible with noise. That was reasonable but not maximally informative.

The least reliable blind predictions are Q06 and Q08, which combine 465 K, 7,200 s, Catalyst B, acetonitrile, new catalyst loadings, new concentration, and 400 rpm. Q12 is also highly uncertain because 465 K lies 75 K above the highest researched set point and its 1,800 s outcome depends sensitively on the unmodeled thermal ramp. Q02 and Q04 extrapolate to 14,400 s at 410 K, twice the longest campaign residence and above the measured temperature range. Their predicted severe endpoint degradation was mechanistically plausible but weakly calibrated.

All twelve predictions also required a Catalyst B/acetonitrile interaction that was never measured. The campaign observed Catalyst B only in water at 330 K and only at the campaign loading. Q01–Q12 varied Catalyst B loading from 4.0% to 17.3% relative to reagent, whereas the campaign used 12.5%. The blind predictions therefore combined several unidentified response surfaces.

Some 80% intervals were probably too narrow. In particular, Q06 and Q08 assigned conversion lower bounds of 0.97 and 0.99, and Q04 assigned 0.97, even though catalyst deactivation, thermal ramp behavior, or unusual high-temperature pathway changes could produce materially lower conversion. The score intervals may also be too narrow because K1 explicitly stated that the score equation was unidentified. Safety-risk intervals were vulnerable to uncertainty about how absolute batch scale, solvent volume, duration, and quenching enter the public risk calculation.

This partially conflicts with K1’s stated applicability limit: K1 said that temperatures above 390 K, different loadings, concentrations, and mixing speeds required “substantially wider uncertainty.” The prediction rationale repeated that warning, and the chemical endpoint intervals were often broad, but several near-saturation conversion intervals did not fully honor the structural uncertainty. Q09 versus Q10 also relied on the assumption that quench changed risk but not chemistry, despite K1 explicitly saying that a chemical quench effect had not been identified.

7. Limitations of the sealed recommendation

The sealed recommendation selected Batch 10: Catalyst D in acetonitrile, nominal 370 K for 3,600 s, because it had the highest observed safe score, approximately 0.364, with yield 0.677 and lower risk and degradation than the hotter Batch 11.

This is only the sample-highest condition among twelve tested batches. It is not proven optimal. Batch 11’s score was approximately 0.362, only about 0.002 below Batch 10, much smaller than a difference I would confidently resolve without replicates. Thus even the claim that Batch 10 is truly better than Batch 11 is uncertain. The untested optimum could lie between 370 and 390 K, at a different residence time, at a lower catalyst loading, or along a temperature trajectory rather than a constant set point.

Repeatability should first be tested with independent replicates of Batch 10, including replicate final assays and preferably a fixed intermediate measurement. This would separate process variation from instrument noise and establish whether the reported score and yield are stable.

Local robustness should then be tested around, rather than only at, the chosen point: for example 360, 370, and 380 K; residence times near 2,700, 3,600, and 4,500 s; modest catalyst-loading changes; and at least two stirring rates. A robust recommendation should retain acceptable yield, selectivity, risk, and score under these perturbations rather than depend on a narrow optimum.

Cross-material generality would require testing the same local design with other catalysts and solvents. Existing data do not establish that Catalyst D remains best in acetonitrile at all temperatures, because the full factorial interactions were not measured. Cross-world generality is even weaker: the materials were anonymous benchmark categories with latent profiles, so no transfer to another hidden world—or to real chemistry—follows from the labels alone.

Accordingly, the correct statement is: Batch 10 was the highest-scoring observed member of this finite, unreplicated campaign and was a reasonable empirical recommendation. It was not demonstrated to be globally optimal, statistically superior to nearby conditions, robust to operating perturbations, or transferable across materials or worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 71.9 | none | 0 |
| Q | yes | 0 | 100.3 | none | 0 |
| K2 | yes | 0 | 97.5 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1098 | 0.9000 | 0.3908 | 0.4248 |
| conversion | 0.0210 | 0.9667 | 0.1417 | 0.1441 |
| safety_risk | 0.0750 | 0.7500 | 0.1917 | 0.3574 |
| score | 0.0413 | 0.9167 | 0.2892 | 0.3019 |
| selectivity | 0.1336 | 0.6667 | 0.3517 | 0.7666 |
| yield | 0.1173 | 0.7000 | 0.3583 | 0.7296 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1800 | 0.0700 | 0.3400 | 0.1394 | 0.1397, 0.1462, 0.1413, 0.1384, 0.1316 |
| conversion | 0.5000 | 0.2900 | 0.7300 | 0.5419 | 0.5369, 0.5361, 0.5497, 0.5430, 0.5438 |
| safety_risk | 0.1100 | 0.0500 | 0.1900 | 0.2496 | 0.2496, 0.2496, 0.2496, 0.2496, 0.2496 |
| score | 0.2300 | 0.1000 | 0.3900 | 0.2633 | 0.2655, 0.2652, 0.2643, 0.2587, 0.2626 |
| selectivity | 0.6800 | 0.4700 | 0.8400 | 0.7421 | 0.7503, 0.7451, 0.7464, 0.7401, 0.7288 |
| yield | 0.3400 | 0.1600 | 0.5400 | 0.4090 | 0.4107, 0.4134, 0.4068, 0.3985, 0.4152 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6200 | 0.3800 | 0.8500 | 0.7361 | 0.7397, 0.7292, 0.7492, 0.7245, 0.7377 |
| conversion | 0.9800 | 0.9000 | 1.0000 | 0.9894 | 0.9940, 0.9820, 0.9971, 0.9889, 0.9850 |
| safety_risk | 0.2200 | 0.1300 | 0.3400 | 0.2515 | 0.2515, 0.2515, 0.2515, 0.2515, 0.2515 |
| score | 0.1800 | 0.0400 | 0.3500 | 0.1240 | 0.1282, 0.1246, 0.1241, 0.1240, 0.1192 |
| selectivity | 0.3000 | 0.1000 | 0.5300 | 0.2740 | 0.2821, 0.2767, 0.2785, 0.2713, 0.2612 |
| yield | 0.2900 | 0.0900 | 0.5100 | 0.2699 | 0.2741, 0.2715, 0.2653, 0.2716, 0.2669 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1300 | 0.4700 | 0.1516 | 0.1469, 0.1490, 0.1465, 0.1682, 0.1471 |
| conversion | 0.9200 | 0.7800 | 0.9900 | 0.9045 | 0.9126, 0.8934, 0.9063, 0.9038, 0.9066 |
| safety_risk | 0.1200 | 0.0600 | 0.2000 | 0.2526 | 0.2526, 0.2526, 0.2526, 0.2526, 0.2526 |
| score | 0.3800 | 0.2100 | 0.5400 | 0.4366 | 0.4406, 0.4357, 0.4386, 0.4338, 0.4345 |
| selectivity | 0.6600 | 0.4700 | 0.8000 | 0.8453 | 0.8629, 0.8401, 0.8425, 0.8499, 0.8314 |
| yield | 0.6100 | 0.4000 | 0.7600 | 0.7624 | 0.7594, 0.7661, 0.7686, 0.7528, 0.7653 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7200 | 0.4800 | 0.9300 | 0.7894 | 0.7706, 0.7875, 0.8048, 0.7903, 0.7936 |
| conversion | 0.9980 | 0.9700 | 1.0000 | 0.9959 | 1.0000, 0.9907, 1.0000, 0.9890, 1.0000 |
| safety_risk | 0.2300 | 0.1400 | 0.3500 | 0.2519 | 0.2519, 0.2519, 0.2519, 0.2519, 0.2519 |
| score | 0.1100 | 0.0100 | 0.2900 | 0.0871 | 0.0917, 0.0894, 0.0841, 0.0875, 0.0830 |
| selectivity | 0.2000 | 0.0400 | 0.4300 | 0.2562 | 0.2603, 0.2645, 0.2443, 0.2601, 0.2517 |
| yield | 0.2000 | 0.0300 | 0.4200 | 0.2596 | 0.2675, 0.2614, 0.2583, 0.2597, 0.2510 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1800 | 0.0700 | 0.3300 | 0.2859 | 0.2874, 0.2976, 0.2794, 0.2754, 0.2894 |
| conversion | 0.5700 | 0.3600 | 0.7600 | 0.7070 | 0.7056, 0.7061, 0.7105, 0.7038, 0.7091 |
| safety_risk | 0.0900 | 0.0400 | 0.1600 | 0.1416 | 0.1416, 0.1416, 0.1416, 0.1416, 0.1416 |
| score | 0.2800 | 0.1400 | 0.4300 | 0.2914 | 0.2937, 0.2855, 0.2896, 0.2953, 0.2931 |
| selectivity | 0.7200 | 0.5400 | 0.8500 | 0.6004 | 0.6055, 0.5865, 0.5961, 0.6143, 0.5996 |
| yield | 0.4100 | 0.2300 | 0.5800 | 0.4163 | 0.4191, 0.4105, 0.4134, 0.4182, 0.4204 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8400 | 0.5900 | 0.9900 | 0.6099 | 0.6123, 0.6066, 0.6036, 0.6193, 0.6079 |
| conversion | 0.9990 | 0.9700 | 1.0000 | 0.9947 | 1.0000, 0.9837, 0.9990, 0.9934, 0.9973 |
| safety_risk | 0.3300 | 0.2100 | 0.4900 | 0.4259 | 0.4259, 0.4259, 0.4259, 0.4259, 0.4259 |
| score | 0.0350 | 0.0000 | 0.1500 | 0.1323 | 0.1345, 0.1397, 0.1227, 0.1333, 0.1313 |
| selectivity | 0.0800 | 0.0100 | 0.2500 | 0.3927 | 0.3842, 0.4258, 0.3714, 0.4011, 0.3809 |
| yield | 0.0800 | 0.0000 | 0.2400 | 0.3962 | 0.4056, 0.3968, 0.3843, 0.3939, 0.4005 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1300 | 0.4700 | 0.3215 | 0.3256, 0.3232, 0.3132, 0.3178, 0.3278 |
| conversion | 0.9700 | 0.8700 | 1.0000 | 0.9676 | 0.9735, 0.9585, 0.9756, 0.9696, 0.9610 |
| safety_risk | 0.1000 | 0.0500 | 0.1700 | 0.1439 | 0.1439, 0.1439, 0.1439, 0.1439, 0.1439 |
| score | 0.3900 | 0.2200 | 0.5500 | 0.4053 | 0.4066, 0.4069, 0.4029, 0.4048, 0.4054 |
| selectivity | 0.6700 | 0.4900 | 0.8100 | 0.6857 | 0.6945, 0.6952, 0.6796, 0.6717, 0.6874 |
| yield | 0.6500 | 0.4500 | 0.7900 | 0.6572 | 0.6533, 0.6575, 0.6531, 0.6640, 0.6580 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9000 | 0.6800 | 1.0000 | 0.6400 | 0.6433, 0.6384, 0.6379, 0.6363, 0.6440 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9930 | 0.9781, 0.9871, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.3500 | 0.2200 | 0.5200 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0150 | 0.0000 | 0.0900 | 0.1053 | 0.1049, 0.1045, 0.0992, 0.1060, 0.1120 |
| selectivity | 0.0400 | 0.0000 | 0.1600 | 0.4013 | 0.4087, 0.3948, 0.3933, 0.3967, 0.4131 |
| yield | 0.0400 | 0.0000 | 0.1600 | 0.3962 | 0.3944, 0.3998, 0.3842, 0.3991, 0.4038 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.2800 | 0.7300 | 0.4912 | 0.4900, 0.4852, 0.4940, 0.4841, 0.5025 |
| conversion | 0.9950 | 0.9400 | 1.0000 | 0.9974 | 1.0000, 0.9923, 1.0000, 1.0000, 0.9946 |
| safety_risk | 0.1800 | 0.1000 | 0.2900 | 0.2523 | 0.2523, 0.2523, 0.2523, 0.2523, 0.2523 |
| score | 0.2700 | 0.1000 | 0.4400 | 0.2752 | 0.2725, 0.2767, 0.2744, 0.2725, 0.2800 |
| selectivity | 0.4300 | 0.2200 | 0.6400 | 0.5164 | 0.5050, 0.5198, 0.5199, 0.5132, 0.5241 |
| yield | 0.4300 | 0.2100 | 0.6300 | 0.5154 | 0.5150, 0.5181, 0.5106, 0.5099, 0.5231 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4900 | 0.2700 | 0.7200 | 0.4949 | 0.4892, 0.4966, 0.4999, 0.5047, 0.4842 |
| conversion | 0.9950 | 0.9400 | 1.0000 | 0.9942 | 0.9991, 0.9998, 1.0000, 0.9939, 0.9781 |
| safety_risk | 0.1500 | 0.0700 | 0.2600 | 0.1459 | 0.1459, 0.1459, 0.1459, 0.1459, 0.1459 |
| score | 0.2900 | 0.1100 | 0.4700 | 0.3201 | 0.3218, 0.3178, 0.3232, 0.3200, 0.3179 |
| selectivity | 0.4400 | 0.2300 | 0.6500 | 0.5173 | 0.5167, 0.5191, 0.5235, 0.5115, 0.5160 |
| yield | 0.4400 | 0.2200 | 0.6400 | 0.5165 | 0.5199, 0.5082, 0.5188, 0.5198, 0.5156 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4500 | 0.2300 | 0.6800 | 0.5489 | 0.5697, 0.5532, 0.5308, 0.5504, 0.5403 |
| conversion | 0.9900 | 0.9100 | 1.0000 | 0.9903 | 0.9833, 0.9865, 0.9912, 0.9955, 0.9949 |
| safety_risk | 0.1400 | 0.0700 | 0.2400 | 0.1434 | 0.1434, 0.1434, 0.1434, 0.1434, 0.1434 |
| score | 0.3000 | 0.1300 | 0.4700 | 0.2810 | 0.2783, 0.2768, 0.2825, 0.2819, 0.2854 |
| selectivity | 0.4900 | 0.2800 | 0.6800 | 0.4585 | 0.4538, 0.4471, 0.4607, 0.4561, 0.4750 |
| yield | 0.4800 | 0.2700 | 0.6700 | 0.4602 | 0.4583, 0.4578, 0.4625, 0.4628, 0.4597 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4200 | 0.2000 | 0.6900 | 0.2069 | 0.2063, 0.2058, 0.1964, 0.2129, 0.2132 |
| conversion | 0.9800 | 0.8600 | 1.0000 | 0.9513 | 0.9555, 0.9519, 0.9512, 0.9428, 0.9552 |
| safety_risk | 0.2000 | 0.1100 | 0.3400 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.3000 | 0.1200 | 0.4800 | 0.3582 | 0.3619, 0.3582, 0.3617, 0.3502, 0.3588 |
| selectivity | 0.5200 | 0.2900 | 0.7200 | 0.7886 | 0.7934, 0.7801, 0.8111, 0.7735, 0.7849 |
| yield | 0.5100 | 0.2800 | 0.7000 | 0.7491 | 0.7543, 0.7544, 0.7438, 0.7407, 0.7521 |

## Recommendation retest

- Selected source batch: `10`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2036 | 0.1910 | -0.0126 |
| conversion | 0.8689 | 0.8681 | -0.0007 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1289 | 0.1142 | -0.0147 |
| safety_risk | 0.2121 | 0.2121 | 0.0000 |
| score | 0.3635 | 0.3588 | -0.0048 |
| selectivity | 0.8053 | 0.7803 | -0.0249 |
| virtual_spectrum_summary | 0.1700 | 0.1564 | -0.0135 |
| yield | 0.6769 | 0.6808 | 0.0039 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
