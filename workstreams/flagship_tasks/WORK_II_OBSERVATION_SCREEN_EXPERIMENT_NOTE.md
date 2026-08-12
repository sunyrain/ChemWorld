# Work II observation/measurement screen — experiment note

状态：**seed-0 development probe freeze；尚未产生新 screen 结果**

## Question

After observation-contract Q0, can public final-assay measurements resolve a controlled intervention
in two task families while keeping replicate noise, truth-to-observation bias and replay auditable?
This is an observation-layer screen, not a participant capability test and not a formal A-O block.

## Tested units and coverage

- Task families: `electrochemical-conversion` and `reaction-to-crystallization`.
- Development probe: world seed `0` only; a later expansion, allowed only after this probe is
  analyzed, uses the unchanged design on world seeds `0–4`.
- Electrochemical fixed context is the v0.2 structural screen context with controlled potential fixed
  at `1.05 V`; controlled current is `{15, 91, 190} mA`.
- Crystallization fixed precursor context is the v0.2 structural screen context with crystallization
  temperature fixed at `290 K`; seed mass is `{0.001, 0.008, 0.015} g`.
- Every level has three independently keyed observation replicates. Each replicate is one complete
  provider-free final-assay recipe; each intervention level additionally has one evaluator-owned
  truth execution for bias auditing.
- Seed-0 denominator: `2 tasks × 3 levels × 3 replicates = 18` noisy executions and `6` truth
  executions. A five-world expansion would be `90` noisy and `30` truth executions.

## Measurements

- final-assay public metric values and finite/observed masks;
- replicate mean, sample standard deviation, maximum bias against evaluator truth and normalized
  bias;
- intervention effect-to-replicate-noise ratio for each task-owned metric;
- exact replay, physical/platform failures, unsafe outcomes and public/private leakage audit.

## Pass/failure rules

For each task/world probe:

- all 9 noisy executions and all 3 truth executions complete, all `12/12` exact-replay, with zero
  platform or physical failures;
- all registered metrics are finite and observed;
- the maximum absolute replicate-mean bias is no larger than
  `max(0.03, 3 × max_replicate_sigma)`;
- at least one task-owned metric has a three-level effect at least
  `max(0.03, 3 × max_replicate_sigma)`;
- no public trajectory or report contains evaluator/private tokens.

If the seed-0 probe fails because of an observation/compiler/runtime defect, fix and rerun the whole
probe from its first query. If it fails scientifically while execution is sound, retain the failure
and do not expand to five worlds. Passing seed 0 authorizes only the unchanged provider-free five-world
screen; it does not authorize participant/provider execution.

## Expected outputs

1. One machine-readable seed-0 screen report with exact denominators and all failures.
2. One readable probe analysis and an explicit expand/do-not-expand decision.
3. No participant config and no provider execution authorization.
