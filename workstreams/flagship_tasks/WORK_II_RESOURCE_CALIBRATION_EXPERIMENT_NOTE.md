# Work II resource-calibration triplets — experiment note

状态：**设计完成，尚未获得真实 provider 执行授权**  
适用阶段：W2-26；不进入 A-E public/private scientific denominator。

## Question

For the 8-, 10-, and 12-experiment task-pattern contracts, can the current single-session
Codex + ChemWorld MCP harness complete the prescribed lifecycle while preserving closeout
reserve, typed checkpoints, exact replay, and auditable provider/resource accounting? The block
calibrates hard process-time, operation, token, and currency ceilings; it does not compare
scientific outcomes or select a more favorable trajectory.

## Tested units and coverage

- Three development triplets, one per frozen pattern size: 8, 10, and 12 complete experiments.
- Each triplet contains the same three information arms (`opaque`, `aligned_nominal`,
  `misindexed_nominal`) in one persistent session per cell.
- The representative task configuration for each pattern, its world seed, provider contract,
  and task-specific resource formula must be written into the calibration manifest before the
  first provider call. No task, arm, seed, pattern size, or pass rule may be changed after launch.
- Participant-selected exact repeats are measured separately from provider retries, MCP schema
  recovery, and infrastructure resume. Those operational retries are never new experiments.

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
- A participant scientific/method failure is retained as a calibration observation and cannot be
  replaced because its resource use is unfavorable.
- A provider, harness, compiler/runtime, observation, replay, or accounting defect invalidates the
  affected calibration block; that block must restart from its first cell with the same manifest.
- The observed maxima plus the protected closeout reserve are the only inputs allowed to generate
  formal hard caps. Planning envelopes remain non-authoritative until this block is complete.
- No result from this note supports H1–H4, law discovery, transfer, model ranking, or a scientific
  endpoint claim.

## Expected outputs

1. One machine-readable calibration summary with exact denominators and all failures.
2. One readable calibration analysis covering the three pattern sizes and each arm.
3. A pattern-owned resource-card proposal for process time, operation limits, repeat limits,
   closeout reserve, token ceilings, and currency ceilings.
4. A zero-provider/readiness receipt that records whether the formal method-qualification triplet
   may be authorized.

