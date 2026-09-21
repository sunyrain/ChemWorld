# P completed-cohort analysis

Descriptive development evidence; five world clusters, one session per arm

Complete chains 14/15; final-assayed source batches 178/180; posttests 45/45; retests 15/15.

Each arm contains five worlds. Purity and recovery are separate outcomes. Recovery is relative to the original reactant charge.
Batch lifecycle totals: {'discarded': 2, 'final_assayed': 178, 'started': 180}.

| Arm | Prediction n | Purity MAE | Recovery MAE | Purity coverage80 | Recovery coverage80 | Purity-eligible retests | Mean recovery, all retests |
|---|---:|---:|---:|---:|---:|---:|---:|
| Aligned | 5/5 | 0.18830 | 0.06865 | 53.3% | 51.7% | 3/5 | 0.04455 |
| MisIndexed | 5/5 | 0.25078 | 0.07271 | 50.0% | 53.3% | 0/5 | 0.32105 |
| Opaque | 5/5 | 0.22396 | 0.06677 | 51.7% | 56.7% | 0/5 | 0.12373 |

## Paired prior contrasts

| Comparison | Metric | First lower MAE / all pairs | Mean difference | First lower MAE / conforming pairs | Conforming mean difference |
|---|---|---:|---:|---:|---:|
| Aligned minus Opaque | purity | 3/5 | -0.03566265988349913 | 2/4 | -0.020603997459014235 |
| Aligned minus Opaque | recovery | 2/5 | 0.0018788263538479816 | 1/4 | 0.00493186627564331 |
| MisIndexed minus Opaque | purity | 2/5 | 0.0268201732436816 | 1/4 | 0.07284043394029141 |
| MisIndexed minus Opaque | recovery | 2/5 | 0.0059343579920133 | 1/4 | 0.016803475637237233 |
| Aligned minus MisIndexed | purity | 3/5 | -0.062482833127180726 | 3/5 | -0.062482833127180726 |
| Aligned minus MisIndexed | recovery | 2/5 | -0.004055531638165319 | 2/5 | -0.004055531638165319 |

## Intervention directions

Directions use the fixed 0.02 resolution. Correct small-effect predictions are reported separately from resolved contrasts; query endpoints are not independent worlds.

| Arm | Factor | Metric | Correct / all | Correct / resolved | Correct / small effect |
|---|---|---|---:|---:|---:|
| Aligned | concentration | purity | 5/5 | 0/0 | 5/5 |
| Aligned | concentration | recovery | 5/5 | 0/0 | 5/5 |
| Aligned | extractant | purity | 3/5 | 3/5 | 0/0 |
| Aligned | extractant | recovery | 2/5 | 2/5 | 0/0 |
| Aligned | phase_ratio | purity | 1/5 | 1/5 | 0/0 |
| Aligned | phase_ratio | recovery | 2/5 | 2/5 | 0/0 |
| Aligned | upstream_time | purity | 3/5 | 3/5 | 0/0 |
| Aligned | upstream_time | recovery | 3/5 | 3/5 | 0/0 |
| Aligned | wash_staging | purity | 1/5 | 0/0 | 1/5 |
| Aligned | wash_staging | recovery | 5/5 | 0/0 | 5/5 |
| Aligned | washing | purity | 3/5 | 3/5 | 0/0 |
| Aligned | washing | recovery | 4/5 | 4/5 | 0/0 |
| MisIndexed | concentration | purity | 4/5 | 0/0 | 4/5 |
| MisIndexed | concentration | recovery | 5/5 | 0/0 | 5/5 |
| MisIndexed | extractant | purity | 1/5 | 1/5 | 0/0 |
| MisIndexed | extractant | recovery | 0/5 | 0/5 | 0/0 |
| MisIndexed | phase_ratio | purity | 0/5 | 0/5 | 0/0 |
| MisIndexed | phase_ratio | recovery | 3/5 | 3/5 | 0/0 |
| MisIndexed | upstream_time | purity | 3/5 | 3/5 | 0/0 |
| MisIndexed | upstream_time | recovery | 3/5 | 3/5 | 0/0 |
| MisIndexed | wash_staging | purity | 0/5 | 0/0 | 0/5 |
| MisIndexed | wash_staging | recovery | 4/5 | 0/0 | 4/5 |
| MisIndexed | washing | purity | 3/5 | 3/5 | 0/0 |
| MisIndexed | washing | recovery | 4/5 | 4/5 | 0/0 |
| Opaque | concentration | purity | 5/5 | 0/0 | 5/5 |
| Opaque | concentration | recovery | 5/5 | 0/0 | 5/5 |
| Opaque | extractant | purity | 4/5 | 4/5 | 0/0 |
| Opaque | extractant | recovery | 1/5 | 1/5 | 0/0 |
| Opaque | phase_ratio | purity | 2/5 | 2/5 | 0/0 |
| Opaque | phase_ratio | recovery | 2/5 | 2/5 | 0/0 |
| Opaque | upstream_time | purity | 3/5 | 3/5 | 0/0 |
| Opaque | upstream_time | recovery | 3/5 | 3/5 | 0/0 |
| Opaque | wash_staging | purity | 1/5 | 0/0 | 1/5 |
| Opaque | wash_staging | recovery | 5/5 | 0/0 | 5/5 |
| Opaque | washing | purity | 2/5 | 2/5 | 0/0 |
| Opaque | washing | recovery | 5/5 | 5/5 | 0/0 |

## Computation accounting

Usage available for 15/15 effective cells and complete for 15/15. Reported totals: input 17,474,996, cached input 14,912,768, uncached input 2,562,228, output 286,221 tokens.

Effective chains only; missing usage and abandoned attempts are not zero cost. Pilot and superseded-block costs remain separate in analysis.json.

| Stage | Cells with timing | Mean seconds | Sum of worker seconds |
|---|---:|---:|---:|
| source | 15/15 | 286.4 | 4296.7 |
| K1 | 15/15 | 92.0 | 1380.7 |
| Q | 15/15 | 98.8 | 1482.6 |
| K2 | 15/15 | 51.5 | 772.2 |
| retest | 15/15 | 0.8 | 11.6 |

Worker seconds overlap under concurrent execution and are not elapsed calendar time. Stage totals exclude pilot, qualification and earlier superseded matrices.

## Scope and retained limitations

- The independent unit is a world cluster, not each queried metric or interval.
- Prior effects include adaptive experiment-selection differences. One session per condition does not isolate direct inference effects or stochastic session variance.
- Primary descriptive means retain all valid planned responses, including sources with fewer than twelve final assays. Paired sensitivity results require both chains to conform; they do not erase the nonconforming source or its resource use.
- Quality eligibility is retest purity >=0.80. The unconditional recovery mean must be read together with quality eligibility; it is not a quality-adjusted score.
- The corrected qualification's 60 fixed Opaque reference batches are reused. Their single keyed observations are prediction targets; replays are not additional noisy repeats.
- Wash staging and concentration are retained small-effect controls. Their inclusion does not establish strong mechanistic discrimination.
- K1 and K2 require qualitative claim/evidence analysis. No mechanistic correctness or information-loss score is inferred from numerical prediction alone.
- Integration pilots, the invalid 12-batch pre-correction pilot, deterministic regressions, qualification batches and interrupted attempts remain separate costs in the machine-readable analysis.

## Failures

```json
[
  {
    "id": "P-W05-B12-E-Opaque",
    "status": "failed",
    "failure": null,
    "source_validation": {
      "batch_count": false,
      "exact_replay": true,
      "execution": true,
      "inventory": true,
      "resource_ledger": true
    },
    "batch_accounting": {
      "discarded": 2,
      "discarded_batches": [
        {
          "lifecycle_index": 1,
          "reason": "Irrecoverable empty phases after phase selection removed the reactant-containing liquid."
        },
        {
          "lifecycle_index": 2,
          "reason": "Extraction constitution failed and organic selection removed product-bearing reactor liquid."
        }
      ],
      "final_assayed": 10,
      "started": 12
    }
  }
]
```

Machine-readable per-world contrasts, token availability and retained failures are in [analysis.json](analysis.json). All cell reports are linked from [REPORT.md](REPORT.md).
