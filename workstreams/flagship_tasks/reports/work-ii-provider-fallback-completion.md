# Work II three-task provider fallback completion

Date: 2026-08-10. Status: development execution complete; not formal or held-out evidence.

## Decision

DeepSeek was attempted first under the frozen persistent-Codex-session contract. Each task reached
its frozen stop condition, so no further DeepSeek cells were launched and no failed cell was
replaced for a more favorable outcome. The pre-authorized WellAU matrices are therefore the
coverage source for the requested three tasks x three prior arms x five world seeds.

## DeepSeek attempts

| Task | Scheduled in launched block | Terminal records | Qualified cells | Complete experiments | Operation attempts | Committed | Exact replay | Resource rejections | Recovered MCP failures | Provider errors | Stop reason |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Electrochemical conversion | 15 | 12 | 11 | 48 / 60 | 300 | 299 | 12 / 12 started | 1 | 0 | 0 | Seed-3 misindexed crossed the frozen no-resource-rejection gate; seed 4 was not started. |
| Reaction-to-crystallization | 15 | 6 | 5 | 21 / 60 | 222 | 220 | 6 / 6 started | 0 | 3 | 0 | Seed-1 misindexed crossed the one-recovered-MCP-failure ceiling; seeds 2--4 were not started. |
| Reaction-to-distillation pilot | 3 | 3 | 2 | 9 / 12 | 98 | 98 | 3 / 3 started | 0 | 3 | 0 | Seed-0 aligned crossed the one-recovered-MCP-failure ceiling; five-seed expansion was not authorized. |
| **Combined attempted** | **33** | **21** | **18** | **78 / 132 launched-block maximum** | **620** | **617** | **21 / 21 started** | **1** | **6** | **0** | **DeepSeek route terminal; fallback selected.** |

The crystallization terminal cell first omitted `decision_audit` from a `step`, recovered, and
later issued another schema-invalid `step` with `decision_audit` present. The exact nested field is
not recoverable from the deliberately sanitized receipt. The distillation terminal cell likewise
recovered from an early `step` that omitted `decision_audit`, then submitted an invalid typed belief
snapshot. Both failures were rejected locally in less than one millisecond. They had zero provider
error events, zero resource rejection and exact replay of every committed operation, so they are
agent--tool contract reliability failures rather than network, context-window or chemical-device
failures. Incomplete interrupted turns do not emit `turn.completed`; their zero token fields mean
usage unavailable, not zero consumption.

DeepSeek machine artifacts:

- `runs/development/work-ii-deepseek-electrochemical-five-seed-envelope-v4/matrix_report.json` —
  SHA-256 `a7bfd5f77c957b31139237ce7acec69413fc419163efe5202eef1358931a23b3`.
- `runs/development/work-ii-deepseek-crystallization-five-seed-guarded-5c4254f3/matrix_report.json`
  — SHA-256 `73ef1e513afefd314fb781dff1c5ac3b890ebbc2b7cd26790748b9af85305405`.
- `runs/development/work-ii-deepseek-distillation-seed0-pilot-guarded-c78be460/matrix_report.json`
  — SHA-256 `8d826106727f21782621c82bca97730f984da10b154137929decc6006d481ed1`.

## WellAU fallback coverage

Every one of the 45 scheduled task-by-prior-by-seed cells reached a terminal state. “Terminal” is
kept distinct from “completed”: the retained distillation failure is part of the denominator and
is not replayed or replaced.

| Task | Scheduled terminal cells | Completed cells | Complete experiments | Operation attempts | Exact replay | Resource rejections |
|---|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 15 / 15 | 15 / 15 | 60 / 60 | 367 | 15 / 15 | 0 |
| Reaction-to-crystallization | 15 / 15 | 15 / 15 | 60 / 60 | 663 | 15 / 15 | 0 |
| Reaction-to-distillation | 15 / 15 | 14 / 15 | 56 / 60 | 517 | 14 / 15 | 0 |
| **Combined** | **45 / 45** | **44 / 45** | **176 / 180** | **1,547** | **44 / 45** | **0** |

The sole fallback failure is reaction-to-distillation, world seed 4, aligned nominal. Its provider
turn completed without a provider error but emitted explanatory text instead of an MCP call; it
therefore has zero physical operations, experiments or checkpoints. The failure is retained as a
participant/harness outcome under the frozen rule.

WellAU machine artifacts:

- `runs/development/work-ii-electrochemical-five-seed-20260808T184013/matrix_report.json` —
  SHA-256 `61793dbedcb34046e2e4011469d3eb97524458c05dff839bca4465a824bdf91a`.
- `runs/development/work-ii-crystallization-five-seed-rerun2/matrix_report.json` — SHA-256
  `3baa5e5edf763c3fb54f59445eb6ff7b8c6c71c90ee21396e34ee6aed5113d52`.
- `runs/development/work-ii-distillation-five-seed-run1/matrix_report.json` — SHA-256
  `26c57db3b774a1ffe24be6f5a67c537974f82ac92c448babfa5f9fe793077b8f`.

## Scope

This closes the requested development provider campaign. It does not by itself complete the Work
II public formal matrix, private sealed confirmation or manuscript-level scientific claims. The
authoritative scientific denominator for any later analysis must preserve the 45 scheduled
terminal cells and the one retained failed cell.
