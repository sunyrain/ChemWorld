# Work II EQ final delivery — 2026-09-20

## Delivered scope

This delivery completes the authorized five-world EQ-S mechanism-characterization matrix and the separately authorized provider-free EQ-E multi-entity substrate gate. It does not start any EQ-E Agent session or bulk provider matrix.

## EQ-S final matrix

- Provider-free gate: 15/15 campaigns, 180/180 batches, 12/12 registered checks, zero provider calls.
- Agent matrix: 15/15 independent cells across five physical worlds and Opaque/Aligned/MisIndexed arms.
- Source evidence: 180/180 autonomous batches; every effective trajectory replayed exactly.
- Sealed posttests: 60/60 (`K1`, `Q`, `K2`, and `EQS`).
- Reference evaluation: 300/300 executions, released only after all EQS responses were sealed.
- Reports: 15 complete English session reports, five world indexes, one aggregate report, machine-readable results, gate summary, and recovery audit.

The first W01 canary retained a provider JSON-schema compatibility failure at EQS: the API rejected `uniqueItems` before model inference. Version v0.2.1 removed only that unsupported provider-facing keyword and retained explicit local uniqueness validation. The three original failures remain preserved; recovery reused the same threads, reran no source experiment, and reused valid K1/Q/K2 outputs unchanged.

### Quantitative result by arm

| Arm | Cells | Mean MAE | Mean 80% coverage | Mean width | Mean interval score |
|---|---:|---:|---:|---:|---:|
| Opaque | 5 | 0.00994378 | 0.930000 | 0.0362389 | 0.0531115 |
| Aligned | 5 | 0.0129193 | 0.931111 | 0.0465333 | 0.0672989 |
| MisIndexed | 5 | 0.0112024 | 0.891111 | 0.0376222 | 0.0713981 |

Opaque had the lowest descriptive aggregate MAE and interval score in this five-world block. Aligned had the highest coverage by a very small margin and the widest intervals. The ordering varies by world and is not a powered causal estimate.

### Structural result

All 15 EQS responses were valid, but all 15 selected `indeterminate`. Network-family accuracy is therefore 0/15 with a 15/15 abstention rate, spanning nine direct-network cells and six ion-pair-network cells. The simulator-level non-collapse gate passed, so the contrast exists in the registered observations; the Agents did not turn their adaptive 12-batch evidence into a categorical topology claim. This unfavorable result is retained without outcome-based re-questioning.

The complete package is [here](../work-ii-eq-s-five-world-20260920-final/REPORT.md).

## EQ-E substrate gate

The new substrate contains three anonymous selectable medium identities. Each identity binds a private joint property vector, while every entity shares the same direct free-ion precipitation species graph and equation set.

- Numerical executions: 45/45.
- Exact replays: 45/45.
- Registered checks: 14/14.
- Provider calls: 0.
- Identity-response test: at each of four common concentrations, at least two public metrics spanned more than 0.03 across identities.
- Scale controls: maximum same-identity, same-concentration mean gap 0.003893 under a 0.015 limit.
- P boundary: an identity-independent response is refuted at matched operating coordinates.
- S boundary: all three entities retain the same direct network and no aqueous intermediate.
- Information arms: Opaque is null; Aligned and MisIndexed are field-matched qualitative mappings under a no-fixed-point cyclic permutation; no numerical constant or query coordinate is public.

The complete gate package is [here](../work-ii-eq-e-provider-free-gate-20260920/REPORT.md). A passing gate licenses five-world O/A/M design work only. EQ-E provider execution remains unauthorized and unstarted.

## Reproducibility and audit trail

- EQ-S design and scientific repair: `configs/benchmark/work_ii_eq_structural_v0.1.design.json` and `work_ii_eq_structural_v0.2.repair.design.json`.
- EQ-S executable freeze: `configs/benchmark/work_ii_eq_structural_freeze_v0.2.1.json`.
- EQ-S experiment and schema-recovery notes: `WORK_II_EQ_S_V0_2_EXPERIMENT_NOTE.md` and `WORK_II_EQ_S_V0_2_1_SCHEMA_RECOVERY.md`.
- EQ-E substrate design: `configs/benchmark/work_ii_eq_entity_substrate_v0.1.json`.
- EQ-E scope note: `WORK_II_EQ_E_SUBSTRATE_GATE_NOTE.md`.

Validation at delivery: 95/95 relevant regression tests passed, all committed report JSON parsed successfully, and all committed report prose passed the English-only audit.

Private authentication material, raw model event streams, session identifiers, and usage accounting are excluded from repository reports. The ignored run namespace retains raw trajectories, original failures, recovery process material, and reference repeats.
