# Work II W2-07 resource, cost and power audit draft

Date: 2026-08-09. Status: measured development baseline and formal-freeze input; W2-07 is not
complete and this document does not authorize formal data collection.

## Audit decision

The three-task development campaign provides a usable engineering baseline, but not a formal
sample-size or monetary freeze. The retained denominator is 45 cells (three tasks x three prior
arms x five worlds), with 44/45 cells and 176/180 experiments complete. Worlds are the independent
clusters; rounds, checkpoints, operations and predictions within a world are repeated observations,
not additional independent samples. Formal power remains blocked on the W2-04 world cohort, W2-05
estimands and W2-06 participant/scaffold matrix.

## Measured development baseline

| Task | Cells passed | Input | Cached | Uncached | Output | Matrix wall time |
|---|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 15 / 15 | 19,459,659 | 17,652,224 | 1,807,435 | 157,356 | 2,661.4 s |
| Reaction-to-crystallization | 15 / 15 | 28,993,580 | 26,322,048 | 2,671,532 | 149,774 | 6,120.0 s |
| Reaction-to-distillation | 14 / 15 | 10,961,222 | 8,850,304 | 2,110,918 | 99,481 | 3,068.9 s |
| **Combined** | **44 / 45** | **59,414,461** | **52,824,576** | **6,589,885** | **406,611** | **11,850.3 s** |

The combined task-wall sum is 3.29 h. Mean usage was 1,320,321 input and 9,035.8 output tokens per
scheduled cell, but the task means differed substantially: 1,297,311 input for electrochemical,
1,932,905 for crystallization and 730,748 for distillation. These are descriptive planning values,
not exchangeable scientific observations. The distillation mean includes the retained failed cell,
which used 15,873 input and 170 output tokens but made no MCP call.

The campaign used 45 host-launched persistent provider sessions, one per scheduled cell. It recorded
1,547 operation attempts: 1,524 committed, 23 validation-failed and zero resource-rejected. There
were 39 provider-error events representing 24 distinct error entries. Errors recovered within a
session remain in the attempt denominator; the failed cell was neither replaced nor rerun. WellAU
currency pricing is not independently verifiable, so its monetary cost is unknown rather than zero.

## Current 45-cell topology envelope

These are the existing development resource cards, not the final W2-11 formal resource freeze.
Every cell schedules four complete experiments and typed checkpoints after 0, 1, 2 and 4 complete
experiments.

| Task | Cells | Operations/cell | Vessels/cell | Final assays/cell | Non-final instrument uses/cell | Process time/cell |
|---|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 15 | 28 | 4 | 4 | 0 | 72,000 s |
| Reaction-to-crystallization | 15 | 56 | 4 | 4 | 8 | 146,400 s |
| Reaction-to-distillation | 15 | 56 | 4 | 4 | 8 | 202,080 s |

The per-cell stock caps are 0.08 mol reagent and 0.16 L solvent for all tasks; crystallization and
distillation additionally cap catalyst at 0.008 mol, and crystallization caps seed at 0.2 g. The
cards retain task-specific stage-repeat and closeout reserves: electrochemical permits one extra
electrolysis; crystallization reserves one extra heat and crystallization stage, four 480 s filters
and up to four 120 s quenches; distillation reserves one extra heat and distillation stage plus up
to four 120 s quenches.

| Task | Input/cell | Uncached/cell | Output/cell | Wall/cell | 15-cell input | 15-cell uncached | 15-cell output | Topology wall upper bound |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 2,400,000 | 320,000 | 24,000 | 5,400 s | 36,000,000 | 4,800,000 | 360,000 | 27,000 s |
| Reaction-to-crystallization | 4,800,000 | 640,000 | 48,000 | 7,200 s | 72,000,000 | 9,600,000 | 720,000 | 36,000 s |
| Reaction-to-distillation | 4,800,000 | 640,000 | 48,000 | 7,200 s | 72,000,000 | 9,600,000 | 720,000 | 36,000 s |
| **Combined** | — | — | — | — | **180,000,000** | **24,000,000** | **1,800,000** | **99,000 s (27.5 h)** |

The topology upper bound assumes each same-seed triplet runs at the configured concurrency of three,
all five seed triplets run sequentially, and every cell reaches its wall limit. It excludes queueing
and provider outages. Observed task-wall sum was 12.0% of this bound. Formal ETA cannot be frozen by
scaling this campaign until the number of worlds, provider repeats, method axes and optional
matched-evidence cells are decided.

## DeepSeek qualification cost boundary

DeepSeek qualification is platform evidence and is outside the 45-cell scientific denominator.
Using the provider's 2026-08-09 listed `deepseek-v4-flash` rates per one million tokens (cache hit
USD 0.0028, cache miss USD 0.14, output USD 0.28), the retained qualification-v1 usage costs:

`2.403456M x 0.0028 + 0.087038M x 0.14 + 0.043647M x 0.28 = USD 0.0311362`.

The qualification-v2 accounting envelope is 2.75M total input, at most 0.32M uncached input and
0.05M output. A ledger that exactly reaches all three limits corresponds to USD 0.065604. Because
these limits are audited at the harness boundary rather than enforced as a provider-side spend cap,
the defensive all-cache-miss cost at the total-input/output caps is USD 0.399. Pricing must be
resolved again on the execution date from the [official DeepSeek pricing page](https://api-docs.deepseek.com/quick_start/pricing).

Qualification-v2 permits one model call, one persistent session, concurrency one and zero
finalization retries. The executed cell used 2.031397M input tokens (1.944704M cached and 0.086693M
uncached) and 0.038993M output tokens, corresponding to USD 0.0285002 at the execution-date rates.
It passed all qualification checks in 332.2 s. The user explicitly authorized the local credential
for this call; the credential remained ignored and untracked. Because its value appeared in chat
context, it should be revoked and rotated before any further provider execution.

## Formal power and retry freeze still required

The formal analysis should use world-level paired contrasts across the frozen prior arms. Mechanism
family and world need explicit variance components; participant/backend, session and their
interactions require either identifiable repeats or an acknowledged confounding boundary. Multiple
operations, checkpoints, prediction snapshots and endpoints within a world improve measurement but
do not increase the independent-world denominator.

Power simulation cannot be completed until the following inputs are frozen:

- W2-04: formal/public/private world counts, mechanism-family balance and world inclusion rules;
- W2-05: primary paired estimand, endpoint covariance, multiplicity and missing/right-censor rules;
- W2-06: participant backend/scaffold axes and whether provider/session repeats are estimand-bearing;
- W2-07: whether the optional matched-evidence probe enters a secondary matrix;
- provider operations: an explicit provider-attempt retry cap and a provider-side or pre-authorized
  monetary ceiling, rather than only an end-of-session token audit.

Early stopping remains limited to infrastructure or safety conditions, never the direction of an arm
contrast. A failed scientific cell is retained without replacement. An implementation repair during
qualification forces the affected qualification block to restart from its first frozen cell; it does
not change scientific denominators or pass rules.

## W2-07 completion boundary

This draft completes the measured resource/cost baseline only. W2-07 remains `DOING` until it freezes
worlds, replicates, provider repeats, maximum provider calls, the formal campaign resource card,
token/currency/wall/concurrency/retry budgets, the formal power calculation and a full execution ETA.
