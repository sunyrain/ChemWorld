# Work II W2-50 yoked opaque-contract repair experiment note

Status: development repair pilot; frozen before provider execution on 2026-08-25.

## Question and fixed coverage

The first pilot retained an unsupported-schema failure. A second repair proved that the provider
accepts the `oneOf`-free schema, but its first returned snapshot exposed a producer/validator drift:
the schema permitted non-empty `suspected_misindexed_fields` in an opaque arm while the canonical
validator forbids them. That returned snapshot and both earlier failed calls remain immutable. This
block fixes the canonical opaque schema to require an empty list and runs exactly one fresh six-turn
yoked session for the same read-only W2-50 donor. No other condition is rerun.

## Measurements and invariants

Retain all provider attempts, one persistent repair thread, five validated belief snapshots, terminal
ranking, Top-1, regret, pairwise ordering, and tool-event counts. W2-50 evidence, scientific inputs,
candidate reveal gate, typed-law validator, and outcome scoring remain unchanged. The only semantic
repair is `maxItems=0` for opaque `suspected_misindexed_fields`; nominal arms retain their declared
field enum.

## Failure and stop rules

Any provider, schema, tool-contamination, same-thread, reveal-gate, or unchanged-validator failure is
retained and stops the session. A poor terminal action is a valid result and cannot be rerun. The two
previous failed provider calls remain in total resource accounting. No physical or truth execution is
authorized.

## Expected outputs

The ignored root `runs/development/w2-50-matched-extension-pilot-yoked-opaque-contract-repair-20260825/`
contains the input binding, progress, provider-turn records, yoked result, and a combined summary
reusing the original no-evidence and learned-law-only sessions.
