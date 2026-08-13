# Work II A-S five-seed D1 production materialization

Status: development implementation; provider execution remains blocked.

## Question and coverage

Can the two locked W2-37 A-S D1 designs be expanded into one deterministic five-seed parent schedule
without changing their scientific contracts or calling a provider? Coverage is
`2 tasks x 5 worlds x 3 prior arms x 12 complete experiments`: partition constitutive-power and
reaction-to-crystallization reversible topology, seeds `0..4`, with belief checkpoints at
`0/3/6/9/12`.

## Measurements and rules

The materializer must accept only the provider-free W2-37 package in which both candidates passed all
five worlds. Every child preserves the locked arms, intervention, public held-out queries,
measurements, operation/resource pattern and pass rules; only world seed and the seed-specific pilot
and keyed-noise namespaces change. Materialization reads no participant outcomes, performs zero
provider calls and leaves provider, formal/R5 and C2 execution unauthorized.

Any missing world, failed W2-37 row, task/candidate mismatch or scientific-config drift fails closed
without producing a partial schedule. The output denominator is exactly 10 campaign children, 30
participant cells and 360 complete experiments. Provider execution and its failure/stop semantics
require a later explicit authorization and are outside this block.

## Expected outputs

One readable static parent JSON and ten static campaign-child JSON configs. No run directory, raw
provider payload, release freeze, audit package or participant result is produced.
