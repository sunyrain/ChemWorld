# EC and PA: five worlds, two budgets, three prior arms

[Fixed design and preparation incident](../../WORK_II_EC_PA_FIVE_WORLD_NOTE.md).

Status: **running**. Model: GPT-5.6 Sol / medium. English protocol.

Sources attempted: 10/102; completed: 9. Current logical-source batches: 127/1764; posttests: 27/306.
Physical source final assays across all attempts: 127. Interrupted and replacement attempts are both charged.

Reference batches: 120/120; operations: 900/900. Exact replay and EC recommendation retests are additional.
Additional verification operations after preparation corrections: 245.

E: 90 sources / 1,620 planned batches / 270 posttests. The EC P/S pilot, if enabled, follows all E sources: 12 sources / 144 batches / 36 posttests.

First-attempt completions: 7; infrastructure recovery attempts: 2 (host-reboot replacements: 0). Additional source attempts: 1; additional posttest attempts: 6. Completion totals above include separately recorded recoveries. The table retains first-attempt outcomes.

| Unit | Status | Batches | Posttests | English output |
| --- | --- | ---: | ---: | --- |
| [EC-W01-B12-discovery-E-Opaque](EC-W01-B12-discovery-E-Opaque/REPORT.md) | completed | 12/12 | 3/3 | True |
| [EC-W01-B12-discovery-E-Aligned](EC-W01-B12-discovery-E-Aligned/REPORT.md) | failed | 12/12 | 0/3 | None |
| ↳ [Infrastructure recovery](EC-W01-B12-discovery-E-Aligned/network-recovery/REPORT.md) | completed (posttests) | 12/12 | 3/3 | True |
| [EC-W01-B12-discovery-E-MisIndexed](EC-W01-B12-discovery-E-MisIndexed/REPORT.md) | failed | 0/12 | 0/3 | None |
| ↳ [Infrastructure recovery](EC-W01-B12-discovery-E-MisIndexed/network-recovery/REPORT.md) | completed (fresh_source) | 12/12 | 3/3 | True |
| [EC-W01-B12-optimization-E-Opaque](EC-W01-B12-optimization-E-Opaque/REPORT.md) | completed | 12/12 | 3/3 | True |
| [EC-W01-B12-optimization-E-Aligned](EC-W01-B12-optimization-E-Aligned/REPORT.md) | completed | 12/12 | 3/3 | True |
| [EC-W01-B12-optimization-E-MisIndexed](EC-W01-B12-optimization-E-MisIndexed/REPORT.md) | completed | 12/12 | 3/3 | True |
| [PA-W01-B12-discovery-E-Opaque](PA-W01-B12-discovery-E-Opaque/REPORT.md) | completed | 12/12 | 3/3 | True |
| [PA-W01-B12-discovery-E-Aligned](PA-W01-B12-discovery-E-Aligned/REPORT.md) | completed | 12/12 | 3/3 | True |
| [PA-W01-B12-discovery-E-MisIndexed](PA-W01-B12-discovery-E-MisIndexed/REPORT.md) | completed | 12/12 | 3/3 | True |
| [EC-W01-B24-discovery-E-Opaque](EC-W01-B24-discovery-E-Opaque/REPORT.md) | failed | 19/24 | 0/3 | None |
| EC-W01-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W01-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W01-B24-optimization-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W01-B24-optimization-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W01-B24-optimization-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| PA-W01-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| PA-W01-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| PA-W01-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W02-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W02-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W02-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W02-B12-optimization-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W02-B12-optimization-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W02-B12-optimization-E-Opaque | not_started | 0/12 | 0/3 |  |
| PA-W02-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| PA-W02-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| PA-W02-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W02-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W02-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W02-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W02-B24-optimization-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W02-B24-optimization-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W02-B24-optimization-E-Opaque | not_started | 0/24 | 0/3 |  |
| PA-W02-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| PA-W02-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| PA-W02-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W03-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W03-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W03-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W03-B12-optimization-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W03-B12-optimization-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W03-B12-optimization-E-Aligned | not_started | 0/12 | 0/3 |  |
| PA-W03-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| PA-W03-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| PA-W03-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W03-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W03-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W03-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W03-B24-optimization-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W03-B24-optimization-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W03-B24-optimization-E-Aligned | not_started | 0/24 | 0/3 |  |
| PA-W03-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| PA-W03-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| PA-W03-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W04-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W04-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W04-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W04-B12-optimization-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W04-B12-optimization-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W04-B12-optimization-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| PA-W04-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| PA-W04-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| PA-W04-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W04-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W04-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W04-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W04-B24-optimization-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W04-B24-optimization-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W04-B24-optimization-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| PA-W04-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| PA-W04-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| PA-W04-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W05-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W05-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W05-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W05-B12-optimization-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W05-B12-optimization-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W05-B12-optimization-E-Opaque | not_started | 0/12 | 0/3 |  |
| PA-W05-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| PA-W05-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| PA-W05-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W05-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W05-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W05-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W05-B24-optimization-E-Aligned | not_started | 0/24 | 0/3 |  |
| EC-W05-B24-optimization-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| EC-W05-B24-optimization-E-Opaque | not_started | 0/24 | 0/3 |  |
| PA-W05-B24-discovery-E-Aligned | not_started | 0/24 | 0/3 |  |
| PA-W05-B24-discovery-E-MisIndexed | not_started | 0/24 | 0/3 |  |
| PA-W05-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
| EC-W01-B12-discovery-P-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-discovery-P-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-discovery-P-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-P-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-P-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-P-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-discovery-S-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-discovery-S-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-discovery-S-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-S-Opaque | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-S-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-S-MisIndexed | not_started | 0/12 | 0/3 |  |

## Live progress

```json
{
  "stage": "verify_host_interruption",
  "completed_sources": 10,
  "planned_sources": 102,
  "unit": "EC-W01-B24-discovery-E-Opaque",
  "elapsed_s": 6.797000000002299,
  "sources_per_hour": 7.2172910254544735,
  "eta_s": 45889.79422222264
}
```

All failures remain in the planned denominator. No result-based retries or substitutions. Single observations per cell do not establish general budget effects.
