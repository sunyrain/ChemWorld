# Work II resource-calibration triplets — experiment note

状态：**九任务设计冻结；runner/validator 整合中，尚未启动 provider 执行**
适用阶段：W2-26；不进入 A-E public/private scientific denominator。

## Question

For every task-specific 8-, 10-, and 12-experiment contract used by C2, can the current single-session
Codex + ChemWorld MCP harness complete the prescribed lifecycle while preserving closeout
reserve, typed checkpoints, exact replay, and auditable provider/resource accounting? The block
calibrates hard process-time, operation, token, and currency ceilings; it does not compare
scientific outcomes or select a more favorable trajectory.

## Tested units and coverage

- Nine development triplets: all five A-E tasks at 8 experiments, both A-P tasks at 10 experiments,
  and both A-S tasks at 12 experiments. No representative-task or cross-task proxy is permitted.
- Each triplet contains the same three information arms (`opaque`, `aligned_nominal`,
  `misindexed_nominal`) in one persistent session per cell.
- Exact denominator: 9 task triplets, 27 cells, 252 complete experiments, 135 typed checkpoints,
  27 accepted provider sessions, and 27 accepted participant model calls.
- The task configuration for each `(locus, task_id, rounds)` unit, its world seed, provider contract,
  and task-specific resource formula must be written into the calibration manifest before the
  first provider call. No task, arm, seed, pattern size, or pass rule may be changed after launch.
- Because this is a development resource calibration rather than release evidence, execution binds
  those three selected campaign configurations and their selection/Q2 inputs directly. It does not
  require a clean worktree or a whole-tree source hash; the common immutable runtime freeze is
  performed once later, at the release boundary.
- Participant-selected exact repeats are measured separately from provider retries, MCP schema
  recovery, and infrastructure resume. Those operational retries are never new experiments.
- A-E contains electrochemical conversion, reaction-to-crystallization, reaction-to-distillation,
  partition discovery, and constrained reaction safety. A-P contains electrochemical conversion
  and constrained reaction safety. A-S contains partition discovery and
  reaction-to-crystallization. These nine task identities are distinct even when they share a
  round count or task family.

## Measurements

For every cell and triplet, record:

- complete experiments, unique recipe count, exact-repeat count, operation attempts and committed
  operations;
- checkpoint stages and typed snapshot validity, final recommendation commit, lifecycle closeout,
  and exact replay;
- process time used, required-stage maximum, repeat allowance, protected reserve and reserve
  consumption by operation class;
- cumulative input, cache-hit input, uncached input, output tokens, provider elapsed time,
  MCP recovery/error counts, provider attempts, and observed currency;
- resource rejection, unsafe outcome, dynamic physical failure, provider error, and platform
  execution failure counts.

## Pass/failure rules

- A cell passes calibration only if all planned experiments close, the required checkpoints and
  final recommendation are present, exact replay passes, and all resource ledgers reconcile.
- The scientific repeat allowance remains fixed at A-E `6 unique + at most 2 repeats`, A-P
  `8 unique + at most 2 repeats`, and A-S `10 unique + at most 2 repeats`. An observed run using
  fewer repeats must not shrink this design allowance.
- Exploration cannot consume protected closeout capacity. A-E and A-P retain 15% protected
  process/stock margin; A-S retains 20%. The final operation reserve is restricted to transfer,
  quench, final assay, discard, or safe termination and its actual consumption is reported.
- A participant scientific/method failure is retained as a calibration observation and cannot be
  replaced because its resource use is unfavorable.
- A provider, harness, compiler/runtime, observation, replay, or accounting defect invalidates the
  affected calibration block; that block must restart from its first cell with the same manifest.
- Task-local observed operation, process-time, token, provider-time, and currency maxima plus the
  frozen task-local protected reserve are the only inputs allowed to generate formal hard caps.
  A card from another task or locus is never portable merely because the round count matches.
  Planning envelopes remain non-authoritative until this block is complete.
- No result from this note supports H1–H4, law discovery, transfer, model ranking, or a scientific
  endpoint claim.

## Expected outputs

1. One machine-readable calibration summary with exact denominators and all failures.
2. One readable calibration analysis covering all nine tasks, three loci, lifecycle sizes, and arms.
3. Nine task-owned resource-card proposals for process time, operation limits, closeout reserve,
   token ceilings, and currency ceilings. Repeat allowance remains a frozen experiment-design field,
   not a measured cap.
4. A zero-provider/readiness receipt that records whether the formal method-qualification triplet
   may be authorized.
