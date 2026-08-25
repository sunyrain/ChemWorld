# Work II W2-50 yoked provider-schema repair experiment note

Status: development repair pilot; frozen before provider execution on 2026-08-25.

## Question and fixed coverage

The original W2-50 matched-extension pilot retained two completed sessions and one yoked runtime
failure. The yoked `pre_evidence` call produced no participant payload and failed before receiving
donor evidence because the provider-facing 9.3 KB snapshot schema used two unsupported `oneOf`
branches. Can a provider-compatible, `oneOf`-free projection of the same output contract complete
the fixed yoked session? Coverage is exactly one fresh six-turn yoked session for the same read-only
donor `A_S_MULTI_TASK_OAD--electrochemical-conversion--seed0--opaque`. No other condition is rerun.

## Measurements and invariants

Retain all six provider turns, one persistent thread, usage, tool-event count, five belief snapshots,
terminal ranking, Top-1, regret, and pairwise ordering. Scientific inputs, W2-50 evidence, candidate
packet, reveal gates, typed-law grammar, and the post-response belief validator are unchanged. The
provider schema may only replace query-specific `oneOf` branches with enum constraints and represent
non-categorical `category_value` as null before deterministic removal and the unchanged validator.

## Failure and stop rules

The original failed call remains immutable and is counted in total provider attempts. Any new
provider, schema, tool-contamination, same-thread, reveal-gate, or post-response validation failure is
retained and stops the repair. A poor terminal action is a valid result and cannot be rerun. No new
physical or truth execution is authorized.

## Expected outputs

The ignored root `runs/development/w2-50-matched-extension-pilot-yoked-schema-repair-20260825/`
contains the repair input binding, progress, six sanitized provider-turn records, the yoked result,
and a combined machine summary that reuses the original no-evidence and learned-law-only results.
