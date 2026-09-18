# Experiment 1 integrated collaborator review snapshot — 2026-09-18

Status: **integrated review snapshot; not a benchmark release and not an execution authorization**.

Review branch: `experiment1-integrated-review-2026-09-18`.

Integration base: `808d16e44111bfc5287ea4443b31b477a5dd0b13`.
The branch combines the release/confirmation track ending at `035cee6` and the
benchmark-expansion track ending at `67cebc3`. The merge point immediately before the integration
repair and this review note is `f8d6347715829dee6aaea88243d71717e6c97e65`.

## Review boundary

This branch is the only branch collaborators need to review for the current combined state. It
preserves the two tracks' histories, resolves their integration bindings, and does not merge or
rewrite `main`.

The snapshot does **not** claim that all 105 units pass, that confirmation has run, or that C/P/D
expansion is complete. No Participant/Agent benchmark execution, provider call, C-S calibration,
P calibration, or D first-build campaign was performed while preparing this integration.

## Suggested review order

1. This snapshot for scope, current counts, and explicit non-authorizations.
2. [`README.md`](README.md) and [`AUTHORITY.md`](AUTHORITY.md) for navigation and authority rules.
3. [`results/EXPERIMENT_1_BENCHMARK_CONVERGENCE_REPORT.md`](results/EXPERIMENT_1_BENCHMARK_CONVERGENCE_REPORT.md)
   and [`results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json`](results/EXPERIMENT_1_CONVERGENCE_REGISTRY.json)
   for the 105-unit development result.
4. [`results/EXPERIMENT_1_CHALLENGE_AUDIT_V1_2.md`](results/EXPERIMENT_1_CHALLENGE_AUDIT_V1_2.md)
   and [`results/EXPERIMENT_1_CHALLENGE_PROBES_V1_2.md`](results/EXPERIMENT_1_CHALLENGE_PROBES_V1_2.md)
   for the latest challenge decision. Earlier unversioned/v1.1 challenge artifacts are provenance,
   not the current decision surface.
5. [`EXPERIMENT_1_CONFIRMATION_NOTE_V1_0.md`](EXPERIMENT_1_CONFIRMATION_NOTE_V1_0.md),
   [`configs/benchmark/experiment_1_confirmation_v1.0.json`](../../../configs/benchmark/experiment_1_confirmation_v1.0.json),
   and [`results/EXPERIMENT_1_CONFIRMATION_PREFLIGHT_V1_0.json`](results/EXPERIMENT_1_CONFIRMATION_PREFLIGHT_V1_0.json)
   for the sealed confirmation design and preflight-only receipt.
6. [`EXPERIMENT_1_BENCHMARK_EXPANSION_CAMPAIGN_V1_0.md`](EXPERIMENT_1_BENCHMARK_EXPANSION_CAMPAIGN_V1_0.md),
   [`systems/C/STRUCTURAL_REDESIGN_AUTHORING_NOTE_V1_2_0.md`](systems/C/STRUCTURAL_REDESIGN_AUTHORING_NOTE_V1_2_0.md),
   and [`systems/P/ASSET_AUTHORING_NOTE_V1_1_0.md`](systems/P/ASSET_AUTHORING_NOTE_V1_1_0.md)
   for the development-only expansion boundary.

## Current 105-unit development result

| System | Qualified-development | Failed-development | Readiness-blocked | Current interpretation |
| --- | ---: | ---: | ---: | --- |
| EC | 15 | 0 | 0 | All three five-World loci are challenge-eligible. |
| RX | 13 | 2 | 0 | RX-P is challenge-eligible; RX-S is challenge-blocked. |
| PA | 15 | 0 | 0 | PA-E is challenge-eligible; PA-P and PA-S are challenge-blocked. |
| FL | 0 | 15 | 0 | Stable scientific failure map; no defensible new fork has been authorized. |
| C | 10 | 5 | 0 | C-E and C-P are challenge-eligible; C-S remains outside this release set. |
| P | 0 | 0 | 15 | First-build assets/contracts exist, but calibration and qualification have not run. |
| D | 0 | 0 | 15 | Formal first build has not started. |

Total: **53 qualified-development / 22 failed-development / 30 readiness-blocked /
0 qualified-confirmed**.

These categories are not interchangeable. A failed-development or readiness-blocked unit cannot be
offset by a passing unit, and development qualification is not confirmation.

## Challenge and confirmation state

Challenge v1.2 evaluates the 10 five-World loci that reached development qualification:

- eligible for process-isolated confirmation: `EC-E`, `EC-P`, `EC-S`, `RX-P`, `PA-E`, `C-E`,
  and `C-P`;
- confirmation-blocked: `RX-S`, `PA-P`, and `PA-S`;
- exact denominator for the confirmation design: 7 loci × 5 Worlds = 35 atomic units.

The confirmation public contract and preflight receipt are frozen. The preflight records 1,585
primary executions plus 1,585 tolerance-zero replays, seven sequential locus processes, one worker,
and zero provider calls. Its status is `ready-but-not-executed`; no confirmation unit or Participant
run has executed, so `qualified-confirmed` remains zero.

The sealed plan and salt are represented in Git only by public commitments. Their values and
realized coordinates are not review artifacts and are not tracked.

## Expansion state

- **C-S:** a genuinely different impurity-occlusion-law family and its frozen authoring contract
  are implemented. The provider-free calibration design contains 252 planned executions and has not
  run. It does not backfill the current release set.
- **P:** five distinct private Worlds, entity dossier/derangement, parametric bands, and a
  constant-K versus composition-coupled structural family are implemented and source-bound. The
  provider-free calibration design contains 80 planned executions and has not run.
- **D:** no formal five-World first build has started.
- **FL:** remains 0/15. The existing failure result is retained instead of manufacturing a passing
  question by threshold relaxation or reuse of a failed structural fork.

## Integration validation

Both work branches were merged with `--no-ff`; Git reported no textual merge conflicts. Integration
nevertheless exposed three semantic/binding issues, all repaired and retested:

1. the C-S source closure was rebound to the integrated execution script and its contract self-hash;
2. the crystallization constitutive fork now uses its frozen binary severity in the generic mechanism
   test path;
3. mass-balance invariance is audited against the noiseless internal process metric rather than a
   noisy public observation.

Validation on the locked server environment:

- Ruff over every Python file changed by the two tracks: passed;
- merged challenge, confirmation, expansion, world-axis, and mechanism suite: **132 passed, 0 failed**;
- targeted post-repair tests: **7 passed, 0 failed**;
- broader integration diagnostic before repair: 337 passed, 7 failed. Three failures were introduced
  by integration and are the repaired items above. The remaining four were reproduced unchanged on
  the integration base and are not represented as newly green:
  - production-source `assert` inventory;
  - legacy species constants in runtime/eval modules;
  - post-separation typed-phase-ledger retention;
  - packaged action schema versus runtime schema synchronization.

Those four baseline architecture debts are outside this integration's scientific scope and should be
handled in a separate cleanup change, not silently mixed into the benchmark review.

## Repository and confidentiality audit

The intended Git surface contains source, public contracts, public notes, summaries, registries, and
preflight receipts. It excludes:

- confirmation salt and realized plan;
- raw confirmation outputs;
- `runs/` development/calibration evidence;
- environment files, credentials, provider payloads, and local caches.

A fresh tracked-file and diff scan is required immediately before push. Any forbidden path or secret
value is a release blocker.

## Requested collaborator decisions

1. Is the seven-locus challenge v1.2 eligibility set scientifically acceptable?
2. Is the 35-unit confirmation denominator and sealed-coordinate design acceptable before execution?
3. Are the C-S and P authoring designs suitable for their separate provider-free calibrations?
4. Should the four inherited architecture debts remain a separate cleanup PR?
5. After review, should confirmation and expansion calibration be authorized as distinct runs rather
   than combined with this integration PR?

Until those decisions are recorded, the branch remains a review snapshot and `main` remains
unchanged.
