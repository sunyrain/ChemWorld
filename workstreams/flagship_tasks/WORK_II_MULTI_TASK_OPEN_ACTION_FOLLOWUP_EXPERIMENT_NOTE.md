# Work II multi-task open-action follow-up experiment note

Status: development-only follow-up; not part of a formal denominator.

## Question

After the one-world three-arm pilot, can the open-action ranking protocol be retained when the
resource contract is corrected for the observed stock-cushion failures, and does the fully
qualified safety-constrained task remain stable across five independent worlds?

## Frozen follow-up blocks

### Recovery block

- Tasks: `electrochemical-conversion` and `reaction-to-crystallization`.
- World: seed `0`, with the same three arms (`opaque`, `aligned_nominal`,
  `misindexed_nominal`), 12 participant experiments per arm, checkpoints `0/3/6/9/12`, and
  the same deterministic eight-candidate ranking-only terminal packet.
- The only changed execution contract is `resource_recovery_v1`: electrochemical solvent stock
  receives a fixed `+0.100 L` cushion and crystallization catalyst stock receives a fixed
  `+0.003 mol` cushion. These values cover the retained rejected requests with a documented
  margin; no candidate, scoring rule, checkpoint, arm, or pass/failure rule changes.
- The complete affected task block is rerun from its first arm. All resource rejections,
  provider/accounting failures, and incomplete cells remain in the denominator and are retained.

### Five-world extension block

- Task: `reaction-safety-constrained`.
- World seeds: `0, 1, 2, 3, 4`; three arms per world; 12 participant experiments per arm;
  checkpoints `0/3/6/9/12`; the same public complete ActionPlan packet and ranking-only terminal
  readout.
- The original pilot resource contract, candidate packet construction, measurements, and
  qualification rules are retained unchanged.
- The five worlds are executed as five independent three-arm clusters. No outcome-based seed or
  candidate replacement is permitted.

## Measurements and decision rules

Retain completion and failure class, committed experiment count, checkpoint status, selected
candidate rank, Top-1, raw and normalized regret, law normalized MAE, resource rejection count,
provider/accounting reconciliation, exact replay, and arm-by-world summaries. A task is eligible
for five-world interpretation only if every scheduled cell is complete and uncontaminated; a
scientific effect is interpreted from action rank/regret together with the mechanism readout, not
from law MAE alone.

## Expected outputs

Each block produces its own campaign configuration, public packet, truth/replay records, retained
cell records, machine-readable summary, progress log, and Chinese report. These outputs remain
development evidence until a later user-authorized release freeze.
