# Work II open-action resource-recovery v2 experiment note

Status: development-only; this is a fresh qualification block after the retained v1 recovery
failures and is not part of a formal denominator.

## Question

Can the same one-world, three-arm open-action decision protocol complete all scheduled sessions
when the resource contract contains fixed cushions for every resource failure observed in the
pilot and recovery-v1 block?

## Frozen coverage

- Tasks: `electrochemical-conversion` and `reaction-to-crystallization`.
- World seed: `0` for each task; arms `opaque`, `aligned_nominal`, and `misindexed_nominal`.
- Twelve participant-chosen experiments per arm; checkpoints `0/3/6/9/12`.
- The same eight deterministic complete ActionPlans, public-plan hashes, ranking-only terminal
  contract, truth queries, metrics, and qualification rules as the original pilot.
- The block is executed from the first arm and all three cells remain in the denominator.

## Fixed resource-contract correction

Relative to the original pilot contract, v2 adds:

- electrochemical `solvent_L`: `+0.100 L`;
- crystallization `catalyst_mol`: `+0.003 mol`;
- crystallization `seed_g`: `+0.040 g`;
- both tasks `process_time_limit_s`: `+30,000 s`.

These values are fixed before provider execution. They correspond to the retained v1 rejection
classes (`stock_limit:solvent_L`, `stock_limit:catalyst_mol`, `stock_limit:seed_g`, and
`protected_closeout_process_time_reserve`) with a finite margin. No action candidate, coverage,
objective, scoring rule, terminal readout, or pass/failure rule changes.

## Measurements and stop rules

Retain every provider action, resource rejection, provider error, timeout, checkpoint, exact
replay, terminal recommendation, and accounting receipt. A cell is eligible only if all 12
experiments, all checkpoints, final recommendation, resource reconciliation, and provider
accounting pass. A v2 failure is not repaired in place; the whole affected task block must be
restarted under a new declared contract.

## Expected outputs

Produce task-level campaign configs, public packets, truth/replay reports, three retained cell
records, machine summaries, progress logs, and Chinese reports. These remain development evidence.
