# P completed-cohort analysis

SUPERSEDED PLATFORM DIAGNOSTIC: aggregate scores below are not primary agent evidence. Descriptive development evidence; five world clusters, one session per arm

Complete chains 10/15; source batches 180/180; posttests 45/45; retests 10/15.

Each arm contains five worlds. Purity and recovery are separate outcomes. Recovery is relative to the original reactant charge.

| Arm | Prediction n | Purity MAE | Recovery MAE | Purity coverage80 | Recovery coverage80 | Purity-eligible retests | Mean recovery, all retests |
|---|---:|---:|---:|---:|---:|---:|---:|
| Aligned | 5/5 | 0.18049 | 0.05925 | 41.7% | 60.0% | 0/5 | 0.22196 |
| MisIndexed | 5/5 | 0.22331 | 0.08365 | 51.7% | 41.7% | 2/5 | 0.05169 |
| Opaque | 5/5 | 0.17863 | 0.08348 | 65.0% | 55.0% | 2/5 | 0.14205 |

## Paired prior contrasts

| Comparison | Metric | First lower MAE / pairs | Mean MAE difference |
|---|---|---:|---:|
| Aligned minus Opaque | purity | 1/5 | 0.0018581111828485958 |
| Aligned minus Opaque | recovery | 4/5 | -0.024229384263157846 |
| MisIndexed minus Opaque | purity | 2/5 | 0.04467182445128758 |
| MisIndexed minus Opaque | recovery | 2/5 | 0.00017343115379413326 |
| Aligned minus MisIndexed | purity | 3/5 | -0.04281371326843898 |
| Aligned minus MisIndexed | recovery | 4/5 | -0.024402815416951978 |

## Scope and retained limitations

- The independent unit is a world cluster, not each queried metric or interval.
- Prior effects include adaptive experiment-selection differences. One session per condition does not isolate direct inference effects or stochastic session variance.
- Quality eligibility is retest purity >=0.80. The unconditional recovery mean must be read together with quality eligibility; it is not a quality-adjusted score.
- The corrected qualification's 60 fixed Opaque reference batches are reused. Their single keyed observations are prediction targets; replays are not additional noisy repeats.
- Wash staging and concentration are retained small-effect controls. Their inclusion does not establish strong mechanistic discrimination.
- K1 and K2 require qualitative claim/evidence analysis. No mechanistic correctness or information-loss score is inferred from numerical prediction alone.
- Integration pilots, the invalid 12-batch pre-correction pilot, deterministic regressions, qualification batches and interrupted attempts remain separate costs in the machine-readable analysis.

## Failures

```json
[
  {
    "id": "P-W01-B12-E-Opaque",
    "status": "failed",
    "failure": null,
    "source_validation": {
      "batch_count": true,
      "exact_replay": true,
      "execution": true,
      "inventory": false,
      "resource_ledger": true
    }
  },
  {
    "id": "P-W01-B12-E-Aligned",
    "status": "failed",
    "failure": null,
    "source_validation": {
      "batch_count": true,
      "exact_replay": true,
      "execution": true,
      "inventory": false,
      "resource_ledger": true
    }
  },
  {
    "id": "P-W03-B12-E-MisIndexed",
    "status": "failed",
    "failure": null,
    "source_validation": {
      "batch_count": true,
      "exact_replay": true,
      "execution": true,
      "inventory": false,
      "resource_ledger": true
    }
  },
  {
    "id": "P-W04-B12-E-MisIndexed",
    "status": "failed",
    "failure": null,
    "source_validation": {
      "batch_count": true,
      "exact_replay": true,
      "execution": true,
      "inventory": false,
      "resource_ledger": true
    }
  },
  {
    "id": "P-W05-B12-E-Aligned",
    "status": "failed",
    "failure": null,
    "source_validation": {
      "batch_count": true,
      "exact_replay": true,
      "execution": true,
      "inventory": false,
      "resource_ledger": true
    }
  }
]
```

Machine-readable per-world contrasts, token availability and retained failures are in [analysis.json](analysis.json). All cell reports are linked from [REPORT.md](REPORT.md).
