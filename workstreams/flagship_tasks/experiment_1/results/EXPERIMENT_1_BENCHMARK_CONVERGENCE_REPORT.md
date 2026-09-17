# ChemWorld Experiment 1 benchmark convergence report

Date: 2026-09-18  
Campaign branch: `experiment1-continuous-qualification`  
Scope: provider-free benchmark authoring, development qualification, replay,
readiness audit, and confirmation preflight only

## Executive decision

The campaign produced a complete, audit-facing status for all 105 atomic units.
It did **not** produce a Participant release.

| Current status | Atomic units |
| --- | ---: |
| `qualified-development` | 53 |
| `failed-development` | 22 |
| `readiness-blocked` | 30 |
| `qualified-confirmed` | 0 |

The baseline contained 41 development-qualified units. Twelve additional units
now qualify: PA-P gained four, C-P gained three, and RX-S gained five. This is a
scientific convergence result, not an attempt to optimize 105/105 PASS.

The authoritative 105-row artifact is
`EXPERIMENT_1_CONVERGENCE_REGISTRY.json`, registry SHA-256
`f79a912b667d413fe8050955184f24bf99c21d72b9f98cf067e4ffd31e13c588`.
It retains truth hashes, available prior hashes, gate results, denominators,
evidence bindings, versions, supersession metadata, blockers, and a separate
confirmation field for every unit.

## Frozen baseline

Before redesign, commit `a5b11d2e0a5cc6971f19799fbe9513c582c2eded`
was frozen as `experiment-1-pre-convergence-a5b11d2`:

- 105 total atomic units;
- 41 development-qualified;
- 34 substantive failures among EC/RX/PA/FL/C;
- 30 P/D readiness-blocked units represented by fail-closed diagnostic rows;
- no Participant execution and no confirmation result.

Historical registries and raw run directories were not overwritten. New
evidence is versioned and, where applicable, carries `supersedes` bindings.

## Phase 1: local repairs

### PA-P v1.0.2

Q6 had tested fixed qualification endpoints instead of a legal three-unique-
experiment Participant design. The repair changed only the budgeted-
falsification discriminator. Worlds, physics, prior centers, effect and noise
thresholds, and budget were unchanged.

Result: 5/5 `qualified-development`, 75/75 primary executions with exact replay.
The repair converts four former failures into PASS.

### C-P v1.0.2

The old absolute yield-crossing estimand did not represent the robust cooling
response. The repair preregistered the task-relevant contrast
`deltaY40 = crystal_yield(270 K) - crystal_yield(310 K)` without changing the
five Worlds, PBM physics, budget, or noise gates.

Result: 5/5 `qualified-development`, 45/45 primary executions with exact replay.
The repair converts three former failures into PASS.

### RX-E authoring

All six global catalyst transpositions were compared using 120 provider-free
calibration executions on five non-benchmark Worlds. Only the unchanged C1/C2
pair qualified all five calibration Worlds. It was not a repair, and a formal
rerun of the unchanged design was therefore rejected.

Current formal status remains 3/5 development-qualified. RX-W02 fails Q5/Q7 and
RX-W03 fails Q7. Thresholds were not reduced and formal Worlds were not replaced.

## Phase 2: structural redesign

### RX-S v1.1.0

The weak stable-catalyst/deactivation question was replaced by an executable
irreversible versus reversible target-pathway fork. Candidate selection used
three non-benchmark calibration Worlds and selected the family that changed the
preregistered temperature/time decision without being absorbable by one scalar
rate refit.

Result: 5/5 `qualified-development`. Primary and independent full replay each
contained 270 executions; all World-report and summary hashes matched. Summary
SHA-256:
`a89d944db3d2e5b1087ee679efadd28a0e778c39c09ce3b9f59f1a94e286da51`.

### C-S v1.1.0 authoring

An executable seed-growth-dominated versus primary-nucleation-dominated PBM fork
was calibrated outside the formal denominator. All 48 executions completed and
exact-replayed, but only 1/3 calibration Worlds changed the preregistered task
decision. The candidate was rejected; formal W01-W05 were not rerun.

Current status: 0/5, `failed-development`. A prompt-only mechanism was not used
to manufacture a structural question.

## Phase 3: FL system redesign

The v1.0.1 runtime confounded residence time with reactor volume. Version 1.1.0
freezes an 18 mL, 4 mm reactor, controls flow rate, and derives `tau=V/Q`.
Because this is a public/runtime contract change, all 15 units were invalidated
and rerun; old evidence was not mixed with the new runtime.

The canary passed. Entity, parametric, and structural primary runs comprised 60,
60, and 90 executions, respectively, and were repeated in full. All 420
executions completed without platform/physical failure, every trajectory exact-
replayed, and every primary/replay summary and World-report hash matched.

Result: 0/15 development-qualified.

- Entity: all five fail Q5 and Q8; catalyst response is below robust noise
  separation.
- Parametric: all five fail Q5; Q7/Q8 also fail in most Worlds, showing that the
  longer-residence effect is not consistently task-relevant and robust.
- Structural: all five fail Q5 and Q7; the reversible-pathway effect accumulates
  but remains below the frozen public effect/consequence requirements.

This is a stable scientific failure. No threshold was lowered and the private
law was not strengthened after seeing formal outcomes. A future FL v1.2 would be
a second, separately preregistered redesign iteration.

## Phases 4–5: P and D formal-build readiness

Fresh server-side audits confirm both task chains are healthy: P and D each pass
5/5 public smoke Worlds with exact replay. The 30 rows are nevertheless
`readiness-blocked`, not substantive qualification failures.

P still lacks frozen task-specific extractant/misindex assets, an S* oracle and
matched bands, and an executable constant-K versus composition-coupled family.
D still lacks frozen five-World manifests/discriminators, an alpha* oracle and
matched bands, and a D-specific constant-alpha versus composition-dependent VLE
family under one invariant public contract.

Building placeholder priors or prompt-only laws would violate the v1.0 design.
The campaign therefore stops these blocks at readiness instead of fabricating
formal evidence.

## Current system matrix

| System | Development-qualified | Failed-development | Readiness-blocked | Interpretation |
| --- | ---: | ---: | ---: | --- |
| EC | 15 | 0 | 0 | all three loci pass development; confirmation pending |
| RX | 13 | 2 | 0 | P/S are five-World candidates; E remains partial |
| PA | 15 | 0 | 0 | all three loci pass development; confirmation pending |
| FL | 0 | 15 | 0 | corrected runtime is stable, scientific questions still fail |
| C | 10 | 5 | 0 | E/P pass; structural candidate rejected |
| P | 0 | 0 | 15 | environment works; formal benchmark assets absent |
| D | 0 | 0 | 15 | environment works; formal benchmark assets absent |

## Challenge audit and confirmation

Ten loci have five development-qualified Worlds: EC-E/P/S, RX-P/S, PA-E/P/S,
and C-E/P. The challenge audit confirms their Q3 leakage, Q4 symmetry, and Q7
consequence evidence. It also finds that the repository does not yet bind frozen
evidence for:

- a system-specific false-prior plausibility envelope;
- default/one-shot non-triviality across all five Worlds;
- incremental information value of an active experimental choice;
- the `trivial_lower_bound < reliable falsification cost` side of the budget
  window.

Under the frozen confirmation protocol, these are preconditions, not optional
documentation. All ten candidates are therefore `confirmation-blocked-fail-
closed`. No secret confirmation set was generated or consumed, and development
reruns were not relabelled as independent confirmation. Challenge-audit SHA-256:
`18a3d6be3e0ad63eb8560c511d3504ebffe207311cfe4256050ba70c27fac3d1`.

## Reproducibility and safety boundary

- Participant/provider calls: 0.
- External LLM calls: 0.
- Participant execution authorization: false.
- Existing raw and failed-development evidence retained.
- Qualification thresholds were not reduced after outcomes.
- Missing, failed, and blocked units remain in the 105-unit denominator.
- Independent full reruns are called replays, not third-party validation.
- No locus is labelled `qualified-confirmed`.

## Required next campaign

The shortest scientifically valid path to a Participant release is:

1. freeze and execute the four missing challenge probes for the ten candidate
   loci;
2. admit only challenge-passing loci into one-shot process-isolated confirmation;
3. separately author P and D executable private assets before any formal run;
4. decide whether RX-E, C-S, and FL warrant their remaining redesign iteration;
5. rebuild the release manifest only from `qualified-confirmed` rows.

Participant execution was not started.
