# Work II held-out evaluator development shakedown

## Question

Can the frozen held-out query compiler execute every registered query for all five Work II tasks, expose every registered truth metric, and replay exactly without a provider call or participant feedback?

## Units and coverage

- Development world seed `0` only; it is excluded from the formal participant denominator.
- Five current Work II campaign tasks.
- Four registered held-out queries per task: 20 evaluator executions total.
- One keyed observation coordinate and one complete experiment per query.

## Measurements

- Completed and failed query counts, with all failures retained.
- Registered query-metric denominator and successfully observed denominator.
- Operation-attempt count and exact-replay result for every query.
- Evaluator provider calls, participant feedback, and participant-ledger impact.

## Pass and failure rules

Pass only if all 20 queries complete once, all 68 registered query-metric values are finite, every trajectory replays exactly, and provider calls, participant feedback, and participant-ledger impact are all zero. Any missing metric, invalid action, replay mismatch, or execution exception is a retained failure and fails the block; no query is replaced or rerun.

## Expected outputs

- Ignored raw plans, trajectories, and receipts under `runs/development/work-ii-held-out-evaluator-shakedown-v0.1/`.
- A readable tracked summary at `workstreams/flagship_tasks/reports/work-ii-held-out-evaluator-development-shakedown-v0.1.json` with exact denominators and all failure types.

## Infrastructure amendment after v0.1

The v0.1 parent command was terminated by an accidentally short outer command timeout after task 1 had completed 4/4 queries. Those artifacts remain immutable and v0.1 is reported as infrastructure-incomplete with 16 unstarted queries. The v0.2 rerun changes only the outer command timeout, starts the unchanged five-task block from the beginning under a new output identity, and preserves every coverage, measurement, pass, and failure rule above. Its raw and tracked outputs use the suffix `v0.2`.
