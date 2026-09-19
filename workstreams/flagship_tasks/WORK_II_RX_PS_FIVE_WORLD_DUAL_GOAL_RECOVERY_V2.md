# Work II RX-P/S five-world dual-goal recovery v2

Status: authorized recovery correction, 2026-09-19.

This note inherits every scientific and information-boundary rule in
[recovery v1](WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V1.md) and changes one
operational value plus the write-once output namespaces.

Recovery v1 set `public_numerics --limit 512`. The calculator executable enforces a hard
range of `1..256`, so its first repaired Q could not initialize the MCP server. The attempt
ended before a provider response, calculator call, laboratory action, or scientific output.
Its log, manifest, validation, and failed receipt remain preserved.

Recovery v2 uses the executable's maximum legal value, `--limit 256`. Repaired posttests are
written to `posttest-repair-v2/`, the zero-action source rerun to `source-repair-v2/`, and the
aggregate recovery state to `recovery-v2/`. No recovery-v1 artifact is overwritten.

The repair targets remain exactly:

- Q then K2 for `RX-W01--S--mechanism_discovery--Opaque`;
- Q then K2 for `RX-W01--S--safety_constrained_optimization--MisIndexed`;
- K1 then Q then K2 for `RX-W02--P--mechanism_discovery--MisIndexed`;
- a separate write-once rerun of the zero-action
  `RX-W02--P--safety_constrained_optimization--Opaque` cell;
- then the 44 never-started frozen cells in their original order.

Prompts, schemas, twelve queries per locus, prior arms, model, reasoning effort, source
conditions, deterministic seeds, truth embargo, and completion criteria are unchanged.
