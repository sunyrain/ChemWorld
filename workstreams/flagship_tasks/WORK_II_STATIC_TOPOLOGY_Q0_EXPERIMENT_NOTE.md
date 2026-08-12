# Work II static reversible-path topology Q0 — experiment note

状态：**seed-0 provider-free Q0 已完成；crystallization 通过、flow 科学拒绝，
不扩展至五 worlds**

## Question

Can two distinct task families expose the same causal-topology distinction: an irreversible target
formation pathway versus a target pathway with a reverse channel? Each execution uses one physical
world from start to finish. There is no changepoint, mid-session physics change or participant in Q0.

## Tested units and coverage

- Tasks: batch `reaction-to-crystallization` and continuous `flow-reaction-optimization`.
- World seed: development seed `0` only. Passing Q0 authorizes an unchanged five-world
  provider-free qualification, not participant/provider execution.
- Candidate laws: baseline topology and one explicit `reversible_target_pathway_stress_v1`
  intervention at severity `0.8`, adding a reverse rate constant of `0.0005 s^-1` after severity
  scaling. The intervention payload and mechanism hashes remain evaluator-only.
- Each task uses a frozen `3 × 3` temperature × reaction/residence-time grid. All other controls and
  downstream operations are fixed. Every grid cell is executed once in each candidate law with the
  same keyed observation-noise coordinate: `2 tasks × 9 cells × 2 laws = 36` executions.

## Measurements

- direct pre-downstream public measurements: HPLC yield/conversion/selectivity for crystallization,
  and UV/Vis yield/selectivity/flow conversion for continuous flow;
- terminal final-assay direct metrics and task score as secondary outcomes;
- paired baseline-minus-reversible effects, declared observation uncertainty, separated supporting
  cells and the duration-dependent accumulation signature;
- completed/physical/platform outcomes, exact replay with the correct intervention context,
  deterministic mechanism binding and participant-visible leakage.

## Pass/failure rules

Each task must pass separately:

- all `18/18` executions complete, all exact-replay, with zero physical or platform failures;
- the topology adds exactly one reverse reaction, changes the mechanism hash deterministically and
  remains fixed for the complete execution;
- all registered direct metrics are finite and publicly observed;
- at least two direct reaction metrics have a paired topology effect at least
  `max(0.05, 3 × declared_observation_sigma)`;
- at least two grid cells separated by Manhattan distance at least two support a direct-metric
  topology effect above its gate;
- for at least one direct product/conversion metric, the mean baseline-minus-reversible gap at the
  longest reaction/residence time exceeds the shortest-time gap by
  `max(0.03, 2 × declared_observation_sigma)`, establishing an accumulated reverse-path signature;
- no participant-visible payload contains mechanism-family, intervention, private or evaluator
  truth tokens.

A platform/compiler/replay defect invalidates the whole Q0 and requires a restart from the first
query after repair. A scientifically weak task is retained and stops the candidate pair; thresholds,
tasks, grid cells and world seed are not changed after seeing the outcome.

## Expected outputs

1. One machine-readable seed-0 report with all 36 executions, exact denominators and failures.
2. One readable analysis with an explicit proceed/do-not-proceed decision.
3. No prior package, participant config or provider execution authorization from Q0 alone.

## Phase conclusion

The complete seed-0 block finished `36/36` executions and `36/36` intervention-aware exact replays
in `208.443 s`, with zero physical failures, platform failures, unsafe outcomes or participant-visible
leakage. Batch reaction-to-crystallization passed every gate: yield, conversion and selectivity
maximum paired effects were `0.1757`, `0.0730` and `0.1703`; six separated cells supported the
topology, and the longest-minus-shortest yield-gap increase was `0.1176` against a `0.0300` gate.

Continuous flow failed scientifically. Its maximum paired effects were only `0.0245` yield,
`0.0269` flow conversion and `0.0538` selectivity, below the frozen UV/Vis gates `0.135`, `0.120`
and `0.120`; its largest duration-accumulation increase was about `0.0137`. Mechanism compilation,
execution binding, paired noise and replay all passed, so this is not a platform defect.

The frozen decision is `retain_q0_scientific_rejection_and_do_not_expand`. The candidate pair does
not enter five-world Q1/Q2, prior construction, participant D1 or provider execution.
