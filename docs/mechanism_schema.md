# Mechanism Schema

ChemWorld mechanisms are versioned, declarative YAML files that compile into a
runtime `CompiledMechanism` before an environment is reset. The runtime never
executes formulas from mechanism files directly.

## Contract

Every mechanism file must declare:

- `schema_version`
- `network_id`
- `species`
- `reactions`

`schema_version` is currently `chemworld_mechanism_v1`. Unknown versions fail at
load time.

Species records contain:

- `species_id`
- `formula`
- optional `phase`
- optional `charge`
- optional `catalyst`
- optional `observable_aliases`

Reaction records contain:

- `reaction_id`
- `equation` or explicit `stoichiometry`
- optional `delta_h_J_per_mol`
- `rate_law`

Rate laws are enum based. `equation_id` must be one of the local ChemWorld rate
law families exposed by `SUPPORTED_RATE_LAW_EQUATION_IDS`, such as
`arrhenius`, `mass_action`, `reversible_arrhenius`, `catalytic_activity`,
`catalyst_deactivation`, `langmuir_hinshelwood`, or `michaelis_menten`.
Mechanism YAML cannot contain Python expressions, `eval`, or arbitrary code.

## Compile-Time Artifact

The compiler emits a `MechanismManifest`:

- `mechanism_id`
- `mechanism_version`
- `mechanism_hash`
- `source_path`
- species and reaction counts
- rate-law equation ids
- species roles
- observable mapping
- score spec
- initial amount policy
- validation report

`ChemWorldEnv.task_info()` exposes this manifest under `mechanism_manifest`, so
agents, submissions, and replay verifiers can audit which mechanism contract was
used.

## Replay

Trajectories and verifier metadata record `mechanism_id` and `mechanism_hash`.
If the mechanism YAML changes, the hash changes and replay must fail rather
than silently comparing trajectories produced by different hidden worlds.

## Reference Reading

This slice was informed by local reference reads of Cantera YAML mechanism
organization and RMG/Arkane species/reaction archival patterns. ChemWorld does
not copy their parsers or schemas. The local contract is smaller and
benchmark-focused: JSON-friendly, deterministic, and safe for student and agent
submissions.
