# EQ bounded-equilibrium block - final execution status

Date: 2026-09-20  
Evidence class: development  
Status: complete; all public reports and evaluations exported

## Final denominator

The frozen EQ-P v2 block contains five physical worlds and three information arms (Opaque, Aligned, and MisIndexed), for 15 independent characterization sessions. Every session used twelve source batches followed by the fixed K1 -> Q -> K2 -> EQS sequence.

| Item | Completed | Planned |
|---|---:|---:|
| Independent source sessions | 15 | 15 |
| Source batches | 180 | 180 |
| Sealed posttests | 60 | 60 |
| Complete posttest chains | 15 | 15 |
| Provider-free reference executions | 300 | 300 |
| Public per-cell reports | 15 | 15 |

All effective results have status `completed`, all 15 posttest chains validate, and the final failure list is empty. Reference truth was generated only after every EQS response was sealed. The environment-derived equilibrium-confidence field was not used as Agent uncertainty or as a score.

## Public result package

The complete sanitized package is in [`v2-public`](v2-public/):

- [`REPORT.md`](v2-public/REPORT.md) is the aggregate report.
- [`INDEX.json`](v2-public/INDEX.json) records all 15 effective cells and final denominators.
- [`sources/`](v2-public/sources/) contains each cell's sanitized `RESULT.json` and English `EXPERIMENT_REPORT.md`, including the twelve observed batches, sealed K1/Q/K2/EQS payloads, prediction evaluation, and post-embargo reference truth.
- [`worlds/`](v2-public/worlds/) provides one index per physical world.
- [`RECOVERY_AUDIT.json`](v2-public/RECOVERY_AUDIT.json) records the effective retained attempt for every cell.
- [`audits/`](v2-public/audits/) contains the provider-free gate and runtime-transition evidence.

Authentication material, raw provider event streams, session identifiers, private Provider state, and usage accounting are excluded from the package.

## Runtime transition

The execution changed to the integrated runtime at commit `a80b156619a11e133fd68000e4c2c062f4e1dfcf` only after recovery attempt 01 had stopped and before any attempt 02 Provider call. The transition retained all prior attempts and did not change the scientific contract, world parameters, prompts, model, or scoring.

The transition audit reports:

- 39 focused tests passed;
- 15/15 provider-free gate campaigns and 180/180 batches passed;
- 15/15 trajectories replayed exactly;
- the scientific gate payload was exactly equal after excluding elapsed time;
- Provider calls during validation were zero; and
- elapsed time fell from 840.40 seconds to 146.01 seconds (about 5.75x faster).

In the final W02 MisIndexed recovery, the optimized runtime completed all twelve source batches and 72 recorded operations before the unchanged K1/Q/K2/EQS chain. Model-generation time remained the dominant cost of the posttests.

## Retained recovery history

Earlier startup, transport, timeout, capacity, and interrupted-attempt records remain in the private write-once run namespace. They are not counted as additional scientific samples. The final effective result for each cell is identified in the public recovery audit, while private credentials and raw provider state remain excluded.

## Exporter provenance

The frozen v2 report wrapper contained a rendering-only recursive-dispatch defect discovered after scientific completion. The frozen file was left unchanged. `scripts/export_work_ii_eq_bounded_equilibrium_reports_v2_1.py` fixes only wrapper dispatch by retaining stable references to the legacy renderers; it does not modify source results, sealed responses, predictions, truth, or scores. The regression test is `tests/test_export_work_ii_eq_bounded_equilibrium_reports_v2_1.py`.
