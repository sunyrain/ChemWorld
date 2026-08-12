# Work II static catalyst-deactivation Q0

Date: 2026-08-12

Status: frozen before execution

## Question and coverage

Can a fixed reaction-safety world expose a participant-identifiable structural distinction between
the declared catalyst-deactivation mechanism and an otherwise identical stable-catalyst mechanism?
The intervention is static for the complete execution: the stable variant removes the unique
`Cat_active -> Cat_dead` reaction at world construction and requires discrete severity `1.0`.

The provider-free seed-0 Q0 contains `3 temperatures x 3 durations x 3 catalyst doses x 2 laws =
54` executions. Temperatures are `350, 410, 465 K`; durations are `1,800, 7,200, 14,400 s`; catalyst
doses are `0.000120, 0.000315, 0.000520 mol`. Reagent, solvent, volume, stirring, catalyst identity,
action order, observation seed and keyed-noise coordinate are paired within each law comparison.

## Measurements

Every execution performs a public HPLC measurement and final assay. Primary direct metrics are
yield, conversion and selectivity. Final safety risk and score are retained as secondary outcomes.
Every trajectory must retain one fixed mechanism hash and pass intervention-aware exact replay.
Unsafe and dynamic physical outcomes remain classified coverage outcomes; they are not platform
failures. No provider or participant session is used.

## Frozen gates

- all `54` attempts are classified and exact replay, with paired action/noise bindings;
- zero platform failures and zero unclassified outcomes; dynamic physical-boundary outcomes remain in
  the denominator but are not treated as platform defects or silently replaced;
- at least `24/27` law pairs complete on both sides, with at least 18 pairs safe on both sides; safe
  completed pairs must cover all three temperature, duration and catalyst-dose levels;
- the stable mechanism deterministically removes exactly the unique catalyst-deactivation reaction,
  changes the mechanism hash, and matches the mechanism hash recorded in every execution;
- all direct metrics from completed outcomes are finite and publicly observed;
- at least two of yield, conversion and selectivity exceed `max(0.05, 3 sigma)` in a paired cell,
  using declared sigmas `0.012, 0.012, 0.018` respectively;
- effect-supporting safe cells cover at least two separated process regions and at least two catalyst
  doses;
- yield or conversion shows a duration-accumulation signature: the mean stable-minus-deactivating
  gap at `14,400 s` exceeds the corresponding mean at `1,800 s` by at least
  `max(0.03, 2 sigma)`;
- participant-visible payloads contain no private mechanism/intervention tokens.

Any platform defect restarts the block from seed 0 with the same grid and gates. A scientific failure
is retained and rejects this candidate without changing the topology, grid or thresholds. Passing
retains reaction-safety as a second A-S candidate for a separately frozen two-task five-world
qualification with the already retained crystallization candidate; it does not authorize a
participant D1 or provider execution.

## Outputs

Expected outputs are ignored raw trajectories and receipts, one tracked machine summary with exact
denominators and all failures, one concise analysis document, and an updated Work II TODO entry.
