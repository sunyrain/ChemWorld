# Work I Known-Policy Threshold Qualification

Status: **qualified_and_frozen**

Qualification report SHA-256: `9a928c28862099049c560b7135067ea86dc6535a7077926b66f39221abbe924e`

Threshold binding SHA-256: `8a55b713ca900a644a301ecd8e83a0a686f9a28b3f60a18a85a4e57b66288c6a`

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

The source manifest contains 12 files and has SHA-256 `459801ffd0109a44f5a64d63f00a80f23c5d22c73ac23d7665f47f9b47756b45`. Execution comprised 10 original campaigns plus 10 exact replays, 720 committed actions, and zero provider calls.

State/resource evidence is canonically serialized to 12 significant digits with absolute residuals below 1e-15 mapped to zero; raw public diagnostic values remain the input to threshold selection.

## Claim boundary

This qualification binds one deterministic diagnostic threshold for the known-policy construct-validity control. It is not an agent-performance result, an endpoint comparison, or evidence from the formal five worlds.
