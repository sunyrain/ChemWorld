# RX-W04--S--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W04`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `11`
- Rationale: Batch 11 achieved the highest observed final safe score (0.3317) while remaining comfortably below the 0.35 safety limit (risk 0.2064); its Catalyst B/toluene, 350 K boundary target for 3600 s procedure balanced conversion, selectivity, and degradation best.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K x 3600 s @ 600 rpm → 340 K x 3600 s @ 600 rpm | no | 0.3748 | 0.4466 | 0.8474 | 0.4757 | 0.2140 | 0.1787 | 0.1659 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.5410 | 0.7203 | 0.7575 | 0.2073 | 0.0766 | 0.1839 | 0.2895 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.3532 | 0.5574 | 0.6188 | 0.2817 | 0.0382 | 0.1618 | 0.1697 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4136 | 0.6836 | 0.6222 | 0.2053 | 0.0654 | 0.1683 | 0.2228 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.3716 | 0.7686 | 0.4861 | 0.1194 | 0.0270 | 0.1183 | 0.2361 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.3399 | 0.6309 | 0.5246 | 0.1979 | 0.0495 | 0.1428 | 0.1819 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.5698 | 0.7637 | 0.7601 | 0.2116 | 0.0635 | 0.1979 | 0.3058 |
| 8 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 5400 s @ 600 rpm | no | 0.6252 | 0.7007 | 0.8827 | 0.2762 | 0.1181 | 0.2073 | 0.3203 |
| 9 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 2400 s @ 600 rpm | no | 0.5851 | 0.7913 | 0.7613 | 0.1633 | 0.0560 | 0.2051 | 0.3157 |
| 10 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 320 K x 7200 s @ 600 rpm | no | 0.5703 | 0.6740 | 0.8650 | 0.2880 | 0.1161 | 0.1989 | 0.2936 |
| 11 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6225 | 0.7720 | 0.8261 | 0.2175 | 0.0851 | 0.2064 | 0.3317 |
| 12 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 4200 s @ 600 rpm | no | 0.6339 | 0.7233 | 0.8588 | 0.2312 | 0.1033 | 0.2099 | 0.3258 |

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
      "target_temperature_K": 340
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
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
    "byproduct_signal": 0.4756549596786499,
    "conversion": 0.8474245667457581,
    "cost": 1.0,
    "degradation_warning": 0.21400916576385498,
    "safety_risk": 0.1786876916885376,
    "score": 0.16590550541877747,
    "selectivity": 0.44662946462631226,
    "virtual_spectrum_summary": 0.35791435837745667,
    "yield": 0.374787837266922
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `15`.

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
  "end_step": 15,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.20727545022964478,
    "conversion": 0.7574639320373535,
    "cost": 1.0,
    "degradation_warning": 0.0765966922044754,
    "safety_risk": 0.18385611474514008,
    "score": 0.2894696593284607,
    "selectivity": 0.7202799916267395,
    "virtual_spectrum_summary": 0.14847001433372498,
    "yield": 0.5409712791442871
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `22`.

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
  "end_step": 22,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.28166887164115906,
    "conversion": 0.6187954545021057,
    "cost": 1.0,
    "degradation_warning": 0.03821668028831482,
    "safety_risk": 0.16181369125843048,
    "score": 0.16972073912620544,
    "selectivity": 0.5574350357055664,
    "virtual_spectrum_summary": 0.17211538553237915,
    "yield": 0.3532464802265167
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `29`.

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
  "end_step": 29,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.20534756779670715,
    "conversion": 0.6222410798072815,
    "cost": 1.0,
    "degradation_warning": 0.06536092609167099,
    "safety_risk": 0.16832391917705536,
    "score": 0.22281430661678314,
    "selectivity": 0.6835644841194153,
    "virtual_spectrum_summary": 0.1423535794019699,
    "yield": 0.41361209750175476
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `36`.

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
  "end_step": 36,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.11941506713628769,
    "conversion": 0.48611828684806824,
    "cost": 1.0,
    "degradation_warning": 0.02698269486427307,
    "safety_risk": 0.11832816898822784,
    "score": 0.2361324429512024,
    "selectivity": 0.7685680985450745,
    "virtual_spectrum_summary": 0.07782050222158432,
    "yield": 0.37156563997268677
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `43`.

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
  "end_step": 43,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.1978645920753479,
    "conversion": 0.5245957970619202,
    "cost": 1.0,
    "degradation_warning": 0.04951167106628418,
    "safety_risk": 0.1428045928478241,
    "score": 0.18187136948108673,
    "selectivity": 0.6309288144111633,
    "virtual_spectrum_summary": 0.13110578060150146,
    "yield": 0.3398541510105133
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `50`.

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
  "end_step": 50,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.2115875780582428,
    "conversion": 0.7600653767585754,
    "cost": 1.0,
    "degradation_warning": 0.06345529854297638,
    "safety_risk": 0.1978960931301117,
    "score": 0.3057899475097656,
    "selectivity": 0.7636739015579224,
    "virtual_spectrum_summary": 0.14492805302143097,
    "yield": 0.5697954893112183
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `57`.

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
      "duration_s": 5400,
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
  "end_step": 57,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.2761818766593933,
    "conversion": 0.8826778531074524,
    "cost": 1.0,
    "degradation_warning": 0.11814942210912704,
    "safety_risk": 0.2072504609823227,
    "score": 0.32027679681777954,
    "selectivity": 0.7007108926773071,
    "virtual_spectrum_summary": 0.20506727695465088,
    "yield": 0.6252349615097046
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `64`.

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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
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
  "end_step": 64,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.16325683891773224,
    "conversion": 0.7612712383270264,
    "cost": 1.0,
    "degradation_warning": 0.0559610091149807,
    "safety_risk": 0.20506535470485687,
    "score": 0.31569159030914307,
    "selectivity": 0.7912600040435791,
    "virtual_spectrum_summary": 0.11497371643781662,
    "yield": 0.5850722193717957
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `71`.

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
      "target_temperature_K": 320
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
  "end_step": 71,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.28802189230918884,
    "conversion": 0.8649740815162659,
    "cost": 1.0,
    "degradation_warning": 0.11612259596586227,
    "safety_risk": 0.19887323677539825,
    "score": 0.29361531138420105,
    "selectivity": 0.6739783883094788,
    "virtual_spectrum_summary": 0.2106672078371048,
    "yield": 0.5702906847000122
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `78`.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2174907624721527,
    "conversion": 0.8261473178863525,
    "cost": 1.0,
    "degradation_warning": 0.08505703508853912,
    "safety_risk": 0.20643991231918335,
    "score": 0.3317343294620514,
    "selectivity": 0.7719954252243042,
    "virtual_spectrum_summary": 0.15789559483528137,
    "yield": 0.6225467324256897
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
      "duration_s": 4200,
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.23115791380405426,
    "conversion": 0.8587656617164612,
    "cost": 1.0,
    "degradation_warning": 0.10326743125915527,
    "safety_risk": 0.20986463129520416,
    "score": 0.32581815123558044,
    "selectivity": 0.7232639193534851,
    "virtual_spectrum_summary": 0.17360720038414001,
    "yield": 0.633911669254303
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidentiary basis

This report describes the bounded synthetic reaction-and-thermal benchmark studied in 12 completed batches. The reagent and catalysts are anonymous benchmark materials. Although the solvents have real names, the public material information explicitly states that their reaction effects are categorical benchmark effects, not predictions based on real solvent chemistry. Accordingly, the mechanism below is a phenomenological explanation of this synthetic world, not a proposed mechanism for a named real reaction.

All batches used 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, and 600 rpm stirring. Thus, the campaign directly identifies categorical catalyst and solvent effects and thermal-program effects, but it does not independently identify concentration, catalyst-loading, reagent-loading, or stirring-rate dependences.

The most important observations are final-assay results. Intermediate HPLC measurements were useful diagnostic observations but had different noise and calibration; differences between an HPLC estimate and the subsequent final assay should not be interpreted automatically as chemical evolution after termination.

2. Proposed process structure

The simplest explanation consistent with the observations is a network with at least three reaction outcomes:

R -> P                    desired product formation
R -> B                    competing byproduct formation
P and/or B -> D           thermally promoted degradation

Here R is the anonymous limiting reactant, P the desired public target, B one or more public byproducts, and D the degradation channel. A minimal kinetic representation would be

  dR/dt = -(kP + kB) R
  dP/dt = kP R - kD,P P
  dB/dt = kB R - kD,B B
  dD/dt = kD,P P + kD,B B

with effective rate constants dependent on catalyst c, solvent s, temperature T, and possibly conversion:

  ki = Ai(c,s) exp[-Ei(c,s)/(Rgas T)] f_i(concentration, mixing, conversion).

This is not claimed as a uniquely identified law. It is a compact way to represent three robust empirical features: catalyst-dependent activity and selectivity, strong solvent-dependent activity, and a thermal-dose trade-off in which conversion rises while selectivity and degradation eventually worsen.

A useful approximate measurement relationship is

  yield ≈ conversion × selectivity,

allowing for assay noise and possible differences in how the synthetic channels are normalized. For example, Batch 11 gave conversion 0.8261 and selectivity 0.7720, whose product is about 0.638, close to the observed yield of 0.6225. The relationship is not exact enough to treat any one of these channels as algebraically redundant.

3. Catalyst effects

Batches 2-4 provide the cleanest catalyst comparison because they used acetonitrile and the same 340 K target for 3600 s:

- Batch 2, Catalyst B: yield 0.5410, selectivity 0.7203, conversion 0.7575, byproduct 0.2073, degradation 0.0766, risk 0.1839, score 0.2895.
- Batch 3, Catalyst C: yield 0.3532, selectivity 0.5574, conversion 0.6188, byproduct 0.2817, degradation 0.0382, risk 0.1618, score 0.1697.
- Batch 4, Catalyst D: yield 0.4136, selectivity 0.6836, conversion 0.6222, byproduct 0.2053, degradation 0.0654, risk 0.1683, score 0.2228.

Catalyst B therefore increased both apparent activity and desired-path selectivity relative to Catalysts C and D under these conditions. Catalyst D was intermediate, while Catalyst C was poorest because of both lower conversion and lower selectivity.

Batch 1 used Catalyst A in acetonitrile but received two successive 340 K, 3600 s heating periods rather than one. Its conversion was high (0.8474), yet yield was only 0.3748, selectivity 0.4466, byproduct 0.4757, and degradation 0.2140. The score was 0.1659. Because the thermal history differs, this batch cannot isolate the intrinsic behavior of Catalyst A. It does show that the Catalyst A/long-thermal-dose combination strongly favored undesired channels. A reasonable but unproven interpretation is that Catalyst A has appreciable conversion activity but poor selectivity or accelerates secondary chemistry.

Thus, the supported catalyst ranking around the tested operating region is B > D > C for safe-score performance. Catalyst A cannot be placed cleanly because its batch was confounded by the doubled heating time.

4. Solvent effects

Batches 2 and 5-7 used Catalyst B and a 340 K target for 3600 s, providing a categorical solvent comparison:

- Batch 5, water: conversion 0.4861, yield 0.3716, selectivity 0.7686, byproduct 0.1194, degradation 0.0270, risk 0.1183, score 0.2361.
- Batch 6, ethanol: conversion 0.5246, yield 0.3399, selectivity 0.6309, byproduct 0.1979, degradation 0.0495, risk 0.1428, score 0.1819.
- Batch 2, acetonitrile: conversion 0.7575, yield 0.5410, selectivity 0.7203, byproduct 0.2073, degradation 0.0766, risk 0.1839, score 0.2895.
- Batch 7, toluene: conversion 0.7601, yield 0.5698, selectivity 0.7637, byproduct 0.2116, degradation 0.0635, risk 0.1979, score 0.3058.

The results imply two solvent-controlled dimensions rather than a single universal solvent factor:

- Activity: toluene and acetonitrile supported much faster desired conversion than water or ethanol.
- Selectivity/suppression of side chemistry: water was relatively selective and clean but slow; ethanol was both slow and less selective; toluene combined high activity with good selectivity; acetonitrile was active but somewhat less favorable than toluene.

In an effective kinetic model, the solvent therefore changes kP and kB independently. It cannot be represented adequately by multiplying every rate constant by one common solvent factor.

The safety response was also solvent-dependent. Under the common 340 K/3600 s program, risk rose from water (0.1183) through ethanol (0.1428) and acetonitrile (0.1839) to toluene (0.1979). This ranking is an observation about the benchmark's categorical solvent profiles, not a real-world solvent safety claim.

5. Temperature-time coupling and the reaction window

Batches 7-12 used Catalyst B in toluene and reveal the thermal-dose response:

- Batch 7: 340 K, 3600 s; conversion 0.7601, yield 0.5698, selectivity 0.7637, degradation 0.0635, risk 0.1979, score 0.3058.
- Batch 8: 340 K, 5400 s; conversion 0.8827, yield 0.6252, selectivity 0.7007, degradation 0.1181, risk 0.2073, score 0.3203.
- Batch 9: 360 K, 2400 s; conversion 0.7613, yield 0.5851, selectivity 0.7913, degradation 0.0560, risk 0.2051, score 0.3157.
- Batch 10: 320 K, 7200 s; conversion 0.8650, yield 0.5703, selectivity 0.6740, degradation 0.1161, risk 0.1989, score 0.2936.
- Batch 11: 350 K, 3600 s; conversion 0.8261, yield 0.6225, selectivity 0.7720, degradation 0.0851, risk 0.2064, score 0.3317.
- Batch 12: 350 K, 4200 s; conversion 0.8588, yield 0.6339, selectivity 0.7233, degradation 0.1033, risk 0.2099, score 0.3258.

These observations support a finite optimum rather than monotonic improvement with time or conversion. More thermal exposure usually increased conversion, but it also increased byproduct/degradation channels and lowered selectivity. At 350 K, extending the treatment from 3600 s in Batch 11 to 4200 s in Batch 12 raised conversion and nominal yield, but selectivity fell from 0.7720 to 0.7233, degradation rose from 0.0851 to 0.1033, risk rose from 0.2064 to 0.2099, and the score declined from 0.3317 to 0.3258.

The comparison of Batch 9 (360 K, 2400 s) and Batch 10 (320 K, 7200 s) also shows that elapsed time is not interchangeable with temperature through one crude scalar such as T × t. The hot-short process maintained high selectivity and low degradation, whereas the cool-long process reached higher conversion but accumulated substantially more degradation and lower selectivity. This is consistent with parallel and consecutive reactions having different activation energies and with prolonged residence time enabling secondary chemistry.

A plausible qualitative rule for this tested region is:

  desired conversion benefit ∝ integral kP(T) R(t) dt,
  side-product burden ∝ integral [kB(T)R(t) + kD(T)P(t)] dt.

The optimum occurs when the marginal gain in desired product becomes smaller than the marginal penalties from lost selectivity, degradation, and safety risk. For Catalyst B/toluene, that balance occurred near the Batch 11 program: a 350 K target for 3600 s.

6. Heating dynamics and safety risk

The vessel did not jump instantly to the requested temperature. In Batch 1, the first 340 K heating period produced a reported temperature change of about 39.77 K; a second identical period changed temperature by only about 0.48 K. This suggests first-order thermal approach to a target, such as

  dT/dt = (Tset - T)/tau,

possibly with solvent-dependent thermal parameters. Consequently, two nominally identical heat commands applied sequentially do not create identical thermal histories.

Safety risk behaved like an accumulated state with at least a composition-dependent baseline and a heating contribution. Adding solvent and concentrated reagent created nonzero risk before heating; catalyst addition itself produced no visible risk increment in the observed setup. For example, in the toluene batches, solvent addition contributed approximately 0.0904 risk and reagent addition a further approximately 0.0359, giving about 0.1263 before heating. Batch 12's 350 K/4200 s heating then increased risk to 0.2099.

A suitable phenomenological form is

  risk = r_solvent(s,V) + r_concentration(nR/V) + integral h(T(t),s,composition) dt,

with h increasing with temperature and possibly including a transient heating-rate or temperature-excursion term. The Batch 1 observation that the second 340 K period added much less risk than the first suggests that risk is not simply proportional to total time at the requested target; the size of the temperature excursion, approach to equilibrium, or saturation of a hazard component matters.

Every completed batch remained below the declared safety limit of 0.35. The highest reported risk among the described batches was only about 0.210. Therefore the campaign identifies a safe tested region, but it does not identify behavior near or beyond the limit, and extrapolation to hotter, more concentrated, or larger-scale conditions is unsupported.

7. Score behavior

The exact score equation was not public. Empirically, score increased with useful yield and selectivity and decreased with byproduct, degradation, and safety burden. It was not simply yield alone: Batch 12 had slightly higher measured yield than Batch 11 (0.6339 versus 0.6225) but scored lower because it had lower selectivity, higher degradation, and higher risk. A generic representation consistent with the observations is

  score = F(yield, selectivity, conversion)
          - G(byproduct, degradation, safety risk, cost),

where F is increasing and G is increasing in each burden. All full-catalyst batches displayed cost at the visible ceiling of 1.0, so the campaign did not identify the cost coefficient or whether lower catalyst loading could improve the net score.

8. How the explanation evolved during the campaign

Batch 1 initially showed that high conversion alone was not sufficient: prolonged heating produced high byproduct and degradation with a poor score. This motivated treating selectivity and secondary degradation as explicit processes rather than assuming a single irreversible conversion.

Batches 2-4 then established that catalyst identity changes both rate and selectivity. Catalyst B was markedly superior in acetonitrile, so subsequent solvent and thermal studies fixed Catalyst B.

Batches 5-7 showed that solvent effects were not merely safety or dilution effects. Water was clean but slow, ethanol was slow and less selective, and toluene gave the best activity-selectivity balance despite its greater safety burden. This shifted the working hypothesis from a one-dimensional solvent activity factor to separate solvent effects on desired and undesired pathways.

Batches 8-10 demonstrated the conversion-versus-degradation trade-off and showed that hot-short and cool-long treatments with superficially comparable overall reaction progress could give very different selectivity. This supported a parallel-plus-consecutive network with distinct temperature sensitivities.

Batches 11-12 localized the optimum more closely. Batch 11 gave the highest final safe score, 0.3317, while Batch 12 showed that a modest additional 600 s at the same 350 K target already moved past the score optimum.

9. Recommended operating interpretation

Within the tested domain, the best supported procedure is Batch 11: 0.080 L toluene, 0.040 mol limiting reagent, 0.005 mol Catalyst B, 600 rpm, and a 350 K target for 3600 s, followed by termination and final assay. Its final observations were yield 0.6225, selectivity 0.7720, conversion 0.8261, byproduct signal 0.2175, degradation warning 0.0851, risk 0.2064, and score 0.3317.

This recommendation is empirical. It should not be read as proof that exactly 350 K and exactly 3600 s are the continuous optimum. The data only show that this tested point outperformed the neighboring tested schedules.

10. Identifiability limits and competing explanations

Several important quantities remain unidentified:

- No catalyst-loading series was performed, so reaction order in catalyst, catalyst saturation, and whether less catalyst would improve cost-adjusted score are unknown.
- Reagent amount and solvent volume were fixed, so concentration dependence and reagent reaction order are unknown.
- Stirring was fixed at 600 rpm, so mass-transfer limitation cannot be separated from intrinsic kinetics.
- Only one batch was run at most exact conditions; process variability and reproducibility are not independently estimated.
- Catalyst A was tested only with a longer thermal history, confounding catalyst identity with exposure time.
- The experiment set is too small for unique Arrhenius parameters or separate numerical values of kP, kB, and kD.
- Final channels are synthetic proxies. A high byproduct signal could represent one species or several unresolved channels.
- HPLC-to-final-assay differences may arise from instrument noise and channel calibration, not time evolution.
- The visible safety metric may combine several latent hazards; its additive decomposition is only a useful hypothesis.

Reasonable competing explanations include catalyst deactivation, product inhibition, reversible desired-product formation, temperature-dependent assay response, or a conversion-dependent selectivity switch rather than literal product degradation. For example, falling selectivity at longer times could arise because the remaining reactant is diverted to a side pathway, even if P itself never degrades. The observed degradation-warning increase favors a secondary-degradation interpretation, but it does not uniquely prove P -> D.

Likewise, the superior hot-short result relative to cool-long could reflect thermal lag and different actual temperature trajectories rather than only different activation energies. The campaign observed requested programs and some public temperature changes, but it did not reconstruct a complete time-resolved vessel-temperature trace.

11. Final model statement

The most defensible description is therefore a catalyst- and solvent-dependent parallel reaction network with thermally activated secondary loss, embedded in a vessel with finite heating dynamics and a composition- plus thermal-history-dependent safety accumulator. Catalyst B and toluene jointly favor the desired path. Increasing thermal dose first raises conversion and yield, then increasingly promotes byproduct/degradation processes and safety burden. The tested optimum lies near a moderately hot, finite residence-time window represented by Batch 11, while both excessive residence time and poorly selective catalyst/solvent combinations lower the safe score.

## Q — Blind predictions

### Overall rationale

These predictions extrapolate the campaign's Catalyst B/acetonitrile observations using a parallel desired/byproduct network with consecutive thermal degradation, finite thermal response, and catalyst-dependent kinetic dose. The training campaign used 0.005 mol catalyst, 0.040 mol reagent, 0.080 L solvent, and temperatures no higher than 360 K; the queries use different catalyst ratios, slightly higher reagent concentration, 400 rpm, and temperatures up to 465 K. I therefore widened the 80% intervals substantially, especially for high-temperature and long-duration cases. Conversion is predicted to saturate under severe conditions, while yield and selectivity decline because complete reactant disappearance is not equivalent to retained target formation. Safety estimates combine an acetonitrile/concentration baseline with a rising thermal-exposure contribution. Q09 and Q10 are predicted similarly because quenching occurs after the same full heat treatment; only a small, uncertain stabilization benefit is assigned to Q10.

### Q01

The 410 K short treatment should compensate substantially for the low Catalyst B loading. I expect high conversion but more thermal side chemistry than in the studied 340–350 K acetonitrile batches. This is a substantial temperature extrapolation, so the interval is broad.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1700 | 0.4300 |
| conversion | 0.8800 | 0.7200 | 0.9800 |
| safety_risk | 0.2600 | 0.2000 | 0.3400 |
| score | 0.2200 | 0.0900 | 0.3400 |
| selectivity | 0.6300 | 0.4300 | 0.7900 |
| yield | 0.5200 | 0.3200 | 0.6800 |

### Q02

Four hours at 410 K should drive nearly complete conversion even at low catalyst loading, but the campaign showed that prolonged exposure sharply increases secondary chemistry. I predict severe selectivity and yield loss, with a material probability of exceeding the 0.35 safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4500 | 0.8200 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.4200 | 0.3100 | 0.5600 |
| score | 0.0250 | 0.0000 | 0.1000 |
| selectivity | 0.1800 | 0.0500 | 0.3800 |
| yield | 0.1200 | 0.0200 | 0.2900 |

### Q03

The higher catalyst loading combined with 410 K should give near-complete conversion within 1800 s. Relative to Q01, the larger kinetic dose is expected to divert more material into byproduct and degradation channels, lowering selectivity and safe score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4800 | 0.3000 | 0.6700 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.2600 | 0.2000 | 0.3400 |
| score | 0.1000 | 0.0250 | 0.2200 |
| selectivity | 0.4000 | 0.2100 | 0.6000 |
| yield | 0.3600 | 0.1700 | 0.5500 |

### Q04

This combines high catalyst loading, 410 K, and the maximum residence time. Conversion should saturate, while consecutive degradation and competing-product formation dominate. The predicted safety risk is above the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7400 | 0.5500 | 0.9000 |
| conversion | 0.9970 | 0.9700 | 1.0000 |
| safety_risk | 0.4200 | 0.3100 | 0.5600 |
| score | 0.0060 | 0.0000 | 0.0350 |
| selectivity | 0.0700 | 0.0100 | 0.2000 |
| yield | 0.0300 | 0.0000 | 0.1200 |

### Q05

At 350 K, the low catalyst loading should make this a moderate-dose experiment despite the two-hour duration. It is the closest query to the productive campaign region, so I expect useful selectivity and a comfortably compliant safety risk, with incomplete conversion limiting yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1100 | 0.3400 |
| conversion | 0.7000 | 0.5000 | 0.8600 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 |
| score | 0.2600 | 0.1300 | 0.3700 |
| selectivity | 0.7400 | 0.5800 | 0.8600 |
| yield | 0.5000 | 0.3200 | 0.6500 |

### Q06

The 465 K, two-hour treatment is far outside the studied thermal window. Even with low catalyst loading, I expect complete reactant disappearance but extensive secondary degradation, very poor target retention, and a clear safety-limit violation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7600 | 0.5700 | 0.9200 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.5800 | 0.4200 | 0.7500 |
| score | 0.0020 | 0.0000 | 0.0150 |
| selectivity | 0.0300 | 0.0000 | 0.1200 |
| yield | 0.0100 | 0.0000 | 0.0600 |

### Q07

Higher catalyst loading should raise conversion strongly at 350 K, but the 7200 s residence time is expected to move beyond the selectivity optimum. Yield may remain useful, although byproduct formation should be appreciably greater than in Q05.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3800 | 0.2300 | 0.5600 |
| conversion | 0.9300 | 0.8200 | 0.9900 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 |
| score | 0.2000 | 0.0800 | 0.3200 |
| selectivity | 0.5800 | 0.3900 | 0.7400 |
| yield | 0.5400 | 0.3400 | 0.6800 |

### Q08

High catalyst loading adds further kinetic severity to the already extreme 465 K, two-hour program. The target product is predicted to be almost completely overtaken by byproduct and degradation channels, while risk substantially exceeds the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8000 | 0.6100 | 0.9500 |
| conversion | 0.9990 | 0.9850 | 1.0000 |
| safety_risk | 0.5800 | 0.4200 | 0.7500 |
| score | 0.0010 | 0.0000 | 0.0080 |
| selectivity | 0.0150 | 0.0000 | 0.0700 |
| yield | 0.0050 | 0.0000 | 0.0300 |

### Q09

The intermediate catalyst loading and 7200 s at 410 K imply a much larger thermal dose than any productive campaign batch. Conversion should be essentially complete, but retained target yield and selectivity should be low. Safety risk is centered slightly above the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6900 | 0.4900 | 0.8600 |
| conversion | 0.9970 | 0.9600 | 1.0000 |
| safety_risk | 0.3700 | 0.2800 | 0.4900 |
| score | 0.0100 | 0.0000 | 0.0550 |
| selectivity | 0.1200 | 0.0250 | 0.2900 |
| yield | 0.0700 | 0.0100 | 0.2000 |

### Q10

The pre-quench chemistry should be almost the same as Q09 because quenching occurs only after the full heating interval. I assign a small benefit from rapid stabilization and reduced terminal thermal hazard, but this effect was not calibrated in the campaign and may be negligible.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6800 | 0.4800 | 0.8500 |
| conversion | 0.9970 | 0.9600 | 1.0000 |
| safety_risk | 0.3400 | 0.2500 | 0.4600 |
| score | 0.0140 | 0.0000 | 0.0750 |
| selectivity | 0.1300 | 0.0300 | 0.3100 |
| yield | 0.0800 | 0.0100 | 0.2200 |

### Q11

At 350 K the temperature is near the productive region, but the four-hour residence time is much longer than the observed optimum. I expect high conversion and moderate retained yield, offset by substantial secondary byproduct formation and selectivity loss.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2700 | 0.6200 |
| conversion | 0.9500 | 0.8400 | 0.9950 |
| safety_risk | 0.2400 | 0.1800 | 0.3200 |
| score | 0.1400 | 0.0500 | 0.2600 |
| selectivity | 0.5500 | 0.3500 | 0.7100 |
| yield | 0.5000 | 0.3000 | 0.6500 |

### Q12

A short 465 K treatment should reach nearly complete conversion at the intermediate catalyst loading, but the extreme temperature is expected to cause rapid competing and consecutive chemistry. The shorter duration prevents the near-total target destruction predicted for Q06 and Q08, although safety compliance remains doubtful.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4300 | 0.8300 |
| conversion | 0.9950 | 0.9400 | 1.0000 |
| safety_risk | 0.3900 | 0.2900 | 0.5200 |
| score | 0.0150 | 0.0000 | 0.0800 |
| selectivity | 0.1800 | 0.0400 | 0.3800 |
| yield | 0.1100 | 0.0150 | 0.2800 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial material packet supplied almost no substantive mechanistic claims to test. It explicitly said that there was no task-specific nominal-property dossier, that the catalysts were anonymous benchmark formulations, and that the named solvents had categorical benchmark effects rather than physically curated reaction effects. Therefore, it did not predict that a particular catalyst, solvent, temperature, or mechanism would be favorable.

Several structural claims in the packet were consistent with the campaign, although this is not the same as independently validating them:

- Catalyst and solvent identities behaved as consequential categorical variables. Batches 2–4 differed strongly when only catalyst identity was intentionally changed, and Batches 2 and 5–7 differed strongly across solvents with Catalyst B. This supports the practical claim that these selectors are coupled to latent activity profiles.
- The public instruments displayed the expected noisy, channel-specific behavior. For example, Batch 11 HPLC estimated yield 0.5996, conversion 0.8363, and selectivity 0.7273, whereas its final assay gave 0.6225, 0.8261, and 0.7720. Such differences are compatible with distinct noisy calibrations. They do not by themselves validate the stated numerical noise model because the instruments did not measure exact replicates of a certified reference state.
- The declared safety limit of 0.35 was operationally relevant, and all actual campaign batches remained below it. The largest observed final risk was about 0.210. This establishes only that the tested region was compliant; it does not validate the world’s behavior close to or beyond the limit.
- The statement that real solvent names should not be interpreted as real chemical predictions remains important. Nothing in the campaign tested that statement against physical samples, so there is no basis for claiming real-world validation.

There were no initial claims about Catalyst B superiority, a parallel-plus-consecutive network, or a 350 K optimum. Those were empirical interpretations developed during the campaign.

I distinguish absence of counterevidence from positive support as follows. The anonymous-benchmark interpretation encountered no counterevidence, but it was not experimentally testable here. The categorical importance of catalyst and solvent did receive positive support. The instrument-noise description was qualitatively consistent with the paired HPLC/final-assay differences, but it was not quantitatively verified.

I am not aware of a clear contradiction to an initial packet claim that appeared and was knowingly left uncorrected. There were, however, tensions with overly simple working ideas. In particular, Batch 1 showed that greater conversion did not imply better outcome, and the later thermal series showed that time and temperature were not interchangeable through one simple dose scalar. Those early simple ideas were revised rather than retained. Similarly, the relation “yield approximately equals conversion times selectivity” was visibly inexact; K1 therefore presented it only as approximate, not as an identity.

2. Experiments that formed or changed the interpretation

The first recipe choice—Catalyst A in acetonitrile—was largely an unvalidated starting guess. The initial packet provided no reason to expect either choice to be best. The choice of full permitted reagent, solvent, and catalyst amounts was also primarily an optimization heuristic, not a mechanistically justified design.

Batch 1 was genuinely formative. After the first 340 K/3600 s treatment, HPLC reported conversion 0.5736, yield 0.3331, selectivity 0.5722, and byproduct 0.2565. I then imposed a second identical heating period. The final assay showed conversion 0.8474 but only 0.3748 yield, selectivity 0.4466, byproduct 0.4757, and degradation 0.2140. This changed the working view from “more conversion is likely better” to “thermal exposure can move material strongly into undesired or degraded channels.” It also provided the clearest evidence for finite residence-time optimization. However, it simultaneously confounded Catalyst A identity with extended heating, preventing a fair catalyst comparison.

Batches 2–4 were the cleanest mechanism-oriented comparison. Under acetonitrile, 340 K, and 3600 s, Catalyst B produced score 0.2895, compared with 0.1697 for Catalyst C and 0.2228 for Catalyst D. Catalyst B’s advantage involved both higher conversion and better selectivity. These batches formed the judgment that catalyst identity affects more than a single common rate multiplier.

Batches 5–7 then changed the solvent interpretation. Water in Batch 5 was selective and clean but slow; ethanol in Batch 6 was slow and less selective; acetonitrile in Batch 2 was active; and toluene in Batch 7 combined high activity with good selectivity. This supported K1’s claim that solvent likely changes desired and undesired pathways differently, rather than merely multiplying all rates by one factor. Choosing Catalyst B for these batches relied directly on the results of Batches 2–4.

Batches 8–10 were selected using the existing Catalyst B/toluene result and a mechanistic guess about thermal dose. They were particularly influential:

- Batch 8 showed that extending 340 K heating from 3600 to 5400 s raised conversion and yield but reduced selectivity and increased degradation.
- Batch 9 showed that 360 K for 2400 s retained high selectivity and relatively low degradation.
- Batch 10 showed that 320 K for 7200 s could reach high conversion while giving worse selectivity and degradation than the hot-short treatment.

Those comparisons produced the K1 judgment that separate pathways have different temperature and residence-time sensitivities. They also argued against treating temperature multiplied by time as a sufficient exposure variable.

Batches 11–12 were primarily local optimization experiments, chosen using the preceding data. Batch 11 at 350 K for 3600 s achieved the highest observed final score, 0.3317. Batch 12 extended that condition to 4200 s and scored 0.3258 despite a slightly higher reported yield, because selectivity, degradation, and risk were less favorable. This localized a score maximum but did not prove a continuous optimum.

Some choices remained guess-driven. The initial acetonitrile/Catalyst A choice, the decision to use maximum catalyst loading throughout, the fixed 600 rpm speed, and the exact thermal grid were not dictated by initial evidence. The move to 350 K was a reasonable interpolation between 340 and 360 K, but the precise 3600 and 4200 s durations were still heuristic.

3. Most important competing mechanisms

The leading K1 interpretation was a parallel-plus-consecutive network:

R → P, R → B, and P and/or B → D.

The most important competitor is a purely conversion-dependent parallel network with little or no destruction of P. Under that explanation, selectivity falls at high conversion because the residual reactant increasingly follows a side pathway, catalyst selectivity changes with composition, or the public channels are normalized differently—not because already formed P is consumed.

The existing experiments can distinguish several coarse propositions:

- A single irreversible R → P process is inconsistent with the substantial byproduct and degradation signals.
- A model in which catalyst or solvent merely changes one universal rate constant is inadequate, because selectivity changes markedly across catalysts and solvents.
- A single temperature-time dose is inadequate, because Batch 9 and Batch 10 produced different selectivity and degradation patterns.
- Longer thermal exposure is associated with more undesired signal in several comparisons.

They cannot uniquely distinguish the following:

- True P → D degradation versus increasing diversion of residual R into B and D.
- Catalyst deactivation versus product inhibition versus substrate-dependent selectivity.
- A reversible R ⇌ P step followed by trapping or degradation.
- Intrinsic Arrhenius differences versus differing actual temperature trajectories caused by vessel thermal lag.
- One chemical byproduct versus multiple unresolved processes represented by the same public signal.
- Real chemical-state changes versus small channel-specific assay biases when differences are comparable to instrument uncertainty.

The increased degradation warning with extended exposure favors a consecutive-loss interpretation, but it does not prove that the desired product itself is the degraded precursor. K1 acknowledged this explicitly as a competing explanation.

A second important competitor concerns safety. K1 proposed a composition baseline plus thermal-history accumulator. An alternative is that reported risk is a bounded state function dominated by current temperature, concentration, and solvent category, rather than a genuinely path-integrated hazard. Batch 1’s much smaller risk increment during its second heat period is compatible with thermal saturation or approach to a steady temperature, but it does not identify the mathematical form.

4. One additional complete experiment

If only one legal complete experiment were available, I would prioritize discrimination between product degradation and conversion-dependent parallel selectivity rather than attempt another score-only optimization.

I would use the Batch 11 composition—0.080 L toluene, 0.040 mol reagent, and 0.005 mol Catalyst B at 600 rpm—and apply a 350 K target. I would measure by HPLC after 3600 s, continue heating at 350 K for another 3600 s, measure again with the same HPLC method, then terminate and perform the required final assay. Using the same nonfinal instrument at both time points would reduce the cross-instrument ambiguity that affected comparisons between one HPLC result and one final assay.

Possible outcomes would change the interpretation as follows:

- If reactant proxy changed little after 3600 s while target-product proxy fell and degradation proxy rose, that would strongly support direct or indirect destruction of accumulated P.
- If target product remained roughly constant while residual reactant declined into byproduct/degradation channels, that would support a conversion-dependent parallel network more than P degradation.
- If both target and byproduct signals declined while degradation rose, a broader thermal decomposition of multiple products would become more plausible.
- If all signals were nearly stationary after 3600 s, the Batch 11/12 differences would be more plausibly attributed to independent-batch variation or measurement noise than to strong kinetics over the additional residence time.
- If conversion and target both continued rising through 7200 s without a selectivity penalty, the present finite-optimum interpretation would need substantial revision.

This experiment would still not identify elementary steps, but it would be more discriminating than another single endpoint. I would not actually execute it under the present instruction.

5. Trade-off between identifiability and score optimization

The campaign made an explicit practical trade-off in favor of finding a strong safe score. The research goal emphasized an operating procedure, so after a limited catalyst and solvent screen I concentrated most remaining batches near the best observed Catalyst B/toluene region.

There were meaningful investments in identifiability:

- Batches 2–4 formed a controlled catalyst comparison.
- Batches 2 and 5–7 formed a controlled solvent comparison.
- Batches 7–10 explored qualitatively different thermal programs.

Those experiments sacrificed some immediate score potential. In particular, testing water, ethanol, Catalysts C and D, and the cool-long schedule was useful for understanding the response surface even though several conditions were unlikely to beat the current leader after early evidence accumulated.

Optimization then dominated Batches 11–12. Interpolating to 350 K and adjusting residence time was effective for score, but it narrowed the design around one catalyst and solvent. No batch varied catalyst loading, reagent concentration, solvent volume, or stirring rate. Consequently, K1 could not identify reaction orders, catalyst saturation, mass-transfer effects, or cost-performance trade-offs.

Maximum catalyst loading was especially consequential. It made all batches display visible cost at the ceiling of 1.0, preventing estimation of how catalyst amount affects either score or cost. This was a clear case in which optimization intuition—use enough catalyst to obtain conversion—sacrificed mechanistic and economic identifiability.

The intermediate measurements were also not used optimally for identification. Most HPLC measurements occurred immediately before termination and final assay. They supplied a second noisy view of the endpoint but not a kinetic trajectory. Time-resolved sampling within fewer batches would have been more mechanistically informative, while endpoint screening across more conditions was more useful for rapid optimization.

Batch 1 illustrates both sides of the trade-off. Extending heating produced valuable evidence about secondary chemistry, but because Catalyst A was not tested under the standard one-period schedule, the experiment reduced catalyst identifiability. Once the campaign found a promising region, no replicate was reserved, so confidence in the recommendation was traded for broader search and local optimization.

6. Underused evidence and weaknesses in the blind predictions

Several evidence sources were underused:

- I relied almost entirely on processed estimates and did not inspect or quantitatively model the full public spectral artifacts. Peak areas and assignments might have supported a more disciplined comparison of reactant, target, byproduct, and degradation proxies.
- The paired HPLC and final-assay observations could have been used to estimate empirical channel offsets or cross-instrument dispersion. Instead, K1 treated their differences qualitatively.
- Operation-level temperature changes and risk increments were not fitted into a thermal-response model. Batch 1 supplied evidence of approach to a target, but the thermal time constant remained unestimated.
- The score observations could have been used to fit several candidate empirical score functions. K1 correctly stated that the exact score equation was unknown, but the retrospective prediction step still relied on an informal score mapping.
- Cost increments and the visible cost ceiling were noted but not exploited because loading never varied.
- No quantitative uncertainty model incorporated between-batch process variation, because exact replicates were absent.

The least reliable blind predictions are Q06 and Q08 (465 K for 7200 s), followed by Q12 (465 K for 1800 s) and Q02/Q04 (410 K for 14400 s). These conditions are far outside the observed temperature range, which ended at 360 K, and they require extrapolation of both desired and degradation kinetics. Predictions near complete conversion, near-zero yield, and very high byproduct signal may be qualitatively plausible but are not strongly calibrated.

Q10 is uniquely uncertain because the campaign never tested quenching. The small safety and stabilization benefit assigned relative to Q09 was explicitly speculative. It could be zero, larger than predicted, or affect public channels in an unanticipated way.

Q01–Q08 also extrapolate catalyst loading substantially away from the single studied ratio. K1 had explicitly identified catalyst loading and reaction order as unknown, so the blind predictions necessarily leaned on an unsupported effective-dose assumption. The different 400 rpm stirring speed and smaller total scale add further uncertainty.

Several intervals were probably too narrow despite being described as broad:

- The Q06/Q08 safety intervals may not adequately cover an unknown high-temperature risk law or saturation behavior.
- The Q06/Q08 yield and selectivity intervals concentrated strongly near zero without direct evidence that the target must be almost completely destroyed at 465 K.
- Q01 and Q03 may have underrepresented uncertainty about whether thermal acceleration or catalyst-loading reduction dominates at 410 K.
- Q10’s interval did not separately represent structural uncertainty about the quench operation.
- Score intervals at extreme conditions may be too narrow because the score equation itself was not identified, especially around safety-limit violations.

This is partly inconsistent with the caution in K1. K1 correctly restricted the mechanistic interpretation to the tested region and stated that hotter and differently loaded conditions were unsupported. The blind-prediction rationale repeated that warning, but some numerical point estimates and tight boundary-clipped intervals conveyed more confidence than the evidence justified. In particular, K1’s observation that hot-short operation preserved selectivity at 360 K did not justify a confident assumption of catastrophic target destruction at 465 K; that was extrapolation, not an established continuation of the observed trend.

7. Limitations of the sealed recommendation

Batch 11 was the sample-in highest observed result, not a proven global or even local optimum. Its final score was 0.3317, compared with 0.3258 for Batch 12 and 0.3203 for Batch 8. These differences are modest relative to possible instrument and process variability. With no exact replicates, I cannot establish that Batch 11 would consistently outperform those neighbors.

The recommendation also uses maximum catalyst loading and therefore carries a cost ceiling of 1.0. A lower-loading procedure might achieve a better practical balance, but that dimension was never tested. Similarly, the chosen 600 rpm may be unnecessarily high or insufficient; no mixing study was performed.

Repeatability should first be tested with multiple independent exact replicates of Batch 11, using the same final assay and preferably a prespecified analysis of score, risk, and individual reaction channels. Replication should estimate both mean performance and variance. A single successful repeat would still be insufficient to characterize reproducibility.

Local robustness should then be tested with a small neighborhood around the recommendation—for example 345, 350, and 355 K; residence times around 3300, 3600, and 3900 s; and modest perturbations in catalyst loading and stirring. The important question is not only whether 350 K/3600 s has the largest mean score, but whether small execution errors cause large losses or safety changes. A broad plateau could be operationally preferable to a narrow numerical maximum.

Cross-material robustness would require repeating a structured neighborhood with other catalysts and solvents. The campaign showed that material interactions are strong, so the Batch 11 thermal schedule cannot be assumed to transfer to Catalyst D, acetonitrile, or water. Cross-scale robustness would require varying reagent amount and solvent volume while controlling concentration, because the present data confound scale and concentration outside the single studied recipe.

Cross-world generalization is even less defensible. The catalysts are anonymous latent profiles, and the solvent effects are benchmark categories. Another world could assign different latent kinetics while preserving the same public labels. The recommendation should therefore be described as conditional on this world and this campaign, not as a universal chemical recipe.

In summary, the sealed recommendation is justified as “the highest observed final safe score among the 12 tested batches.” It has not been demonstrated to be globally optimal, continuously locally optimal, repeatable, robust to execution error, transferable across materials, or portable to another benchmark world.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 92.4 | none | 0 |
| Q | yes | 0 | 84.8 | none | 0 |
| K2 | yes | 0 | 102.1 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1452 | 0.5833 | 0.3408 | 0.6428 |
| conversion | 0.0386 | 0.7833 | 0.1092 | 0.1358 |
| safety_risk | 0.0958 | 0.4167 | 0.2058 | 0.3909 |
| score | 0.1225 | 0.4167 | 0.1253 | 0.8298 |
| selectivity | 0.2165 | 0.3667 | 0.2779 | 1.2548 |
| yield | 0.2256 | 0.4167 | 0.2421 | 1.5408 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1700 | 0.4300 | 0.2139 | 0.2057, 0.2159, 0.2138, 0.2254, 0.2086 |
| conversion | 0.8800 | 0.7200 | 0.9800 | 0.6957 | 0.6897, 0.6952, 0.6940, 0.7017, 0.6977 |
| safety_risk | 0.2600 | 0.2000 | 0.3400 | 0.2754 | 0.2754, 0.2754, 0.2754, 0.2754, 0.2754 |
| score | 0.2200 | 0.0900 | 0.3400 | 0.2839 | 0.2842, 0.2837, 0.2876, 0.2807, 0.2834 |
| selectivity | 0.6300 | 0.4300 | 0.7900 | 0.6862 | 0.6900, 0.6867, 0.6939, 0.6790, 0.6813 |
| yield | 0.5200 | 0.3200 | 0.6800 | 0.4861 | 0.4859, 0.4853, 0.4909, 0.4809, 0.4873 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6400 | 0.4500 | 0.8200 | 0.8398 | 0.8417, 0.8440, 0.8409, 0.8398, 0.8323 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9941 | 0.9985, 0.9966, 0.9872, 0.9935, 0.9947 |
| safety_risk | 0.4200 | 0.3100 | 0.5600 | 0.2761 | 0.2761, 0.2761, 0.2761, 0.2761, 0.2761 |
| score | 0.0250 | 0.0000 | 0.1000 | 0.0474 | 0.0508, 0.0504, 0.0416, 0.0466, 0.0477 |
| selectivity | 0.1800 | 0.0500 | 0.3800 | 0.1699 | 0.1754, 0.1686, 0.1553, 0.1814, 0.1686 |
| yield | 0.1200 | 0.0200 | 0.2900 | 0.1699 | 0.1737, 0.1776, 0.1662, 0.1609, 0.1713 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4800 | 0.3000 | 0.6700 | 0.2111 | 0.2055, 0.2061, 0.2203, 0.2139, 0.2099 |
| conversion | 0.9800 | 0.9000 | 1.0000 | 0.9681 | 0.9692, 0.9731, 0.9736, 0.9533, 0.9713 |
| safety_risk | 0.2600 | 0.2000 | 0.3400 | 0.2778 | 0.2778, 0.2778, 0.2778, 0.2778, 0.2778 |
| score | 0.1000 | 0.0250 | 0.2200 | 0.4196 | 0.4168, 0.4197, 0.4258, 0.4180, 0.4177 |
| selectivity | 0.4000 | 0.2100 | 0.6000 | 0.7914 | 0.7897, 0.8013, 0.8003, 0.7930, 0.7728 |
| yield | 0.3600 | 0.1700 | 0.5500 | 0.7661 | 0.7599, 0.7589, 0.7746, 0.7647, 0.7722 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7400 | 0.5500 | 0.9000 | 0.8675 | 0.8672, 0.8797, 0.8595, 0.8702, 0.8611 |
| conversion | 0.9970 | 0.9700 | 1.0000 | 0.9944 | 0.9863, 1.0000, 0.9939, 0.9952, 0.9966 |
| safety_risk | 0.4200 | 0.3100 | 0.5600 | 0.2766 | 0.2766, 0.2766, 0.2766, 0.2766, 0.2766 |
| score | 0.0060 | 0.0000 | 0.0350 | 0.0157 | 0.0080, 0.0161, 0.0181, 0.0189, 0.0174 |
| selectivity | 0.0700 | 0.0100 | 0.2000 | 0.1642 | 0.1513, 0.1625, 0.1614, 0.1705, 0.1754 |
| yield | 0.0300 | 0.0000 | 0.1200 | 0.1666 | 0.1574, 0.1674, 0.1745, 0.1706, 0.1633 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2000 | 0.1100 | 0.3400 | 0.4095 | 0.4077, 0.4061, 0.4111, 0.4131, 0.4099 |
| conversion | 0.7000 | 0.5000 | 0.8600 | 0.8332 | 0.8312, 0.8310, 0.8387, 0.8337, 0.8316 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 | 0.1425 | 0.1425, 0.1425, 0.1425, 0.1425, 0.1425 |
| score | 0.2600 | 0.1300 | 0.3700 | 0.2864 | 0.2824, 0.2871, 0.2854, 0.2868, 0.2905 |
| selectivity | 0.7400 | 0.5800 | 0.8600 | 0.5133 | 0.5031, 0.5128, 0.5051, 0.5121, 0.5337 |
| yield | 0.5000 | 0.3200 | 0.6500 | 0.4276 | 0.4245, 0.4302, 0.4290, 0.4291, 0.4254 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7600 | 0.5700 | 0.9200 | 0.7282 | 0.7218, 0.7240, 0.7313, 0.7302, 0.7337 |
| conversion | 0.9990 | 0.9800 | 1.0000 | 0.9965 | 1.0000, 0.9919, 1.0000, 1.0000, 0.9907 |
| safety_risk | 0.5800 | 0.4200 | 0.7500 | 0.4363 | 0.4363, 0.4363, 0.4363, 0.4363, 0.4363 |
| score | 0.0020 | 0.0000 | 0.0150 | 0.0498 | 0.0537, 0.0446, 0.0465, 0.0489, 0.0551 |
| selectivity | 0.0300 | 0.0000 | 0.1200 | 0.2795 | 0.2971, 0.2653, 0.2673, 0.2764, 0.2912 |
| yield | 0.0100 | 0.0000 | 0.0600 | 0.2719 | 0.2700, 0.2689, 0.2704, 0.2708, 0.2794 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3800 | 0.2300 | 0.5600 | 0.4184 | 0.4194, 0.4145, 0.4188, 0.4197, 0.4197 |
| conversion | 0.9300 | 0.8200 | 0.9900 | 0.9928 | 0.9971, 1.0000, 0.9906, 0.9925, 0.9836 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 | 0.1442 | 0.1442, 0.1442, 0.1442, 0.1442, 0.1442 |
| score | 0.2000 | 0.0800 | 0.3200 | 0.3581 | 0.3580, 0.3569, 0.3566, 0.3613, 0.3579 |
| selectivity | 0.5800 | 0.3900 | 0.7400 | 0.5934 | 0.5896, 0.5947, 0.5866, 0.6035, 0.5928 |
| yield | 0.5400 | 0.3400 | 0.6800 | 0.5909 | 0.5920, 0.5851, 0.5918, 0.5926, 0.5930 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8000 | 0.6100 | 0.9500 | 0.7445 | 0.7388, 0.7527, 0.7424, 0.7462, 0.7422 |
| conversion | 0.9990 | 0.9850 | 1.0000 | 0.9968 | 0.9985, 0.9993, 1.0000, 0.9924, 0.9936 |
| safety_risk | 0.5800 | 0.4200 | 0.7500 | 0.4367 | 0.4367, 0.4367, 0.4367, 0.4367, 0.4367 |
| score | 0.0010 | 0.0000 | 0.0080 | 0.0264 | 0.0286, 0.0246, 0.0267, 0.0239, 0.0283 |
| selectivity | 0.0150 | 0.0000 | 0.0700 | 0.2798 | 0.2745, 0.2727, 0.2802, 0.2749, 0.2966 |
| yield | 0.0050 | 0.0000 | 0.0300 | 0.2857 | 0.2940, 0.2849, 0.2854, 0.2835, 0.2808 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6900 | 0.4900 | 0.8600 | 0.6057 | 0.6253, 0.6067, 0.5983, 0.5999, 0.5984 |
| conversion | 0.9970 | 0.9600 | 1.0000 | 0.9992 | 1.0000, 1.0000, 0.9973, 1.0000, 0.9986 |
| safety_risk | 0.3700 | 0.2800 | 0.4900 | 0.2770 | 0.2770, 0.2770, 0.2770, 0.2770, 0.2770 |
| score | 0.0100 | 0.0000 | 0.0550 | 0.1944 | 0.1933, 0.1986, 0.1912, 0.1959, 0.1929 |
| selectivity | 0.1200 | 0.0250 | 0.2900 | 0.4029 | 0.4000, 0.4142, 0.3995, 0.4034, 0.3976 |
| yield | 0.0700 | 0.0100 | 0.2000 | 0.4116 | 0.4105, 0.4149, 0.4062, 0.4149, 0.4113 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6800 | 0.4800 | 0.8500 | 0.6042 | 0.6019, 0.6084, 0.6143, 0.5968, 0.5997 |
| conversion | 0.9970 | 0.9600 | 1.0000 | 0.9984 | 1.0000, 0.9989, 0.9932, 1.0000, 1.0000 |
| safety_risk | 0.3400 | 0.2500 | 0.4600 | 0.1480 | 0.1480, 0.1480, 0.1480, 0.1480, 0.1480 |
| score | 0.0140 | 0.0000 | 0.0750 | 0.2470 | 0.2512, 0.2477, 0.2453, 0.2458, 0.2452 |
| selectivity | 0.1300 | 0.0300 | 0.3100 | 0.4078 | 0.4094, 0.4099, 0.4019, 0.4050, 0.4126 |
| yield | 0.0800 | 0.0100 | 0.2200 | 0.4036 | 0.4126, 0.4037, 0.4043, 0.4019, 0.3957 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4300 | 0.2700 | 0.6200 | 0.6571 | 0.6562, 0.6608, 0.6647, 0.6504, 0.6535 |
| conversion | 0.9500 | 0.8400 | 0.9950 | 0.9983 | 1.0000, 1.0000, 1.0000, 0.9978, 0.9939 |
| safety_risk | 0.2400 | 0.1800 | 0.3200 | 0.1435 | 0.1435, 0.1435, 0.1435, 0.1435, 0.1435 |
| score | 0.1400 | 0.0500 | 0.2600 | 0.2115 | 0.2165, 0.2075, 0.2108, 0.2113, 0.2114 |
| selectivity | 0.5500 | 0.3500 | 0.7100 | 0.3493 | 0.3619, 0.3389, 0.3456, 0.3487, 0.3513 |
| yield | 0.5000 | 0.3000 | 0.6500 | 0.3529 | 0.3571, 0.3490, 0.3530, 0.3529, 0.3525 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6400 | 0.4300 | 0.8300 | 0.2829 | 0.2739, 0.3016, 0.2847, 0.2771, 0.2769 |
| conversion | 0.9950 | 0.9400 | 1.0000 | 0.9872 | 0.9900, 0.9898, 0.9852, 0.9794, 0.9916 |
| safety_risk | 0.3900 | 0.2900 | 0.5200 | 0.4375 | 0.4375, 0.4375, 0.4375, 0.4375, 0.4375 |
| score | 0.0150 | 0.0000 | 0.0800 | 0.3230 | 0.3291, 0.3202, 0.3270, 0.3198, 0.3191 |
| selectivity | 0.1800 | 0.0400 | 0.3800 | 0.7109 | 0.7179, 0.6994, 0.7261, 0.7010, 0.7101 |
| yield | 0.1100 | 0.0150 | 0.2800 | 0.7129 | 0.7230, 0.7125, 0.7138, 0.7129, 0.7025 |

## Recommendation retest

- Selected source batch: `11`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2175 | 0.2233 | 0.0058 |
| conversion | 0.8261 | 0.8252 | -0.0009 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.0851 | 0.0749 | -0.0101 |
| safety_risk | 0.2064 | 0.2064 | 0.0000 |
| score | 0.3317 | 0.3202 | -0.0115 |
| selectivity | 0.7720 | 0.7436 | -0.0283 |
| virtual_spectrum_summary | 0.1579 | 0.1565 | -0.0014 |
| yield | 0.6225 | 0.6117 | -0.0108 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
