# Work II DeepSeek recovery-amended full development results

Date: 2026-08-10. Status: complete development experiment; not formal or held-out evidence.

Machine analysis:
`workstreams/flagship_tasks/reports/work-ii-deepseek-recovery-amended-analysis-v0.1.json`.
Source manifest:
`configs/benchmark/work_ii_deepseek_recovery_amended_analysis_sources_v0.1.json`.

## Execution result

The frozen recovery amendment was executed from a clean committed checkout with DeepSeek
`deepseek-v4-flash`, high reasoning, one persistent Codex session per cell and three concurrent
prior arms within each world seed. Every task restarted from seed 0 in a new immutable run root.

| Task | Terminal cells | Completed cells | Complete experiments | Attempts / committed | MCP tool failures | Provider errors | Resource rejects | Exact replay | Matrix wall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Electrochemical conversion | 15/15 | 15/15 | 60/60 | 373 / 372 | 13 | 0 | 0 | 15/15 | 1,891.5 s |
| Reaction to crystallization | 15/15 | 13/15 | 54/60 | 606 / 605 | 18 | 0 | 0 | 15/15 | 2,136.2 s |
| Reaction to distillation | 15/15 | 15/15 | 60/60 | 637 / 637 | 7 | 0 | 0 | 15/15 | 2,321.7 s |
| **Combined** | **45/45** | **43/45** | **174/180** | **1,616 / 1,614** | **38** | **0** | **0** | **45/45** | **6,349.4 s** |

All 15 task-by-seed clusters reached a three-arm terminal denominator; 13/15 clusters completed all
three arms. The two incomplete cells remain in the denominator and were not replayed or replaced.

## Retained failures

Both failures occurred in crystallization and are participant--tool contract outcomes rather than
provider, network, resource or physical-device failures.

- Seed 3, misindexed nominal: zero complete experiments and two operation attempts. Three
  consecutive MCP failures crossed the frozen consecutive ceiling of one.
- Seed 4, opaque: two complete experiments and 24 operation attempts. Four total MCP failures
  crossed the frozen per-cell ceiling of three; maximum consecutive failures remained one.

Both cells had zero provider error events and zero resource rejection. Every terminal trajectory,
including the completed prefixes of the failed cells, passed exact physical/resource replay.

## Descriptive prior-arm results

Each value below is the mean paired world-seed difference in best observed endpoint score. These are
development summaries without formal tests or confidence intervals.

| Task | Aligned minus opaque | Positive seeds | Misindexed minus opaque | Positive seeds |
|---|---:|---:|---:|---:|
| Electrochemical conversion | +0.0785, n=5 | 2/5 | +0.0915, n=5 | 3/5 |
| Reaction to crystallization | +0.0305, n=5 | 4/5 | +0.0690, n=4 | 3/4 |
| Reaction to distillation | +0.0374, n=5 | 5/5 | +0.1080, n=5 | 5/5 |

The explicit-prior arms changed endpoint behavior, but the result is not the expected simple ranking
`aligned > opaque > misindexed`. Misindexed information was often as helpful as or more helpful than
aligned information, most clearly in distillation. Endpoint improvement therefore cannot be treated
as evidence that the supplied prior was correct, that the hidden law was recovered, or that a wrong
prior was rejected.

## Belief-signal audit

The mean paired aligned-minus-misindexed change in self-reported prior reliability was +0.024 in
electrochemical conversion (n=5), -0.005 in crystallization (n=4) and +0.030 in distillation (n=5).
These small heterogeneous differences do not separate correct from wrong prior use.

Final explicit misindex warnings were even less specific:

| Task | Opaque | Aligned nominal | Misindexed nominal |
|---|---:|---:|---:|
| Electrochemical conversion | 0/5 | 5/5 | 3/5 |
| Reaction to crystallization | 0/4 | 5/5 | 4/4 |
| Reaction to distillation | 0/5 | 5/5 | 5/5 |

The model largely treated the presence of a nominal dossier as suspicious, rather than selectively
identifying a misindexed dossier. A verbal warning is therefore not a valid bias-rejection endpoint.

## Token and cost audit

Provider-reported usage totals were 168,314,516 input tokens, including 163,415,168 cached and
4,899,348 uncached tokens, plus 1,787,773 output tokens. The aggregate input cache-hit ratio was
97.09%; cached input is reused context, not repeated generated output. At the DeepSeek rates frozen
in the 2026-08-10 experiment record, the reconstructed API cost is USD 1.64405: USD 0.45756 cached
input, USD 0.68591 uncached input and USD 0.50058 output.

## Claim boundary

This block supports the development observation that explicit prior conditions can strongly reshape
experimental behavior and endpoints, while current belief self-reports do not reliably distinguish
aligned from misindexed information. It does not establish law discovery, calibrated wrong-prior
rejection, held-out prediction, transfer, a DeepSeek-versus-WellAU model advantage, or a formal causal
effect. Those claims require evaluator-truth scoring, blind recommendation replay and the frozen
public/private formal programme.
