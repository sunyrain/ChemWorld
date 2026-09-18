# EC and PA: five worlds, two budgets, three prior arms

[Fixed design and preparation incident](../../WORK_II_EC_PA_FIVE_WORLD_NOTE.md).

Status: **running**. Model: GPT-5.6 Sol / medium. English protocol.

Sources attempted: 3/102; completed: 3. Source batches: 36/1764; posttests: 9/306.

Reference batches: 120/120; operations: 900/900. Exact replay and EC recommendation retests are additional.
Additional verification operations after preparation corrections: 108.

E: 90 sources / 1,620 planned batches / 270 posttests. The EC P/S pilot, if enabled, follows all E sources: 12 sources / 144 batches / 36 posttests.

First-attempt completions: 1; network recovery attempts: 2. Additional source attempts: 1; additional posttest attempts: 6. Completion totals above include separately recorded recoveries. The table retains first-attempt outcomes.

| Unit | Status | Batches | Posttests | English output |
| --- | --- | ---: | ---: | --- |
| [EC-W01-B12-discovery-E-Opaque](EC-W01-B12-discovery-E-Opaque/REPORT.md) | completed | 12/12 | 3/3 | True |
| [EC-W01-B12-discovery-E-Aligned](EC-W01-B12-discovery-E-Aligned/REPORT.md) | failed | 12/12 | 0/3 | None |
| ↳ [Network recovery](EC-W01-B12-discovery-E-Aligned/network-recovery/REPORT.md) | completed (posttests) | 12/12 | 3/3 | True |
| [EC-W01-B12-discovery-E-MisIndexed](EC-W01-B12-discovery-E-MisIndexed/REPORT.md) | failed | 0/12 | 0/3 | None |
| ↳ [Network recovery](EC-W01-B12-discovery-E-MisIndexed/network-recovery/REPORT.md) | completed (fresh_source) | 12/12 | 3/3 | True |
| EC-W01-B12-optimization-E-Opaque | running | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-E-Aligned | not_started | 0/12 | 0/3 |  |
| EC-W01-B12-optimization-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| PA-W01-B12-discovery-E-Opaque | not_started | 0/12 | 0/3 |  |
| PA-W01-B12-discovery-E-Aligned | not_started | 0/12 | 0/3 |  |
| PA-W01-B12-discovery-E-MisIndexed | not_started | 0/12 | 0/3 |  |
| EC-W01-B24-discovery-E-Opaque | not_started | 0/24 | 0/3 |  |
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
  "stage": "source",
  "completed_sources": 3,
  "planned_sources": 102,
  "elapsed_s": 703.25,
  "sources_per_hour": 7.628126030768373,
  "eta_s": 46721.82899999886,
  "phase": "K2",
  "unit": "EC-W01-B12-optimization-E-Opaque",
  "operations": 0,
  "batches": 0,
  "planned_batches": 12
}
```

All failures remain in the planned denominator. No result-based retries or substitutions. Single observations per cell do not establish general budget effects.
