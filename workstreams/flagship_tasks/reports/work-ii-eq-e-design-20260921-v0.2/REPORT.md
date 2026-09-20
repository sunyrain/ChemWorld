# EQ-E v0.2 formal design and provider-free qualification

Status: **DESIGN PASS / PROVIDER SEALED**.

This artifact records the human-review checkpoint for the five-world EQ-E design. It authorizes
neither an Agent canary nor bulk provider execution. Provider calls made by this qualification: **0**.

## Scientific boundary

EQ-E is an open-form mechanism-characterization task about the mapping from an anonymous selectable
aqueous-medium identity to a joint effective-property bundle and the transfer of that mapping across
concentration and scale. It is not medium selection, score optimization, a closed-set identity quiz,
or reaction-network-family selection.

All five worlds and all three arms use the same public reaction background and the same private direct
weak-acid/free-ion-precipitation topology. Only the E-locus selector-to-property mapping changes
between worlds and information arms. This separates E from P (one shared scalar law) and S (a change
in species graph or reaction network).

## Frozen matrix

- Five physical worlds: `EQ-E-W01` through `EQ-E-W05`.
- Three information arms: `Opaque`, `Aligned`, and `MisIndexed`.
- Fifteen independent source sessions; twelve source batches per session; 180 source batches total.
- Participant posttests: exactly `K1 -> Q -> K2`; 45 posttests total.
- K1 and K2: canonical v1.1 task-delivery prompts, with English report output.
- Q: twelve EQ-E-specific blind numerical queries, with English rationales.
- No participant EQE/EQS supplement and no operation recommendation.

The information contrast is narrow. Opaque receives no instance-level entity mapping. Aligned receives
the correct qualitative local mapping. MisIndexed receives the same rows, fields, vocabulary, and
precision after the no-fixed-point cycle `0 -> 1 -> 2 -> 0`. Numerical constants, world identifiers,
query coordinates, recipes, and answer labels are forbidden from all dossiers.

## Five-world logic

Each selector binds pKa shift, solubility product, available-cation fraction, and activity ratio as one
private bundle. W01 is concordant; W02 introduces an ionization/solid-formation trade-off; W03 changes
the numerical bundle behind a superficially similar ordering; W04 relocates the high-ionization and
early-solid roles; W05 counterbalances the remaining selector roles. Every selector therefore occupies
`higher`, `intermediate`, and `lower` at least once on both public descriptor axes. There is no stable
global selector ranking for an Agent to exploit.

## Q design

| Query block | Selectors | Concentration | Volume | Scientific contrast |
|---|---|---:|---:|---|
| Q01-Q03 | 0, 1, 2 | 0.005 M | 0.024 L | dilute entity contrast |
| Q04-Q06 | 0, 1, 2 | 0.080 M | 0.024 L | interior entity contrast |
| Q07-Q09 | 0, 1, 2 | 0.600 M | 0.024 L | concentrated entity contrast |
| Q10-Q12 | 0, 1, 2 | 0.080 M | 0.048 L | equal-concentration scale control |

Every query predicts `pH_normalized`, `acid_dissociation_fraction`, and `precipitation_signal` as a
point estimate plus 80% prediction interval. The matrix measures entity contrast, within-entity
concentration transfer, and same-concentration scale transfer without defining a preferred entity.

## Provider-free qualification

The final counterbalanced design completed 15/15 campaigns, 180/180 numerical batches, and 180/180
tolerance-zero exact replays.

| Check | Result |
|---|---|
| Provider calls | 0 |
| Design checks | 21/21 pass |
| Arm physics at matched actions and noise | identical |
| Qualifying entity-response metrics at every world/concentration | at least 2/3 |
| Within-entity concentration-transfer signal | pass for all 15 entity profiles |
| Maximum observed equal-concentration scale gap | 0.008280 (limit 0.015) |
| Maximum solver residual | 8.7567e-12 (limit 1e-8) |
| Registered qualitative descriptors | 5/5 worlds pass |
| Selector-role counterbalancing | pass |
| Opaque / Aligned / MisIndexed contract and leakage checks | pass |

Design config SHA-256: `da556c2173d6c76e76b46056e3199b36ca045b7cc31957fe129a433445a27218`.

Q payload SHA-256: `b65d12c6da88b0200093e9a9aaea4f535f19b864ded24ff4f2aa04d13c3cc6b2`.

## Review decision requested

The design is ready for human review. If approved, the next implementation step is to bind a formal
runner and immutable freeze manifest, then run only the `EQ-E-W01` Opaque/Aligned/MisIndexed canary.
W02-W05 must remain sealed until all three canary sessions finish twelve source batches and valid
K1/Q/K2 chains. Reference truth remains embargoed until all fifteen K2 reports are sealed.

## Bound artifacts

- `configs/benchmark/work_ii_eq_entity_v0.2.design.json`
- `scripts/run_work_ii_eq_entity_design_gate_v0_2.py`
- `tests/test_work_ii_eq_entity_design_gate_v0_2.py`
- `workstreams/flagship_tasks/WORK_II_EQ_E_V0_2_FORMAL_DESIGN.md`
- `workstreams/flagship_tasks/WORK_II_CANONICAL_K1_Q_K2_PROTOCOL_V1_1.md`
