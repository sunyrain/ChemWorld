# World-authoring contract

This is the author-facing entry point for creating an auditable ChemWorld world fork.
It documents the frozen Work I v0.1 contract; it does not extend the registered
component inventory or replace the F05--F07 execution and qualification certificate.

## The boundary in one sentence

A valid fork changes exactly one registered private-physics intervention target,
recomputes content and lineage identities, and leaves all other non-identity components
byte-identical--including the complete public action, observation, instrument, resource,
failure, scoring, task, material-catalog, and constitution/safety contract.

The authority is
`configs/benchmark/work_i_world_fork_component_inventory_v0.1.json`, inventory
`chemworld-work-i-world-components-v0.1`, SHA-256
`654b710fcfb0a66232e4a3c6e14f1abb1dd6c24357e7eac995d23d11f64ee6da`.

## Frozen component model

| Layer | Count | Authoring rule |
| --- | ---: | --- |
| Derived identity | 2 | Never hand-author `world_sha256` or lineage as experimental inputs; the builder derives them. |
| Private physics | 6 | Only the three registered intervention targets may change, one per fork. |
| Public contract | 9 | Every digest must remain identical across parent and child. |

The allowed target map is:

| Intervention class | Allowed target |
| --- | --- |
| `mechanism_or_constitutive_law` | `private_physics.constitutive_laws` or `private_physics.reaction_mechanism` |
| `material_law_counterfactual` | `private_physics.material_laws` |

Initial conditions, randomness, runtime kernels, and every public-contract component are
invariant. A new target or intervention class requires a new versioned inventory and a
new protocol; it cannot be introduced by adding a field to an example.

## Authoring workflow

1. Choose one registered intervention class and one compatible target.
2. Give the intervention a non-empty, JSON-serializable payload. Its canonical digest is
   part of the fork identity.
3. Bind the parent snapshot to all 15 non-identity component digests.
4. Change only the chosen target digest in the child snapshot.
5. Build `WorldForkSpec`; do not manually repair its world, lineage, intervention, or fork
   hashes after validation fails.
6. Obtain a public-contract invariance certificate before execution.
7. Preregister the expected private-physics and public-observation divergence.
8. Execute the same typed operation sequence on parent and child, then exact-replay both.
9. Publish the spec, invariance certificate, divergence audit, trace identities, resource
   ledgers, and replay hashes together.

Steps 1--5 establish a structurally valid fork. They do not establish execution,
divergence, replay, scientific validity, or agent performance. Those claims require the
frozen F03--F07 gates.

## Valid examples

- `examples/world-authoring/mechanism-fork-v0.1.json` changes one constitutive-law
  family.
- `examples/world-authoring/material-law-fork-v0.1.json` changes one private material-law
  mapping while preserving public material codes and interfaces.

The examples are compact authoring requests. The validator deterministically constructs
synthetic content-addressed parent and child snapshots, passes them through the production
`WorldForkSpec` builder, and confirms that all nine public-contract components remain
invariant. Synthetic digests demonstrate schema and lineage behavior only; they are not
qualification traces.

The release pipeline validates both examples against the frozen contract and records a
self-hashed receipt. Public users do not need repository-maintainer commands to inspect or
reuse the example specifications.

## Validator stages

The validator fails closed in this order:

1. exact example fields and supported example schema;
2. non-empty identity, purpose, and intervention payload;
3. non-negative integer world seed and non-promotional claim boundary;
4. frozen inventory identity and content hash;
5. registered target and compatible intervention class;
6. complete parent/child component sets and canonical component digests;
7. exactly one changed component, equal to the declared target;
8. complete ordered invariant set;
9. recomputed intervention, world, lineage, fork, and spec identities;
10. equality of all nine public-contract components.

## Common failures

| Failure | Why it is rejected | Correct response |
| --- | --- | --- |
| Unknown example field | The wrapper is versioned and exact-keyed. | Remove it or version the contract. |
| Public component selected as target | Public-surface mutation is a benchmark-contract change, not a world fork. | Keep the public digest invariant. |
| Two private components changed | The certificate identifies one causal intervention edge. | Create two separately declared forks. |
| Class/target mismatch | Intervention semantics are frozen in the inventory. | Choose a compatible registered target. |
| Missing component digest | A partial snapshot is not content-addressed. | Bind all 15 non-identity components. |
| Hand-edited digest or lineage | Identity would no longer bind the payload and ancestry. | Rebuild from the source payload. |
| Parent and child world identity equal | No content change occurred. | Correct the declared target payload. |
| Execution or divergence claim from an example | Schema validity is not runtime evidence. | Run the F03--F07 gates. |
| Agent-performance conclusion | The fork certificate measures apparatus behavior only. | Use a separately frozen agent experiment. |

## What an evidence bundle must preserve

- inventory ID and SHA-256;
- parent and child component digests;
- intervention payload and canonical SHA-256;
- parent/child world and lineage SHA-256 values plus `fork_id`;
- the single changed target and complete invariant set;
- public-contract certificate and non-disclosure audit;
- expected divergence oracle, realized checkpoints, and tolerance verdict;
- original/replay trace hashes and resource-ledger identities;
- explicit claim boundary: no agent-performance claim.

Git history is the archive. Do not overwrite a frozen fork because a later run is more
favorable, and do not select artifacts by version-looking filenames when a current
registry entry exists.
