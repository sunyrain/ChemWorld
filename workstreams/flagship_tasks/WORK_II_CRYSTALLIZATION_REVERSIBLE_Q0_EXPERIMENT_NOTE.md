# Work II crystallization reversible-topology A-S Q0 experiment note

Date frozen: 2026-08-12. This note authorizes one provider-free seed-0 qualification in the
repository's development execution mode. Development execution does not require a clean worktree
or a release source binding and its result is not release eligible. It does not authorize a
participant session, provider call, D1, C2 admission, or formal execution. The scientific question,
coverage, measurements, denominators, and pass/failure rules below remain frozen across execution
modes; a later release rerun requires the one-time minimal execution-surface manifest.

## Question and tested units

Can the public `reaction-to-crystallization` task distinguish its baseline irreversible target
pathway from the registered `reversible_target_pathway_stress_v1` alternative using genuinely
separate temperature and reaction-duration intervention families? The immutable unit is one of
nine `3 x 3` temperature-by-duration coordinates in public world seed 0. Every coordinate executes
both candidate laws with the same action-plan hash and keyed-noise coordinate.

## Measurements and denominators

The frozen block contains 9 paired coordinates, 2 laws, and exactly 18 primary executions. Each
trajectory must pass intervention-aware exact replay. Direct HPLC yield, conversion and selectivity,
terminal outcomes, safety, mechanism binding, action/noise pairing, all failures, and exact
denominators are recorded. Provider and participant counts are zero.

## Pass and failure rules

All 18 executions must complete safely and replay exactly, with zero physical/platform failures.
The altered mechanism must add exactly one deterministic reverse reaction while preserving the
public task contract. At least two direct metrics must exceed `max(0.05, 3 sigma)`; at least two
separated cells must support the contrast; and at least one product/conversion metric must show a
long-minus-short duration accumulation increase of `max(0.03, 2 sigma)`. The public payload must
not expose evaluator truth. Any platform failure stops the block and requires a complete rerun after
repair. A scientific failure is retained without changing the grid, law, seed, or thresholds.

## Expected outputs

One self-hashed raw task report, one self-hashed readable summary, exact failure denominators, raw
file hashes, and one uniform execution-context envelope. A development pass authorizes only the
unchanged provider-free five-world development qualification; it cannot authorize C2 admission.
