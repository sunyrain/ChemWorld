# Work II W2-63 DeepSeek B3 full-cohort replication

Status: prospective development experiment; frozen before provider execution on 2026-09-02 and
authorized by the user's instruction to complete every participant-bearing main experiment with
both DeepSeek and Codex.

## Question and fixed coverage

Does the `gpt-5.6-sol`/medium B3 result on participant-visible identifiable laws and unseen action
selection replicate for `deepseek-v4-flash`/high on the identical scientific surface? The block
contains the same five frozen public partition worlds, three prior arms and two fresh sessions per
arm/world as W2-56, for `30` two-turn sessions and zero participant physical experiments. Evidence
and scoring rosters, public packets, world seeds, mechanism families, exponent grid, evaluator
truth, typed-law schema, query-ID action encoding and every scientific threshold are unchanged.

The historical DeepSeek B3 canaries remain immutable and are excluded. In particular, their
participant-schema failures are not converted into passes and their completed session is not
spliced into this denominator. W2-63 starts at the first cell in a new root and uses fresh provider
threads throughout. The first world's replicate-1 three-arm triplet is an in-denominator
operational canary rather than a separate scientific admission gate.

## Measurements and comparison

The existing B3 evaluator records pre/post prediction error, mechanism family, exponent and
absolute exponent error, typed-law commitment, selected unseen action, true action rank, Top-1,
regret and availability-aware gain over the evidence incumbent. Report all `30` scheduled cells,
all failures, same-thread continuity, provider receipts, usage and tool events. Comparison with the
completed Codex cohort is model-stratified and world-clustered; it is not a pooled leaderboard.

## Failure, recovery and stop rules

Every session is attempted once in manifest order. Participant, scientific and schema failures are
terminal outcomes, remain in the scheduled denominator and do not stop later independent cells.
Ordinary provider/session failure after at least one durable provider receipt is likewise retained
without replacement. There are no outcome-selected retries. A result file and attempt marker are
never overwritten; after process interruption, completed cells are reused and a marked cell lacking
a result becomes an explicit interrupted failure rather than being called again.

Only participant-visible contamination, input/packet/provider binding drift, a tool event, or a
runner/provider infrastructure failure with zero durable provider receipts pauses later calls. The
first triplet applies these same rules: an unfavorable answer or a schema-invalid answer does not
reject the remaining cohort. Coverage, prompts, schemas, thresholds, worlds and evaluator rules
cannot change after execution begins.

## Expected outputs

The ignored run root contains the reused provider-free manifest binding, immutable attempt markers,
all `30` terminal result slots when the block completes, sanitized provider receipts, progress,
the existing B3 scientific summary and a failure-aware run summary with exact scheduled and missing
denominators. Raw provider payloads and credentials do not enter Git.
