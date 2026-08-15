# Work II DeepSeek A-S crystallization resource-recovery experiment note

## Question

After exposing physically valid crystallization recovery actions, can DeepSeek complete and
interpret the fixed A-S reaction-to-crystallization cohort when thermal retries are not artificially
limited to one heat/cool cycle per scheduled experiment? How do opaque, aligned-nominal, and
misindexed-nominal initial world models affect experiment selection, belief revision, mechanism
recovery, and final recommendations under the corrected finite resource envelope?

## Fixed units and coverage

- Execute only the predeclared A-S `reaction-to-crystallization` block: 5 fixed worlds × 3 fixed
  prior arms = 15 sessions.
- Each session targets 12 completed experiments, for 180 scheduled complete experiments. Worlds,
  arms, ordering, paired noise, model `deepseek-v4-flash`, reasoning setting, prompt, checkpoints,
  held-out queries, evaluator, and scientific pass/failure rules remain unchanged.
- Preserve the previous 173/180 run as historical evidence. This block starts from its first cell in
  a new output root and never overwrites or splices the previous cohort.
- Provider calls are unlimited/report-only. Laboratory resources remain finite: heat, cooling, and
  split seeding allow 24 committed actions each; final assays remain 12; nonfinal measurements
  remain 36. Up to 15 batches may be started so as many as three participant-discarded batches can
  be replaced. Stocks, operation attempts, and process time scale only to 15/12 of the original
  batch envelope, not 2×.

## Measurements

Record all operations, measurements, belief checkpoints, held-out predictions, final
recommendations, blind evaluation, resource receipts and rejection reasons, provider usage,
right-censoring, exact replay, completed and discarded batches, and resource utilization by class.
Compare the incidence and location of heat/cool/seed exhaustion with the preserved prior run.

## Pass, failure, and stop rules

- The reporting denominator is all 15 terminal sessions and all 180 scheduled completed
  experiments. Completed, discarded, right-censored, and retained participant/method failures all
  remain in the report; no world or arm is outcome-replaced.
- A resource-exhausted operation must disappear from `available_actions` and be exposed as
  `cannot_complete` with actionable reason codes. A direct invalid submission is retained and
  charged according to the resource ledger; the host does not repair it.
- Physical, safety, stock, process-time, operation-attempt, checkpoint, exact-repeat, and final-assay
  constraints remain hard. The model controls any replacement batch and recovery sequence.
- A new platform defect that changes participant-visible feedback or committed trajectories stops
  unstarted triplets and requires this affected 15-session block to restart. A zero-operation
  infrastructure failure may resume only under the existing missing-infrastructure rule.

## Outputs

Write the generated config and plan to an ignored formal-input root and the run to a new ignored
formal output root. Retain per-cell trajectories and summaries, progress, the terminal cohort
summary, provider accounting, and all failures. Do not create a new audit, SHA inventory, readiness
chain, or overwrite historical evidence.
