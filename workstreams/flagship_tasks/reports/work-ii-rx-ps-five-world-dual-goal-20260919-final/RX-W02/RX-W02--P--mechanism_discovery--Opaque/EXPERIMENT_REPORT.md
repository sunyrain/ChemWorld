# RX-W02--P--mechanism_discovery--Opaque

## Run summary

- World: `RX-W02`
- Locus: `P`
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

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `5`
- Rationale: Batch 5 gave the highest observed final score and target yield among the tested conditions while remaining comfortably below the safety limit; it also provides a clean 7200 s Catalyst B/water operating point before the longer-time selectivity loss seen in Batch 11.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2197 | 0.6200 | 0.3810 | 0.1597 | 0.0159 | 0.1074 | 0.1326 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.3509 | 0.5548 | 0.6222 | 0.2744 | 0.0326 | 0.1246 | 0.1852 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 310 K x 7200 s @ 600 rpm | no | 0.1744 | 0.5109 | 0.3479 | 0.1695 | 0.0097 | 0.0967 | 0.0887 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 410 K x 1800 s @ 600 rpm | no | 0.2580 | 0.6701 | 0.3734 | 0.1290 | 0.0189 | 0.2159 | 0.1109 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.3956 | 0.5880 | 0.6425 | 0.2738 | 0.0916 | 0.1299 | 0.2110 |
| 6 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.3424 | 0.5966 | 0.5827 | 0.2524 | 0.0882 | 0.1251 | 0.1881 |
| 7 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.3318 | 0.5479 | 0.6048 | 0.2812 | 0.0748 | 0.1236 | 0.1745 |
| 8 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.3518 | 0.4829 | 0.7294 | 0.3725 | 0.1046 | 0.1539 | 0.1651 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.3483 | 0.4681 | 0.7405 | 0.4098 | 0.1732 | 0.1742 | 0.1520 |
| 10 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.3666 | 0.4800 | 0.7679 | 0.4088 | 0.1396 | 0.1866 | 0.1595 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 7200 s @ 600 rpm → 350 K x 7200 s @ 600 rpm | no | 0.3900 | 0.4338 | 0.8691 | 0.4930 | 0.2523 | 0.1446 | 0.1863 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | yes | 0.3728 | 0.6038 | 0.6432 | 0.2598 | 0.0911 | 0.1232 | 0.2090 |

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
    "byproduct_signal": 0.15966244041919708,
    "conversion": 0.3809926509857178,
    "cost": 1.0,
    "degradation_warning": 0.015945635735988617,
    "safety_risk": 0.10744091123342514,
    "score": 0.13261742889881134,
    "selectivity": 0.6199578642845154,
    "virtual_spectrum_summary": 0.09498988091945648,
    "yield": 0.21969273686408997
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
      "catalyst": 0,
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
    "byproduct_signal": 0.2744125723838806,
    "conversion": 0.6222435235977173,
    "cost": 1.0,
    "degradation_warning": 0.03262026607990265,
    "safety_risk": 0.12460010498762131,
    "score": 0.18520967662334442,
    "selectivity": 0.5547580718994141,
    "virtual_spectrum_summary": 0.1656060367822647,
    "yield": 0.3509146273136139
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.16952158510684967,
    "conversion": 0.3478633761405945,
    "cost": 1.0,
    "degradation_warning": 0.009655303321778774,
    "safety_risk": 0.09673486649990082,
    "score": 0.08873384445905685,
    "selectivity": 0.510917067527771,
    "virtual_spectrum_summary": 0.09758175909519196,
    "yield": 0.17437231540679932
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.12896564602851868,
    "conversion": 0.3733978867530823,
    "cost": 1.0,
    "degradation_warning": 0.01889919675886631,
    "safety_risk": 0.2158617228269577,
    "score": 0.11090785264968872,
    "selectivity": 0.6700697541236877,
    "virtual_spectrum_summary": 0.07943574339151382,
    "yield": 0.25797101855278015
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
    "byproduct_signal": 0.2737865447998047,
    "conversion": 0.6425002217292786,
    "cost": 1.0,
    "degradation_warning": 0.09155740588903427,
    "safety_risk": 0.12990990281105042,
    "score": 0.21101760864257812,
    "selectivity": 0.5880085825920105,
    "virtual_spectrum_summary": 0.19178342819213867,
    "yield": 0.39556223154067993
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
    "byproduct_signal": 0.2523803412914276,
    "conversion": 0.5826772451400757,
    "cost": 1.0,
    "degradation_warning": 0.08824454993009567,
    "safety_risk": 0.1250932663679123,
    "score": 0.18809394538402557,
    "selectivity": 0.596587598323822,
    "virtual_spectrum_summary": 0.17851923406124115,
    "yield": 0.3424282371997833
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
    "byproduct_signal": 0.2812485694885254,
    "conversion": 0.6047674417495728,
    "cost": 1.0,
    "degradation_warning": 0.07483772188425064,
    "safety_risk": 0.12362637370824814,
    "score": 0.17452767491340637,
    "selectivity": 0.5478867888450623,
    "virtual_spectrum_summary": 0.1883636862039566,
    "yield": 0.33177775144577026
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
    "byproduct_signal": 0.372530460357666,
    "conversion": 0.7293748259544373,
    "cost": 1.0,
    "degradation_warning": 0.10455738753080368,
    "safety_risk": 0.1538717895746231,
    "score": 0.1651485711336136,
    "selectivity": 0.4829082190990448,
    "virtual_spectrum_summary": 0.25194257497787476,
    "yield": 0.3518158495426178
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
    "byproduct_signal": 0.40981513261795044,
    "conversion": 0.7405049800872803,
    "cost": 1.0,
    "degradation_warning": 0.17322899401187897,
    "safety_risk": 0.1741504818201065,
    "score": 0.15203283727169037,
    "selectivity": 0.4680773913860321,
    "virtual_spectrum_summary": 0.30335137248039246,
    "yield": 0.34832674264907837
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
    "byproduct_signal": 0.4088094234466553,
    "conversion": 0.7678958773612976,
    "cost": 1.0,
    "degradation_warning": 0.139634370803833,
    "safety_risk": 0.18661417067050934,
    "score": 0.15946733951568604,
    "selectivity": 0.4799816906452179,
    "virtual_spectrum_summary": 0.28768065571784973,
    "yield": 0.36664676666259766
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
      "duration_s": 7200,
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
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.49298617243766785,
    "conversion": 0.8690680861473083,
    "cost": 1.0,
    "degradation_warning": 0.25225797295570374,
    "safety_risk": 0.1445952206850052,
    "score": 0.18627791106700897,
    "selectivity": 0.4337512254714966,
    "virtual_spectrum_summary": 0.38465848565101624,
    "yield": 0.39000287652015686
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
  "end_step": 86,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.25976356863975525,
    "conversion": 0.6431794762611389,
    "cost": 1.0,
    "degradation_warning": 0.09112571179866791,
    "safety_risk": 0.12316843867301941,
    "score": 0.2089877873659134,
    "selectivity": 0.6038258075714111,
    "virtual_spectrum_summary": 0.18387652933597565,
    "yield": 0.37284794449806213
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This account is based only on the 12 completed synthetic-benchmark batches. All numerical outcomes below are public observations, not reconstructed hidden concentrations. Catalysts are anonymous formulations A–D, and the named solvents have calibrated categorical effects in this world; their real-world chemical properties should not be used to infer a named reaction or catalyst identity.

Each batch used 0.040 mol reagent, 0.005 mol catalyst, and 0.080 L solvent. Unless noted otherwise, stirring was 600 rpm. Every batch received one intermediate HPLC measurement and a final assay after termination. Consequently, small differences between an intermediate HPLC result and a final assay can reflect both process evolution and independent measurement noise.

2. Proposed process structure

The simplest explanation consistent with the campaign is a catalytic network with at least two competing routes:

R -> P  (desired target formation)
R -> B  (competing conversion/byproduct formation)
P -> D  (secondary loss or degradation, especially at long residence time)

A useful phenomenological model is:

dR/dt = -a(t)[kP(T,catalyst,solvent) + kB(T,catalyst,solvent)]R

dP/dt = a(t)kP(T,catalyst,solvent)R - kD(T,solvent)P

dB/dt = a(t)kB(T,catalyst,solvent)R + fB kD(T,solvent)P

da/dt = -kd(T,solvent)a

Here R is unconverted reagent, P is target, B is the measured competing-product pool, D denotes degradation products, and a(t) is effective catalyst activity. This is an explanatory family rather than an identified rate law: the data do not establish reaction orders, whether B is one compound, or whether catalyst deactivation is truly first order.

Temperature should be represented by the actual thermal history rather than simply the requested set point. A first-order heating approximation such as dT/dt = (Tset - T)/tau is plausible. The observed temperature increases were about 49.16 K during the nominal 350 K experiments, 11.69 K in Batch 3 at a 310 K request, and 99.17 K during Batch 4 at a 410 K request. Thus the vessels did not instantaneously occupy the set-point temperature, and Batch 4 apparently remained roughly 10 K below its requested target at the end. Rate constants would normally be represented locally by Arrhenius-like relations, ki(T) = Ai exp(-Ei/RT), but the campaign is insufficient to estimate Ai and Ei separately.

The principal qualitative coupling is that temperature, solvent, catalyst, and residence time affect both total conversion and the branching between P and B. Increasing conversion is not equivalent to increasing useful yield. Long exposure also increases the degradation channel and safety burden.

3. Temperature and residence-time evidence

Batches 1–4 used Catalyst A in water.

Batch 1, nominally 350 K for 3600 s, ended with final conversion 0.3810, yield 0.2197, selectivity 0.6200, byproduct signal 0.1597, degradation warning 0.01595, and safety risk 0.1074.

Batch 2 extended the same nominal condition to 7200 s. Final conversion rose to 0.6222 and yield to 0.3509, while selectivity fell to 0.5548 and byproduct signal rose to 0.2744. Degradation warning was 0.03262 and risk 0.1246. This establishes continued target formation between 1 and 2 hours, but also an increasing competing fraction.

Batch 3 used a 310 K request for 7200 s. It produced only 0.3479 conversion and 0.1744 yield, with selectivity 0.5109 and byproduct signal 0.1695. This is strong evidence that the useful reaction is thermally activated over this range. The lower selectivity also shows that low temperature does not simply suppress the competing route more strongly than the target route.

Batch 4 used a 410 K request for only 1800 s and experienced a temperature increase of 99.17 K. It reached conversion 0.3734 and yield 0.2580, with the highest Catalyst-A selectivity, 0.6701. Thus high temperature greatly accelerated target formation on this shorter time scale. However, safety risk rose to 0.2159, versus 0.0967–0.1246 in Batches 1–3. The comparison is confounded by duration and incomplete attainment of the requested temperature, so it does not identify an activation energy. It does show a steep safety-temperature coupling.

The clearest evidence for late-time competition is Batch 11, using Catalyst B in water at nominal 350 K for two consecutive 7200 s heating periods. At 7200 s, HPLC reported conversion 0.6516, yield 0.3859, selectivity 0.5983, and byproduct signal 0.2613. After 14400 s, the final assay reported conversion 0.8691 but yield only 0.3900; selectivity had fallen to 0.4338, byproduct signal had risen to 0.4930, and degradation warning had risen to 0.2523. The roughly 0.218 increase in conversion produced almost no net increase in target yield. Therefore, after about 7200 s under this condition, additional reaction is dominated by byproduct/degradation chemistry.

This late behavior can be explained by depletion of R into a slower but less selective regime, by preferential deactivation of the target-forming catalytic state, or by secondary conversion of P. The nearly flat observed yield combined with sharply increasing byproduct and degradation signals is compatible with a combination of residual R -> B and P -> D. It does not uniquely demonstrate catalyst deactivation.

4. Catalyst effects

Batches 2 and 5–7 compared catalysts in water at nominal 350 K for 7200 s:

Catalyst A, Batch 2: conversion 0.6222, yield 0.3509, selectivity 0.5548, byproduct 0.2744, degradation 0.03262.
Catalyst B, Batch 5: conversion 0.6425, yield 0.3956, selectivity 0.5880, byproduct 0.2738, degradation 0.09156.
Catalyst C, Batch 6: conversion 0.5827, yield 0.3424, selectivity 0.5966, byproduct 0.2524, degradation 0.08824.
Catalyst D, Batch 7: conversion 0.6048, yield 0.3318, selectivity 0.5479, byproduct 0.2812, degradation 0.07484.

Catalyst B gave the largest target yield and conversion in this comparison. Catalyst C gave slightly higher reported selectivity and the lowest byproduct signal, but at lower conversion and yield. Catalyst D was least attractive for target yield. Catalyst A had a notably lower degradation warning than B–D, although a single replicate per catalyst prevents separating a catalyst-specific degradation effect from batch and assay variation.

The data support catalyst-dependent activity and branching factors rather than a simple universal rate multiplier. If catalysts only scaled all rates equally, their selectivities at matched conversion and time would be expected to be more similar. Nevertheless, the catalyst differences are modest enough that quantitative rankings other than the observed Batch-5 optimum should be treated cautiously.

5. Solvent effects

Batches 5 and 8–10 used Catalyst B at nominal 350 K for 7200 s:

Water, Batch 5: conversion 0.6425, yield 0.3956, selectivity 0.5880, byproduct 0.2738, degradation 0.09156.
Ethanol, Batch 8: conversion 0.7294, yield 0.3518, selectivity 0.4829, byproduct 0.3725, degradation 0.1046.
Acetonitrile, Batch 9: conversion 0.7405, yield 0.3483, selectivity 0.4681, byproduct 0.4098, degradation 0.1732.
Toluene, Batch 10: conversion 0.7679, yield 0.3666, selectivity 0.4800, byproduct 0.4088, degradation 0.1396.

The nonaqueous solvents increased total conversion relative to water but reduced selectivity and did not increase target yield. Toluene gave the highest conversion, yet its yield remained below the water result because much more material entered the competing pool. Acetonitrile had the largest degradation warning in this series. Therefore, the solvent acts on pathway partitioning, not merely on a common overall rate. In model terms, ethanol, acetonitrile, and toluene appear to increase kB relative to kP, or increase kD, even if they also increase the overall disappearance rate of R.

Because the benchmark defines solvent effects categorically, this evidence should not be extrapolated to polarity, proticity, boiling point, or any specific real chemical mechanism.

6. Quench and termination

Batch 12 repeated the Catalyst-B/water/350 K/7200 s condition but quenched before the intermediate HPLC measurement and termination. The quench lowered temperature by 45 K over 58.36 s and reduced the instantaneous reported risk by 0.00674. Its final assay gave conversion 0.6432, yield 0.3728, selectivity 0.6038, byproduct 0.2598, degradation 0.09113, and risk 0.1232.

The matched unquenched Batch 5 gave conversion 0.6425, yield 0.3956, selectivity 0.5880, byproduct 0.2738, degradation 0.09156, and risk 0.1299. The near-identical conversion and degradation warning imply that quenching mainly halted further evolution and reduced thermal risk rather than reversing chemistry. Batch 12 had somewhat better final selectivity and lower byproduct, but lower final yield. With only one run per condition and independent assay noise, this is not decisive evidence of a chemical selectivity benefit. It does support prompt quenching as a control action near the chosen endpoint, especially if physical handling continues before termination.

The post-quench HPLC in Batch 12 reported conversion 0.6532, yield 0.3859, selectivity 0.5719, and byproduct 0.3019, whereas its later final assay gave the values above. Those differences demonstrate why small HPLC-to-final changes should not automatically be interpreted as real post-quench chemistry.

7. Practical predictive account

Within the tested domain, I would predict outcomes using a staged rule:

1. Propagate the actual temperature trajectory rather than assuming immediate set-point attainment.
2. During early heating, advance both target and competing conversion with temperature-, catalyst-, and solvent-specific rates.
3. Reduce remaining R as conversion grows.
4. Allow target accumulation to approach a plateau near 7200 s under Catalyst B/water/350 K conditions.
5. Beyond that point, allocate most additional conversion to B and degradation, causing selectivity to fall sharply.
6. On quench, sharply reduce all thermal rates and the safety contribution; do not assume any recovery of lost target.

A parsimonious local recommendation from the scientific evidence is Catalyst B in water, heated toward 350 K for about 7200 s, followed by prompt quench/termination. Batch 5 was selected because it had the best observed final score, 0.2110, and the highest final target yield among the principal 7200 s comparisons, 0.3956, while risk remained 0.1299, well below the 0.35 limit. The recommendation is an observed optimum over the tested grid, not proof of a global optimum.

8. Limits of identification and competing explanations

Only one final replicate was obtained for each designed condition. Instrument noise and batch variability therefore limit fine distinctions, especially between Batches 5 and 12 or between catalyst selectivities.

The measurements expose aggregate conversion, target yield/selectivity, byproduct signal, and degradation warning, but not species identities or concentrations. Parallel R -> B, sequential P -> D, and multiple hidden byproducts cannot be separated uniquely.

Catalyst deactivation was not directly measured. The Batch-11 target plateau may instead arise from substrate depletion, reversible target formation, product inhibition, a changing thermal state, or preferential consumption of a reactive reagent subpopulation.

No isothermal time series within a single batch was obtained beyond the Batch-11 midpoint/final pair. Therefore, reaction orders, equilibrium constants, Arrhenius parameters, heat-transfer constants, and catalyst-deactivation constants are not identifiable.

The high-temperature result is informative but not directly comparable with the 7200 s experiments because Batch 4 ran for only 1800 s and did not fully reach its 410 K request. Predictions close to 470 K, below 310 K, or at substantially different heating rates would be extrapolations.

All experiments used the same reagent amount, catalyst loading, solvent volume, and stirring rate. Concentration effects, catalyst-loading order, mass-transfer limitations, and stirring-speed dependence remain untested.

A reversible reaction R <-> P followed by irreversible R -> B is a reasonable competitor to the degradation model. It could also produce a target plateau while conversion continues. However, the large degradation warning and byproduct increase in Batch 11 make explicit late degradation or changing pathway selectivity more plausible than a purely reversible two-state process.

Overall, the most defensible account is a thermally activated, catalyst- and solvent-dependent competitive network with useful target formation early, progressively unfavorable branching at long residence time, and a separate steep temperature dependence of safety risk. The exact microscopic mechanism remains unidentified.

## Q — Blind predictions

### Overall rationale

The predictions use the competitive-network interpretation developed from the campaign: thermally activated target and byproduct formation, followed at long or hot exposure by target loss and increasingly unfavorable pathway partitioning. Catalyst B and acetonitrile were anchored to Batch 9, while temperature and time responses were informed by Batches 1–4 and the late-time transition in Batch 11. Quench adjustments were kept small because Batches 5 and 12 showed nearly unchanged conversion and degradation, with only modest risk and selectivity differences. Intervals include final-assay noise, batch variability, uncertain thermal ramping, the higher catalyst-to-reagent ratio and concentration in these queries, and substantial extrapolation above the studied Catalyst-B/acetonitrile temperature. Score estimates follow the public behavior inferred from the completed campaign, approximately score = -0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion - 0.45·safety_risk, with the lower boundary respected.

### Q01

Catalyst B and acetonitrile should produce high conversion at 420 K, but the elevated temperature and 3300 s exposure should favor competing conversion and degradation. This is an extrapolation above the directly studied Catalyst-B/acetonitrile condition.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.4000 | 0.6200 |
| conversion | 0.8600 | 0.7600 | 0.9400 |
| safety_risk | 0.3100 | 0.2500 | 0.3800 |
| score | 0.1090 | 0.0400 | 0.1800 |
| selectivity | 0.4400 | 0.3400 | 0.5400 |
| yield | 0.3800 | 0.2900 | 0.4600 |

### Q02

The quench should leave conversion essentially unchanged while slightly limiting post-heating competition and lowering final thermal risk. The expected chemical benefit is modest because termination follows immediately and the prior quench comparison was noisy.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4800 | 0.3800 | 0.6000 |
| conversion | 0.8600 | 0.7600 | 0.9400 |
| safety_risk | 0.2900 | 0.2300 | 0.3500 |
| score | 0.1230 | 0.0500 | 0.2000 |
| selectivity | 0.4550 | 0.3500 | 0.5600 |
| yield | 0.3850 | 0.2950 | 0.4700 |

### Q03

At 390 K, conversion should be lower than at 420 K, but pathway partitioning should be more favorable. The predicted yield therefore remains near the Q01 yield despite lower conversion, with substantially less byproduct and risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3400 | 0.2500 | 0.4500 |
| conversion | 0.7000 | 0.5900 | 0.8000 |
| safety_risk | 0.2200 | 0.1700 | 0.2800 |
| score | 0.1450 | 0.0800 | 0.2200 |
| selectivity | 0.5200 | 0.4300 | 0.6100 |
| yield | 0.3600 | 0.2900 | 0.4300 |

### Q04

The 450 K exposure should drive nearly complete conversion but also severe competing conversion and a safety-limit exceedance. The score is expected to be at or near its lower boundary despite appreciable target formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6800 | 0.5600 | 0.8200 |
| conversion | 0.9500 | 0.8900 | 0.9900 |
| safety_risk | 0.4200 | 0.3400 | 0.5100 |
| score | 0.0010 | 0.0000 | 0.0800 |
| selectivity | 0.3000 | 0.1800 | 0.4300 |
| yield | 0.3000 | 0.1700 | 0.4100 |

### Q05

Shortening the 420 K hold should preserve selectivity and suppress byproduct formation, although conversion will be incomplete because a meaningful fraction of the 1500 s period is spent heating toward the set point.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2500 | 0.1600 | 0.3600 |
| conversion | 0.5500 | 0.4100 | 0.6800 |
| safety_risk | 0.2500 | 0.2000 | 0.3100 |
| score | 0.1160 | 0.0500 | 0.1800 |
| selectivity | 0.5800 | 0.4800 | 0.6800 |
| yield | 0.3200 | 0.2400 | 0.3900 |

### Q06

The long 420 K treatment should enter the late regime observed in Batch 11: conversion continues toward completion while target yield plateaus or declines and byproduct formation dominates. Risk is predicted near the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6900 | 0.5600 | 0.8200 |
| conversion | 0.9500 | 0.9000 | 0.9900 |
| safety_risk | 0.3400 | 0.2800 | 0.4200 |
| score | 0.0350 | 0.0000 | 0.1200 |
| selectivity | 0.2900 | 0.1700 | 0.4200 |
| yield | 0.3000 | 0.1800 | 0.4100 |

### Q07

The initial 390 K phase should form target before the second 450 K phase drives rapid completion. Because already formed target is then exposed to the hottest segment, secondary loss and byproduct formation are expected to be substantial.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4500 | 0.7200 |
| conversion | 0.9000 | 0.8100 | 0.9600 |
| safety_risk | 0.3600 | 0.2900 | 0.4500 |
| score | 0.0670 | 0.0000 | 0.1500 |
| selectivity | 0.3800 | 0.2500 | 0.5100 |
| yield | 0.3600 | 0.2400 | 0.4600 |

### Q08

Heating first to 450 K should create rapid early conversion, while the subsequent 390 K segment should be less destructive than ending with the high-temperature phase. Possible early catalyst deactivation makes both the conversion and the order advantage uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.3800 | 0.6400 |
| conversion | 0.8700 | 0.7800 | 0.9400 |
| safety_risk | 0.3000 | 0.2400 | 0.3800 |
| score | 0.1120 | 0.0300 | 0.1900 |
| selectivity | 0.4300 | 0.3100 | 0.5500 |
| yield | 0.3800 | 0.2700 | 0.4700 |

### Q09

The short 440 K treatment should achieve moderate-to-high conversion with better selectivity than the longer high-temperature cases. Its risk remains elevated because the requested temperature is well above the studied 350 K Catalyst-B/acetonitrile condition.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3200 | 0.2100 | 0.4400 |
| conversion | 0.6500 | 0.5100 | 0.7700 |
| safety_risk | 0.3100 | 0.2500 | 0.3800 |
| score | 0.1020 | 0.0300 | 0.1800 |
| selectivity | 0.5300 | 0.4200 | 0.6400 |
| yield | 0.3600 | 0.2700 | 0.4400 |

### Q10

Relative to Q09, quenching should principally reduce final thermal risk and halt residual hot-state reaction. Conversion should be unchanged, with only a small expected improvement in selectivity and byproduct signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.2000 | 0.4200 |
| conversion | 0.6500 | 0.5100 | 0.7700 |
| safety_risk | 0.2900 | 0.2300 | 0.3600 |
| score | 0.1160 | 0.0400 | 0.1900 |
| selectivity | 0.5400 | 0.4300 | 0.6500 |
| yield | 0.3650 | 0.2750 | 0.4500 |

### Q11

The 370 K condition combines a relatively long residence time with a milder temperature. It should reach substantial conversion without the extreme degradation expected above 420 K, giving one of the better score predictions in this set.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3700 | 0.2700 | 0.4800 |
| conversion | 0.7200 | 0.6100 | 0.8200 |
| safety_risk | 0.2100 | 0.1600 | 0.2700 |
| score | 0.1510 | 0.0800 | 0.2200 |
| selectivity | 0.5000 | 0.4100 | 0.5900 |
| yield | 0.3700 | 0.3000 | 0.4400 |

### Q12

This is the strongest extrapolation: 460 K for 6300 s should exhaust nearly all reagent but heavily degrade or divert the target. A large safety-limit violation and a score at the lower boundary are expected.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8800 | 0.7200 | 0.9700 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.5000 | 0.4000 | 0.6200 |
| score | 0.0000 | 0.0000 | 0.0500 |
| selectivity | 0.1200 | 0.0300 | 0.2700 |
| yield | 0.1400 | 0.0300 | 0.3000 |

## K2 — Retrospective analysis

1. Assessment of claims in the initial information

The initial material packet deliberately supplied almost no substantive mechanistic claim. It stated that the catalysts were anonymous benchmark formulations, that solvent effects were categorical benchmark effects rather than predictions from real solvent properties, and that no task-specific nominal property dossier was available. Thus there was no proposed reaction mechanism, catalyst ranking, activation law, or optimum condition to confirm or refute.

Several operational claims were supported. Catalyst and solvent identities did affect the outcomes: at the matched water/350 K/7200 s condition, Batches 2 and 5–7 differed by catalyst, while Batches 5 and 8–10 showed large solvent-dependent changes. The warning not to infer behavior from real solvent properties also remained appropriate. The experiments established only empirical categorical rankings; they did not show that polarity, proticity, or any real molecular property caused those rankings.

The stated partial-observation and noise limitations were also borne out. For example, Batch 12 gave an intermediate HPLC yield of 0.3859 and a final-assay yield of 0.3728, while its byproduct estimates changed from 0.3019 to 0.2598. Such differences limited interpretation of small apparent process changes.

The initial safety limit of 0.35 was not challenged by the completed campaign: all observed batches stayed below it, including Batch 4 at risk 0.2159. That is only an absence of counterevidence within the tested domain, not proof that the limit could not be exceeded under hotter or longer conditions.

There was no substantive initial claim for which clear counterevidence appeared and was knowingly ignored. A different issue is that I initially acted as if equal, maximum recipe allocations were a sensible neutral design. That was my unvalidated design convention, not a claim in the supplied information. The campaign never tested whether 0.040 mol reagent, 0.005 mol catalyst, and 0.080 L solvent were mechanistically preferable or kinetically well behaved.

2. Experiments that formed or changed the interpretation

Batch 1 established the first baseline for Catalyst A in water at nominal 350 K for 3600 s. Its conversion of 0.3810, yield of 0.2197, and selectivity of 0.6200 supplied the initial evidence for simultaneous target and byproduct formation.

Batch 2 genuinely changed the time interpretation. Doubling the nominal hold to 7200 s increased conversion to 0.6222 and yield to 0.3509, but reduced selectivity to 0.5548 and raised byproduct signal to 0.2744. That result motivated the view that additional conversion becomes progressively less useful.

Batches 3 and 4 formed the temperature interpretation. Batch 3 at a 310 K request gave only 0.3479 conversion after 7200 s, while Batch 4 at a 410 K request gave 0.3734 conversion and 0.2580 yield after only 1800 s. Batch 4 also raised risk to 0.2159. These observations motivated the claims that useful formation is thermally activated and that safety has a strong temperature coupling. They did not justify a numerical Arrhenius law because time and actual temperature history were confounded.

Batches 5–7 produced the catalyst ranking. Batch 5, Catalyst B, gave the highest target yield in that matched comparison, 0.3956. Catalyst C in Batch 6 had slightly higher reported selectivity, 0.5966 versus 0.5880, but lower conversion and yield. These results changed the campaign from broad catalyst screening to using Catalyst B for the solvent study.

Batches 8–10 changed the solvent interpretation. Ethanol, acetonitrile, and toluene all increased conversion relative to water but decreased selectivity and failed to improve yield. The clearest example was Batch 10: toluene produced conversion 0.7679 but yield only 0.3666, below the water result in Batch 5. This supported solvent-dependent pathway partitioning rather than a single common rate multiplier.

Batch 11 was the strongest mechanistic experiment. From its 7200 s HPLC observation to its 14400 s final assay, conversion increased from 0.6516 to 0.8691, yet yield changed only from 0.3859 to 0.3900. Meanwhile byproduct signal rose from 0.2613 to 0.4930 and degradation warning reached 0.2523. This caused me to emphasize a late competing/degradation regime and to reject any simple model in which longer time monotonically increases useful target in proportion to conversion.

Batch 12 informed the quench interpretation but did not establish a strong causal chemical benefit. Relative to Batch 5, it had nearly identical conversion and degradation warning, with modestly higher selectivity, lower byproduct, and lower yield. I therefore treated quenching primarily as a way to stop further hot-state evolution and modestly lower risk.

Some choices were based mainly on the initial resource structure rather than prior evidence: using equal maximum material allocations, one intermediate HPLC measurement per batch, and a common 600 rpm stirring speed. The initial temperature and time grid was a reasoned but unvalidated guess. Later choices were more data-driven: Catalyst B was selected after Batches 5–7, and Batch 11 was explicitly motivated by the apparent time-dependent selectivity loss. Choosing only a single run per condition was driven by coverage and resource allocation, not by evidence that process variability was negligible.

3. Most important competing mechanisms

The sealed report favored a competitive network with parallel R→P and R→B routes, possible secondary P→D loss, and optional catalyst deactivation. The most important competing explanations are:

(a) Parallel competition plus secondary target degradation. Under this account, P forms early and is later converted into degradation products or contributes to the byproduct pool.

(b) Parallel competition without target degradation. Remaining R may simply enter an increasingly dominant R→B route as R is depleted or the reactive mixture changes. Batch 11 can fit this mechanism because target yield remained approximately constant rather than clearly decreasing.

(c) Catalyst-state evolution or selective deactivation. A target-selective catalytic state may deactivate faster than a less selective state, causing late conversion to favor B. The sealed report explicitly said that Batch 11 did not uniquely demonstrate deactivation.

(d) Product inhibition, substrate heterogeneity, or reversible R↔P behavior followed by irreversible R→B. These alternatives can also produce a target plateau while total conversion continues.

(e) Apparent kinetics created partly by thermal history. The requested set point was not the actual temperature throughout a hold. Batch 4, for example, increased by about 99.17 K rather than simply existing at 410 K for 1800 s. Differences attributed to chemical kinetics could partly reflect heating and cooling trajectories.

(f) Measurement and latent-species aggregation. “Byproduct signal” and “degradation warning” need not represent single species. Some HPLC-to-final differences can be measurement variation rather than actual chemistry.

The experiments can distinguish a constant-selectivity, single-pathway model from a time-varying competitive process: Batches 2 and 11 clearly contradict simple proportional accumulation of target with conversion. They also distinguish a solvent-independent common multiplier from solvent-dependent branching because Batches 5 and 8–10 changed selectivity substantially.

They cannot distinguish whether Batch 11’s late byproduct came from residual R or from P. They cannot identify catalyst deactivation separately from product inhibition, substrate depletion, or a change in branching with conversion. They also cannot estimate unique reaction orders, activation energies, or equilibrium constants. The sealed report acknowledged these non-identifiabilities, but its differential equations were illustrative rather than fitted or uniquely supported.

4. One additional complete experiment

I would run Catalyst B in water with the same starting recipe as Batch 11, heat toward 350 K for 7200 s, obtain an HPLC measurement, add a fresh catalyst aliquot, then heat for another 7200 s, terminate, and obtain the final assay. The added amount would have to remain within the legal per-action and available-stock limits; if a full 0.005 mol redose were legal, that would provide the strongest perturbation.

The diagnostic target would be selective catalyst deactivation. Batch 11 already supplies the closest no-redose comparator.

If fresh catalyst caused a renewed increase in target yield substantially beyond the approximately 0.390 plateau, with selectivity recovering and without a disproportionate byproduct increase, that would support loss of target-forming catalyst activity as an important late limitation.

If fresh catalyst increased conversion but almost exclusively increased byproduct and degradation while target remained near the Batch-11 plateau, that would argue against simple global deactivation. It would favor substrate-state evolution, target degradation, or intrinsically unfavorable branching at high conversion.

If the redose produced almost no additional conversion, substrate depletion, product inhibition, equilibrium, or severe irreversible catalyst poisoning would become more plausible. The result would still not distinguish those possibilities fully.

If the first 7200 s observation failed to reproduce the Batch-5/Batch-11 neighborhood, that would reveal process variability and weaken all fine mechanistic comparisons before the redose was interpreted.

This experiment would not by itself prove that P degrades. A species-resolved or labeled experiment would be better for that question, but such an operation or instrument was not available in the public contract.

5. Tradeoff between identifiability and operational score

The campaign mixed screening, mechanism probing, and optimization. Batches 3 and 4 sacrificed likely score to explore temperature response. Batch 3 gave a score of only 0.0887, and Batch 4 gave 0.1109 with higher risk, but together they were important for identifying thermal sensitivity. Batch 11 also sacrificed score and selectivity by extending the reaction to 14400 s; its score was 0.1863 rather than exceeding Batch 5, but it provided the strongest evidence for the late competing regime.

Conversely, after Batch 5 emerged as strong, using Catalyst B for Batches 8–10 served both optimization and mechanism screening. However, the solvent screen held time and temperature fixed and used no replicates. That favored broad coverage over precise identification of solvent effects.

Batch 12 was partly an operational refinement of the best observed region. It tested whether a quench could preserve performance and reduce risk. This leaned more toward robust operation than toward identifying a microscopic pathway.

Several choices sacrificed identifiability for campaign breadth: no replicated factorial center point, no catalyst-loading series, no reagent-concentration series, no stirring comparison, and only one intermediate measurement in each batch. Equal use of all four catalysts and all four solvents improved categorical coverage but left insufficient batches for robust kinetic parameter estimation.

There was also some optimization sacrifice for identification. The low-temperature, high-temperature, and very long-duration experiments were not chosen because they were expected to maximize score. That was appropriate because the primary research goal emphasized an explanatory and predictive account, with safe score explicitly secondary.

Still, the design did not fully capitalize on that goal. A more identification-focused campaign would have included repeated center points, a structured time series, matched two-stage temperature-order experiments, and a catalyst-loading perturbation. My design was closer to an adaptive screening campaign than a statistically efficient mechanism-discrimination design.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts and spectra were not inspected. I relied on processed estimates, thereby leaving potentially useful peak structure, calibration flags, replicate information, and missingness metadata unused. This was a significant missed opportunity because aggregate byproduct and degradation channels could conceal multiple species.

The actual thermal evidence was also underused. I recorded endpoint temperature changes, such as 49.16 K in the nominal 350 K experiments and 99.17 K in Batch 4, but did not fit even a provisional heat-transfer model. Consequently, the blind predictions treated requested temperature too directly and only qualitatively allowed for ramping.

Intermediate HPLC versus final-assay discrepancies were difficult to exploit because they mixed elapsed process changes with different instruments and independent noise. Batch 12 illustrated this problem clearly. I correctly warned against treating every difference as chemistry, but I did not quantitatively propagate the instrument-specific uncertainties.

Safety-risk trajectories, physical-cost changes, and the quench temperature drop were not incorporated into a calibrated dynamic safety model. Likewise, all campaign experiments used the same concentration, catalyst loading, and stirring speed, whereas the blind queries used a smaller volume, higher reagent concentration, a higher catalyst-to-reagent ratio, and 400 rather than 600 rpm. K1 mentioned those extrapolations but did not model them.

The least reliable blind predictions were Q12, Q04, and Q06. Q12 extrapolated to 460 K for 6300 s, far outside the directly studied Catalyst-B/acetonitrile condition; its conversion interval of 0.95–1.00 and score interval of 0–0.05 were probably too narrow. Q04 at 450 K for 3300 s and Q06 at 420 K for 5100 s similarly depended on an uncalibrated degradation law and an assumed score floor.

Q07 and Q08 were also highly uncertain because K1 assigned an order effect—low-then-high versus high-then-low—without any matched order experiment in the campaign. The rationale that Q08 should be less destructive was mechanistically plausible but unvalidated. Their selectivity, yield, safety-risk, and score intervals should have been wider and more overlapping.

The quench-pair predictions Q01/Q02 and Q09/Q10 may have implied more systematic chemical improvement than the evidence justified. Batch 12 supported a modest risk reduction, but its yield was lower than the unquenched Batch 5 result. The point shifts in K1 were therefore speculative.

The score relation used in K1 reproduced the observed campaign scores extremely closely: approximately -0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion - 0.45·safety risk. Even so, uncertainty in the predicted inputs should have produced broader score intervals, particularly near a presumed lower boundary. Treating the fitted relation as stable outside the observed risk and temperature domain added unacknowledged structural uncertainty.

These weaknesses are partly consistent with K1’s stated caveats: it explicitly identified substantial extrapolation, uncertain thermal ramping, different concentration and catalyst ratio, and path dependence. However, several numerical intervals—especially Q12 conversion and score, Q04 score, and the separation between Q07 and Q08—were narrower than those caveats warranted. Thus the prose acknowledged more uncertainty than the numbers consistently represented.

7. Limitations of the sealed recommendation

Batch 5 was the sample-best observed operation, not a proven optimum. It gave the highest observed final score, 0.2110, and yield 0.3956 among the completed batches, but Batch 12’s score of 0.2090 was extremely close. With one replicate per condition and assay noise, the apparent difference is not persuasive evidence that unquenched Batch 5 is truly superior.

The recommendation was local to one recipe scale, concentration, catalyst loading, stirring rate, solvent category, and benchmark world. The campaign did not determine whether 7200 s was the exact best stopping time; it only showed that 3600 s was less converted and 14400 s had entered an unfavorable regime. An optimum could lie anywhere between or near those points.

Repeatability should first be tested with independent exact replicates of Batch 5 and Batch 12, including identical intermediate and final assays. Replication would estimate process variance, reveal whether Catalyst B’s apparent advantage is stable, and determine whether the small quench differences are real.

Local robustness should then be tested around the recommendation with a compact design varying temperature, time, and catalyst loading—for example, temperatures near 340–360 K and stopping times around 5400–9000 s—while retaining a replicated center point. Small deliberate changes in reagent concentration and stirring speed would test whether the operating region is flat or fragile. Measuring actual temperature histories would be essential.

Cross-material robustness would require repeating the local design with at least Catalyst C, which showed similar selectivity but lower yield, and with at least one nonaqueous solvent. The existing solvent data warn that increased conversion may conceal poorer pathway partitioning.

Cross-world generalization is especially limited. The supplied packet explicitly described categorical benchmark couplings and anonymous catalysts. Nothing in the campaign establishes that the Catalyst-B/water ranking transfers to a different hidden world, a real catalyst, or a real named synthesis. Validation in another world would require new experiments rather than mechanistic analogy from solvent identities.

Accordingly, the sealed recommendation should be read as: “best observed completed batch within this 12-run campaign, with acceptable observed safety.” It should not be read as “globally optimal,” “statistically superior,” “mechanistically unique,” or “portable across materials and worlds.”

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 80.5 | none | 0 |
| Q | yes | 0 | 137.3 | none | 0 |
| K2 | yes | 0 | 101.5 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1035 | 0.6500 | 0.2333 | 0.3449 |
| conversion | 0.0725 | 0.8333 | 0.1767 | 0.2287 |
| safety_risk | 0.0657 | 0.6667 | 0.1392 | 0.2978 |
| score | 0.1537 | 0.0833 | 0.1300 | 0.9490 |
| selectivity | 0.1503 | 0.1667 | 0.2208 | 0.6423 |
| yield | 0.1582 | 0.0833 | 0.1900 | 0.8673 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.4000 | 0.6200 | 0.3836 | 0.3734, 0.3868, 0.3803, 0.3950, 0.3827 |
| conversion | 0.8600 | 0.7600 | 0.9400 | 0.9113 | 0.9157, 0.9053, 0.9151, 0.9099, 0.9105 |
| safety_risk | 0.3100 | 0.2500 | 0.3800 | 0.2966 | 0.2966, 0.2966, 0.2966, 0.2966, 0.2966 |
| score | 0.1090 | 0.0400 | 0.1800 | 0.2601 | 0.2571, 0.2614, 0.2573, 0.2593, 0.2654 |
| selectivity | 0.4400 | 0.3400 | 0.5400 | 0.5841 | 0.5840, 0.5757, 0.5727, 0.5924, 0.5958 |
| yield | 0.3800 | 0.2900 | 0.4600 | 0.5362 | 0.5276, 0.5462, 0.5353, 0.5293, 0.5424 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4800 | 0.3800 | 0.6000 | 0.3906 | 0.3930, 0.3884, 0.3893, 0.3965, 0.3858 |
| conversion | 0.8600 | 0.7600 | 0.9400 | 0.9175 | 0.9113, 0.9188, 0.9132, 0.9228, 0.9215 |
| safety_risk | 0.2900 | 0.2300 | 0.3500 | 0.1501 | 0.1501, 0.1501, 0.1501, 0.1501, 0.1501 |
| score | 0.1230 | 0.0500 | 0.2000 | 0.3248 | 0.3234, 0.3233, 0.3237, 0.3251, 0.3287 |
| selectivity | 0.4550 | 0.3500 | 0.5600 | 0.5911 | 0.5892, 0.5834, 0.5943, 0.5979, 0.5907 |
| yield | 0.3850 | 0.2950 | 0.4700 | 0.5358 | 0.5348, 0.5365, 0.5320, 0.5309, 0.5446 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3400 | 0.2500 | 0.4500 | 0.3087 | 0.3157, 0.3089, 0.3085, 0.3032, 0.3072 |
| conversion | 0.7000 | 0.5900 | 0.8000 | 0.8036 | 0.7933, 0.8122, 0.8088, 0.8086, 0.7952 |
| safety_risk | 0.2200 | 0.1700 | 0.2800 | 0.1838 | 0.1838, 0.1838, 0.1838, 0.1838, 0.1838 |
| score | 0.1450 | 0.0800 | 0.2200 | 0.3023 | 0.3041, 0.3097, 0.2897, 0.3038, 0.3041 |
| selectivity | 0.5200 | 0.4300 | 0.6100 | 0.6337 | 0.6380, 0.6422, 0.6027, 0.6458, 0.6397 |
| yield | 0.3600 | 0.2900 | 0.4300 | 0.5108 | 0.5151, 0.5219, 0.4974, 0.5057, 0.5138 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6800 | 0.5600 | 0.8200 | 0.4622 | 0.4734, 0.4523, 0.4509, 0.4650, 0.4696 |
| conversion | 0.9500 | 0.8900 | 0.9900 | 0.9697 | 0.9792, 0.9558, 0.9587, 0.9743, 0.9804 |
| safety_risk | 0.4200 | 0.3400 | 0.5100 | 0.4024 | 0.4024, 0.4024, 0.4024, 0.4024, 0.4024 |
| score | 0.0010 | 0.0000 | 0.0800 | 0.1963 | 0.1952, 0.1920, 0.1963, 0.1963, 0.2014 |
| selectivity | 0.3000 | 0.1800 | 0.4300 | 0.5321 | 0.5351, 0.5235, 0.5294, 0.5198, 0.5527 |
| yield | 0.3000 | 0.1700 | 0.4100 | 0.5136 | 0.5068, 0.5119, 0.5182, 0.5203, 0.5110 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2500 | 0.1600 | 0.3600 | 0.1829 | 0.1707, 0.1919, 0.1797, 0.1931, 0.1789 |
| conversion | 0.5500 | 0.4100 | 0.6800 | 0.6703 | 0.6578, 0.6772, 0.6781, 0.6645, 0.6737 |
| safety_risk | 0.2500 | 0.2000 | 0.3100 | 0.2954 | 0.2954, 0.2954, 0.2954, 0.2954, 0.2954 |
| score | 0.1160 | 0.0500 | 0.1800 | 0.2593 | 0.2598, 0.2599, 0.2612, 0.2568, 0.2586 |
| selectivity | 0.5800 | 0.4800 | 0.6800 | 0.7357 | 0.7407, 0.7348, 0.7392, 0.7342, 0.7294 |
| yield | 0.3200 | 0.2400 | 0.3900 | 0.4946 | 0.4960, 0.4951, 0.4951, 0.4907, 0.4959 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6900 | 0.5600 | 0.8200 | 0.5573 | 0.5538, 0.5681, 0.5640, 0.5472, 0.5532 |
| conversion | 0.9500 | 0.9000 | 0.9900 | 0.9768 | 0.9686, 0.9802, 0.9791, 0.9727, 0.9834 |
| safety_risk | 0.3400 | 0.2800 | 0.4200 | 0.2966 | 0.2966, 0.2966, 0.2966, 0.2966, 0.2966 |
| score | 0.0350 | 0.0000 | 0.1200 | 0.1909 | 0.1909, 0.1912, 0.1921, 0.1841, 0.1962 |
| selectivity | 0.2900 | 0.1700 | 0.4200 | 0.4482 | 0.4519, 0.4443, 0.4502, 0.4383, 0.4562 |
| yield | 0.3000 | 0.1800 | 0.4100 | 0.4356 | 0.4353, 0.4379, 0.4368, 0.4258, 0.4422 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.4500 | 0.7200 | 0.4398 | 0.4380, 0.4368, 0.4499, 0.4299, 0.4443 |
| conversion | 0.9000 | 0.8100 | 0.9600 | 0.9511 | 0.9415, 0.9511, 0.9583, 0.9525, 0.9519 |
| safety_risk | 0.3600 | 0.2900 | 0.4500 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.0670 | 0.0000 | 0.1500 | 0.1956 | 0.1920, 0.1982, 0.1914, 0.2003, 0.1961 |
| selectivity | 0.3800 | 0.2500 | 0.5100 | 0.5529 | 0.5496, 0.5581, 0.5368, 0.5640, 0.5560 |
| yield | 0.3600 | 0.2400 | 0.4600 | 0.5315 | 0.5270, 0.5349, 0.5292, 0.5359, 0.5307 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.3800 | 0.6400 | 0.4319 | 0.4283, 0.4399, 0.4231, 0.4256, 0.4425 |
| conversion | 0.8700 | 0.7800 | 0.9400 | 0.9366 | 0.9327, 0.9364, 0.9484, 0.9279, 0.9377 |
| safety_risk | 0.3000 | 0.2400 | 0.3800 | 0.1966 | 0.1966, 0.1966, 0.1966, 0.1966, 0.1966 |
| score | 0.1120 | 0.0300 | 0.1900 | 0.2902 | 0.2934, 0.2889, 0.2888, 0.2910, 0.2891 |
| selectivity | 0.4300 | 0.3100 | 0.5500 | 0.5541 | 0.5686, 0.5514, 0.5495, 0.5630, 0.5378 |
| yield | 0.3800 | 0.2700 | 0.4700 | 0.5122 | 0.5120, 0.5106, 0.5083, 0.5107, 0.5192 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3200 | 0.2100 | 0.4400 | 0.2066 | 0.2146, 0.2032, 0.2027, 0.2104, 0.2020 |
| conversion | 0.6500 | 0.5100 | 0.7700 | 0.7555 | 0.7568, 0.7444, 0.7700, 0.7602, 0.7463 |
| safety_risk | 0.3100 | 0.2500 | 0.3800 | 0.3753 | 0.3753, 0.3753, 0.3753, 0.3753, 0.3753 |
| score | 0.1020 | 0.0300 | 0.1800 | 0.2530 | 0.2504, 0.2538, 0.2518, 0.2541, 0.2548 |
| selectivity | 0.5300 | 0.4200 | 0.6400 | 0.7259 | 0.7192, 0.7384, 0.7148, 0.7205, 0.7365 |
| yield | 0.3600 | 0.2700 | 0.4400 | 0.5536 | 0.5509, 0.5506, 0.5539, 0.5587, 0.5538 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3000 | 0.2000 | 0.4200 | 0.2116 | 0.2138, 0.2015, 0.2046, 0.2200, 0.2179 |
| conversion | 0.6500 | 0.5100 | 0.7700 | 0.7544 | 0.7531, 0.7604, 0.7467, 0.7581, 0.7538 |
| safety_risk | 0.2900 | 0.2300 | 0.3600 | 0.1695 | 0.1695, 0.1695, 0.1695, 0.1695, 0.1695 |
| score | 0.1160 | 0.0400 | 0.1900 | 0.3429 | 0.3416, 0.3388, 0.3404, 0.3465, 0.3473 |
| selectivity | 0.5400 | 0.4300 | 0.6500 | 0.7322 | 0.7342, 0.7219, 0.7184, 0.7429, 0.7436 |
| yield | 0.3650 | 0.2750 | 0.4500 | 0.5516 | 0.5475, 0.5462, 0.5558, 0.5529, 0.5557 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3700 | 0.2700 | 0.4800 | 0.4180 | 0.4080, 0.4208, 0.4177, 0.4150, 0.4286 |
| conversion | 0.7200 | 0.6100 | 0.8200 | 0.8748 | 0.8749, 0.8864, 0.8724, 0.8680, 0.8722 |
| safety_risk | 0.2100 | 0.1600 | 0.2700 | 0.1534 | 0.1534, 0.1534, 0.1534, 0.1534, 0.1534 |
| score | 0.1510 | 0.0800 | 0.2200 | 0.2774 | 0.2781, 0.2806, 0.2751, 0.2802, 0.2733 |
| selectivity | 0.5000 | 0.4100 | 0.5900 | 0.5286 | 0.5273, 0.5329, 0.5317, 0.5379, 0.5132 |
| yield | 0.3700 | 0.3000 | 0.4400 | 0.4673 | 0.4696, 0.4696, 0.4601, 0.4701, 0.4671 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8800 | 0.7200 | 0.9700 | 0.7513 | 0.7441, 0.7519, 0.7528, 0.7701, 0.7379 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9990 | 0.9998, 1.0000, 1.0000, 1.0000, 0.9950 |
| safety_risk | 0.5000 | 0.4000 | 0.6200 | 0.4196 | 0.4196, 0.4196, 0.4196, 0.4196, 0.4196 |
| score | 0.0000 | 0.0000 | 0.0500 | 0.0284 | 0.0287, 0.0254, 0.0296, 0.0336, 0.0248 |
| selectivity | 0.1200 | 0.0300 | 0.2700 | 0.2706 | 0.2657, 0.2678, 0.2706, 0.2778, 0.2710 |
| yield | 0.1400 | 0.0300 | 0.3000 | 0.2757 | 0.2792, 0.2696, 0.2784, 0.2839, 0.2674 |

## Recommendation retest

- Selected source batch: `5`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2738 | 0.2730 | -0.0007 |
| conversion | 0.6425 | 0.6457 | 0.0032 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.0916 | 0.1030 | 0.0115 |
| safety_risk | 0.1299 | 0.1299 | 0.0000 |
| score | 0.2110 | 0.2059 | -0.0052 |
| selectivity | 0.5880 | 0.5751 | -0.0129 |
| virtual_spectrum_summary | 0.1918 | 0.1965 | 0.0048 |
| yield | 0.3956 | 0.3899 | -0.0056 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
