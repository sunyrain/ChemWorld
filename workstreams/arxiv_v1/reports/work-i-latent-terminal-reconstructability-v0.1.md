# Work I Pre-discard Reconstructability Audit

Status: **reconstructable**

Report SHA-256: `995f16032de09044ecf11a54b7d6fef9f0b3463eab2dad331adc52f7c4533857`

## Result

All **36/36** frozen discard checkpoints were reconstructed before the original `discard_batch` action. Each hidden-state, resource-snapshot and complete checkpoint identity matched a second independent deterministic replay.

The indexed raw root contains **53 files** and **127883533 bytes**; every path, byte count and SHA-256 matches the frozen terminal index, with zero unindexed files.

## Outcome boundary

- Shadow terminal evaluations executed: **0**.
- Latent discard scores accessed: **0**.
- Agent/provider calls: **0**.
- Hidden state publication: hashes only; no hidden payload is emitted.
- Terminal replacement: not performed; L05 owns formal shadow execution.

## Census

| Cell | World | Arm | Raw steps | Discards | Full replay | Checkpoints |
| --- | ---: | --- | ---: | ---: | --- | --- |
| `cell-01` | 0 | `opaque_codes` | 62 | 5 | PASS | PASS |
| `cell-02` | 0 | `anonymous_nominal_properties` | 128 | 0 | PASS | PASS |
| `cell-03` | 1 | `anonymous_nominal_properties` | 64 | 4 | PASS | PASS |
| `cell-04` | 1 | `opaque_codes` | 109 | 5 | PASS | PASS |
| `cell-05` | 2 | `opaque_codes` | 84 | 2 | PASS | PASS |
| `cell-06` | 2 | `anonymous_nominal_properties` | 71 | 4 | PASS | PASS |
| `cell-07` | 3 | `anonymous_nominal_properties` | 94 | 3 | PASS | PASS |
| `cell-08` | 3 | `opaque_codes` | 78 | 5 | PASS | PASS |
| `cell-09` | 4 | `opaque_codes` | 78 | 5 | PASS | PASS |
| `cell-10` | 4 | `anonymous_nominal_properties` | 121 | 3 | PASS | PASS |

## Gates

- `L01_contract_valid_and_outcome_blind`: **PASS**
- `raw_root_exactly_matches_terminal_index`: **PASS**
- `ten_source_trajectories_exactly_replay`: **PASS**
- `all_36_frozen_discards_enumerated`: **PASS**
- `all_36_pre_discard_checkpoints_reconstructable`: **PASS**
- `all_36_resource_ledgers_match_recorded_prefix`: **PASS**
- `all_36_hidden_states_match_independent_replay`: **PASS**
- `original_source_bytes_unchanged`: **PASS**
- `shadow_terminal_evaluations_executed_zero`: **PASS**
- `latent_discard_scores_accessed_zero`: **PASS**
- `agent_provider_calls_zero`: **PASS**

## Evidence limitation

The historical raw trajectory did not persist a pre-discard hidden-state digest. This audit therefore binds deterministic independent reconstruction to the frozen configuration, exact recorded prefix, public observations, resource-ledger hash, and source bytes; it does not claim comparison with a previously published hidden-state digest.

This audit establishes deterministic reconstructability only. It does not evaluate a discarded state and contains no terminal-quality result.
