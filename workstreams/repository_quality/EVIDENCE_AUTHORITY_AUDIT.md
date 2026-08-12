# Evidence authority and status-surface audit

Audit owner: **Codex `/root` — 清衡**
Audit batch: **QH-02**
Measured: **2026-08-12**
Mode: **read-only design; no status, hash, receipt, or evidence node was regenerated**

## Current evidence topology

`configs/current.json` contains **71 evidence nodes** and all 71 declared paths exist in the current
checkout.

| Dimension | Count |
| --- | ---: |
| protocol inputs | 29 |
| generated-current nodes | 15 |
| formal results | 13 |
| development diagnostics | 8 |
| release attestations | 4 |
| fixture / frozen derived data | 2 |
| immutable lifecycle | 61 |
| generated lifecycle | 10 |
| current artifact state | 68 |
| stale artifact state | 3 |
| passed gates | 28 |
| blocked gates | 2 |
| invalidated gates | 3 |
| not-applicable gates | 38 |

The DAG itself is not missing files. The current publication blocker is semantic freshness, not path
absence.

## Non-passing nodes

### Current but scientifically blocked — 2

- `work_i_latent_terminal_formal_shadow`: current/fresh formal result, blocked by unresolved latent
  receipts;
- `work_i_latent_terminal_analysis`: current/fresh downstream analysis, blocked by the formal-shadow
  gate.

These must remain current-but-blocked. “Current” means the artifact matches its declared lineage; it
does not mean the scientific estimand is complete.

### Stale and invalidated — 3

- `first_paper_composition_qualification`;
- `first_paper_deterministic_use_case_qualification`;
- `first_paper_agent_instrument_use`.

All three report `stale_dependency_binding` and form an ordered dependency chain. They require an
authorized Work I rerun from each affected block's first unit after the runtime stabilizes. Editing
hashes or changing `artifact_state` would be invalid.

## Authority hierarchy

The repository should expose four different questions rather than one overloaded “ready” flag:

| Question | Canonical scope | Example answer now |
| --- | --- | --- |
| Is the runtime contract validated on this source? | runtime/source qualification | candidate validated; clean attestation pending |
| Is an environment/protocol gate scientifically qualified? | scoped environment gate | mechanism Gate A historical/scoped pass |
| Is a formal Agent benchmark complete and authorized? | formal benchmark | no; remaining participant/private gates |
| Is a manuscript/release ready to submit? | publication release | no; Work I bindings stale |

Recommended canonical field names for the next registry schema:

- `runtime.contract_validation_status`;
- `runtime.clean_release_attestation_status`;
- `environment_gates.<gate_id>.status`;
- `formal_benchmark.status` and `formal_benchmark.execution_authorized`;
- `publication.status` and `publication.release_ready`.

Avoid reusing `benchmark_ready` at both a mechanism-subtree and repository-wide level. Until the
schema changes, reader-facing documentation must continue to state the conservative global result:
`benchmark_ready=false`, `publication_ready=false`.

## Single-source derivation contract

1. `configs/current.json` is the machine-readable status authority.
2. Node identity, path, role, lifecycle, dependencies, freshness, and gate status live only in the
   evidence DAG node definition.
3. Top-level summaries must be mechanically derived or tested against the DAG; they do not create a
   second truth.
4. Reader-facing README/site status is generated from a small public projection or checked against
   exact registry markers.
5. Workstream TODO files describe planned actions and interpretation, not artifact freshness.
6. Immutable reports remain scientific records; generated-current reports are rebuilt only by their
   declared producer.
7. Development outputs never become formal merely because a top-level summary points to them.

## Generated-node simplification

Only 10 nodes have generated lifecycle. Their producers already form a mostly clear chain:

```text
runtime integration
├── runtime affordance
├── reachability
├── state-transition invariants
├── public boundary
└── maturity truth
    └── backend candidate

mechanism protocol → public matrix → mechanism preflight
formal static summary → task design matrix
```

The next implementation should encode this order once in `scripts/evidence_pipeline.py` and make any
secondary readiness builder consume its output rather than restating dependencies. Do not add a new
manual SHA inventory.

## Required implementation sequence

1. Stabilize and integrate the active Work II development changes.
2. Draft registry schema vNext with scoped readiness names and a backward-compatible reader.
3. Add derivation tests for top-level summaries, publication bindings, and public status projection.
4. Migrate documentation status markers without changing scientific meaning.
5. Choose Work I or Work II as the only release-freeze route.
6. Rebuild only that route's affected generated nodes once.

This audit advances the design of `CL-ST-01`, `CL-ST-03`, and `CL-EV-04`, but leaves them TODO because
no authority surface or generated artifact was changed.
