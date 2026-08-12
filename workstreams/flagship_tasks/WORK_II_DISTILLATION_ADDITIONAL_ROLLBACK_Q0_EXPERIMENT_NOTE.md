# Work II reaction-to-distillation additional-rollback A-S seed-0 Q0

状态：**执行前冻结；仅授权 provider-free seed-0 Q0，不授权生成数据以外的扩展**

## Question

Can public reaction-stage measurements distinguish the native reactive-distillation network from the
same network with one additional target-rollback pathway? The native mechanism is already reversible:
`Acid + Alcohol <=> Ester + Water`. This experiment does **not** compare an irreversible law with a
reversible law. The intervention retains that native reversible esterification and adds one explicit
mass-action rollback reaction, `Ester + Water => Acid + Alcohol`, at effective
`k = 0.0005 s^-1`.

## Tested units and coverage

- Task: `reaction-to-distillation`; development world seed `0`; zero participant/provider calls.
- Laws: `native_reversible_network` and `native_plus_additional_rollback`.
- Frozen reaction grid: temperature `{350, 385, 420} K` × duration `{1200, 3600, 7200} s`.
- All material, loading, stirring, evaporation, distillation, reflux and collection controls are
  identical across paired laws. Each cell uses the same keyed observation-noise coordinate.
- Denominator: `9 cells × 2 laws = 18` complete paired executions, each followed by exact replay with
  its own intervention context.

## Measurements

- Primary direct evidence: the first HPLC measurement after reaction/quench and before evaporation or
  distillation, reporting public yield, conversion and selectivity.
- Secondary outcomes: terminal distillate purity, distillate recovery and score.
- Paired topology effects, separated supporting cells and duration-dependent rollback accumulation.
- Mechanism binding, action/noise pairing, completion, physical/platform/unsafe outcomes, exact replay
  and participant-visible leakage. The machine summary reports exact attempted/completed denominators
  and every observed failure.

## Frozen gates and stop rules

The task passes only if:

- all `18/18` executions complete, all exact-replay, with zero physical/platform failures;
- the native target reaction remains reversible, the intervention preserves it and adds exactly one
  deterministic `Ester + Water => Acid + Alcohol` reaction without removing or rewriting native paths;
- paired action plans and pre-distillation HPLC noise coordinates match exactly;
- at least two of yield, conversion and selectivity reach
  `max(0.05, 3 × declared_sigma)`, using declared sigmas `0.012/0.012/0.018`;
- at least two grid cells separated by Manhattan distance at least two support a direct-metric effect;
- for yield or conversion, the mean native-minus-additional-rollback gap at `7200 s` exceeds the mean
  gap at `1200 s` by `max(0.03, 2 × declared_sigma)`;
- no participant-visible payload exposes intervention, hidden-state, private or evaluator truth.

A compiler, execution-contract, observation or replay defect stops the runner immediately; after a
fix, the whole 18-execution block restarts from the first unit under a new output identity. A
schema-valid physical boundary is retained as a protocol-owned outcome; the frozen matrix continues
so the complete scientific denominator and all failures remain visible, but the task cannot pass. A
scientifically weak completed block is retained and not expanded. Gates, cells, law strength and task
cannot change after outcomes are observed.

## Expected outputs

1. One machine-readable summary with the complete denominator, all failures and exact replay counts.
2. One raw task report binding all 18 receipts and trajectories.
3. A proceed/do-not-proceed decision for an unchanged five-world provider-free qualification only;
   Q0 never authorizes participant/provider execution.
