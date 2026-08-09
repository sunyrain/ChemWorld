# Work II blind evaluator development shakedown

- Question: can the frozen evaluator execute and exactly replay both registered targets across all
  three paired-noise replicates without provider calls, participant feedback, or participant-ledger
  contamination?
- Unit and coverage: one completed development seed-0 electrochemical campaign is used only as an
  action-plan fixture. Its observed incumbent is copied into a clearly labelled synthetic
  recommendation; this is not a participant recommendation or a scientific comparison. The fixed
  coverage is two targets by three paired replicates, six evaluator executions total.
- Measurements: completed/failed execution counts, exact-replay status, target means, paired-noise
  identity, provider-call count, participant-operation denominator impact, feedback flag, and all
  failure types.
- Pass rule: 6/6 executions complete, 6/6 exact replay, zero evaluator provider calls, zero
  participant-operation impact, no participant feedback, and no failures. Any missing, invalid,
  non-finite, non-replayable, or overwritten execution fails the shakedown and remains reported.
- Outputs: raw development artifacts under
  `runs/development/work-ii-blind-evaluator-shakedown-v0.2/` (Git-ignored) and a sanitized
  machine-readable summary at
  `workstreams/flagship_tasks/reports/work-ii-blind-evaluator-development-shakedown-v0.2.json`.
