# Work II staged-belief snapshot seed-2 qualification

Date: 2026-08-13. Status: protocol frozen; provider execution not started. This is a
development platform/method qualification block, not formal or publication evidence.

Question: Can a persistent provider session complete the frozen Work II campaign after the
one-shot belief payload is replaced by immutable staged submission, without losing scientific
content, changing checkpoint denominators, leaking evaluator truth, or allowing a partial draft to
count as a checkpoint?

Coverage: two already-qualified A-P tasks x three prior arms (opaque, aligned nominal and
misindexed nominal) x world seed 2 = 6 cells. Each cell contains 10 complete experiments and five
belief checkpoints at complete-experiment counts 0/2/4/7/10: 60 physical experiments and 30
finalized checkpoints in total. Every checkpoint uses `begin`, fixed ordered prediction pages,
fixed ordered law pages and `finalize`. The failed v0.10 one-shot block remains retained as
historical development evidence. This replacement block starts from its first cell and does not
reuse a partial cell, checkpoint or provider session. The task configs remain authoritative for
the exact checkpoint schedule, and focused tests bind this note's schedule to those configs.

Measurements: complete experiments; finalized checkpoints; accepted and rejected staged calls;
page IDs and exact query/metric denominators; immutable draft manifests/fragments; partial-draft
step rejection; canonical finalized snapshot equality with the existing parser; participant
recommendation; all physical/resource/provider/MCP failures; full resource accounting; exact
replay; and a readable machine summary with exact denominators. Draft fragments remain attached to
their session receipt but do not enter the checkpoint count. Evaluator truth and scoring feedback
are never exposed through staging.

Pass/failure and stop rules: the platform/method block qualifies only if all 6 cells reach terminal,
all 60 experiments and 30 checkpoints are present, each accepted page is immutable and exactly
matches its host-published IDs/order, `step` fails closed before `finalize`, finalized snapshots pass
the unchanged full parser, session receipts preserve all partial fragments, and exact replay and
resource checks pass. Page, platform, denominator, checkpoint and replay defects fail the block.
Provider/agent-invalid outcomes are measured and retained rather than silently repaired or removed;
if any such outcome prevents the block from reaching 60/60 experiments or 30/30 finalized
checkpoints, the qualification fails and cannot be interpreted as a platform pass. Any platform fix
restarts all six cells from the first cell. Stop immediately on an unsafe
event, missing/corrupt receipt, denominator drift, unexpected truth exposure, checkpoint bypass, or
an attempt to overwrite an accepted fragment. Do not change coverage or gates in response to the
outcome.

Expected outputs: six terminal cell receipts outside Git, one machine-readable qualification
summary reporting 6/6 cells, 60/60 experiments and 30/30 checkpoints plus every failure, and a short
human-readable conclusion. Raw provider responses, credentials, ignored run directories and local
caches remain outside Git.
