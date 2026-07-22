# ChemWorld integrated correction roadmap

Updated: 2026-07-22

This is the single current execution list for repository correction and mechanism-adaptation work.
Historical plans, negative runs, and superseded decisions remain in Git history and versioned reports;
they must not be copied back into current status.

## Current project position

- ChemWorld is an Agent capability evaluation and training environment for physical-chemistry
  world-model behavior. It provides environments, interventions, observations, scoring, and replay;
  evaluation does not retrain or update hosted model weights.
- Mechanism-adaptation Gate A v0.2.2 passes at the primary budget of two experiments. The active
  oracle reaches 0.981 top-1 accuracy (95% lower bound 0.952), and the fixed-trajectory decoder
  reaches 0.986 (95% lower bound 0.959). This certifies environment-side identifiability under the
  frozen public contract; it is not evidence that DeepSeek or another Agent discovers mechanisms.
- Gate A v0.2 and v0.2.1 results are immutable design-history evidence. They must not be rewritten
  to match v0.2.2.
- Gates B-E remain pending. No new external-provider mechanism-adaptation campaign has been completed,
  and no live-LLM v0.4.11 report currently exists.
- The general formal benchmark remains 0/6 method families ready. Backend validation, Gate A
  identifiability, and formal benchmark readiness are separate state dimensions.
- There is no active NCS manuscript. The 2026-07-21 draft is archived under
  `paper/archive/ncs-working-draft-2026-07-21/`.

## Execution policy and scope

- [x] Exclude CI design and CI-provider work from this correction cycle.
- [x] Use targeted checks for the changed contracts and code paths. Do not run the complete pytest
  suite unless explicitly requested.
- [x] Preserve frozen scientific reports and older live-LLM v0.4.8-v0.4.10 diagnostics.
- [x] Do not delete a report merely because `configs/current.json` does not reference it.
- [x] Do not spend external-provider budget until the P0 repository-integrity gate below passes.
- [ ] Keep `configs/current.json`, this roadmap, active claims, and user-facing status language
  consistent in every correction commit.

## P0 — restore repository truth and portability

P0 blocks new provider spending and release attestation. It does not invalidate the completed Gate A
v0.2.2 certificate.

### P0.1 Current-registry completeness and fail-closed evidence checks

Problem: `configs/current.json` points to
`workstreams/benchmark_v1/reports/live-llm-dev-v0.4.11.json`, but that artifact does not exist. The
current evidence DAG still passes because it validates declared DAG nodes and bindings, not every
required current-registry path.

- [x] Remove the false current-artifact assertion. Until a real v0.4.11 run completes, represent it
  as an explicit planned/pending output rather than a materialized report.
- [x] Add schema-aware current-path validation to `scripts/evidence_pipeline.py`.
- [x] Distinguish required materialized artifacts from planned outputs, optional diagnostics, and
  archived history; do not infer the distinction from filename or version suffix.
- [x] Fail closed when a required current path is missing, points outside the repository, or has the
  wrong artifact role.
- [x] Add a regression fixture in which a valid-looking current pointer names a missing file and
  prove that `--check` fails.
- [x] Regenerate the current DAG only after the registry and validation rules agree.

Acceptance:

- [x] Every materialized path declared by `configs/current.json` exists.
- [x] `python scripts/evidence_pipeline.py --check` passes with zero missing paths and zero stale
  bindings.
- [x] `pytest tests/test_evidence_pipeline.py tests/test_repository_current_registry.py
  tests/test_mechanism_adaptation_execution.py -q` passes.

### P0.2 Mechanism-adaptation type integrity

Problem: current mypy reports 13 errors in `mechanism_design_audit.py` and
`mechanism_adaptation_execution.py`.

- [x] Add concrete types for `field_schema`, `task_trials`, and the four accumulated trial lists.
- [x] Replace untyped `**dict[str, object]` session construction with an explicitly typed constructor
  path or typed configuration object.
- [x] Constrain candidate-label mode to `Literal["semantic", "anonymous"]` at the parse boundary.
- [x] Preserve runtime behavior and serialized schemas while repairing types.

Acceptance:

- [x] `python -m mypy src/chemworld/eval/mechanism_design_audit.py
  src/chemworld/eval/mechanism_adaptation_execution.py` passes.
- [x] `python -m mypy src/chemworld` passes.
- [x] `pytest tests/test_mechanism_adaptation_execution.py tests/test_mechanism_adaptation.py -q`
  passes.

### P0.3 Portable flagship reanalysis

Problem: the v0.1 flagship diagnostics report stores author-machine paths such as
`D:\Projects\ChemWorld\runs\...`, and reanalysis opens those paths directly. Tests pass on the author
machine but do not certify a relocated checkout.

- [x] Keep the source-bound v0.1 report immutable; do not silently rewrite historical evidence.
- [x] Define a repository-relative trajectory reference contract for newly generated reports.
- [x] Add a documented legacy resolver that maps an old repository-root suffix to the current root,
  or generate a new explicitly versioned portable source manifest.
- [x] Reject absolute paths outside the recognized legacy contract instead of reading arbitrary
  host files.
- [ ] Remove stored author-machine paths from notebook outputs when the affected notebooks are next
  regenerated; notebook cleanup is not a blocker for the runtime fix.

Acceptance:

- [x] Flagship reanalysis passes from a copied/relocated temporary checkout with the original
  `D:\Projects\ChemWorld` path unavailable.
- [x] `pytest tests/test_flagship_reanalysis.py -q` passes.
- [x] Newly generated report trajectory references are repository-relative.

### P0.4 Repair public-document audit semantics

Problem: the public-document audit currently fails on exact wording and exact navigation equality,
even though README contains an explicit 0/6 benchmark boundary and the English navigation exists
with an additional valid System Model page.

- [x] Replace the fixed README sentence check with semantic current-status markers.
- [x] Require the English navigation contract as an ordered required subset; allow declared,
  existing additional pages.
- [x] Validate the Engine/Bench/Lab/Bridge system model semantically rather than requiring the old
  phrase `Core、Bench 与 Bridge`.
- [x] Retain strict checks for missing targets, duplicate targets, locale leakage, unimplemented CLI,
  and maintainer-only paths.

Acceptance:

- [x] `python scripts/audit_public_docs.py` passes without weakening genuine boundary checks.
- [x] `pytest tests/test_public_docs.py -q` passes.

### P0.5 Reconcile governance and status language

- [x] Update `DEVELOPMENT.md` so it no longer calls `paper/ncs/` the current NCS draft.
- [x] Close or replace the active `mechanism-adaptation-v02-execution-integration` claim after this
  correction scope is committed; its replacement must include v0.2.2 paths if work continues.
- [x] Replace ambiguous combinations such as `passed=true`, `success=false`, and
  `release_claim_ready=false` with a canonical lifecycle/status enum plus derived booleans.
- [x] Document the intentional two-commit source/evidence attestation pattern so an evidence-only
  commit is not misread as a stale source commit.
- [x] Keep backend candidate readiness, mechanism Gate A, general benchmark readiness, manuscript
  status, and release attestation as separate fields.

Acceptance:

- [x] Repository status documents contain no active-manuscript contradiction.
- [x] `python scripts/manage_claims.py check` passes.
- [x] A single status reader can explain why Gate A is passed while the formal benchmark remains
  0/6 and publication readiness remains false.

### P0 completion gate

- [x] P0.1-P0.5 acceptance checks pass.
- [x] `python -m ruff check` passes for changed Python files.
- [x] `git diff --check` passes.
- [x] The evidence DAG is refreshed only after all source changes are committed or otherwise bound
  according to the documented attestation pattern.
- [x] No full-repository pytest run is required for this gate.

## P1 — consolidate evidence engineering

P1 reduces recurrence risk. It should follow the P0 correctness fixes and remain behavior-preserving.

### P1.1 One evidence model with explicit artifact roles

- [x] Define artifact roles: `protocol_input`, `generated_current`, `formal_result`,
  `development_diagnostic`, `fixture`, `superseded`, and `archive`.
- [x] Record role, producer, dependencies, source binding, and lifecycle in one machine-readable
  manifest/DAG.
- [x] Make generation order a topological property of the DAG rather than knowledge distributed
  across scripts and maintainer memory.
- [x] Keep formal results and protocol inputs immutable; generated summaries may be refreshed only
  by their declared producer.
- [x] Split mutable project state from evidence locks/attestations if `configs/current.json` cannot
  express these roles without duplicated truth.
- [x] Generate human-readable maturity/runtime summaries from the canonical graph rather than
  updating parallel ledgers manually.

Acceptance:

- [x] One command explains every current artifact's role, producer, dependencies, and freshness.
- [x] One command refreshes generated nodes in dependency order and refuses to regenerate immutable
  inputs/results.
- [x] A missing current artifact, stale digest, role mismatch, or undeclared producer is reported as
  a distinct error.

### P1.2 Centralize repeated provenance and serialization helpers

- [x] Introduce one tested internal module for canonical JSON hashing, file hashing, atomic JSON
  writes, Git source commit, and tracked-tree dirty detection.
- [x] Preserve the existing canonicalization contract and report hashes during migration.
- [x] Migrate scripts in small families; do not mechanically rewrite all scripts in one change.
- [x] Remove local helper implementations only after their report-schema regression tests pass.

Acceptance:

- [x] New scripts do not define private copies of the shared helpers.
- [x] Migrated reports remain byte/schema compatible unless a versioned schema change is declared.
- [x] Provenance tests cover clean, dirty, untracked-only, and evidence-only commit states.

### P1.3 Resume mechanism-adaptation Agent attribution

Only start after the P0 completion gate.

- [x] Decide explicitly whether live LLM v0.4.11 remains in the candidate method set before spending
  provider budget.
- [x] If retained, create a fresh v0.4.11 cache and report; never resume v0.4.8-v0.4.10 caches.
- [x] Run the smallest complete changed/no-change pilot pair first.
- [x] Gate 0: verify integrity, leakage resistance, provider identity, and replay completeness.
- [x] Gate B: report change-detection sensitivity, false-positive rate, AUROC, Brier score, and delay
  under randomized no-change/change timing where supported.
- [ ] Gate C: separate same-prefix local feedback response from full-campaign feedback utility.
- [ ] Gate D: compare frozen, open-loop, adaptive, and oracle recovery over budgets
  `k in {1, 2, 4, 8}` where the protocol permits.
- [x] Gate E: report autonomous procedural score separately from assisted scientific score.
- [x] Record explicitly that no Agent weight update is performed by the environment.

## P2 — reduce repository maintenance surface

P2 items are real maintenance debt but do not block the next scientific pilot unless the affected
component is being changed.

### P2.1 Consolidate duplicated runners

- [ ] Extract a shared off-policy/on-policy preflight execution core from the PPO and SAC v0.4.8
  scripts while retaining algorithm-specific adapters.
- [ ] Consolidate classic/operation development-run orchestration where schemas are identical.
- [ ] Keep CLI compatibility or provide explicit migration aliases.

### P2.2 Define report and large-artifact lifecycle

- [ ] Inventory non-current reports by role; do not equate "not in current" with "unused".
- [ ] Move genuinely superseded reports to an archive only after inbound references are checked.
- [ ] Investigate the two exact duplicate PPO replay pairs and label them intentional or regenerate
  them with distinct seeds.
- [ ] Define which checkpoints, replay buffers, and raw provider payloads must be Git-tracked and
  which belong in an external artifact store with a content hash and retrieval manifest.
- [ ] Keep portable release fixtures self-contained even when that intentionally duplicates a golden
  fixture.

### P2.3 Split code hotspots incrementally

- [ ] Split `test_world_architecture.py` by contract domain.
- [ ] Separate equilibrium, equilibrium-chemistry, and spectroscopy constitutive models from cards,
  adapters, and serialization boundaries.
- [ ] Split flagship diagnostics into trajectory loading, metric computation, and report rendering.
- [ ] Split formal RL training/runner code by lifecycle phase.
- [ ] Require behavior-preserving, targeted tests for each extraction; line count alone is not a
  sufficient reason to refactor.

## Protected facts — do not reopen without new evidence

- [x] Gate A v0.2.2 is the current environment-side identifiability certificate and passes.
- [x] Gate A does not establish Agent mechanism-discovery performance or publication readiness.
- [x] The current evidence DAG has zero declared-node stale bindings after the Gate A refresh; P0.1
  adds the missing current-path completeness guarantee.
- [x] The most recent source attestation recorded a clean tracked tree; the new correction changes
  require a fresh attestation after they are committed.
- [x] Backend candidate validation and formal benchmark 0/6 readiness are intentionally different.
- [x] There is no active manuscript.
- [x] Historical negative results remain immutable and interpretable under their original protocol.

## Targeted verification commands

```powershell
# Evidence and current-registry integrity
.\.venv\Scripts\python.exe scripts\evidence_pipeline.py --check
.\.venv\Scripts\python.exe -m pytest tests\test_evidence_pipeline.py `
  tests\test_repository_current_registry.py tests\test_mechanism_adaptation_execution.py -q

# Mechanism type and behavior checks
.\.venv\Scripts\python.exe -m mypy src\chemworld\eval\mechanism_design_audit.py `
  src\chemworld\eval\mechanism_adaptation_execution.py
.\.venv\Scripts\python.exe -m pytest tests\test_mechanism_adaptation_execution.py `
  tests\test_mechanism_adaptation.py -q

# Portability and public-document contracts
.\.venv\Scripts\python.exe -m pytest tests\test_flagship_reanalysis.py -q
.\.venv\Scripts\python.exe scripts\audit_public_docs.py
.\.venv\Scripts\python.exe -m pytest tests\test_public_docs.py -q

# Governance and changed-file hygiene
.\.venv\Scripts\python.exe scripts\manage_claims.py check
git diff --check
```

## Completion definition

The integrated correction cycle is complete only when:

- [ ] all P0 acceptance items pass;
- [ ] current status contains no missing materialized artifact and no contradictory lifecycle state;
- [ ] targeted tests cover the repaired failure modes, including relocated-checkout portability;
- [ ] current evidence is regenerated and verified from the documented DAG order;
- [ ] the active correction claim is closed or replaced with an accurate narrow scope;
- [ ] the final commit contains no accidental cache, generated site, secret, or audit-draft files;
- [ ] P1/P2 remaining work is explicitly retained here rather than represented as completed.

Until Gates B-E pass, allowed language remains limited to environment capability, protocol
completeness, environment-side identifiability, and explicitly labeled development evidence. Do not
claim reliable Agent mechanism discovery, formal model ranking, or publication readiness.
