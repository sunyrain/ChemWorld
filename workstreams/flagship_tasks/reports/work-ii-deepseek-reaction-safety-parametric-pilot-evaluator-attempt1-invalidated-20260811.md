# Invalidated reaction-safety parametric evaluator attempt 1

Date: 2026-08-11

The first zero-provider evaluator attempt completed 4/4 truth queries and the opaque arm's 6/6
blind replays, then stopped before the aligned arm because the shared blind-plan builder required
`summary.completed=true`. The aligned participant trajectory had 4/4 experiments, 4/4 checkpoints
and exact replay, but remained operationally unqualified because its maximum consecutive recovered
MCP failures was 2 against the frozen limit of 1.

This was an evaluator compatibility defect, not a participant or chemistry rerun condition. Attempt 1
produced no tracked scientific report, made zero provider calls and did not modify participant data.
The replacement evaluator keeps operational qualification failed, admits only development trajectories
that are independently terminal and exact-replayable, and forbids this override for formal cells. The
entire zero-provider evaluator is rerun from the first truth query under a fresh raw-output identity.
