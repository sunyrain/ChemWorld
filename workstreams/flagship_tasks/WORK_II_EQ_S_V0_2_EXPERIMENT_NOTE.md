# Work II EQ-S v0.2 experiment note

## Aim

Test whether an autonomous Agent can characterize a bounded aqueous-equilibrium world and distinguish a direct free-ion precipitation network from a network containing a distinct aqueous ion-pair intermediate, without revealing hidden constants or prediction questions during source experiments.

## Frozen experimental unit

- Prior locus: `S` (mechanism structure).
- Physical worlds: five (`EQ-S-W01` through `EQ-S-W05`).
- Information arms per world: `Opaque`, `Aligned`, and `MisIndexed`.
- Source task: one characterization session per cell, exactly 12 independent experimental batches.
- Sealed posttests: `K1`, `Q`, `K2`, then `EQS`.
- Prediction set: 12 fixed new batches and three public endpoints.
- Reference truth: five repeats per prediction condition, generated only after all 15 `EQS` responses are sealed.

The formal denominator is 15 source sessions, 180 source batches, 60 sealed posttests, and 300 reference executions. The Opaque arm receives no instance-level dossier. Aligned and MisIndexed expose the same fields, with MisIndexed carrying the opposite mechanism-family claim. No hidden numerical constant, query coordinate, or recommended recipe is public.

## Staged execution and stopping rules

1. Run a provider-free gate: 15 deterministic campaigns and 180 batches, exact replay, public response span checks, scale controls, leakage checks, and the preregistered four-parameter direct-network null fit with fixed holdouts.
2. Fail closed if any registered gate check fails. Retain the failure and repair by version; do not relax thresholds in place.
3. Freeze code, configuration, prompts, query set, scorer, and the passing gate evidence.
4. Run the complete `EQ-S-W01` three-arm canary. Do not release the other worlds unless all three 12-batch and four-posttest chains seal successfully.
5. Run the remaining 12 cells with at most eight isolated workers and automatic queue refill.
6. If a cell fails for an engineering or provider reason, retain its failed attempt and resume or retry the same frozen cell without changing the scientific contract.
7. Only after all 15 chains are sealed, generate reference truth, score numeric prediction and structural outputs, and export English session and aggregate reports.

## Scope boundary

This run is characterization, not operational optimization. `E` is not included in the bulk matrix. A separate multi-entity `EQ-E` substrate and provider-free non-collapse gate may be developed only after EQ-S is complete; it requires no provider execution at this stage.

## Planned output namespace

`runs/development/work-ii-eq-structural-20260920-v0.2`

