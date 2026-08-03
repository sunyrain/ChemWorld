# Work I Incremental Data Contract

Status: **FROZEN**

Contract SHA-256: `e3a941c5a4d958b8284a244947a4c3e1b4ae3639576d12e27a005dbb9baa363c`

## Frozen populations

| Track | Primary unit | Formal counts | Excluded verification evidence |
| --- | --- | --- | --- |
| F | one parent-child fork pair | 6 pairs; 24 total traces | exact replay traces are verification, not extra pairs |
| V | one original campaign profile | 30 campaigns; 180 closed lifecycles | 30 campaigns / 180 lifecycles of deterministic retest |
| L | one frozen discarded lifecycle | 36 discards in 10 cells; 60 terminal lifecycles total | evaluator shadows are not original agent decisions or experiments |

The L campaign-oracle estimand has exactly nine opportunity cells; `cell-02` has no discard opportunity and remains null rather than zero.

## Counting invariants

- Never pool the distinct F-pair, V-campaign, and L-discard primary units.
- Primitive operations and lifecycle rows are repeated events, not independent samples.
- Exact replay, deterministic retest, and synthetic qualification never inflate a primary denominator.
- Every summary discloses its numerator, denominator, and unit.
- Duplicate `(track, record_type, record_id)` keys are fatal.
- Missing numeric values use JSON `null`; NaN, infinity, and string sentinels are forbidden.
- Failed or unresolved units retain identity, denominator membership, and failure reasons.
- Complete-case substitution is forbidden for registered primary L estimands.

## Record schemas

| Track | Record type | Expected rows | Analysis role |
| --- | --- | ---: | --- |
| F | `world_fork_pair` | 6 | `primary` |
| F | `world_fork_trace` | 24 | `audit_only` |
| F | `world_fork_expectation` | 12 | `primary` |
| V | `policy_campaign_profile` | 30 | `primary` |
| V | `policy_lifecycle` | 180 | `primary` |
| V | `policy_retest_campaign` | 30 | `reliability` |
| L | `latent_discard_unit` | 36 | `primary` |
| L | `terminal_lifecycle` | 60 | `primary` |
| L | `latent_campaign_cell` | 10 | `primary` |

## Unit registry

| Unit ID | Canonical unit | JSON type |
| --- | --- | --- |
| `count` | `count` | `integer` |
| `ordinal` | `ordinal` | `integer` |
| `world_seed` | `seed` | `integer` |
| `dimensionless_fraction` | `1` | `number` |
| `dimensionless_ratio` | `1` | `number` |
| `normalized_score` | `1` | `number` |
| `normalized_score_difference` | `1` | `number` |
| `mole` | `mol` | `number` |
| `liter` | `L` | `number` |
| `second` | `s` | `number` |
| `volt` | `V` | `number` |
| `milliampere` | `mA` | `number` |
| `joule` | `J` | `number` |
| `kelvin` | `K` | `number` |
| `pascal` | `Pa` | `number` |
| `currency` | `currency` | `number` |
| `risk` | `risk` | `number` |
| `sha256` | `sha256_hex` | `string` |

## Immutable source bindings

| Artifact | Role | Embedded SHA-256 | File SHA-256 |
| --- | --- | --- | --- |
| `world_fork_qualification` | `immutable_formal_report` | `62684d414e9f9037b70d170abc6b29b442a928cf76df900a6bb53a3d60f2ee02` | `d16981dd3937d661ae65a972bcaacd22c793f086403410f78d103078d25288b8` |
| `world_fork_certificate` | `immutable_summary_certificate` | `5b09842469956d749370ace16d2b0698ec55eb69f46a13044810f6b2ca63ef78` | `8a0299b6957a700e720f46401a62b30a1da4ac2f8d71d57f00071805abcf9ad9` |
| `known_policy_validity_report` | `immutable_formal_report` | `ebb56a052929944330acdf594e4a341c8c8fdb2b4ea2e276556384e7ce6b2064` | `58458670f1db62a1f048a778539e054131a125941ff04fa38d5892d27c382dee` |
| `known_policy_delivery_manifest` | `immutable_delivery_manifest` | `9127224b38ae9af94f8c003bb4f55a8c256b89e4ca4cce5d17d92798ef179e4c` | `8742ac12ee336b5d84b65523e92d0262adb148440257c40a16bdfd6d1972c96e` |
| `latent_terminal_estimand_contract` | `immutable_protocol_input` | `55a0d6a7cb983ce4099dbea24586ea63ccc9433e106d36011d349472809efe30` | `e69db432f7018a3cc41287fa02335337c624caf5ba7f0b487a0695809e052ce5` |
| `latent_terminal_reconstructability` | `immutable_outcome_blind_audit` | `995f16032de09044ecf11a54b7d6fef9f0b3463eab2dad331adc52f7c4533857` | `ec18b041543f44b9c2d2f16ee56a08da727efbe0128622778a8ae6d688afcba3` |
| `latent_terminal_replay_qualification` | `immutable_synthetic_qualification` | `14d0e3358fe4ae00b13e2705519e64f3b8a8644f987dd878b6814fc61247b10f` | `ac3023715ab027221887b5a0b3404a655064939444c63241e9459a88c2cbcde5` |

## Boundary

W1-D01 freezes interfaces and counting semantics only. It executes no world, agent, provider, or formal shadow assay; reads no formal latent outcome; and does not regenerate the global derived-data layer, evidence DAG, ledger, manuscript, figure manifest, or release manifest. W1-D03 must bind its output to this contract hash.
