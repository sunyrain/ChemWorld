# EQ bounded-equilibrium block — retained execution status

Date: 2026-09-20  
Evidence class: development  
Status: blocked at the W01 Opaque K1 boundary; truth remains embargoed

## Frozen design and provider-free gate

The block contains five frozen worlds, three matched prior arms, one characterization task, twelve source batches per independent source, and same-thread K1 → fixed Q → K2 posttests. Its full planned denominator is 15 sources, 180 source batches, 45 posttests, and 300 provider-free reference executions.

The v1.1 provider-free gate passed all registered checks with 15/15 campaigns, 180/180 batches, 15/15 exact replays, and zero provider calls. The gate, resolved config, source runner, recovery runner, exporter, tests, canonical posttest protocol, EQ protocols, and experiment note are bound by the current v1.5 freeze manifest. The earlier failed query grid and every remote startup/recovery failure remain retained.

## Canary result available now

| Cell | Source batches | Operations | Rollbacks | Exact replay | K1 | Q | K2 | Effective status |
|---|---:|---:|---:|---|---|---|---|---|
| EQ-W01 Opaque | 12/12 | 60 | 0 | passed | no valid payload | not opened | not opened | retained nonconforming |
| EQ-W01 Aligned | 0/12 | 0 | 0 | not run | not opened | not opened | not opened | sealed |
| EQ-W01 MisIndexed | 0/12 | 0 | 0 | not run | not opened | not opened | not opened | sealed |

The complete Opaque source is preserved and will not be rerun. Its first K1 turn exposed a mismatch between the already intended 128-attempt calculator policy and an inherited eight-attempt outer monitor; that failure had no payload. The repaired same-thread K1 turn then reached the fixed 1200-second provider timeout without a payload. The single authorized provider-timeout retry also reached 1200 seconds without a payload. Both timeout turns used zero calculator calls, had no laboratory access, and received no truth or score.

## Retained platform chain

The audit retains, in separate write-once locations:

1. a detached-shell executable-path failure before Agent construction;
2. a missing private output-parent failure before provider-process construction;
3. a login-shell proxy omission causing uniform pre-action network errors;
4. a 30-second laboratory-MCP startup threshold that failed before a model response or scientific action;
5. the successful 12-batch Opaque source followed by the outer-monitor K1 failure;
6. the first same-thread K1 provider timeout; and
7. the single authorized same-thread K1 provider-timeout retry.

No failed or recovered attempt is counted as a new scientific source. No credential, raw provider event stream, session identifier, or usage accounting is included here.

## Stopping boundary and heartbeat

The canary cannot pass while W01 Opaque lacks a valid K1/Q/K2 chain. Consequently, W01 Aligned, W01 MisIndexed, the remaining twelve sources, reference truth, scoring, and final report export have not started. This preserves the planned denominator and truth embargo.

A persistent hourly heartbeat is active in the current Codex task. It inspects only sanitized status, public trajectory counts, sealed result/recovery files, and process liveness. It stays quiet while nothing changes and is forbidden to issue another same-class provider retry, expand the matrix, or generate truth without new authority.

## Decision required

Continuing requires an explicit amendment because the single authorized provider-timeout retry has been consumed. A valid amendment must state whether to permit another same-thread K1 turn, change the 1200-second posttest timeout, change the model or reasoning effort, or stop the EQ block with the current retained development evidence. No such choice is inferred from the original authorization.
