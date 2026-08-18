# Work II multi-task open-action pilot experiment note

Status: development-only interface/scientific workflow pilot; not part of a formal denominator.

## Question

Can the same twelve-round open-action longitudinal decision protocol support complete-plan
ranking on three distinct Work II tasks, rather than only partition discovery? The pilot is meant
to expose task-specific schema, scoring-contract, and action-plan problems before any five-world
expansion.

## Frozen coverage

- Tasks: `electrochemical-conversion`, `reaction-to-crystallization`, and
  `reaction-safety-constrained`.
- One independent world per task, using world seed `0`.
- Three information arms per task: `opaque`, `aligned_nominal`, `misindexed_nominal`.
- One persistent agent session per arm; twelve participant-chosen experiments per session.
- Checkpoints after 0, 3, 6, 9, and 12 experiments.
- Eight deterministic candidate queries/plans per task-world. The complete ordered ActionPlan,
  parameters, initial-state contract, terminal assay, and omitted-operation declarations are
  public; outcomes, ranks, checkpoint truth, and other-arm evidence remain hidden.
- Terminal mode is ranking-only: the agent ranks the eight public plans and selects one; it is not
  asked to provide 32 numerical predictions.

## Measurements

For each arm, retain completion/failure class, committed experiment count, checkpoint status,
selected candidate rank, Top-1, raw and normalized regret, candidate score range, and final-law
normalized MAE. Also retain public/truth/executed plan hashes and task-specific metric IDs.

## Pass/failure and stop rules

Before provider execution, every checkpoint and candidate truth query must pass tolerance-zero
replay and public/truth plan binding. During provider execution, all three arms and all scheduled
experiments remain in the denominator; provider, schema, resource, scientific, and replay
failures are retained. No outcome-based candidate replacement or favorable rerun is allowed. A
platform repair affecting plan compilation, terminal parsing, or task wiring invalidates the
affected task block and requires rerunning that task from its first arm.

## Expected outputs

One development output directory per task containing the frozen campaign config, public packet,
truth/replay reports, three arm records, machine-readable summary, and a short Chinese report.
Results will be used only to decide which two tasks, if any, merit a five-world expansion.
