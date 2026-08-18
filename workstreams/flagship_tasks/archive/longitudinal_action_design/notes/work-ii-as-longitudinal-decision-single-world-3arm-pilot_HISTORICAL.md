# Work II A-S single-world three-arm development pilot

Status: historical development protocol diagnostic; not part of any formal denominator and not a
paper-level action-quality result. Raw records remain under the ignored development run root.

## Question

Can the current W2-47 implementation complete one persistent twelve-round partition-discovery
session in each of the three matched prior-information arms and produce a valid ranking-only
terminal decision after eight outcome-blind candidates are revealed?

## Frozen units and coverage

- One partition world: `world_seed=153150025`.
- One public candidate packet: `candidate_packet_seed=400`.
- Three matched arms: `opaque`, `aligned_nominal`, and `misindexed_nominal`.
- One unchanged provider thread per arm; twelve participant-chosen experiments per session.
- Typed checkpoints at `0/3/6/9/12`; the final checkpoint is committed before candidate reveal.
- Eight candidates, with distinct material pairs and balanced volume/mixing coverage; ranking-only
  output and one selected action, with no per-candidate numeric predictions.

## Measurements and provider-free gate

- Sixteen checkpoint truth queries and eight candidate truth queries are executed without provider
  calls; every query must have tolerance-zero exact replay (`24/24` truth and `24/24` replay).
- Candidate selection must remain independent of truth, hidden rank, checkpoint outcomes, and
  participant outcomes; no candidate may collide with a checkpoint truth action plan.
- For each arm retain completion count, checkpoint stages, same-thread status, ranking, selected
  rank, Top-1, raw/normalized regret, candidate overlap, law normalized MAE, all failures, provider
  receipts, resource accounting, and exact replay.

## Pass/failure and stop rules

- The provider phase starts only after the provider-free gate passes and the command explicitly
  supplies `--allow-provider-execution`.
- All three arms remain in the scheduled denominator. Any provider, schema, scientific, resource,
  or platform failure is retained and stops no other arm; no outcome-based seed/candidate replacement
  or favorable rerun is allowed.
- A failed or contaminated cell is not counted as eligible, but its full raw record is retained.
- The pilot stops after the three arm records are closed; it authorizes no formal W2-47 inference.

## Expected outputs

One pilot manifest, deterministic candidate/checkpoint truth and replay records, three retained cell
records, a machine-readable summary, and a short Chinese report describing ranking and mechanism
readouts without promoting this single-world result to formal evidence.
