# Work II W2-07 resource, cost and power audit

Date: 2026-08-10. Status: formal resource topology frozen; currency ceiling and qualified expected
ETA remain open. This report does not authorize formal data collection. The machine-readable source
of truth is `work-ii-analysis-power-audit.json`.

## Current decision

The 25 independent task×world clusters provide 75 matched participant cells across opaque,
aligned-nominal and misindexed-nominal prior arms. The one-sided task-fixed-effect planning audit
has power 0.8946 at standardized effect 0.6 and an 80% MDE of 0.5150. It supports only
moderate-to-large effects. Operations, experiments, checkpoints, queries, provider repeats and
blind executions are nested observations, not additional independent samples.

W2-06 is now a completed execution-contract freeze. Each cell has one campaign-scoped Codex
process, one accepted provider session/model call, one host-owned MCP loop and one shared campaign
resource ledger. Checkpoints and the final recommendation remain in that session. There is no
automatic action repair or closeout. W2-10 still owns the separate final real-provider method
qualification receipt.

## Frozen five-task CampaignResourceCards

Every accepted cell schedules four complete experiments and checkpoints after 0, 1, 2 and 4
completed experiments.

| Task | Ops | Vessels | Assays | Non-final instruments | Process time | Wall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Electrochemical conversion | 28 | 4 | 4 | 0 | 72,000 s | 5,400 s |
| Reaction-to-crystallization | 56 | 4 | 4 | 8 | 146,400 s | 7,200 s |
| Reaction-to-distillation | 56 | 4 | 4 | 8 | 202,080 s | 7,200 s |
| Partition discovery | 48 | 4 | 4 | 8 | 9,000 s | 7,200 s |
| Safety-constrained reaction | 40 | 4 | 4 | 4 | 36,480 s | 7,200 s |

Each card carries its task-specific stock caps, repeat caps, implicit quench/filter time and explicit
process-time formula. Closeout is participant-owned: the final-assay path reserves two operations
per planned batch (`terminate` then `final_assay`), while explicit discard requires one. Across four
batches these reference reserves are eight and four operations respectively. They are advisory
within the shared hard card; no hidden allocation or host closeout changes the participant budget.

## Matrix resource bounds

The accepted-cell envelope is:

- 75 provider sessions/model calls, 300 complete experiments and 3,420 operation attempts;
- 300 vessel starts, 300 final assays and 420 non-final instrument uses;
- 324,000,000 input, 43,200,000 uncached input and 3,240,000 output tokens;
- 25 sequential same-world prior triplets at concurrency three, with a 47.5 h wall-time limit.

One pure-infrastructure resume is allowed only before a persisted scientific trajectory. If every
cell exhausted that allowance, the host-process/model-call hard cap would be 150, token caps would
be 648,000,000 input, 86,400,000 uncached input and 6,480,000 output, and the serial wall hard cap
would be 95 h. A scientific/method failure or any persisted trajectory is retained and cannot be
replaced.

MCP tool calls, operation attempts, committed operations, complete experiments, cells and blind
executions are separate denominators. MCP calls have no independent numeric hard cap because status,
history and artifact inspection calls are not physical operations; their actual count comes from
the per-session MCP receipt. They remain indirectly bounded by the fixed token and wall limits.

## Variance and confounding boundary

- World cluster is the independent random sampling unit within task.
- Task/mechanism is a five-level fixed effect and heterogeneity axis.
- Prior arm is paired within each world cluster.
- Model and scaffold have one frozen level, so method version is confounded with that level and no
  cross-model generalization is allowed.
- One provider session and one provider repeat are nested within each cell; their variance cannot be
  estimated separately.
- Task×prior heterogeneity is estimable, but model×session interaction is not.

## Historical development calibration

The retained earlier three-task development campaign completed 44/45 cells and 176/180 experiments,
with 59,414,461 input tokens, 6,589,885 uncached input tokens, 406,611 output tokens and 11,850.3 s
of summed task wall time. It remains an engineering baseline only. It cannot calibrate the final
expected ETA because it used a different incomplete task breadth and is not the final qualified
formal method. The retained DeepSeek seed-0 qualification likewise remains provider/harness
development evidence outside the formal scientific denominator.

## Remaining W2-07 blockers

W2-07 remains `DOING` for exactly two reasons:

1. no user-approved formal currency hard ceiling exists, and WellAU attributable pricing remains
   unknown rather than zero;
2. the expected (not merely worst-case) ETA must be calibrated from the final current-method W2-10
   qualification receipt.

Early stopping remains limited to infrastructure or safety conditions, never result direction.
