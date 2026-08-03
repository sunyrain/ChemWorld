# Work I Known-Policy Threshold Qualification

Status: **qualified_and_frozen**

Qualification report SHA-256: `a22cf42c415aa94bb16aaf83e3049fda371fe85c69766c46e18525258676d7aa`

Threshold binding SHA-256: `12b661d19e1b9ecb12570e96bba1d89a5f4497f939aa3154d0b15896f946a0b3`

## Frozen result

The public UV-vis conversion threshold is **0.0079845613799989223**. The comparator is `>=`: values at or above the threshold take one further electrolysis step and proceed to final assay; values below it are discarded.

This value was selected only from qualification world seeds [1000, 1001, 1002, 1003, 1004]. Formal seeds [0, 1, 2, 3, 4] were not executed or inspected by this qualification and cannot be used for retuning.

## Selection

- Original qualification signals: 60
- Unique signal values: 19
- Midpoint candidates: 18
- Admissible candidates: 18
- Pooled median: 0.0079845613799989223
- Selected threshold: 0.0079845613799989223
- Signal range: 0 to 0.065695531666278839
- Signal median: 0.0079845613799989223

| Information arm | Discard branch | Continue-and-assay branch |
| --- | ---: | ---: |
| `opaque_codes` | 15 | 15 |
| `anonymous_nominal_properties` | 15 | 15 |

## Qualification-world signals

The paired arms must have identical vectors because the policies do not read the material dossier and the paired worlds share keyed-noise coordinates.

| World | Opaque conversion vector | Nominal conversion vector | Match |
| ---: | --- | --- | --- |
| 1000 | `[0.000000, 0.057712, 0.038317, 0.016381, 0.007582, 0.042248]` | `[0.000000, 0.057712, 0.038317, 0.016381, 0.007582, 0.042248]` | True |
| 1001 | `[0.043746, 0.000000, 0.000000, 0.029854, 0.000000, 0.033714]` | `[0.043746, 0.000000, 0.000000, 0.029854, 0.000000, 0.033714]` | True |
| 1002 | `[0.016020, 0.004840, 0.029745, 0.000000, 0.052850, 0.000000]` | `[0.016020, 0.004840, 0.029745, 0.000000, 0.052850, 0.000000]` | True |
| 1003 | `[0.000000, 0.000000, 0.000000, 0.040309, 0.065696, 0.000000]` | `[0.000000, 0.000000, 0.000000, 0.040309, 0.065696, 0.000000]` | True |
| 1004 | `[0.031283, 0.004629, 0.000000, 0.045265, 0.008387, 0.000000]` | `[0.031283, 0.004629, 0.000000, 0.045265, 0.008387, 0.000000]` | True |

## Gates and provenance

| Gate | Pass |
| --- | --- |
| `all_120_original_and_replay_signals_finite` | True |
| `all_20_campaigns_close_six_lifecycles` | True |
| `all_720_actions_committed` | True |
| `all_exact_replays_match` | True |
| `all_matched_information_arms_preserve_physical_trace` | True |
| `provider_call_count_is_zero` | True |
| `qualification_worlds_disjoint_from_formal_worlds` | True |
| `selected_threshold_has_both_branches_in_every_arm` | True |
| `ten_original_and_ten_replay_campaigns` | True |

The source manifest contains 12 files and has SHA-256 `e7a8a09d119ef2b5f04019fa343a0a5b8585dadc01ea8dbf996c9f678831518e`. Execution comprised 10 original campaigns plus 10 exact replays, 720 committed actions, and zero provider calls.

State/resource evidence is canonically serialized to 15 significant digits to remove sub-1e-15 runtime-library tails; raw public diagnostic values remain the input to threshold selection.

## Claim boundary

This qualification binds one deterministic diagnostic threshold for the known-policy construct-validity control. It is not an agent-performance result, an endpoint comparison, or evidence from the formal five worlds.
