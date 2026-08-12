# Work II A-E prior distinguishability qualification v0.2

Status: design frozen before any v0.2 environment execution. This note and the
standalone contract must not be changed after either cohort starts. The v0.1 note,
contract, report, thresholds, and unfavorable result remain historical evidence and
are neither edited nor overwritten by this block.

## Question and tested units

Can one outcome-blind eight-round diagnostic policy directly reach and distinguish the
two anonymously transposed material categories, under two frozen nuisance settings,
without being told the moved pair or a favorable region? The final matrix contains all
five A-E tasks. The scientific unit is a task x held-out world; each world contains
three independent eight-round policy replicates.

Construction and qualification are disjoint. Construction uses the five previously
exposed public worlds per task and is frozen at 25 task-worlds, 75 policy replicates,
and 600 primary executions. Its outcomes and failures are retained and reported, but
cannot modify this note, the contract, metric support, recipes, thresholds, or held-out
worlds. Held-out qualification uses 25 new task-worlds, 75 policy replicates, and 600
primary executions and is the only scientific admission denominator. The full run is
therefore 1,200 primary executions plus 1,200 tolerance-zero exact-replay checks.

The held-out seeds were generated before execution by taking the first eight SHA-256
bytes of
`work-ii-ae-prior-v0.2-heldout-qualification-20260812:<task_id>:<index>`, reducing
modulo 900,000,000, and adding 100,000,000. The exact seeds are stored in the standalone
contract. Construction seeds are also enumerated there.

## Frozen policy and nuisance coverage

The policy is given only the task and its categorical target field. It never receives
the target pair, descriptor permutation, observations, metric values, or region labels.
For each policy replicate it executes four categories once at nuisance anchor 0 and all
four once at nuisance anchor 1: exactly eight rounds and eight unique recipes. The two
anchors are outcome-blind deterministic hash-uniform complementary vectors in [0.15,
0.85], with the target coordinate overwritten by the category midpoint. The namespace,
algorithm, bounds, ordering, and recipe mapper are frozen in the contract. The hidden
analyzer alone uses the descriptor permutation after execution to test whether both
moved categories were actually visited at both anchors.

## Measurements and noise

All campaign-allowed metrics are collected and reported. A predeclared subset is the
decision-relevant, causally affected support used for thresholds; remaining allowed
metrics are reported separately as negative/control metrics and never dilute a support
average. The support and controls are fixed per task in the contract and cannot be
selected from observed outcomes.

Observation noise is independent but reproducible. Every phase x task x world x policy
replicate x anchor x category execution receives its own deterministic observation seed
and namespace. No left/right category comparison shares either value, so the design
noise covariance is zero. For each anchor and metric, the moved-category contrast uses
the three independent policy replicates on each side. Its uncertainty is the Welch
standard error `sqrt(sample_variance(left)/3 + sample_variance(right)/3)`. Support
separation is the mean absolute support contrast; single-metric separation is the
maximum absolute support contrast; aggregate uncertainty is the RMS of the support
metric standard errors; SNR is support separation divided by aggregate uncertainty
with a 1e-12 numerical floor. Controls receive the same contrast and uncertainty
reporting but no pass threshold.

## Pass, failure, and stop rules

An anchor passes only when every execution completes and replays exactly, all allowed
metrics are finite in [0,1], mean support separation is at least 0.05, maximum support
separation is at least 0.03, and support SNR is at least 2.0. A world passes only when
the blind reachability checks pass independently for all three policy replicates and
both nuisance anchors pass. A held-out task passes only if all five held-out worlds
pass; the matrix passes only if all five tasks pass. Construction status is shown but
cannot change the held-out or matrix decision.

All attempted executions, failures, support metrics, negative/control metrics, exact
replay outcomes, and exact denominators are retained in the machine report. There is no
result-directed retry, replacement, threshold change, metric-support change, task
deletion, or early stop. A platform fix invalidates the affected cohort and requires it
to restart at its first unit. No participant or model-provider calls are permitted.

Expected output: a plan, 1,200 execution receipts and trajectories, a readable JSON
report, and a Markdown summary in a new v0.2 output directory. This development runner
does not make the result formal or release-eligible.
