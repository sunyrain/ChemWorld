# RX-W04--S--mechanism_discovery--Opaque

## Run summary

- World: `RX-W04`
- Locus: `S`
- Goal: `mechanism_discovery`
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

- Selected batch: `12`
- Rationale: Batch 12 gave the highest observed final yield and campaign score while remaining below the safety limit; the 370 K, 3600 s condition with prompt quench also directly demonstrated high conversion with controlled post-reaction risk.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.2692 | 0.6435 | 0.4064 | 0.1570 | 0.0260 | 0.1528 | 0.1404 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.4460 | 0.7859 | 0.5511 | 0.1268 | 0.0492 | 0.1711 | 0.2530 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.2577 | 0.5880 | 0.4255 | 0.1758 | 0.0016 | 0.1518 | 0.1243 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.2950 | 0.7261 | 0.4191 | 0.1231 | 0.0198 | 0.1566 | 0.1710 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.2561 | 0.8163 | 0.3193 | 0.0717 | 0.0052 | 0.1074 | 0.1901 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.2470 | 0.6685 | 0.3745 | 0.1193 | 0.0000 | 0.1324 | 0.1438 |
| 7 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.4426 | 0.8096 | 0.5556 | 0.1116 | 0.0198 | 0.1711 | 0.2580 |
| 8 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 1800 s @ 600 rpm | no | 0.4670 | 0.8055 | 0.5735 | 0.1202 | 0.0260 | 0.1848 | 0.2624 |
| 9 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | no | 0.3482 | 0.7923 | 0.4341 | 0.0984 | 0.0211 | 0.1680 | 0.2052 |
| 10 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 1800 s @ 600 rpm | no | 0.5504 | 0.7927 | 0.6939 | 0.1285 | 0.0468 | 0.2088 | 0.2938 |
| 11 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 600 s @ 600 rpm | no | 0.1835 | 0.8199 | 0.1921 | 0.0540 | 0.0076 | 0.1519 | 0.1292 |
| 12 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | yes | 0.6813 | 0.7426 | 0.9128 | 0.2485 | 0.1322 | 0.2095 | 0.3552 |

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
  "end_step": 7,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.15704578161239624,
    "conversion": 0.40636226534843445,
    "cost": 1.0,
    "degradation_warning": 0.025990484282374382,
    "safety_risk": 0.15283197164535522,
    "score": 0.14043033123016357,
    "selectivity": 0.6434990763664246,
    "virtual_spectrum_summary": 0.0980708971619606,
    "yield": 0.269234299659729
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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.1268320530653,
    "conversion": 0.5510530471801758,
    "cost": 1.0,
    "degradation_warning": 0.04923022910952568,
    "safety_risk": 0.17109911143779755,
    "score": 0.25298261642456055,
    "selectivity": 0.7858568429946899,
    "virtual_spectrum_summary": 0.09191122651100159,
    "yield": 0.4460192918777466
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.17581596970558167,
    "conversion": 0.4254535138607025,
    "cost": 1.0,
    "degradation_warning": 0.0016492038266733289,
    "safety_risk": 0.15179824829101562,
    "score": 0.12432070821523666,
    "selectivity": 0.5880287289619446,
    "virtual_spectrum_summary": 0.0974409282207489,
    "yield": 0.25769346952438354
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.12310628592967987,
    "conversion": 0.419119268655777,
    "cost": 1.0,
    "degradation_warning": 0.01978832483291626,
    "safety_risk": 0.15662945806980133,
    "score": 0.17096483707427979,
    "selectivity": 0.7261490225791931,
    "virtual_spectrum_summary": 0.07661320269107819,
    "yield": 0.29499727487564087
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.0716501995921135,
    "conversion": 0.3193441331386566,
    "cost": 1.0,
    "degradation_warning": 0.005163365509361029,
    "safety_risk": 0.10739839822053909,
    "score": 0.19012397527694702,
    "selectivity": 0.8163487315177917,
    "virtual_spectrum_summary": 0.041731126606464386,
    "yield": 0.25607913732528687
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.119346983730793,
    "conversion": 0.3745047152042389,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.13235029578208923,
    "score": 0.14380158483982086,
    "selectivity": 0.6684585809707642,
    "virtual_spectrum_summary": 0.06564084440469742,
    "yield": 0.2469852864742279
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
      "solvent": 2,
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.11163531988859177,
    "conversion": 0.5555585026741028,
    "cost": 1.0,
    "degradation_warning": 0.019818900153040886,
    "safety_risk": 0.17109911143779755,
    "score": 0.25798875093460083,
    "selectivity": 0.8096224665641785,
    "virtual_spectrum_summary": 0.07031793147325516,
    "yield": 0.4425547420978546
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
      "solvent": 3,
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.1201772391796112,
    "conversion": 0.5735483765602112,
    "cost": 1.0,
    "degradation_warning": 0.026011820882558823,
    "safety_risk": 0.1848485767841339,
    "score": 0.26235324144363403,
    "selectivity": 0.8055285811424255,
    "virtual_spectrum_summary": 0.07780279964208603,
    "yield": 0.4669952690601349
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
      "solvent": 3,
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.09840910136699677,
    "conversion": 0.43407538533210754,
    "cost": 1.0,
    "degradation_warning": 0.021064188331365585,
    "safety_risk": 0.16795673966407776,
    "score": 0.20518161356449127,
    "selectivity": 0.792250394821167,
    "virtual_spectrum_summary": 0.06360389292240143,
    "yield": 0.3482300341129303
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
      "solvent": 3,
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
    "byproduct_signal": 0.128497913479805,
    "conversion": 0.6939120292663574,
    "cost": 1.0,
    "degradation_warning": 0.046833585947752,
    "safety_risk": 0.20877373218536377,
    "score": 0.2937704920768738,
    "selectivity": 0.7927486896514893,
    "virtual_spectrum_summary": 0.09174896776676178,
    "yield": 0.5503507852554321
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
      "solvent": 3,
      "volume_L": 0.08
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.05403317138552666,
    "conversion": 0.19209454953670502,
    "cost": 1.0,
    "degradation_warning": 0.0076285540126264095,
    "safety_risk": 0.15187083184719086,
    "score": 0.12923169136047363,
    "selectivity": 0.8198681473731995,
    "virtual_spectrum_summary": 0.03315109387040138,
    "yield": 0.18349269032478333
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.24846209585666656,
    "conversion": 0.9128464460372925,
    "cost": 1.0,
    "degradation_warning": 0.1321973353624344,
    "safety_risk": 0.20949068665504456,
    "score": 0.355197012424469,
    "selectivity": 0.7426288723945618,
    "virtual_spectrum_summary": 0.19614295661449432,
    "yield": 0.6813148856163025
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

# Mechanistic report

## 1. Scope and evidential status

This report describes a synthetic benchmark world with anonymous reagent, target, impurity/degradation channels, and categorical catalyst effects. I do not assign real chemical identities to the catalyst or reaction species. Solvent names are real selectable identities, but their observed effects here should be interpreted as benchmark categorical effects rather than transferable predictions about real chemistry.

All twelve batches used 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring. Consequently, the campaign identifies relative catalyst, solvent, temperature, and time effects only at that composition and agitation. It does not establish reaction orders in reagent or catalyst.

## 2. Empirical picture of the world

The simplest account consistent with the observations is a thermally activated catalytic conversion of reactant R into desired target P, accompanied by a competing impurity channel and an exposure-dependent degradation channel. Catalyst identity mainly changes activity and branching selectivity. Solvent identity changes activity, selectivity, and the initial safety-risk state. Increasing temperature accelerates conversion strongly. Extending hot residence time continues target formation, but increasingly favors impurity formation or target degradation, lowering selectivity. Quenching rapidly reduces temperature and risk and appears to arrest further conversion.

Final-assay yield was approximately, though not exactly because of measurement noise, conversion multiplied by selectivity. For example, batch 10 had conversion 0.6939 and selectivity 0.7927, whose product is about 0.550, matching its measured yield of 0.5504. Thus I interpret conversion as total reagent consumption and selectivity as the fraction of converted material assigned to target.

## 3. Proposed kinetic structure

A useful minimal process model is:

R --kP--> P
R --kB--> B
P --kD--> D

where B is a directly formed competing product and D is thermally generated degradation material. One possible set of equations is

    dR/dt = -a(t)[kP(T,S,C) + kB(T,S,C)]R
    dP/dt =  a(t)kP(T,S,C)R - kD(T,S)P
    dB/dt =  a(t)kB(T,S,C)R
    dD/dt =  kD(T,S)P

Here C is catalyst identity, S is solvent identity, and a(t) is the fraction of active catalyst. If deactivation exists, a possible extension is

    da/dt = -kdeact(T,S,C)a.

The present observations do not require strong deactivation to explain overall conversion, so a(t)=1 is an adequate first approximation over 600–3600 s. Deactivation remains plausible as a contributor to changing selectivity.

Each kinetic coefficient could be represented phenomenologically by

    ki(T,S,C) = Ai × fS,i(S) × fC,i(C) × exp[-Ei/(RT)].

This form is explanatory rather than a uniquely identified fit. The experiments distinguish categorical activity and branching effects, but do not determine separate Ai and Ei values for all pathways.

For engineering prediction inside the explored region, a simpler conversion model works reasonably well:

    X(t) ≈ 1 - exp[-kapp(T,S,C)t].

For Catalyst B in toluene, apparent rate constants calculated from final conversion were approximately:

- Batch 9, nominal 330 K for 1800 s: kapp ≈ 3.16×10^-4 s^-1.
- Batch 8, nominal 350 K for 1800 s: kapp ≈ 4.74×10^-4 s^-1.
- Batch 10, nominal 370 K for 1800 s: kapp ≈ 6.58×10^-4 s^-1.
- Batch 12, nominal 370 K for 3600 s: kapp ≈ 6.78×10^-4 s^-1.

The agreement of the two 370 K estimates is notable and supports approximately first-order conversion without major loss of overall catalyst activity over 3600 s. A rough Arrhenius comparison of the 330 and 370 K apparent constants gives an effective activation energy near 19 kJ mol^-1. This number is only a local empirical descriptor: the batches experienced heat-up transients rather than perfect isothermal histories, and the estimate is based on few points.

## 4. Actual thermal history

The imposed target temperature was not reached instantaneously. Starting near 300 K, the measured temperature changes during heating were:

- Approximately +49.2 K during nominal 350 K, 1800 s batches.
- +30.28 K in batch 9 at nominal 330 K for 1800 s.
- +67.71 K in batch 10 at nominal 370 K for 1800 s.
- +47.72 K in batch 11 at nominal 350 K for 600 s.
- +67.57 K in batch 12 at nominal 370 K for 3600 s.

Thus the system approached, but generally remained slightly below, its set point. The 600 s experiment was already close to 350 K by termination, but it spent a greater fraction of its residence time in the heat-up transient. Any kinetic equation should ideally integrate over the actual temperature path:

    cumulative exposure = integral from 0 to t of kapp[T(u),S,C] du,
    X = 1 - exp(-cumulative exposure).

The available temperature information provides only net temperature changes, not a dense time trace, so the exact thermal response constant is not identifiable.

## 5. Catalyst effects

Batches 1–4 compared all four catalysts in acetonitrile at nominal 350 K for 1800 s.

- Batch 1, Catalyst A: conversion 0.4064, selectivity 0.6435, yield 0.2692, byproduct 0.1570.
- Batch 2, Catalyst B: conversion 0.5511, selectivity 0.7859, yield 0.4460, byproduct 0.1268.
- Batch 3, Catalyst C: conversion 0.4255, selectivity 0.5880, yield 0.2577, byproduct 0.1758.
- Batch 4, Catalyst D: conversion 0.4191, selectivity 0.7261, yield 0.2950, byproduct 0.1231.

Catalyst B was clearly the best of the tested formulations at this condition because it improved both conversion and selectivity. Catalyst D appeared more selective than A or C but less active than B. Catalyst C had the weakest target branching despite moderate conversion.

The nominal repeat with Catalyst B and acetonitrile, batch 7, produced conversion 0.5556, selectivity 0.8096, and yield 0.4426. Its agreement with batch 2 supports reproducibility and suggests that the catalyst ranking is not merely assay noise.

This catalyst comparison caused me to reject a model in which catalysts affect only total rate. They also affect pathway branching: similar conversions for A, C, and D produced substantially different selectivities.

## 6. Solvent effects

Batches 5–8 used Catalyst B at nominal 350 K for 1800 s:

- Batch 5, water: conversion 0.3193, selectivity 0.8163, yield 0.2561, byproduct 0.0717, risk 0.1074.
- Batch 6, ethanol: conversion 0.3745, selectivity 0.6685, yield 0.2470, byproduct 0.1193, risk 0.1324.
- Batch 7, acetonitrile: conversion 0.5556, selectivity 0.8096, yield 0.4426, byproduct 0.1116, risk 0.1711.
- Batch 8, toluene: conversion 0.5735, selectivity 0.8055, yield 0.4670, byproduct 0.1202, risk 0.1848.

Toluene and acetonitrile were the fastest environments, while water was slow but selective and generated the lowest byproduct signal and risk. Ethanol was both slower and less selective than the two fastest solvents. Therefore solvent affects at least two independent quantities: the overall conversion rate and the target/impurity branching ratio. A single solvent polarity multiplier on all rates would not explain these results.

Toluene was selected for subsequent thermal exploration because it gave the largest yield, not because it was intrinsically safest. Water offered a lower-risk alternative if conversion could be raised by longer residence time, but that extrapolation was not experimentally tested.

## 7. Temperature dependence

With Catalyst B in toluene for 1800 s:

- Batch 9 at nominal 330 K: conversion 0.4341, selectivity 0.7923, yield 0.3482, byproduct 0.0984, risk 0.1680.
- Batch 8 at nominal 350 K: conversion 0.5735, selectivity 0.8055, yield 0.4670, byproduct 0.1202, risk 0.1848.
- Batch 10 at nominal 370 K: conversion 0.6939, selectivity 0.7927, yield 0.5504, byproduct 0.1285, risk 0.2088.

Conversion rose monotonically with temperature, while selectivity stayed near 0.79–0.81 over this 1800 s series. This initially suggested that temperature accelerated target and primary competing conversion by roughly similar factors over 330–370 K. The degradation-warning signal nevertheless increased from 0.0211 in batch 9 to 0.0468 in batch 10, indicating that adverse exposure begins to matter at the high end even before selectivity falls strongly.

## 8. Time, competing conversion, and degradation

Batch 11 at nominal 350 K for only 600 s gave conversion 0.1921, selectivity 0.8199, yield 0.1835, byproduct 0.0540, and degradation warning 0.0076. Compared with batch 8 at the same nominal temperature for 1800 s, the longer run produced much more conversion and yield, with a modest decrease in selectivity and increases in byproduct and degradation indicators.

Batch 12 extended the nominal 370 K run to 3600 s. Before quenching, HPLC measured conversion 0.9134, selectivity 0.7088, yield 0.6751, and byproduct 0.2601. The final assay after quench measured conversion 0.9128, selectivity 0.7426, yield 0.6813, byproduct 0.2485, and degradation warning 0.1322.

Compared with batch 10 at 370 K for 1800 s, batch 12 increased conversion from 0.6939 to 0.9128 and yield from 0.5504 to 0.6813, but selectivity fell from 0.7927 to 0.7426, byproduct almost doubled from 0.1285 to 0.2485, and degradation warning rose from 0.0468 to 0.1322. This is the strongest evidence for an exposure-dependent adverse pathway.

Two mechanisms remain credible:

1. Desired target P undergoes secondary thermal degradation, P→D.
2. The direct impurity branch R→B becomes relatively more important at prolonged exposure, possibly because catalyst state changes.

The degradation-warning increase favors the first account, but the available aggregate channels cannot separate it decisively from catalyst deactivation or a changing branch ratio. A combined model is also possible.

## 9. Termination and quench behavior

Batch 12 was quenched after its intermediate HPLC measurement. The quench lowered temperature by 45 K over 57.87 s and reduced reported safety risk from 0.22734 to 0.20949, a decrease of 0.01785. Conversion was effectively unchanged between the pre-quench HPLC result (0.9134) and final assay (0.9128). This supports the operational interpretation that quenching arrests conversion while immediately reducing the thermal-risk state.

The changes in selectivity, yield, and byproduct between HPLC and final assay are comparable to what may arise from different instrument calibrations and measurement noise; they should not be treated as proof that quenching chemically improved selectivity. There was no matched 370 K/3600 s batch terminated without quenching, so the chemical effect of quench versus simple termination is not separately identified.

## 10. Safety coupling

Safety risk depended on both formulation and thermal history. At otherwise matched Catalyst B/350 K/1800 s conditions, final risks ranged from 0.1074 in water to 0.1848 in toluene. Raising toluene conditions from 330 to 370 K increased risk from 0.1680 to 0.2088. Extending the 370 K exposure to 3600 s raised pre-quench risk to 0.2273, after which quenching reduced it to 0.2095.

A plausible qualitative risk-state equation is

    dr/dt = gS(S) + gT[T(t)] + gexp[T(t),t] - gq(quench),

with gT increasing nonlinearly above ambient and gq active during cooling. The fact that doubling the 370 K heating time did not double the heat-associated risk suggests that risk is not simply cumulative energy exposure; it likely includes bounded temperature, formulation, and duration components. Every batch remained below the stated safety limit of 0.35.

## 11. Why batch 12 was recommended

Batch 12 had the highest observed final yield, 0.6813, and highest final score, 0.3552, while remaining below the safety limit. It also provided the clearest evidence about the high-conversion regime and the cost of prolonged exposure: high conversion was achieved, but with declining selectivity and substantially larger impurity and degradation signals. The recommendation is therefore an empirical optimum among tested batches, not a claim that 370 K for 3600 s is the global optimum. A somewhat shorter high-temperature residence might retain most of the yield while improving selectivity, but that is an untested interpolation.

## 12. Limits and competing explanations

The following quantities remain unidentified:

- Reaction order in reagent, because initial reagent amount and volume were fixed.
- Catalyst loading dependence, because catalyst amount was fixed.
- Effects of concentration, mixing, or mass transfer, because volume and stirring rate were fixed.
- Separate activation energies for target formation, direct impurity formation, and target degradation.
- The presence and rate of catalyst deactivation.
- Whether degradation warning corresponds specifically to loss of P or to another correlated high-temperature species.
- Exact temperature trajectories during heat-up and cooling.
- Chemical effects of quenching versus termination, because there was no matched control.

A parallel-reaction-only model, R→P and R→B with time-dependent branching, can reproduce the aggregate conversion and selectivity without invoking P degradation. Conversely, a consecutive model R→P→D could explain the selectivity loss at long exposure even if the direct impurity branch were small. The most defensible present model contains both pathways but treats their separate contributions as uncertain.

Within the tested domain—Catalyst B, 0.5 M nominal starting reagent concentration, 600 rpm, toluene or the other tested solvents, approximately 330–370 K, and 600–3600 s—the first-order conversion model with catalyst- and solvent-specific multipliers and an exposure-dependent selectivity penalty is the most useful predictive account. Extrapolation beyond those ranges, especially to different loadings, concentrations, or much longer times, would be conjectural.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported parallel target/impurity model with exposure-dependent target degradation. Conversion was extrapolated with an approximately first-order rate, a catalyst-concentration multiplier, and local Arrhenius temperature dependence. Yield was treated as surviving target, selectivity as yield divided by conversion, and byproduct signal as approximately converted material not remaining in the target channel. The scoring relation inferred exactly from the campaign observations was score = -0.10 + 0.40×yield + 0.25×selectivity + 0.10×conversion - 0.45×safety_risk, clipped at zero. Intervals include assay noise and, more importantly, structural uncertainty from changes in concentration, catalyst loading, stirring speed, long residence time, and extrapolation from the observed 330–370 K range to 410–465 K.

### Q01

Low catalyst concentration limits conversion despite 410 K. The short exposure should preserve most of Catalyst B's intrinsic selectivity, with moderate thermal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1300 | 0.0700 | 0.2400 |
| conversion | 0.5700 | 0.3800 | 0.7400 |
| safety_risk | 0.1600 | 0.1100 | 0.2300 |
| score | 0.2500 | 0.1500 | 0.3600 |
| selectivity | 0.7700 | 0.6600 | 0.8500 |
| yield | 0.4400 | 0.2900 | 0.5800 |

### Q02

Fourteen-thousand-four-hundred seconds at 410 K should drive nearly complete conversion even at low catalyst loading, but prolonged hot residence is predicted to convert much of the target channel into degradation or impurity signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4300 | 0.8200 |
| conversion | 0.9950 | 0.9300 | 1.0000 |
| safety_risk | 0.3100 | 0.2200 | 0.4300 |
| score | 0.0900 | 0.0000 | 0.2400 |
| selectivity | 0.3600 | 0.1800 | 0.5600 |
| yield | 0.3600 | 0.1800 | 0.5500 |

### Q03

The high catalyst concentration should make the 1800 s reaction nearly complete. Because residence time is short, target formation should still dominate over accumulated degradation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2400 | 0.1300 | 0.3800 |
| conversion | 0.9700 | 0.8800 | 1.0000 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 |
| score | 0.3900 | 0.2700 | 0.4900 |
| selectivity | 0.7500 | 0.6300 | 0.8400 |
| yield | 0.7300 | 0.5900 | 0.8400 |

### Q04

Conversion should saturate early at this catalyst loading. Most of the remaining 410 K residence time therefore acts as adverse thermal exposure, producing low final selectivity and substantial byproduct signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6800 | 0.4800 | 0.8600 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.3500 | 0.2500 | 0.4800 |
| score | 0.0500 | 0.0000 | 0.2100 |
| selectivity | 0.3200 | 0.1400 | 0.5200 |
| yield | 0.3200 | 0.1400 | 0.5200 |

### Q05

At 350 K the low catalyst concentration gives moderate conversion over 7200 s. The lower temperature should retain relatively high selectivity and keep risk low.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1600 | 0.0800 | 0.2700 |
| conversion | 0.6900 | 0.5000 | 0.8300 |
| safety_risk | 0.1100 | 0.0700 | 0.1700 |
| score | 0.3200 | 0.2200 | 0.4200 |
| selectivity | 0.7700 | 0.6700 | 0.8500 |
| yield | 0.5300 | 0.3900 | 0.6500 |

### Q06

The 465 K exposure is far outside the characterized temperature range. The mechanistic extrapolation predicts complete conversion but severe target degradation, high byproduct signal, and safety risk above the stated limit; uncertainty is correspondingly wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8500 | 0.6500 | 0.9700 |
| conversion | 1.0000 | 0.9600 | 1.0000 |
| safety_risk | 0.5200 | 0.3800 | 0.7200 |
| score | 0.0000 | 0.0000 | 0.0900 |
| selectivity | 0.1500 | 0.0400 | 0.3400 |
| yield | 0.1500 | 0.0400 | 0.3400 |

### Q07

High catalyst concentration should achieve nearly complete conversion at 350 K before degradation becomes dominant. This is predicted to be the strongest yield/score condition in the set.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2400 | 0.1300 | 0.3700 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.1400 | 0.0900 | 0.2000 |
| score | 0.4300 | 0.3400 | 0.5000 |
| selectivity | 0.7600 | 0.6600 | 0.8400 |
| yield | 0.7500 | 0.6400 | 0.8400 |

### Q08

High catalyst loading makes conversion effectively immediate relative to the 7200 s treatment, leaving a long 465 K degradation period. Both degradation and safety extrapolations are severe and poorly constrained.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8700 | 0.6900 | 0.9800 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.6200 | 0.4600 | 0.8200 |
| score | 0.0000 | 0.0000 | 0.0600 |
| selectivity | 0.1300 | 0.0300 | 0.2900 |
| yield | 0.1300 | 0.0300 | 0.2900 |

### Q09

The catalyst concentration nearly matches the campaign concentration. At 410 K for 7200 s, conversion should be complete, while accumulated degradation lowers yield and selectivity to roughly one half.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4600 | 0.3000 | 0.6400 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.2500 | 0.1800 | 0.3400 |
| score | 0.2400 | 0.1100 | 0.3600 |
| selectivity | 0.5400 | 0.3600 | 0.6900 |
| yield | 0.5400 | 0.3600 | 0.6900 |

### Q10

The quench occurs after the entire heated residence, so I predict essentially the same chemical endpoints as Q09. Based on batch 12, quenching should primarily lower the final thermal-risk state and therefore modestly improve score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4600 | 0.3000 | 0.6400 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.2000 | 0.1300 | 0.2800 |
| score | 0.2600 | 0.1400 | 0.3800 |
| selectivity | 0.5400 | 0.3600 | 0.6900 |
| yield | 0.5400 | 0.3600 | 0.6900 |

### Q11

The long 350 K treatment should reach almost complete conversion. Degradation is predicted to be appreciable but much slower than at 410–465 K, leaving a comparatively high final yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3100 | 0.1700 | 0.4700 |
| conversion | 1.0000 | 0.9500 | 1.0000 |
| safety_risk | 0.1600 | 0.1000 | 0.2300 |
| score | 0.3800 | 0.2700 | 0.4700 |
| selectivity | 0.6900 | 0.5400 | 0.8000 |
| yield | 0.6900 | 0.5400 | 0.8000 |

### Q12

At 465 K the matched catalyst concentration should give essentially complete conversion within 1800 s. The shorter exposure limits degradation relative to Q06 and Q08, but selectivity, yield, and safety remain uncertain because 465 K is an extrapolation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4500 | 0.2700 | 0.6500 |
| conversion | 1.0000 | 0.9500 | 1.0000 |
| safety_risk | 0.3000 | 0.2100 | 0.4200 |
| score | 0.2200 | 0.0800 | 0.3600 |
| selectivity | 0.5500 | 0.3500 | 0.7200 |
| yield | 0.5500 | 0.3500 | 0.7200 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, and untested

The initial material packet supplied almost no substantive mechanistic claims. It explicitly said that the catalysts were anonymous benchmark formulations, that solvent effects were categorical benchmark effects rather than predictions from real solvent-property correlations, and that experimental evidence was authoritative. My K1 report respected those limits: I did not assign real identities to the catalysts or reaction species, and I treated the solvent labels as selectable categories rather than as evidence for a named real reaction. Nothing in the experiments contradicted that interpretation, but this is an absence of contradiction, not experimental confirmation of the packet's ontology.

The initial task contract did make operational claims that were supported: final assay was available only after termination, HPLC supplied conversion/yield/selectivity/byproduct information, quenching altered the thermal state, and the stated safety limit was 0.35. All twelve observed batches remained below 0.35. Batch 12 showed a concrete quench effect on reported risk, from 0.22734 before quench to 0.20949 afterward.

No initial claim specified the catalyst ranking, solvent ranking, kinetic law, degradation mechanism, activation energy, or optimum. Those were genuinely open questions. Consequently, statements in K1 such as “Catalyst B was clearly the best of the tested formulations at this condition” and the proposed R→P, R→B, and P→D network came from the campaign rather than from the initial packet.

Several issues remained untested rather than supported: reaction order, catalyst-loading dependence, concentration effects, mixing dependence, exact thermal response, and transferability across scales. K1 explicitly listed these limitations. The later blind queries varied catalyst concentration, reagent concentration, stirring rate, temperature up to 465 K, and duration up to 14,400 s; those variations lay outside the experimentally established domain.

There was no clear case in which the initial packet supplied a chemical assertion, the data contradicted it, and I knowingly retained it. There was, however, a weaker methodological analogue: my early working assumption that a common 350 K/1800 s condition would provide a useful neutral comparison was unvalidated when adopted. The campaign subsequently showed that time and temperature strongly controlled both conversion and adverse exposure. I refined the account, but the original design had already committed many batches to a single condition.

2. Experiments that formed or changed my judgment

Batches 1–4 genuinely established the catalyst comparison. At the common acetonitrile/350 K/1800 s condition, Catalyst B in batch 2 produced conversion 0.5511, selectivity 0.7859, and yield 0.4460, exceeding the target performance of Catalysts A, C, and D. The differing selectivities at broadly similar conversions for A, C, and D changed my view from a possible rate-only catalyst effect to a catalyst-dependent branching effect. Batch 7, a nominal repeat of Catalyst B in acetonitrile, gave conversion 0.5556 and yield 0.4426. That agreement materially increased my confidence in the ranking.

Batches 5–8 formed the solvent judgment. Water in batch 5 was slower but safer and cleaner, whereas acetonitrile and toluene were faster. Toluene in batch 8 gave the largest yield in that solvent series, 0.4670, but also the largest risk, 0.1848. This led to the two-factor interpretation in K1: solvent changes both overall rate and branching/safety behavior, rather than merely multiplying every pathway by one common factor.

Batches 9, 8, and 10 provided the most useful temperature comparison at 330, 350, and 370 K for 1800 s in toluene with Catalyst B. Conversion rose from 0.4341 to 0.5735 to 0.6939, while selectivity remained near 0.79–0.81. That evidence supported a thermally activated conversion process and initially suggested similar temperature sensitivity for target and primary competing formation over that limited interval.

Batch 11 changed the time interpretation by showing that 600 s at 350 K gave only 0.1921 conversion but retained selectivity of 0.8199. Batch 12 was the strongest update: at 370 K for 3600 s it reached conversion 0.9128 and yield 0.6813, but selectivity fell to 0.7426, byproduct signal rose to 0.2485, and degradation warning rose to 0.1322. Comparing batches 10 and 12 caused me to add an exposure-dependent adverse pathway rather than extrapolate the approximately constant 1800 s selectivity indefinitely.

The quench in batch 12 informed the operational conclusion that quenching rapidly reduced risk and arrested observable conversion. It did not establish that quenching chemically improved selectivity; K1 correctly treated the HPLC-to-final-assay changes as potentially instrumental.

Several choices were based more on unverified guesses than on existing evidence. Acetonitrile, 350 K, 1800 s, 600 rpm, and maximum permitted reagent/catalyst/solvent quantities were selected before any kinetic data existed. The decision to use Catalyst B in later batches was evidence-based after batches 1–4. The choice of toluene for the thermal series was evidence-based after batches 5–8, but it favored yield over the safer water condition. The exact 330/350/370 K and 600/1800/3600 s grid was a pragmatic sparse design, not the result of an identified kinetic model.

3. Current competing mechanisms and what the data distinguish

The leading account remains the combined network stated in K1:

R→P, R→B, and P→D,

with catalyst and solvent affecting the first two branches and temperature/time increasing both conversion and adverse exposure. This account explains the approximate identity yield ≈ conversion×selectivity and the worsening byproduct/degradation indicators at long high-temperature exposure.

The most important competing explanation is a parallel-reaction-only model in which R forms P and B directly, but the effective branch ratio changes with time because the catalyst changes state. That catalyst-state change could be selective deactivation of the target pathway, activation of an impurity pathway, or a temperature-dependent catalyst speciation change. Such a model can reproduce falling selectivity without any P→D reaction.

A second alternative is that “degradation warning” is merely a correlated measurement channel for high thermal exposure, rather than direct evidence that target P is being destroyed. The warning rose strongly in batch 12, but the target yield itself still rose from batch 10 to batch 12. Thus the campaign did not directly observe a decline in the absolute amount of target during continued heating.

The experiments can distinguish several features. They show that Catalyst B changes more than rate, because catalyst identity affected selectivity. They show that solvent effects are not reducible to one common rate multiplier. They show that conversion is thermally activated and that prolonged high-temperature residence worsens final selectivity and impurity indicators.

They cannot distinguish direct late impurity formation from target degradation, cannot identify a catalyst-deactivation law, and cannot establish whether the apparent first-order conversion law is fundamental or merely local. The close apparent rate constants inferred from batches 10 and 12 at 370 K argue against severe loss of total catalytic activity over 3600 s, but they do not exclude selective catalyst changes. Nor can the data uniquely assign separate activation energies to target formation, impurity formation, and degradation.

4. One additional experiment I would choose

I would use the batch-12 formulation—0.040 mol reagent, 0.080 L toluene, and 0.005 mol Catalyst B at 600 rpm—but perform a paired time-course experiment at 370 K. I would heat for 1800 s, measure HPLC, then continue heating at 370 K for another 12,600 s, terminate, and obtain the required final assay. This remains within the legal 14,400 s maximum for a single heat operation if implemented as a second 12,600 s heat after the first stage.

The purpose would be to move far enough beyond batch 12 to determine whether target yield eventually peaks and declines. The intermediate HPLC would anchor the state within the same vessel, reducing between-batch variability relative to comparing separate endpoints.

If conversion approached one while absolute yield subsequently fell and degradation/byproduct signals rose, that would strongly support P→D target degradation. If yield continued rising or plateaued while selectivity fell only because additional reagent was converted mainly to impurity, a changing parallel branch would be favored. If conversion itself stalled well below one while selectivity and yield stopped changing, catalyst deactivation would become more plausible. If both conversion and product distribution remained unexpectedly stable after the first measurement, my temperature/exposure model would be too aggressive and the batch-12 changes would require more emphasis on batch variability or instrument differences.

This experiment would still have a limitation: intermediate HPLC and final assay are different instruments. A target decline larger than their known noise and the batch-2/batch-7 reproducibility scale would be persuasive, but a small change would remain ambiguous.

5. Tradeoff between identifiability and operational score

The research objective explicitly prioritized an explanatory and predictive account over the public safe score, and the design partly reflected that. Batches 1–4 sacrificed immediate score optimization to screen all catalysts. Batches 5 and 6 tested water and ethanol even though they were not expected, after early evidence, to beat the best acetonitrile result. Batches 9 and 11 explored lower temperature and shorter time and therefore knowingly accepted lower yields to identify kinetic effects. Those were identifiability-oriented choices.

Conversely, the design increasingly shifted toward optimization after Catalyst B and toluene looked favorable. Batch 10 raised temperature to 370 K, and batch 12 doubled the high-temperature residence and added a quench. Batch 12 became the highest-scoring observed batch, but this optimization step combined a time change and a quench relative to earlier work. That reduced causal identifiability. A matched quenched/nonquenched pair or a denser time series would have been scientifically cleaner.

Using the same maximum reagent, solvent, and catalyst quantities in every batch simplified comparisons and exhausted the stock evenly, but it sacrificed identification of concentration and catalyst-loading laws. Likewise, holding stirring at 600 rpm removed one nuisance variable but left transport effects untested. The later blind prediction set exposed the cost of that choice because it required extrapolation to 400 rpm and multiple catalyst concentrations.

There was therefore a real two-way tradeoff. Catalyst and solvent screens, low-temperature batch 9, and short-time batch 11 sacrificed score for knowledge. Selection of Catalyst B/toluene and the long 370 K batch sacrificed some mechanistic separability for yield and score. The overall campaign was mixed rather than purely mechanistic or purely optimizing.

6. Underused evidence and weaknesses in the blind predictions

The most underused evidence was the collection of intermediate HPLC measurements. K1 emphasized selected HPLC/final comparisons, especially batch 12, but did not systematically model the discrepancy between intermediate HPLC and final assay across all batches. Those paired readings could have informed an instrument-offset/noise model and produced better uncertainty intervals.

The actual heat-operation temperature changes were used qualitatively, but not fitted as a common thermal-response model. K1 correctly noted that only net temperature changes, not dense trajectories, were available. Still, the differences between the 600, 1800, and 3600 s temperature responses could have been propagated more explicitly into kinetic uncertainty.

The catalyst-specific heat-risk increments in batches 1–4 were also difficult to exploit. They may reflect catalyst activity and exothermic conversion, but formulation risk, stochastic process variation, and temperature response are entangled. Raw spectral structure and artifact-level information were not analyzed, so potentially useful evidence about whether “byproduct” and “degradation” were distinct channels was left unused.

The least reliable blind predictions are Q06 and Q08: both impose 465 K for 7200 s, far beyond the observed 330–370 K range. Their predicted near-complete conversion, very low yield/selectivity, and high risk depend heavily on extrapolated Arrhenius and degradation laws. Q12, at 465 K for 1800 s, is also highly uncertain. Q02 and Q04 are next most fragile because 14,400 s at 410 K is a fourfold extension beyond the longest observed hot residence and combines that with untested catalyst concentrations. Q03 and Q07 extrapolate high catalyst concentration, while Q01, Q02, Q05, and Q06 extrapolate low catalyst concentration. No campaign batch identified whether rate scales linearly, saturates, or is inhibited by catalyst concentration.

Several intervals were probably too narrow. In particular, conversion intervals close to [0.98,1.00] for Q04, Q08, Q09, and Q11 expressed excessive confidence in catalyst-loading scaling and long-time first-order behavior. The selectivity/yield intervals for Q03 and Q07 may also be too narrow because high catalyst concentration could alter branching rather than only rate. Risk intervals for the 465 K cases may be too narrow because the observed risk model was calibrated only up to 370 K and could be nonlinear or clipped.

This weakness is in tension with K1's stated applicability limit: K1 said the model was useful within approximately 330–370 K, 600–3600 s, fixed loading, concentration, and stirring, and that extrapolation beyond those ranges was conjectural. The blind-prediction rationale acknowledged this, but some numerical intervals did not fully reflect it. The point estimates were legitimate model-based extrapolations; the overconfidence lay mainly in the interval widths.

The inferred score equation was much stronger than the chemical extrapolation: the campaign values were consistent with score = -0.10 + 0.40×yield + 0.25×selectivity + 0.10×conversion - 0.45×safety risk, with clipping at zero. Nevertheless, score intervals inherit all uncertainty in the chemical and risk predictions, so exact knowledge of the arithmetic scoring map does not justify narrow score intervals.

7. Limits of the sealed recommendation

Batch 12 was the sample-internal winner: among the twelve completed batches, it had the highest final yield, 0.6813, and highest score, 0.3552, while its post-quench risk of 0.2095 remained below 0.35. That supports the sealed recommendation as the best observed completed operation.

It does not prove global optimality. Batch 12 had no exact replicate. It combined 370 K, 3600 s, toluene, Catalyst B, and a quench, so the individual contribution of each feature is not isolated. Its selectivity and impurity indicators were already worsening, implying that a shorter residence might offer a better balance. Temperatures between 350 and 370 K, times between 1800 and 3600 s, different catalyst loadings, and water-based longer reactions were not locally optimized.

Repeatability should first be tested by exact independent replication of batch 12, including the same setup quantities, actual thermal history, HPLC timing, quench, termination, and final assay. Local robustness should then be examined with small perturbations around it—for example 360/370/380 K and 2700/3600/4500 s—while repeating the center condition to separate curvature from drift. Catalyst loading and stirring perturbations would test whether the recommendation depends on the fixed campaign recipe or on transport.

Cross-material generalization would require repeating the local design with the other solvents and, separately, at least the next-best catalyst. Cross-world generalization is even weaker: because the catalysts and kinetic effects are explicitly anonymous benchmark constructs, the recommendation should not be transferred to a real named chemical system or another benchmark world without new calibration.

Thus the correct claim is: batch 12 was the highest-performing observed member of this twelve-batch sample and provided a useful high-conversion operating point. The unsupported stronger claim would be: batch 12 is the unique or globally optimal recipe. The campaign did not establish that.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 101.0 | none | 0 |
| Q | yes | 0 | 181.7 | none | 0 |
| K2 | yes | 0 | 104.5 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1650 | 0.6000 | 0.2992 | 0.6345 |
| conversion | 0.0253 | 0.9167 | 0.0975 | 0.1002 |
| safety_risk | 0.0698 | 0.7500 | 0.1883 | 0.2602 |
| score | 0.0543 | 0.9167 | 0.1967 | 0.2454 |
| selectivity | 0.1620 | 0.6500 | 0.2808 | 0.6366 |
| yield | 0.1441 | 0.7167 | 0.3000 | 0.5064 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1300 | 0.0700 | 0.2400 | 0.2139 | 0.2057, 0.2159, 0.2138, 0.2254, 0.2086 |
| conversion | 0.5700 | 0.3800 | 0.7400 | 0.6957 | 0.6897, 0.6952, 0.6940, 0.7017, 0.6977 |
| safety_risk | 0.1600 | 0.1100 | 0.2300 | 0.2754 | 0.2754, 0.2754, 0.2754, 0.2754, 0.2754 |
| score | 0.2500 | 0.1500 | 0.3600 | 0.2839 | 0.2842, 0.2837, 0.2876, 0.2807, 0.2834 |
| selectivity | 0.7700 | 0.6600 | 0.8500 | 0.6862 | 0.6900, 0.6867, 0.6939, 0.6790, 0.6813 |
| yield | 0.4400 | 0.2900 | 0.5800 | 0.4861 | 0.4859, 0.4853, 0.4909, 0.4809, 0.4873 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6400 | 0.4300 | 0.8200 | 0.8398 | 0.8417, 0.8440, 0.8409, 0.8398, 0.8323 |
| conversion | 0.9950 | 0.9300 | 1.0000 | 0.9941 | 0.9985, 0.9966, 0.9872, 0.9935, 0.9947 |
| safety_risk | 0.3100 | 0.2200 | 0.4300 | 0.2761 | 0.2761, 0.2761, 0.2761, 0.2761, 0.2761 |
| score | 0.0900 | 0.0000 | 0.2400 | 0.0474 | 0.0508, 0.0504, 0.0416, 0.0466, 0.0477 |
| selectivity | 0.3600 | 0.1800 | 0.5600 | 0.1699 | 0.1754, 0.1686, 0.1553, 0.1814, 0.1686 |
| yield | 0.3600 | 0.1800 | 0.5500 | 0.1699 | 0.1737, 0.1776, 0.1662, 0.1609, 0.1713 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2400 | 0.1300 | 0.3800 | 0.2111 | 0.2055, 0.2061, 0.2203, 0.2139, 0.2099 |
| conversion | 0.9700 | 0.8800 | 1.0000 | 0.9681 | 0.9692, 0.9731, 0.9736, 0.9533, 0.9713 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 | 0.2778 | 0.2778, 0.2778, 0.2778, 0.2778, 0.2778 |
| score | 0.3900 | 0.2700 | 0.4900 | 0.4196 | 0.4168, 0.4197, 0.4258, 0.4180, 0.4177 |
| selectivity | 0.7500 | 0.6300 | 0.8400 | 0.7914 | 0.7897, 0.8013, 0.8003, 0.7930, 0.7728 |
| yield | 0.7300 | 0.5900 | 0.8400 | 0.7661 | 0.7599, 0.7589, 0.7746, 0.7647, 0.7722 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6800 | 0.4800 | 0.8600 | 0.8675 | 0.8672, 0.8797, 0.8595, 0.8702, 0.8611 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9944 | 0.9863, 1.0000, 0.9939, 0.9952, 0.9966 |
| safety_risk | 0.3500 | 0.2500 | 0.4800 | 0.2766 | 0.2766, 0.2766, 0.2766, 0.2766, 0.2766 |
| score | 0.0500 | 0.0000 | 0.2100 | 0.0157 | 0.0080, 0.0161, 0.0181, 0.0189, 0.0174 |
| selectivity | 0.3200 | 0.1400 | 0.5200 | 0.1642 | 0.1513, 0.1625, 0.1614, 0.1705, 0.1754 |
| yield | 0.3200 | 0.1400 | 0.5200 | 0.1666 | 0.1574, 0.1674, 0.1745, 0.1706, 0.1633 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1600 | 0.0800 | 0.2700 | 0.4095 | 0.4077, 0.4061, 0.4111, 0.4131, 0.4099 |
| conversion | 0.6900 | 0.5000 | 0.8300 | 0.8332 | 0.8312, 0.8310, 0.8387, 0.8337, 0.8316 |
| safety_risk | 0.1100 | 0.0700 | 0.1700 | 0.1425 | 0.1425, 0.1425, 0.1425, 0.1425, 0.1425 |
| score | 0.3200 | 0.2200 | 0.4200 | 0.2864 | 0.2824, 0.2871, 0.2854, 0.2868, 0.2905 |
| selectivity | 0.7700 | 0.6700 | 0.8500 | 0.5133 | 0.5031, 0.5128, 0.5051, 0.5121, 0.5337 |
| yield | 0.5300 | 0.3900 | 0.6500 | 0.4276 | 0.4245, 0.4302, 0.4290, 0.4291, 0.4254 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8500 | 0.6500 | 0.9700 | 0.7282 | 0.7218, 0.7240, 0.7313, 0.7302, 0.7337 |
| conversion | 1.0000 | 0.9600 | 1.0000 | 0.9965 | 1.0000, 0.9919, 1.0000, 1.0000, 0.9907 |
| safety_risk | 0.5200 | 0.3800 | 0.7200 | 0.4363 | 0.4363, 0.4363, 0.4363, 0.4363, 0.4363 |
| score | 0.0000 | 0.0000 | 0.0900 | 0.0498 | 0.0537, 0.0446, 0.0465, 0.0489, 0.0551 |
| selectivity | 0.1500 | 0.0400 | 0.3400 | 0.2795 | 0.2971, 0.2653, 0.2673, 0.2764, 0.2912 |
| yield | 0.1500 | 0.0400 | 0.3400 | 0.2719 | 0.2700, 0.2689, 0.2704, 0.2708, 0.2794 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2400 | 0.1300 | 0.3700 | 0.4184 | 0.4194, 0.4145, 0.4188, 0.4197, 0.4197 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9928 | 0.9971, 1.0000, 0.9906, 0.9925, 0.9836 |
| safety_risk | 0.1400 | 0.0900 | 0.2000 | 0.1442 | 0.1442, 0.1442, 0.1442, 0.1442, 0.1442 |
| score | 0.4300 | 0.3400 | 0.5000 | 0.3581 | 0.3580, 0.3569, 0.3566, 0.3613, 0.3579 |
| selectivity | 0.7600 | 0.6600 | 0.8400 | 0.5934 | 0.5896, 0.5947, 0.5866, 0.6035, 0.5928 |
| yield | 0.7500 | 0.6400 | 0.8400 | 0.5909 | 0.5920, 0.5851, 0.5918, 0.5926, 0.5930 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8700 | 0.6900 | 0.9800 | 0.7445 | 0.7388, 0.7527, 0.7424, 0.7462, 0.7422 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9968 | 0.9985, 0.9993, 1.0000, 0.9924, 0.9936 |
| safety_risk | 0.6200 | 0.4600 | 0.8200 | 0.4367 | 0.4367, 0.4367, 0.4367, 0.4367, 0.4367 |
| score | 0.0000 | 0.0000 | 0.0600 | 0.0264 | 0.0286, 0.0246, 0.0267, 0.0239, 0.0283 |
| selectivity | 0.1300 | 0.0300 | 0.2900 | 0.2798 | 0.2745, 0.2727, 0.2802, 0.2749, 0.2966 |
| yield | 0.1300 | 0.0300 | 0.2900 | 0.2857 | 0.2940, 0.2849, 0.2854, 0.2835, 0.2808 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4600 | 0.3000 | 0.6400 | 0.6057 | 0.6253, 0.6067, 0.5983, 0.5999, 0.5984 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9992 | 1.0000, 1.0000, 0.9973, 1.0000, 0.9986 |
| safety_risk | 0.2500 | 0.1800 | 0.3400 | 0.2770 | 0.2770, 0.2770, 0.2770, 0.2770, 0.2770 |
| score | 0.2400 | 0.1100 | 0.3600 | 0.1944 | 0.1933, 0.1986, 0.1912, 0.1959, 0.1929 |
| selectivity | 0.5400 | 0.3600 | 0.6900 | 0.4029 | 0.4000, 0.4142, 0.3995, 0.4034, 0.3976 |
| yield | 0.5400 | 0.3600 | 0.6900 | 0.4116 | 0.4105, 0.4149, 0.4062, 0.4149, 0.4113 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4600 | 0.3000 | 0.6400 | 0.6042 | 0.6019, 0.6084, 0.6143, 0.5968, 0.5997 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9984 | 1.0000, 0.9989, 0.9932, 1.0000, 1.0000 |
| safety_risk | 0.2000 | 0.1300 | 0.2800 | 0.1480 | 0.1480, 0.1480, 0.1480, 0.1480, 0.1480 |
| score | 0.2600 | 0.1400 | 0.3800 | 0.2470 | 0.2512, 0.2477, 0.2453, 0.2458, 0.2452 |
| selectivity | 0.5400 | 0.3600 | 0.6900 | 0.4078 | 0.4094, 0.4099, 0.4019, 0.4050, 0.4126 |
| yield | 0.5400 | 0.3600 | 0.6900 | 0.4036 | 0.4126, 0.4037, 0.4043, 0.4019, 0.3957 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3100 | 0.1700 | 0.4700 | 0.6571 | 0.6562, 0.6608, 0.6647, 0.6504, 0.6535 |
| conversion | 1.0000 | 0.9500 | 1.0000 | 0.9983 | 1.0000, 1.0000, 1.0000, 0.9978, 0.9939 |
| safety_risk | 0.1600 | 0.1000 | 0.2300 | 0.1435 | 0.1435, 0.1435, 0.1435, 0.1435, 0.1435 |
| score | 0.3800 | 0.2700 | 0.4700 | 0.2115 | 0.2165, 0.2075, 0.2108, 0.2113, 0.2114 |
| selectivity | 0.6900 | 0.5400 | 0.8000 | 0.3493 | 0.3619, 0.3389, 0.3456, 0.3487, 0.3513 |
| yield | 0.6900 | 0.5400 | 0.8000 | 0.3529 | 0.3571, 0.3490, 0.3530, 0.3529, 0.3525 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4500 | 0.2700 | 0.6500 | 0.2829 | 0.2739, 0.3016, 0.2847, 0.2771, 0.2769 |
| conversion | 1.0000 | 0.9500 | 1.0000 | 0.9872 | 0.9900, 0.9898, 0.9852, 0.9794, 0.9916 |
| safety_risk | 0.3000 | 0.2100 | 0.4200 | 0.4375 | 0.4375, 0.4375, 0.4375, 0.4375, 0.4375 |
| score | 0.2200 | 0.0800 | 0.3600 | 0.3230 | 0.3291, 0.3202, 0.3270, 0.3198, 0.3191 |
| selectivity | 0.5500 | 0.3500 | 0.7200 | 0.7109 | 0.7179, 0.6994, 0.7261, 0.7010, 0.7101 |
| yield | 0.5500 | 0.3500 | 0.7200 | 0.7129 | 0.7230, 0.7125, 0.7138, 0.7129, 0.7025 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2485 | 0.2423 | -0.0061 |
| conversion | 0.9128 | 0.9205 | 0.0077 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1322 | 0.1203 | -0.0119 |
| safety_risk | 0.2095 | 0.2095 | 0.0000 |
| score | 0.3552 | 0.3484 | -0.0068 |
| selectivity | 0.7426 | 0.7337 | -0.0089 |
| virtual_spectrum_summary | 0.1961 | 0.1874 | -0.0087 |
| yield | 0.6813 | 0.6680 | -0.0133 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
