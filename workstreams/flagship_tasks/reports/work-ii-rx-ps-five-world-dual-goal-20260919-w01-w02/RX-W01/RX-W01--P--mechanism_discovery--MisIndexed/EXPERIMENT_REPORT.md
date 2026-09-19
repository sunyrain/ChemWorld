# RX-W01--P--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W01`
- Locus: `P`
- Goal: `mechanism_discovery`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay: `{'checked_steps': 85, 'max_abs_error': 0.0, 'mismatches': [], 'verified': True}`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `2`
- Rationale: The 420 K, 1800 s Catalyst B/acetonitrile batch gave the highest observed target yield and selectivity while remaining below the safety limit, avoiding the degradation seen at longer residence times.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | no | 0.6702 | 0.6755 | 0.9878 | 0.3236 | 0.2248 | 0.2832 | 0.3422 |
| 2 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K × 1800 s @ 400 rpm | no | 0.7161 | 0.7851 | 0.9000 | 0.1913 | 0.1082 | 0.2829 | 0.3806 |
| 3 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K × 5400 s @ 400 rpm | no | 0.5349 | 0.5282 | 0.9834 | 0.4636 | 0.3937 | 0.2830 | 0.2492 |
| 4 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 390 K × 3300 s @ 400 rpm | no | 0.6832 | 0.7173 | 0.9165 | 0.2586 | 0.1728 | 0.1809 | 0.3967 |
| 5 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 440 K × 3300 s @ 400 rpm | no | 0.6548 | 0.6546 | 0.9973 | 0.3637 | 0.2721 | 0.3629 | 0.2959 |
| 6 | S2 (0.0050 L) | 0.003000 mol | C0 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | no | 0.6499 | 0.6848 | 0.9437 | 0.2902 | 0.0888 | 0.2826 | 0.3533 |
| 7 | S2 (0.0050 L) | 0.003000 mol | C2 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | no | 0.6598 | 0.6994 | 0.9305 | 0.2933 | 0.1194 | 0.2827 | 0.3511 |
| 8 | S2 (0.0050 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | no | 0.6036 | 0.6274 | 0.9704 | 0.3951 | 0.2923 | 0.2830 | 0.2935 |
| 9 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | no | 0.6205 | 0.7263 | 0.8689 | 0.2444 | 0.1097 | 0.2410 | 0.3427 |
| 10 | S1 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | no | 0.6615 | 0.7033 | 0.9363 | 0.3038 | 0.1565 | 0.2648 | 0.3491 |
| 11 | S3 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | no | 0.6638 | 0.6827 | 0.9711 | 0.3274 | 0.1784 | 0.2957 | 0.3344 |
| 12 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K × 3300 s @ 400 rpm | yes | 0.6736 | 0.6959 | 0.9823 | 0.3135 | 0.2376 | 0.1492 | 0.4051 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

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
      "stirring_speed_rpm": 400,
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
    "byproduct_signal": 0.3235764503479004,
    "conversion": 0.9877637624740601,
    "cost": 0.6608999967575073,
    "degradation_warning": 0.22480729222297668,
    "safety_risk": 0.28322550654411316,
    "score": 0.34218618273735046,
    "selectivity": 0.6755287647247314,
    "virtual_spectrum_summary": 0.27913033962249756,
    "yield": 0.6701726913452148
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
    "byproduct_signal": 0.19133742153644562,
    "conversion": 0.90003502368927,
    "cost": 0.6484000086784363,
    "degradation_warning": 0.10822692513465881,
    "safety_risk": 0.28292572498321533,
    "score": 0.3805687725543976,
    "selectivity": 0.7850905060768127,
    "virtual_spectrum_summary": 0.1539376974105835,
    "yield": 0.7161230444908142
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
    "byproduct_signal": 0.4636225402355194,
    "conversion": 0.9834161400794983,
    "cost": 0.6783999800682068,
    "degradation_warning": 0.39374056458473206,
    "safety_risk": 0.2830022871494293,
    "score": 0.24918098747730255,
    "selectivity": 0.5282079577445984,
    "virtual_spectrum_summary": 0.4321756362915039,
    "yield": 0.534946084022522
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
      "stirring_speed_rpm": 400,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2585923969745636,
    "conversion": 0.9164563417434692,
    "cost": 0.6608999967575073,
    "degradation_warning": 0.17284522950649261,
    "safety_risk": 0.18092088401317596,
    "score": 0.39673158526420593,
    "selectivity": 0.7173168063163757,
    "virtual_spectrum_summary": 0.22000618278980255,
    "yield": 0.6831528544425964
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 440
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
    "byproduct_signal": 0.3636617362499237,
    "conversion": 0.9973280429840088,
    "cost": 0.6608999967575073,
    "degradation_warning": 0.2720574140548706,
    "safety_risk": 0.362907737493515,
    "score": 0.2959153652191162,
    "selectivity": 0.6546180844306946,
    "virtual_spectrum_summary": 0.3224397897720337,
    "yield": 0.6548162698745728
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
    "byproduct_signal": 0.29020559787750244,
    "conversion": 0.9437437057495117,
    "cost": 0.45089998841285706,
    "degradation_warning": 0.08881454914808273,
    "safety_risk": 0.28256121277809143,
    "score": 0.3532867133617401,
    "selectivity": 0.6847822070121765,
    "virtual_spectrum_summary": 0.1995796263217926,
    "yield": 0.6498983502388
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
      "solvent": 2,
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
      "stirring_speed_rpm": 400,
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
    "byproduct_signal": 0.2932879626750946,
    "conversion": 0.9305024147033691,
    "cost": 0.5349000096321106,
    "degradation_warning": 0.1193680390715599,
    "safety_risk": 0.28271013498306274,
    "score": 0.35114213824272156,
    "selectivity": 0.6994484663009644,
    "virtual_spectrum_summary": 0.21502399444580078,
    "yield": 0.6598483324050903
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
      "stirring_speed_rpm": 400,
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3951321244239807,
    "conversion": 0.9703781604766846,
    "cost": 0.7448999881744385,
    "degradation_warning": 0.2923316955566406,
    "safety_risk": 0.28300872445106506,
    "score": 0.29348859190940857,
    "selectivity": 0.6274209022521973,
    "virtual_spectrum_summary": 0.34887194633483887,
    "yield": 0.6035987138748169
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
      "stirring_speed_rpm": 400,
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.24440813064575195,
    "conversion": 0.868940532207489,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.10971502214670181,
    "safety_risk": 0.24096040427684784,
    "score": 0.3426681458950043,
    "selectivity": 0.726253092288971,
    "virtual_spectrum_summary": 0.1837962418794632,
    "yield": 0.6205325126647949
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
      "stirring_speed_rpm": 400,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3037784993648529,
    "conversion": 0.9362525939941406,
    "cost": 0.6577000021934509,
    "degradation_warning": 0.1565348505973816,
    "safety_risk": 0.26482757925987244,
    "score": 0.3491086959838867,
    "selectivity": 0.703342616558075,
    "virtual_spectrum_summary": 0.23751886188983917,
    "yield": 0.6614754796028137
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
      "stirring_speed_rpm": 400,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3274328410625458,
    "conversion": 0.971145510673523,
    "cost": 0.6589000225067139,
    "degradation_warning": 0.17837557196617126,
    "safety_risk": 0.2956642806529999,
    "score": 0.3343675434589386,
    "selectivity": 0.68268221616745,
    "virtual_spectrum_summary": 0.2603570818901062,
    "yield": 0.6638034582138062
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.31352484226226807,
    "conversion": 0.9822528958320618,
    "cost": 0.6940852403640747,
    "degradation_warning": 0.23759466409683228,
    "safety_risk": 0.14922666549682617,
    "score": 0.4050978422164917,
    "selectivity": 0.6958975791931152,
    "virtual_spectrum_summary": 0.2793562710285187,
    "yield": 0.6736466884613037
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and experimental basis

I completed 12 batches using 0.003 mol reagent, 0.000525 mol catalyst, 0.005 L solvent, and 400 rpm in every batch. Thus, the explored recipe had a nominal reagent concentration of 0.60 mol/L and a catalyst-to-reagent ratio of 0.175. The controlled factors were heating temperature, heating duration, catalyst identity, solvent identity, and whether the mixture was quenched after heating. Each batch received one in-process HPLC measurement and one final assay. The instruments report synthetic public observables rather than identified molecular species, so the terms reactant, target, byproduct, and degradation product below are mechanistic roles, not chemical identities.

The strongest conclusion is that the system is not governed by a single irreversible conversion directly to stable target. Conversion can remain very high while target yield and selectivity fall sharply with prolonged or hotter treatment. The data are most consistent with desired target formation accompanied by competing conversion and subsequent loss of target or a target-forming intermediate.

2. Minimal explanatory mechanism

A useful minimal network is:

R -> P                         desired pathway
R -> B                         parallel undesired conversion
P -> D                         secondary degradation or overreaction

Here R is the limiting reagent, P is the measured target, B is a primary competing product, and D represents one or more secondary degradation products. A catalyst-dependent active fraction, a(t), may multiply the formation rates and may itself decline during exposure.

One possible kinetic representation is:

dR/dt = -a(t)[kP(T,c,s) + kB(T,c,s)]R

dP/dt = a(t)kP(T,c,s)R - kD(T,c,s)P

dB/dt = a(t)kB(T,c,s)R + fB kD(T,c,s)P

dD/dt = (1-fB)kD(T,c,s)P

da/dt = -kdeact(T,c,s)a

where c and s denote catalyst and solvent categories. A conventional but unverified temperature dependence would be k_j = A_j,c,s exp[-E_j/(RT)]. The observations imply that the undesired terms, especially kD and possibly kB, become important with cumulative thermal exposure. Catalyst deactivation is plausible but is not required to explain the final results; the available data do not distinguish deactivation from substrate depletion, reversible intermediate accumulation, or changing pathway selectivity.

The measured quantities can be approximately interpreted as:

conversion ≈ 1 - R/R0

yield ≈ P/R0

selectivity ≈ P/(R0-R)

The numerical relation yield ≈ conversion × selectivity is reasonably close in many batches. For example, batch 2 gave conversion 0.9000 and selectivity 0.7851, whose product is about 0.707, compared with measured yield 0.7161. The discrepancy is compatible with measurement/process noise and the fact that the channels may not have identical calibration definitions. Byproduct signal broadly rises as selectivity falls, while degradation warning appears to be a partially independent indicator of thermally accumulated damage.

3. Evidence from residence time

The time series using Catalyst B in acetonitrile at a 420 K setpoint is the most diagnostic evidence.

Batch 2, heated for 1800 s, gave final conversion 0.9000, yield 0.7161, selectivity 0.7851, byproduct signal 0.1913, and degradation warning 0.1082. This was the highest final target yield and selectivity observed.

Batch 1, heated for 3300 s under the same nominal formulation, gave conversion 0.9878, yield 0.6702, selectivity 0.6755, byproduct signal 0.3236, and degradation warning 0.2248.

Batch 3, heated for 5400 s, gave conversion 0.9834, yield 0.5349, selectivity 0.5282, byproduct signal 0.4636, and degradation warning 0.3937.

Thus, extending treatment from 1800 to 3300 s increased conversion toward completion but lowered target yield, and extending it to 5400 s produced little additional conversion while causing a large loss of yield and selectivity. The simultaneous increases in byproduct and degradation channels support secondary overreaction. A simple stable-product model, R -> P plus R -> B with constant rate ratios, would normally approach a fixed selectivity rather than show this pronounced decline after high conversion. The P -> D term, or an equivalent time-dependent deterioration of the productive pathway, is therefore important.

The exact yield maximum was not located. It lies plausibly near or somewhat before 1800 s at 420 K for this formulation, but that statement is an interpolation/extrapolation rather than an observation because no shorter-time batch was run.

4. Temperature dependence and thermal history

At 3300 s with Catalyst B and acetonitrile, lowering the setpoint to 390 K in batch 4 produced conversion 0.9165, yield 0.6832, selectivity 0.7173, byproduct 0.2586, degradation warning 0.1728, and safety risk 0.1809. The reported temperature change was 83.14 K.

The comparable 420 K batches produced reported temperature changes near 106.17 K and safety risk near 0.283. Their final yields were approximately 0.670-0.674, with selectivity approximately 0.676-0.696 and degradation warning approximately 0.225-0.238.

At a 440 K setpoint, batch 5 produced conversion 0.9973, yield 0.6548, selectivity 0.6546, byproduct 0.3637, degradation warning 0.2721, and safety risk 0.3629. Its reported temperature change was 120.67 K, and it exceeded the task safety limit of 0.35.

These observations imply that increasing temperature accelerates disappearance of reagent but does not monotonically improve target formation. Undesired formation or target degradation is more temperature-sensitive in the explored upper range. At a fixed 3300 s duration, 390 K gave a better final target balance and substantially lower risk than 420 or 440 K. The supplied incomplete prior claim that the higher-temperature side should retain safe balanced performance was therefore not supported at 440 K and should be restricted, at most, to a narrower region below that setting.

Only the setpoint, duration, and net reported temperature change were observed; no continuous temperature trace was measured. I therefore cannot separate heat-up time, true time at setpoint, thermal lag, or a possible reaction exotherm. A generic thermal model such as dT/dt = (Tset-T)/tau + Qreaction/(mCp) is plausible, but tau and Qreaction are unidentified. The close temperature changes among repeated 420 K operations suggest reproducible controller behavior, not proof of identical internal temperature histories.

5. Catalyst effects

Catalysts were compared in acetonitrile at 420 K for 3300 s.

Catalyst A, batch 6: conversion 0.9437, yield 0.6499, selectivity 0.6848, byproduct 0.2902, degradation warning 0.0888.

Catalyst B, batches 1 and 12: conversion 0.9878 and 0.9823; yield 0.6702 and 0.6736; selectivity 0.6755 and 0.6959; byproduct 0.3236 and 0.3135; degradation warning 0.2248 and 0.2376.

Catalyst C, batch 7: conversion 0.9305, yield 0.6598, selectivity 0.6994, byproduct 0.2933, degradation warning 0.1194.

Catalyst D, batch 8: conversion 0.9704, yield 0.6036, selectivity 0.6274, byproduct 0.3951, degradation warning 0.2923.

Catalyst B appears relatively active: it reaches high conversion and gives good yield, but at 3300 s it also accumulates appreciable degradation. Catalyst C gives lower conversion but slightly better selectivity and a lower degradation warning. Catalyst A has similar selectivity but lower yield and conversion, with the lowest degradation warning in this comparison. Catalyst D gives high conversion but the poorest yield/selectivity and the strongest byproduct/degradation response, suggesting that it accelerates undesired chemistry or generates a less selective active state.

These catalyst comparisons do not directly prove deactivation. Evidence for deactivation would require time-resolved catalyst activity, catalyst-loading variation, catalyst addition at different times, or reuse experiments. The current outcomes can equally be represented by fixed catalyst-specific values of kP, kB, and kD.

6. Solvent effects

Solvents were compared with Catalyst B at 420 K for 3300 s. Because the benchmark defines solvent effects categorically, I do not infer them from real-world polarity, boiling point, or other physical properties.

Water, batch 9: conversion 0.8689, yield 0.6205, selectivity 0.7263, byproduct 0.2444, degradation warning 0.1097, safety risk 0.2410.

Ethanol, batch 10: conversion 0.9363, yield 0.6615, selectivity 0.7033, byproduct 0.3038, degradation warning 0.1565, safety risk 0.2648.

Acetonitrile, batches 1 and 12: conversion approximately 0.982-0.988, yield approximately 0.670-0.674, selectivity approximately 0.676-0.696, byproduct approximately 0.314-0.324, degradation warning approximately 0.225-0.238, safety risk 0.2832.

Toluene, batch 11: conversion 0.9711, yield 0.6638, selectivity 0.6827, byproduct 0.3274, degradation warning 0.1784, safety risk 0.2957.

The solvent mainly appears to change effective activity, selectivity, degradation, and safety jointly. Water suppresses total conversion and yield but gives comparatively high selectivity, low byproduct/degradation signals, and low risk. Ethanol provides an intermediate compromise. Acetonitrile gives the highest conversion and slightly higher yield but more accumulated damage at 3300 s. Toluene also gives high conversion but no yield advantage and the highest solvent-comparison risk. These effects can be represented as solvent-specific multipliers on kP, kB, kD, and the thermal-risk function.

Because each non-acetonitrile solvent was tested only once and only with Catalyst B at one temperature and time, catalyst-solvent and solvent-temperature interactions remain unidentified.

7. Quench and termination

Batch 12 repeated the nominal batch-1 formulation and thermal program but was quenched after its in-process HPLC measurement and before termination. Immediately before quenching, HPLC reported conversion 0.9637, yield 0.6745, selectivity 0.6822, and byproduct 0.3107. The final assay reported conversion 0.9823, yield 0.6736, selectivity 0.6959, byproduct 0.3135, and degradation warning 0.2376.

Batch 1, which was terminated without the explicit quench, gave a similar final yield of 0.6702 and broadly similar signals. This suggests that a quench applied only after the full 3300 s exposure mainly freezes an already established composition; it does not reverse accumulated degradation. The differences between batches 1 and 12 are too small, and the design too weak, to assign a chemical quench effect separately from batch and instrument variability. The higher safe score in batch 12 is an observed operational outcome, but it should not be interpreted as proof of higher chemical yield.

An earlier quench near the productive maximum would plausibly prevent the loss seen between 1800 and 5400 s. That is a mechanistic extrapolation, not a tested result: batch 2 was terminated at 1800 s but was not explicitly quenched, and no matched early-quench pair was run.

8. Safety relationship

Within this fixed-scale study, safety risk depended strongly on thermal setting and also on solvent category. At 3300 s with Catalyst B/acetonitrile it rose from 0.1809 at 390 K to about 0.283 at 420 K and 0.3629 at 440 K. The 440 K batch crossed the 0.35 limit. At 420 K, the solvent series ranged from 0.2410 in water to 0.2957 in toluene. Catalyst substitutions at fixed charge and solvent had little visible effect on the reported risk compared with temperature and solvent.

A purely empirical local risk model could be written as:

risk = r0 + rT(T, exposure) + rsolvent(s) + rscale(charge, volume) + interactions.

Only a narrow slice of this function was measured. It would be unsafe to extrapolate linearly above 440 K, to larger reagent inventories, or to different volumes.

9. Model revision caused by the experiments

My initial working expectation was that higher temperature might preserve safe balanced performance near the supplied reference region. Batch 5 changed that view: 440 K increased conversion but reduced selectivity and crossed the safety limit. Batch 4 showed that 390 K could retain similar or better target yield with less degradation and much lower risk.

The time comparison caused the larger mechanistic revision. Batch 2 showed that the target is already near its observed optimum before full conversion. Batch 3 showed that prolonged reaction drives the system toward byproduct/degradation rather than more target. I therefore replaced a simple conversion-limited account with a formation-plus-secondary-loss account.

Catalyst D in batch 8 further demonstrated that high conversion is not evidence of productive catalysis. The solvent series reinforced the same conclusion: variables that raise conversion can simultaneously worsen byproduct formation, degradation, or safety.

10. Applicability and prediction rules

The model is best regarded as a local qualitative or semi-quantitative model for approximately 0.003 mol reagent, 0.000525 mol catalyst, 0.005 L solvent, 400 rpm, 390-440 K, and 1800-5400 s. Within that domain, I would use the following prediction logic:

- Increasing exposure from an under-reacted state initially raises conversion and target amount.
- Near the target maximum, additional conversion gives diminishing target benefit.
- Further thermal exposure lowers target yield and selectivity while increasing byproduct and degradation signals.
- Higher temperature compresses these stages in time and raises safety risk; it may move the optimum to a shorter duration.
- Catalyst identity changes both productive activity and undesired-pathway activity, not merely the overall rate.
- Solvent identity changes activity, selectivity, degradation tendency, and risk simultaneously.
- Quenching is useful primarily if applied before or near the target maximum; a late quench cannot recover degraded target.

The sealed recommended experiment, batch 2, is consistent with this account: Catalyst B/acetonitrile at 420 K for 1800 s gave the highest measured final yield and selectivity while remaining below the safety limit. This is an observed best point among the tested batches, not proof of a global optimum. Batch 4 at 390 K for 3300 s is an alternative lower-risk regime with slightly lower yield but better selectivity than the 3300 s 420 K batches.

11. Unidentified factors and competing explanations

Several important quantities remain unidentified: elementary reaction order, activation energies, equilibrium constants, catalyst active concentration, catalyst deactivation rate, induction time, heat-transfer time constant, actual continuous temperature history, and the molecular correspondence of the public instrument channels. Catalyst loading, reagent concentration, solvent volume, stirring speed, order of addition, and scale were not varied.

There are also reasonable competing explanations. The decline in target selectivity could arise from reversible target formation followed by equilibrium displacement, conversion of an unobserved intermediate into different products, time-dependent catalyst speciation, or instrument response changes, rather than direct degradation of P. A model with only parallel pathways but a changing catalyst state could mimic a P -> D model. Degradation warning supports accumulated thermal damage but does not identify its source. Likewise, byproduct signal may combine primary byproduct and degraded target.

Most factor levels lack replication. Batches 1 and 12 provide only an approximate repeat because their termination procedures differed. In-process HPLC and final-assay values are not interchangeable measurements and contain stated noise. Consequently, small differences—especially among Catalysts A-C or among 3300 s solvent outcomes—should not be treated as exact rankings. The large time and high-temperature effects are much more credible than those small contrasts.

Overall, the most economical account is a thermally accelerated, catalyst- and solvent-dependent competition between target formation, parallel byproduct formation, and cumulative target/intermediate degradation. Conversion alone is a misleading optimization variable; productive yield is maximized by stopping before prolonged high-temperature exposure, while safety imposes an additional upper-temperature constraint.

## Q — Blind predictions

### Overall rationale

Predictions use the local formation-plus-secondary-loss account developed from the campaign. Exact or near-exact repeats are anchored to observed batches; time points are interpolated using the strong 1800/3300/5400 s trend; temperature extrapolations assume productive and undesired rates both accelerate, with the undesired pathway more temperature-sensitive. Safety risk is treated mainly as a function of peak temperature under this fixed formulation. The 80% intervals combine final-assay noise, observed batch variability, and additional model uncertainty, especially for staged histories and conditions outside 390-440 K. Quenching is assumed to preserve composition at the time it is applied rather than reverse prior degradation.

### Q01

This exactly matches the principal 420 K, 3300 s Catalyst B/acetonitrile condition. The estimate pools the closely related observations from batches 1 and 12 while giving greater weight to unquenched batch 1 for the score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3190 | 0.2800 | 0.3600 |
| conversion | 0.9850 | 0.9600 | 1.0000 |
| safety_risk | 0.2830 | 0.2740 | 0.2920 |
| score | 0.3500 | 0.3100 | 0.3900 |
| selectivity | 0.6860 | 0.6400 | 0.7300 |
| yield | 0.6720 | 0.6400 | 0.7050 |

### Q02

This matches batch 12 apart from its negligible prior analytical sampling. A late quench should preserve approximately the composition already established at 3300 s. The higher score estimate reflects the observed operational advantage of the explicit quench, although its magnitude is uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3140 | 0.2750 | 0.3550 |
| conversion | 0.9820 | 0.9550 | 1.0000 |
| safety_risk | 0.2830 | 0.2740 | 0.2920 |
| score | 0.4050 | 0.3600 | 0.4500 |
| selectivity | 0.6960 | 0.6500 | 0.7400 |
| yield | 0.6740 | 0.6400 | 0.7100 |

### Q03

This is directly anchored by batch 4. Lower temperature reduced conversion relative to 420 K but also suppressed byproduct formation, degradation, and safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2590 | 0.2200 | 0.3000 |
| conversion | 0.9160 | 0.8800 | 0.9500 |
| safety_risk | 0.1810 | 0.1720 | 0.1900 |
| score | 0.3970 | 0.3600 | 0.4350 |
| selectivity | 0.7170 | 0.6750 | 0.7600 |
| yield | 0.6830 | 0.6500 | 0.7150 |

### Q04

This extrapolates 10 K above unsafe batch 5. Conversion should be effectively complete, but the more temperature-sensitive undesired pathway should further reduce yield and selectivity. The safety limit is very likely to be exceeded.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3950 | 0.3300 | 0.4700 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.4050 | 0.3850 | 0.4300 |
| score | 0.2350 | 0.1500 | 0.3200 |
| selectivity | 0.6250 | 0.5500 | 0.6900 |
| yield | 0.6250 | 0.5500 | 0.6900 |

### Q05

This is a modest interpolation below the 1800 s condition of batch 2. Less reagent should be converted, but selectivity should be higher because less target has undergone secondary degradation. The predicted yield is near, but slightly below, the observed 1800 s maximum.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1650 | 0.1100 | 0.2250 |
| conversion | 0.8550 | 0.7900 | 0.9100 |
| safety_risk | 0.2830 | 0.2740 | 0.2920 |
| score | 0.3750 | 0.3250 | 0.4250 |
| selectivity | 0.8150 | 0.7550 | 0.8700 |
| yield | 0.6950 | 0.6400 | 0.7400 |

### Q06

This interpolates between the 3300 s baseline and batch 3 at 5400 s. Conversion is already saturated, while continued exposure primarily increases byproduct and degradation at the expense of target.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4450 | 0.3900 | 0.5000 |
| conversion | 0.9840 | 0.9550 | 1.0000 |
| safety_risk | 0.2830 | 0.2740 | 0.2920 |
| score | 0.2600 | 0.2050 | 0.3150 |
| selectivity | 0.5500 | 0.4900 | 0.6100 |
| yield | 0.5550 | 0.5000 | 0.6100 |

### Q07

The combined exposure should nearly exhaust the reagent. Heating first at 390 K allows target to accumulate before the 450 K segment, so the final high-temperature period is expected to degrade an already substantial target pool. The 450 K excursion also makes the batch unsafe.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3850 | 0.3100 | 0.4700 |
| conversion | 0.9940 | 0.9600 | 1.0000 |
| safety_risk | 0.4050 | 0.3800 | 0.4350 |
| score | 0.2550 | 0.1600 | 0.3500 |
| selectivity | 0.6300 | 0.5400 | 0.7100 |
| yield | 0.6250 | 0.5300 | 0.7000 |

### Q08

The integrated conversion should resemble Q07, but sequence may matter. Placing the high-temperature segment first leaves the final 390 K segment less aggressive toward accumulated target, so I predict moderately better retention than in Q07. This order effect is mechanistic extrapolation and therefore has a wide interval.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3450 | 0.2700 | 0.4300 |
| conversion | 0.9940 | 0.9600 | 1.0000 |
| safety_risk | 0.4050 | 0.3800 | 0.4350 |
| score | 0.2850 | 0.1900 | 0.3800 |
| selectivity | 0.6650 | 0.5800 | 0.7450 |
| yield | 0.6550 | 0.5600 | 0.7300 |

### Q09

At 440 K, 1500 s should produce more conversion than the 420 K, 1500-1800 s region but also faster secondary loss. The yield is therefore predicted near the observed optimum, with lower selectivity and an unsafe risk level inherited from the high temperature.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2350 | 0.1700 | 0.3050 |
| conversion | 0.9300 | 0.8700 | 0.9700 |
| safety_risk | 0.3630 | 0.3520 | 0.3750 |
| score | 0.3100 | 0.2450 | 0.3750 |
| selectivity | 0.7450 | 0.6700 | 0.8100 |
| yield | 0.6950 | 0.6300 | 0.7500 |

### Q10

The late quench should leave chemical composition close to Q09 but prevent further post-heating change. Based on batch 12, I assign a possible operational score benefit without predicting a meaningful reduction in the peak safety risk already incurred at 440 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1650 | 0.3000 |
| conversion | 0.9300 | 0.8700 | 0.9700 |
| safety_risk | 0.3630 | 0.3520 | 0.3750 |
| score | 0.3650 | 0.2950 | 0.4350 |
| selectivity | 0.7500 | 0.6750 | 0.8150 |
| yield | 0.6970 | 0.6300 | 0.7550 |

### Q11

This is a substantial temperature extrapolation below the measured range. Long residence should still give high conversion, while the lower temperature should suppress degradation and risk. Uncertainty is wide because the balance between slow target formation and slow degradation was not directly measured at 370 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2350 | 0.1600 | 0.3200 |
| conversion | 0.9200 | 0.8300 | 0.9700 |
| safety_risk | 0.1300 | 0.1050 | 0.1600 |
| score | 0.4250 | 0.3400 | 0.5000 |
| selectivity | 0.7400 | 0.6500 | 0.8200 |
| yield | 0.6800 | 0.5900 | 0.7500 |

### Q12

This is the most severe extrapolation: hotter than batch 5 and longer than batch 3. Reagent conversion should be complete, but extensive secondary degradation should strongly reduce target yield and selectivity while increasing byproduct signal. The batch is predicted to be clearly unsafe.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7000 | 0.5000 | 0.8700 |
| conversion | 1.0000 | 0.9850 | 1.0000 |
| safety_risk | 0.4550 | 0.4200 | 0.5000 |
| score | 0.0800 | 0.0100 | 0.1800 |
| selectivity | 0.3000 | 0.1200 | 0.4900 |
| yield | 0.3000 | 0.1200 | 0.4900 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material packet contained one substantive directional claim: near the 420 K, 3300 s reference region, the higher-temperature side was expected to retain safe, balanced performance more reliably than the lower-temperature side. It also cautioned that the supplied model was incomplete and that experimental evidence should dominate. No task-specific molecular dossier, catalyst identity, elementary mechanism, or quantitative kinetic law was supplied; the solvents had names, but their reaction effects were explicitly categorical benchmark effects.

The temperature claim encountered affirmative counterevidence. Batch 4 at 390 K and 3300 s gave yield 0.6832, selectivity 0.7173, degradation warning 0.1728, safety risk 0.1809, and score 0.3967. Batch 5 at 440 K and 3300 s gave lower yield and selectivity, 0.6548 and 0.6546, a higher degradation warning of 0.2721, risk 0.3629, and score 0.2959. The latter crossed the 0.35 safety limit. Even the 420 K reference batches were not superior to 390 K on balanced performance. Thus, this was not merely a case of “no support found”; actual counterevidence appeared, and I did revise the interpretation in K1, writing that the prior claim “was therefore not supported at 440 K” and should be restricted, if retained at all, to a narrower region.

The packet’s warning that the model was local and incomplete was strongly supported. Temperature, residence time, catalyst, and solvent all affected different observables in different directions. High conversion did not guarantee high target yield or safety.

Several matters remained untested. I did not test temperatures just above and below 420 K closely enough to determine whether a very narrow locally favorable high-temperature direction exists. I also did not test whether a temperature-bound rollback would occur; batch 5 executed and returned an unsafe outcome rather than a rollback. No supplied claim about catalyst deactivation was available to test, and the opaque catalyst identities prevented material-specific mechanistic inference.

2. Experiments that formed or changed my judgment

Batch 1 was primarily a reference anchor. Its condition was taken directly from the supplied reference context rather than discovered from data. Its high conversion, 0.9878, combined with only 0.6702 yield and 0.6755 selectivity, initially suggested that conversion and productive outcome were not interchangeable, but one batch alone could not establish why.

Batches 2 and 3 genuinely formed the central mechanistic judgment. At 420 K, shortening exposure to 1800 s in batch 2 gave conversion 0.9000, yield 0.7161, selectivity 0.7851, byproduct 0.1913, and degradation warning 0.1082. Extending exposure to 5400 s in batch 3 left conversion high at 0.9834 but reduced yield and selectivity to 0.5349 and 0.5282 while raising byproduct and degradation signals to 0.4636 and 0.3937. These observations motivated the K1 statement that the world required a “formation-plus-secondary-loss account” rather than a simple conversion-limited model.

Batches 4 and 5 changed my temperature judgment and directly challenged the initial directional claim. Batch 4 demonstrated that lower temperature could preserve yield and selectivity with much lower risk. Batch 5 showed that a hotter setting could increase conversion while worsening the productive balance and violating the safety constraint.

Batches 6-8 changed the catalyst interpretation from a one-dimensional activity ranking to pathway-dependent catalysis. Catalyst D in batch 8 was especially informative: conversion remained high at 0.9704, but yield was only 0.6036, selectivity 0.6274, byproduct 0.3951, and degradation warning 0.2923. This supported the K1 rule that “high conversion is not evidence of productive catalysis.” Catalysts A and C suggested lower degradation than Catalyst B, but the absence of replication makes those finer differences provisional.

Batches 9-11 showed that solvent affected conversion, selectivity, degradation, risk, and not merely a global rate multiplier. Water in batch 9 reduced conversion to 0.8689 but retained selectivity of 0.7263 with low degradation warning and risk. These experiments broadened the model but did not identify molecular solvent effects because the benchmark explicitly treated solvent coupling categorically.

Batch 12 was intended partly as a repeat and partly as a quench comparison. It established that a late quench did not obviously reverse accumulated degradation, but it was a weak causal test because it lacked a matched contemporaneous unquenched replicate, and its prior HPLC measurement made it not perfectly identical to batch 1. My later prediction of a quench-related score benefit relied too heavily on the score difference between batches 1 and 12.

The overall design depended on three different sources. The initial packet determined the baseline formulation and made temperature an obvious axis. Accumulating data motivated the time series and the rejection of a purely conversion-driven account. Several choices were still unverified guesses: that one-factor-at-a-time catalyst and solvent screens at 420 K would transfer across time and temperature; that 440 K was an informative but tolerable challenge; and that a single late-quench batch could reveal a quench effect.

3. Principal competing mechanisms and what can be distinguished

K1 proposed the minimal network R -> P, R -> B, and P -> D, optionally with catalyst deactivation. This remains economical, but it is not uniquely identified.

The most important competing explanation is a time-varying catalyst-state model. Instead of stable P undergoing direct degradation, the catalyst could change from a productive state to an unselective state, so later conversion preferentially forms byproducts. Such a model can reproduce rising conversion, falling selectivity, and increasing degradation warning without requiring substantial P -> D conversion.

A second competitor is an unobserved-intermediate network: R -> I, followed by I -> P or I -> B/D. Temperature and time could change intermediate partitioning, and the public channels might classify late intermediate products as degradation. A third is reversible target formation followed by a temperature-dependent equilibrium shift. A fourth, less chemically specific explanation is that the measured degradation and byproduct channels are overlapping summaries of a changing product distribution rather than separate species.

The experiments can reject a simple fixed-ratio parallel model in which R converts irreversibly to stable P and B with constant branching. Batch 2 versus batch 3 shows too much decline in yield and selectivity after conversion has nearly saturated. The data also distinguish catalysts by productive versus nonproductive behavior and establish that the upper-temperature region carries additional risk.

They cannot distinguish direct degradation of isolated P from changing catalyst speciation, delayed intermediate partitioning, or reversible target loss. No isolated target was reheated. No catalyst was added midway to test activity recovery. Catalyst loading was not varied, and catalyst reuse or active-state measurements were absent. The in-process HPLC and final assay used different analytical contracts, so their differences cannot serve as a clean within-batch species trajectory. Consequently, the differential equations in K1 are an explanatory scaffold, not an identified kinetic law.

4. One additional complete experiment

If only one legal complete experiment were available, I would use the standard Catalyst B/acetonitrile formulation and split a 420 K heat treatment into two segments: heat for 1800 s, measure by HPLC, then heat for another 3600 s at 420 K, terminate, and perform the required final assay. This would place a measurement near the batch-2 optimum and finish at the total 5400 s exposure of batch 3, within one vessel and one thermal history. I would not quench between segments because the purpose would be to observe continued evolution.

If the 1800 s HPLC result resembled batch 2 and the final result resembled batch 3—high target at the midpoint followed by a large decline—then within-batch evidence for secondary loss or a time-evolving pathway would become much stronger. It would reduce the plausibility that the batch-2/batch-3 contrast was mostly between-batch variability.

If midpoint target were low but the final target rose, the supposed 1800 s optimum would look less reproducible, and an induction-period or intermediate-accumulation model would gain support.

If midpoint target were high and remained high at 5400 s, then the severe batch-3 result would look batch-specific, and K1 would have overstated the evidence for inevitable secondary loss.

If conversion increased while target stayed constant, a late parallel byproduct pathway would be favored over direct target degradation. If target declined substantially with little additional conversion, direct degradation, reversible loss, or a changing analytical assignment would be favored.

This experiment would still not perfectly identify chemistry because HPLC and final assay differ. Nevertheless, it would provide more mechanistic leverage than another single endpoint and would remain below the observed 440 K safety problem.

5. Tradeoff between identifiability and operating score

The research goal explicitly made explanatory understanding primary and safe score secondary. My allocation reflected that: three residence times, three temperatures, all four catalysts, all four solvents, and one quench comparison covered broad causal axes. Batches 3, 5, and 8 were knowingly unlikely to maximize score but were informative. Batch 3 exposed late degradation; batch 5 tested and contradicted the initial high-temperature claim, though it crossed the safety limit; batch 8 revealed that high conversion under Catalyst D was nonproductive. These were cases where I sacrificed operating performance for discrimination.

Conversely, batch 2 served both purposes. It probed a shorter residence time and became the highest-yield/selectivity condition. Batch 4 also combined mechanistic value with strong safe performance. After those results, I could have spent later batches refining time and temperature near the apparent optimum. I did not, because the research objective favored catalyst and solvent coverage. Thus, I sacrificed potential score improvement and local optimization precision for broader mechanism mapping.

The design was not maximally identifiable despite this emphasis. Most levels were unreplicated, the sweeps were one-factor-at-a-time, and catalyst-temperature, solvent-temperature, and time-temperature interactions were not estimated. The late-quench experiment used a scarce batch without testing the more mechanistically important early-quench hypothesis. A factorial or sequential design with replicated center points would have supported stronger causal estimates, but it would have covered fewer categories.

There was also one questionable balance: batch 5 at 440 K generated valuable counterevidence but exceeded the safety limit. A 430 K point might have mapped the onset of degradation and risk more responsibly, although it would have been less decisive against the initial claim.

6. Underused evidence and weaknesses in the blind predictions

The paired in-process HPLC and final-assay readings were not fully exploited, partly because they are difficult to compare. Several apparent conversion decreases illustrate the problem: batch 4 changed from HPLC conversion 0.9440 to final-assay conversion 0.9165; batch 6 changed from 0.9677 to 0.9437; and batch 11 changed from 0.9966 to 0.9711. Literal reactant conversion should not reverse under the minimal irreversible model. These differences probably reflect instrument noise, calibration differences, process variability, or channel definitions, but they should have caused me to be even more cautious about treating endpoint differences as exact kinetics.

The net temperature changes were reproducible near 420 K but did not provide continuous temperature histories. K1 acknowledged that heat-up time, lag, and exotherm were unidentified. I nevertheless treated nominal temperature and duration too much like uniform isothermal exposure in the staged blind predictions.

The score evidence was particularly underdetermined. Batches 1 and 12 had similar chemistry and the same observed risk, yet their scores were 0.3422 and 0.4051. I attributed much of this difference to explicit quenching in Q02 and Q10, but one unmatched pair cannot identify a quench bonus. Latent process variability or unobserved scoring components are equally plausible. The score intervals for those queries should therefore have been wider.

The least reliable blind predictions were Q12, Q07, Q08, and Q11. Q12 at 460 K for 6300 s was outside both the temperature and time scope stated in K1. Q11 at 370 K was below the measured temperature range. Q07 and Q08 required order-sensitive predictions for two-stage thermal histories even though K1 explicitly said that continuous temperature history and heat-transfer dynamics were unidentified. Their predicted ordering—better retention when 450 K preceded 390 K—was a mechanistic guess, not a result established by the campaign.

Q04 at 450 K was also extrapolative, although closer to batch 5. Q05 at 1500 s was near batch 2 but still depended on an unlocated yield maximum. Q09 and Q10 were chemically plausible interpolations in duration at 440 K, but their safety-risk intervals were probably too narrow because only one 440 K batch existed and it lay near the constraint boundary.

The prediction intervals for safety risk in Q04 and Q09-Q12 were generally overconfident. I treated risk as a smooth, nearly deterministic temperature function despite not knowing controller behavior, thermal history, or whether peak risk has nonlinear thresholds. Score intervals were also too narrow relative to the unexplained batch-1/batch-12 contrast. Q12 had broad composition intervals, but its risk interval of 0.42-0.50 still implied more knowledge of high-temperature scaling than the data justified.

These weaknesses partly conflict with K1’s own scope statement, which limited the model to approximately 390-440 K and 1800-5400 s and warned against extrapolation above 440 K. The prediction rationales admitted that Q11 and Q12 were extrapolations, so the conceptual caveat was retained, but the numerical precision did not fully honor it. Likewise, K1 said staged thermal history was unidentified, while Q07 and Q08 assigned fairly specific order effects. Those estimates should have had substantially wider, more overlapping intervals.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 2: Catalyst B in acetonitrile at 420 K for 1800 s. Its basis was valid but narrow. It had the highest observed final yield, 0.7161, and selectivity, 0.7851, while remaining below the safety limit. It was therefore the sample-internal best condition for the chosen chemical criteria among the 12 completed experiments.

It was not the highest observed score: batch 12 scored 0.4051 and batch 4 scored 0.3967, compared with 0.3806 for batch 2. The recommendation prioritized target yield/selectivity and acceptable safety rather than the public score alone, consistent with the research goal. It also did not prove that 1800 s was optimal. No nearby times such as 1500, 2100, or 2400 s were tested, and batch 2 was not replicated.

Repeatability should first be tested by multiple exact independent repeats of batch 2, preserving order of addition, volume, stirring, thermal program, termination, and assay protocol. That would estimate process variance and determine whether its advantage over batch 4 and the 3300 s batches exceeds noise.

Local robustness should then be tested around the recommendation rather than only at the nominal point: modest temperature perturbations around 410-425 K, residence times around 1500-2200 s, and small variations in catalyst charge, reagent concentration, and stirring. A replicated local response-surface design would reveal whether batch 2 lies on a broad operating plateau or a narrow peak. An explicitly timed quench near the optimum should be evaluated with matched quenched and unquenched controls.

Cross-material generalization is unproven. Catalyst B was best under the selected acetonitrile/time combination, but catalyst-by-time and catalyst-by-temperature interactions were never mapped. The solvent ranking at 3300 s need not hold at 1800 s. Testing the same local design with Catalysts A and C and with ethanol would establish whether the inferred stopping-time principle transfers while allowing material-specific optima.

Cross-world generalization is even more limited. The catalysts and reaction species are anonymous benchmark entities, and the real solvent names do not imply that the observed categorical kinetics predict real chemistry. A new world would require new calibration experiments and should not inherit the numerical optimum without evidence.

Accordingly, batch 2 should be described as the best observed candidate under one fixed scale and material combination, not as a globally or even locally proven optimum. Its recommendation is a defensible starting point for confirmation and refinement, not a completed optimization result.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 111.6 | none | 0 |
| Q | yes | 0 | 83.0 | none | 0 |
| K2 | yes | 0 | 113.6 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
