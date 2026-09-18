# Experiment 1 P asset calibration note v1.0.0

Status: **FROZEN BEFORE CALIBRATION; FORMAL QUALIFICATION NOT AUTHORIZED**

## Purpose and denominator

This provider-free campaign tests whether the five authored P Worlds and the constant-K versus
composition-coupled private family produce a replayable, publicly distinguishable runtime fork.
It is calibration evidence only and does not enter the Experiment 1 formal denominator.

- Worlds: P-W01--P-W05, exactly five;
- public extractants: X0--X3, exactly four per World;
- reagent loads: `0.008` and `0.012 mol`, exactly two per extractant;
- cells: `5 × 4 × 2 = 40`;
- paired laws: constant K and composition-coupled K, exactly two per cell;
- execution denominator: `80`;
- the parent and child in a cell use the identical public action plan and keyed observation seed.

The protocol fixes solvent 2, catalyst 1, 385 K reaction, quench, 0.012 L aqueous phase,
0.018 L extractant, 240 s mixing at 850 rpm and 420 s settling. Only registered World,
extractant and reagent-load coordinates vary.

## Hard gates

The campaign passes only if all 80 executions complete, replay at tolerance zero, bind the
expected private World/fork hashes, expose no forbidden private token, and have public process
mass-balance absolute error at most `1e-8`. Parent/child action hashes and keyed-noise coordinates
must match in every cell.

For every World, at least one public endpoint among purity, recovery, product in organic,
product in aqueous and impurity signal must have a paired law gap of at least `0.02`. In addition,
the purity law gap must change by at least `0.01` between the two reagent loads for at least one
extractant. All five Worlds must pass; failures remain failures and no threshold is adjusted after
execution begins.

Public metrics retained in receipts are purity, recovery, phase ratio, product in organic,
product in aqueous, impurity signal and process mass-balance error. Exact replay, completion,
truth binding, leakage findings and the per-World fork statistic are also retained.

## Stop rule

No calibration execution is authorized until the machine contract, source-closure bindings,
five-World asset manifest and this note pass independent review. This note authorizes no Agent
benchmark run and no formal qualification. Participant/provider calls are fixed at zero.
