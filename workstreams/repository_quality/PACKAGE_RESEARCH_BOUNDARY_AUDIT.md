# Package and research-workflow boundary audit

Audit owner: **Codex `/root` — 清衡**
Audit batch: **QH-02; exact AST baseline added in QH-05**
Measured: **2026-08-12**
Mode: **QH-02 read-only design; QH-05 added a non-regression guard without moving consumers**

## Finding

The installable package contains **26 Python modules** with string literals naming or beginning with
repository-only path prefixes `workstreams/`, `scripts/`, or `configs/benchmark/`. Of these,
**25 are in `chemworld.eval`** and one is `chemworld.agents.known_policy`.

QH-02's broad textual scan reported 25 modules. QH-05 replaced that approximation with an AST scan
of complete path literals. The first QH-05 pass counted 24 prefix literals; final review expanded the
scanner to root literals later joined or passed as Git pathspecs and found two legitimate consumers:
`arxiv_v1_derived_data` and `cross_world_infrastructure_qualification`. Neither `chemworld.cli` nor
`chemworld.eval.paper_artifact` contains a `paper/` path literal; `paper_artifact` remains in scope
because it binds `scripts/`.

This is not evidence that the core environment is broken. Core run/verify/evaluate and wheel smoke
already pass. It does mean that the package boundary currently combines three different products:

```text
portable ChemWorld runtime and replay library
├── repository-bound research protocol implementation
└── paper/evidence/release orchestration
```

The safe objective is to remove repository discovery and paper/workstream policy from portable core
imports while retaining explicit research entry points. It is not to rewrite runtime behavior or
invalidate immutable artifacts.

## Current bound modules

### Portable paper convenience — 1 module

- `chemworld.eval.paper_artifact` refers to reproduction scripts.

The `run`, `evaluate`, `verify`, task, scenario, dataset, and submission surfaces should remain
portable. Paper artifact generation can remain an optional command, but its repository dependency
must be explicit and fail with a clear “repository checkout required” diagnostic.

### Work I and historical policy workflow — 12 modules

- `chemworld.agents.known_policy`;
- `chemworld.eval.arxiv_v1_derived_data`;
- `chemworld.eval.composition_qualification`;
- `chemworld.eval.cross_world_infrastructure_qualification`;
- `chemworld.eval.deterministic_use_cases`;
- `chemworld.eval.first_paper_u05_complete_agent`;
- `chemworld.eval.known_policy_threshold`;
- `chemworld.eval.latent_terminal_contract`;
- `chemworld.eval.latent_terminal_reconstructability`;
- `chemworld.eval.latent_terminal_replay`;
- `chemworld.eval.policy_validity_qualification`;
- `chemworld.eval.work_i_data_contract`.

These modules bind experiment notes, TODOs, scripts, configs, reports, or claims. Several are part of
immutable Work I evidence and cannot simply move before their import paths, manifests, and replay
consumers are audited.

### Work II/release workflow — 13 modules

- `chemworld.eval.autonomous_material_replication_audit`;
- `chemworld.eval.mechanism_adaptation_preflight`;
- `chemworld.eval.mechanism_preregistration`;
- `chemworld.eval.work_ii_c2_admission`;
- `chemworld.eval.work_ii_formal`;
- `chemworld.eval.work_ii_formal_evaluators`;
- `chemworld.eval.work_ii_preregistration`;
- `chemworld.eval.work_ii_private_execution`;
- `chemworld.eval.work_ii_public_c2`;
- `chemworld.eval.work_ii_qualification`;
- `chemworld.eval.work_ii_release`;
- `chemworld.eval.work_ii_runtime_semantics_impact`;
- `chemworld.eval.work_ii_structural_candidate_qualification`.

These are active and inside the main process's protected execution surface. They must not be moved or
renamed during the current Work II development block.

## Target boundary

Use a two-stage boundary before considering separate distributions or repositories.

### Stage 1 — package-internal separation

```text
chemworld/
├── foundation, physchem, world, runtime, envs
├── data, schemas, task contracts, portable eval/replay/metrics
├── agents and providers with no repository discovery at import time
└── research/
    ├── common       explicit repository context and artifact I/O
    ├── work_i       Work I builders, validators, and compatibility readers
    ├── work_ii      Work II plans, execution, evaluation, and release gates
    └── publication  paper/release orchestration
```

The exact namespace is a later implementation decision; the invariant is more important than the
name: portable imports may not depend on `workstreams`, paper sources, or script filenames.

### Stage 2 — optional distribution split

Only after Stage 1 succeeds should the project decide whether research workflows become a separate
extra or distribution. A physical repository split is P3 and is not required for current closeout.

## Migration contracts

1. Introduce an explicit `RepositoryContext` or equivalent object with repository root, current
   registry, governed input paths, and output root. Do not search parent directories implicitly in
   portable code.
2. Move path constants out of domain logic. Builders and validators accept explicit paths/contracts;
   thin CLI scripts resolve the current repository paths.
3. Keep canonical serialization and hashes stable. A file move alone must not change scientific
   content identity unless the governing schema defines paths as content.
4. Preserve old public imports with deprecated forwarding modules for at least one declared release
   window when external or immutable consumers use them.
5. Keep old formal artifacts read-only. Compatibility readers may remain without allowing old
   writers to produce new current evidence.
6. Test both modes: portable wheel outside the repository and explicit research workflow inside a
   checkout.
7. Do not combine module moves with changes to physics, evaluator semantics, experiment coverage, or
   statistical gates.

## Recommended implementation waves

| Wave | Scope | Risk | Entry condition | Exit evidence |
| --- | --- | --- | --- | --- |
| AR-A | Add import-boundary rules and a repository-context abstraction without moving modules | low | quiet `main` | boundary tests, wheel smoke, no output changes |
| AR-B | Isolate paper artifact and CLI repository-only command routing | low/medium | AR-A | core CLI works outside checkout; paper command gives explicit diagnostic |
| AR-C | Move Work II repository constants behind explicit context | medium/high | current Work II block integrated; no release freeze active | focused Work II tests and byte-stable builders where required |
| AR-D | Move Work I workflow modules with compatibility forwarding imports | high | Work I qualification replacement or explicit decision to preserve current artifacts | Work I replay/release tests, immutable reference audit |
| AR-E | Consolidate thin scripts and remove superseded wrappers | medium | all callers enumerated | one current entry point per workflow, CLI forwarding tests |

## Import-boundary policy to enforce

- `foundation` must not import `physchem`, `world`, `runtime`, `envs`, `agents`, `providers`, `eval`,
  `research`, paper, or workstreams;
- `physchem` may use `foundation`, but not env/eval/research/provider workflows;
- `world` may use `foundation` and `physchem`;
- `runtime` may use foundation/world/physchem contracts;
- `envs` may orchestrate runtime/world/tasks but must not import research release logic;
- portable `data`, replay, metrics, and verification may use public runtime/task contracts;
- `research` may depend downward on portable modules; portable modules must not depend upward on
  research;
- providers remain adapters and must not be imported by the physical substrate;
- docs, paper, workstreams, and scripts are never import dependencies of portable modules.

QH-05 adds `scripts/check_package_research_boundary.py` and the reviewed machine baseline
`package_research_boundary_baseline.json`. The guard fails only on newly introduced module/prefix
pairs; when a dependency is removed it reports an eligible baseline deletion. Existing consumers are
not moved, and no execution or evidence behavior changes.

QH-08 adds a second AST guard for upward Python imports across `foundation`, `physchem`, `world`,
`runtime`, `envs`, and `data`. The reviewed baseline has **13 modules / 16 upward edges**: two data
modules import `eval`, one foundation module imports `agents` and `world`, eight physchem adapter
modules import `runtime` (one also imports `world`), and two world modules import `runtime`. These are
documented migration debt, not newly approved design. The guard rejects any new module/target edge
and reports removed edges as baseline entries eligible for deletion.

`CL-AR-01` through `CL-AR-04` remain TODO because the underlying dependencies have not migrated.
`CL-AR-05` remains open for eliminating the 16 reviewed upward edges, but both new repository-path
dependencies and new upward imports are now mechanically blocked.
