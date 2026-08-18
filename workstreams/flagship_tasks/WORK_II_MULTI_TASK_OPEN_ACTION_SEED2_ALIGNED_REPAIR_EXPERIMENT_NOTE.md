# Work II open-action seed-2 aligned repair block

Status: development repair / sensitivity block; it does not replace the original formal cell.

## Question

Was the `reaction-to-crystallization / world_seed=2 / aligned_nominal` failure caused by a
provider/session interruption rather than by the agent's scientific trajectory, and can the same
frozen protocol complete when started in a fresh session?

## Frozen coverage and controls

- One cell only: `reaction-to-crystallization`, world seed `2`, arm `aligned_nominal`.
- Reuse the original cell's complete ActionPlan packet, checkpoint truth, candidate truth, hidden
  boundary, ranking-only terminal contract, resource-recovery-v2 contract, and tested runtime
  binding exactly.
- Start a fresh same-thread provider session; no candidate, metric, resource, stopping, or
  pass/failure rule changes.
- The original failed cell remains retained and remains part of the original 45-cell denominator.

## Measurements and disposition

Retain the full trajectory, all operations, resource ledger, checkpoints, provider receipts, final
recommendation, exact replay, and result hash. A completed repair is reported as a technical
sensitivity result beside the original failure; it is not substituted into the original aggregate
summary. A second interruption or any scientific early-stop remains retained without another
automatic rerun.

