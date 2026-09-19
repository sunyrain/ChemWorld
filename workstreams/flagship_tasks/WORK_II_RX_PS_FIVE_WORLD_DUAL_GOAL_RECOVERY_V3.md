# Work II RX-P/S five-world dual-goal recovery v3

Status: authorized recovery correction, 2026-09-19.

This note inherits the scientific design and information boundaries of
[recovery v1](WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V1.md) and the legal
calculator-server limit correction in
[recovery v2](WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V2.md).

Recovery v2 successfully initialized `public_numerics` with its legal maximum of 256 calls,
restored the original thread, and began the first repaired Q. It was nevertheless stopped by a
separate inherited outer monitor that still treated more than eight calculator attempts as
`tool_budget_exceeded`. Fifteen calculator calls were retained, but there was no final Q payload
and therefore no sealed scientific answer. No laboratory tool was enabled, no source experiment
was added, and reference truth remained absent.

Recovery v3 sets both limits to 256:

- MCP calculator execution limit: 256;
- outer posttest tool-attempt monitor: 256.

The recovery always restores the archived original source thread, not the partial recovery-v1
or recovery-v2 continuation, so unsealed intermediate repair attempts are not fed into the new
answer. Artifacts use new write-once namespaces: `posttest-repair-v3/`, `source-repair-v3/`, and
`recovery-v3/`.

Repair targets, prompts, schemas, query rows, prior arms, model, reasoning effort, source
conditions, deterministic seeds, truth embargo, and completion criteria remain unchanged.
