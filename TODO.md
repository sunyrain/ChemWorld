# ChemWorld Unified TODO

Last updated: 2026-07-09

This is the single active task board for ChemWorld. Earlier release,
professionalization, and deepening task boards have been consolidated here.
All planning, ownership, status updates, and completion accounting should use
this file.

## 1. Current Answer

ChemWorld is not blocked by lack of features. It is blocked by benchmark trust:
task contracts, replay, scoring, submission artifacts, user-facing docs, and
clear maturity boundaries.

Current remaining work:

- 45 items remain out of 58.
- 7 P0/P1 items block a credible pre-release benchmark.
- 18 P0/P1/P2/P4 items remain for a usable public pre-release package.
- 27 P3 items remain for long-term professional physical-chemistry deepening.

Release interpretation:

- P0/P1 are the immediate benchmark-trust gates.
- P2 makes the environment usable by RL, BO, LLM, and student agents.
- P3 is long-horizon professional model deepening; it should not block the
  first public pre-release unless a frozen benchmark task directly depends on
  that model.
- P4 is documentation, tutorial, site, and release packaging.

## 2. Progress Count

| Scope | Total | Done | Active | Claimed | Open | Remaining |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 Pre-release benchmark hardening | 12 | 9 | 0 | 0 | 3 | 3 |
| P1 Runtime and environment consistency | 8 | 4 | 0 | 0 | 4 | 4 |
| P2 Agent-facing interaction and datasets | 6 | 0 | 0 | 0 | 6 | 6 |
| P3 Professional physchem deepening | 27 | 0 | 0 | 3 | 24 | 27 |
| P4 Docs, notebooks, site, release packaging | 5 | 0 | 0 | 0 | 5 | 5 |
| Total | 58 | 13 | 0 | 3 | 42 | 45 |

Near-term cutline:

| Milestone | Remaining | Meaning |
| --- | ---: | --- |
| Benchmark trust minimum | 7 | Finish all P0/P1 items |
| Public pre-release package | 18 | Finish P0/P1/P2/P4 |
| Full visible roadmap | 45 | Finish all open and claimed items |

## 3. Current System Position

ChemWorld currently has:

- one formal Gymnasium entrypoint: `gym.make("ChemWorld", task_id=...)`;
- a unified task registry with a shared `world_law_id`;
- Runtime v2 concepts: transactional records, typed ledgers, mechanism
  compilation, operation kernels, domain services, observation kernels,
  scoring contracts, replay verification, and task/profile/mechanism/scoring
  hashes;
- agent-facing views for RL, tool JSON, and lab-report usage;
- dataset export hooks and submission-bundle infrastructure;
- a published MkDocs site;
- selected professional-candidate physchem slices, but not a fully rigorous
  process simulator.

The next phase should not add many new tasks. It should harden the three frozen
pre-release tasks:

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

## 4. Work Rules

- Work from `main`.
- Pull before starting a task.
- Claim or mark exactly one item `Active` before doing nontrivial work.
- Update this file immediately when a task is completed.
- Push after every completed item.
- Do not maintain a second active TODO file.
- Do not mark proxy/lite work as professional.
- Do not copy source code from reference repositories.
- Each done item must include code, tests, docs, or an explicit no-test
  rationale.

Status meanings:

| Status | Meaning |
| --- | --- |
| Open | Ready to start |
| Claimed | Reserved by an owner, implementation not started |
| Active | Implementation in progress |
| Review | Pushed and waiting for review |
| Done | Complete, tested, documented where needed, and pushed |
| Blocked | Explicit blocker recorded in the task note |

Definition of done:

- implementation exists;
- tests or an explicit no-test rationale exist;
- docs are updated when behavior or workflow changes;
- TODO status and count are updated;
- change is committed and pushed.

## 5. Recommended Next Sprint

Do these next, in order:

1. `P1-CONSIST-05`: audit campaign vs single-experiment semantics.
2. `P0-BENCH-10`: produce benchmark paper artifact skeleton.
3. `P0-BENCH-11`: add CI-like local release command.
4. `P0-BENCH-12`: write pre-release limitations statement.
5. `P1-CONSIST-06`: audit ledger single-source-of-truth.
6. `P1-CONSIST-07`: audit public observation leakage.
7. `P1-CONSIST-08`: scan runtime boundaries.

This sequence reduces public benchmark risk before expanding model scope.

## P0: Pre-Release Benchmark Hardening

Goal: make the first public benchmark small, reproducible, and credible.

Frozen core tasks:

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P0-BENCH-01 | Codex | Done | Freeze the three-task pre-release contract | Task cards specify objective, budget, allowed operations, instruments, seeds, score metrics, safety limits, maturity tags, and expected qualitative behavior |
| P0-BENCH-02 | Codex | Done | Build official seed suite | `chemworld seeds show` exposes the pre-release seed suite, public-dev/public-test seeds, private-eval salt policy, and suite/baseline CLI paths load the official plan unless explicit smoke seeds are provided |
| P0-BENCH-03 | Codex | Done | Generate official baseline table | `chemworld baselines report` runs random, scripted, BO, safe BO, ToolUsingLLMStub, and LLMReplay across frozen task seeds; `baseline_summary_table.json` and docs report mean, stderr, invalid rate, final-assay count, and AUC |
| P0-BENCH-04 | Codex | Done | Calibrate BO budgets and initial samples | BO acquisition diagnostics are recorded in agent traces, metrics, baseline summaries, tests, and docs; GP-BO/safe GP-BO enter acquisition under default budgets and outperform random without saturating score |
| P0-BENCH-05 | Codex | Done | Lock golden trajectories | `tests/fixtures/golden/pre_release_scripted_trajectories.json` locks scripted trajectories for `reaction-to-assay`, `reaction-to-purification`, and `partition-discovery`; tests regenerate summaries from `scripted_chemistry` and compare actions, observations, rewards, transaction metadata, final assay output, and final metrics |
| P0-BENCH-06 | Codex | Done | Audit scoring contracts | `audit_scoring_contract` recomputes `obs["score"]`, `reward`, `observed_reward`, final-assay `leaderboard_score`, processed metric alignment, `scoring_contract_hash`, and `evaluate_records.final_best_score` for the three frozen pre-release tasks; tampered score and non-final leaderboard score are rejected |
| P0-BENCH-07 | Codex | Done | Harden replay verifier | `verify_records` catches tampered mechanism hash, scoring hash, profile hash, reward, observation, operation metadata, runtime transaction status, world events, state patch summaries, and early-termination replay drift; tests cover first-record and mid-trajectory contract hash tampering |
| P0-BENCH-08 | Codex | Done | Build one valid submission bundle example | `chemworld submission example` and `examples/demo_submission_bundle.py` generate a bundle with `manifest.json`, trajectories, results, explanations, dependency notes, README, reproducible command, validation, summary, and replay verification |
| P0-BENCH-09 | Codex | Done | Build local teacher/student evaluation smoke | `local_eval_server/teacher_side/eval_machine.py` supports `init-demo`, `validate`, `run`, `aggregate`, `summarize`, and `demo`; tests cover one-command demo plus manual `init-demo -> validate -> run -> summarize` over the simulated `team_alpha` student sandbox with trajectory, result, verify, leaderboard, and summary artifacts |
| P0-BENCH-10 |  | Open | Produce benchmark paper artifact skeleton | Includes task contracts, baseline report, dataset card, replay manifest, and release checklist |
| P0-BENCH-11 |  | Open | Add CI-like local release command | One documented command runs lint, type check, tests, docs build, audit script, and baseline smoke |
| P0-BENCH-12 |  | Open | Write pre-release limitations statement | Clearly states virtual semi-mechanistic scope, model maturity, non-real-predictor boundary, and known proxy/lite surfaces |

## P1: Runtime And Environment Consistency

Goal: make actions, ledgers, observations, spectra, scoring, logs, replay, and
docs tell the same story.

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P1-CONSIST-01 | Codex | Done | Run and document environment self-consistency audit | Full audit covers 14 formal tasks over seeds 0/1/2 with complete task/profile/mechanism/scoring/observation hash coverage, replay verification, and documented warnings |
| P1-CONSIST-02 | Codex | Done | Spectra-metric semantic alignment | Downstream final assay spectra use selected-phase public species calibration; full audit reports zero spectra failures and zero spectra warnings |
| P1-CONSIST-03 | Codex | Done | Action affordance consistency | `available_actions`, ActionMaskWrapper, OperationValidator affordance, task policy, operation registry, and action masks are covered by cross-task tests; affordance-level invalid reasons no longer include payload-field failures |
| P1-CONSIST-04 | Codex | Done | Invalid action atomicity | Schema, task-policy, payload-bound, and state-precondition failures are covered by material-ledger atomicity tests; invalid actions only mutate process/cost/risk ledgers and emit explicit validation or rollback penalty metadata |
| P1-CONSIST-05 |  | Open | Campaign vs single-experiment semantics audit | Final assay ends an experiment in campaign tasks but ends the episode only in single-experiment tasks |
| P1-CONSIST-06 |  | Open | Ledger single-source-of-truth audit | Material amounts come from typed phase ledgers; equipment/process/vessel state does not fall back to metadata |
| P1-CONSIST-07 |  | Open | Public observation leakage audit | Agent-visible observations, tool JSON, lab reports, spectra labels, and trajectories do not expose hidden species ids or rate constants |
| P1-CONSIST-08 |  | Open | Runtime boundary scan | `ChemWorldEnv` remains thin, no operation-specific if/elif dispatch returns, and runtime does not import legacy core modules |

## P2: Agent-Facing Interaction And Dataset Layer

Goal: make ChemWorld comfortable for RL, BO, LLM, and student agents without
requiring internal source reading.

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P2-AGENT-01 |  | Open | Polish `task_prompt()` for the three pre-release tasks | Prompts include objective, constraints, hidden-info policy, success criteria, and allowed tools in concise human-readable form |
| P2-AGENT-02 |  | Open | Improve lab-report summaries | Failed actions, spectra packets, final assay, campaign progress, and recovery suggestions are deterministic and public-observation-only |
| P2-AGENT-03 |  | Open | Stabilize RL observation view | Vector, mask, cost channel, bounds, and NaN-safe behavior are documented and covered by tests |
| P2-AGENT-04 |  | Open | Add agent trace to dataset export examples | Prompt summary, selected action, validation result, observation summary, and memory note are exported in JSONL/Parquet |
| P2-AGENT-05 |  | Open | Multi-round ToolUsingLLMStub probe | At least one task runs 12+ decision rounds over seeds 0/1/2 with best-score AUC and invalid-action recovery metrics |
| P2-AGENT-06 |  | Open | LLMReplay benchmark fixture | A fixed reasoning/action trace replays deterministically and is usable as a public baseline artifact |

## P3: Professional PhysChem Deepening

Goal: replace remaining proxy/lite gaps with narrow, auditable, validated
physical-chemistry slices. These are long-horizon tasks, not blockers for the
first benchmark pre-release unless a task contract depends on them.

The three `liyijun` items are intentionally marked `Claimed`; they should not
be duplicated by Codex unless explicitly reassigned.

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| DEEP-D1A | liyijun | Claimed | Component identity registry | Aliases, CAS/InChI-like placeholders, formula, charge, molecular weight, provenance, duplicate checks, JSON round-trip |
| DEEP-D1B | liyijun | Claimed | Unit-dimension checker | Canonical dimensions for amount, mass, volume, temperature, pressure, energy, transport properties, and instrument response |
| DEEP-D1C | liyijun | Claimed | Data conflict policy | Deterministic source priority, uncertainty fields, warning vs hard-fail reports, dataset-card provenance |
| DEEP-D4B |  | Open | LLE phase-split solver | TPD-style heuristic, initialization policy, mass-balance checks, extraction-task integration |
| DEEP-D4C |  | Open | Aqueous acid-base equilibrium | Charge balance, activity simplifications, pH observation kernel, precipitation hooks |
| DEEP-D4D |  | Open | Gibbs-minimization toy solver hardening | Small stoichiometric examples with convexity and constraint diagnostics |
| DEEP-D5A |  | Open | Thermochemistry-coupled reversibility | Equilibrium constants from standard-state Gibbs energy, detailed balance, reactor ODE integration |
| DEEP-D5B |  | Open | Pressure-dependent and falloff kinetics | Troe/Lindemann-style compact slice, third-body efficiencies, validation cases |
| DEEP-D6B |  | Open | CSTR dynamics | Dynamic mass/energy balance, residence time, stability, startup/shutdown, multiple steady states |
| DEEP-D6C |  | Open | PFR/plug-flow slice | Axial integration, pressure-drop coupling, heat-transfer boundary, validation cases |
| DEEP-D6D |  | Open | Solver backend interface | Deterministic tolerances, event handling, failure diagnostics, replay verification |
| DEEP-D7A |  | Open | Rigorous flash unit | Material and energy balance, vapor-liquid split, enthalpy duty, nonideal hooks |
| DEEP-D7C |  | Open | Extraction unit | Distribution coefficients from activity/partition model, entrainment, wash sequence, recovery/purity metrics |
| DEEP-D7D |  | Open | Crystallization unit | Solubility curve, supersaturation, nucleation/growth compact model, impurity occlusion, CSD metadata |
| DEEP-D8A |  | Open | Phase-change and equipment heat transfer | Boiling/condensation warnings, jacket/coil/shell corrections, fouling evolution, energy-ledger validation |
| DEEP-D8B |  | Open | Two-phase pressure drop | Documented correlation slice with validity limits replacing homogeneous proxy |
| DEEP-D8C |  | Open | Relief and safety envelope | Pressure/temperature hazard envelopes, runaway indicators, safety-cost integration |
| DEEP-D8D |  | Open | Equipment cards | Vessel, pump, mixer, condenser, heat exchanger, and column specs with constraints |
| DEEP-D9A |  | Open | Empirical HPLC/GC method sensitivity | Retention-index examples, temperature/mobile-phase sensitivity, detector response calibration, asymmetric peak flags |
| DEEP-D9C |  | Open | NMR slice | Chemical shift anchors, multiplicity/coupling metadata, integration, solvent reference, failure modes |
| DEEP-D9D |  | Open | MS slice | Simple fragmentation metadata, isotope envelopes for small formulas, detector response uncertainty |
| DEEP-D10C |  | Open | Reference-baseline reports | Task-specific official tables, seed confidence intervals, public/private generalization gaps |
| DEEP-D10D |  | Open | Solver/provenance manifest | Commit hash, dependency lock, optional backend versions, tolerances, hidden-scenario salt policy |
| DEEP-D11B |  | Open | Mass-transfer limiting-current slice | Diffusion-layer approximation, limiting current, depletion, current-efficiency loss, analytical plateau checks |
| DEEP-D11C |  | Open | Potentiostatic and galvanostatic controllers | Controller semantics, clipping, ramp/hold recipes, operation logs, replay contracts |
| DEEP-D11D |  | Open | Double-layer and capacitive-current slice | RC transient, non-Faradaic current, startup artifacts, current-trace observations |
| DEEP-D11E |  | Open | Electrochemical scenario cards | Redox metadata, electrode area, electrolyte window, side-reaction thresholds, hidden-parameter generation |

## P4: Docs, Notebooks, Site, And Release Packaging

Goal: make the project legible without letting documentation outrun tested
behavior.

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P4-DOCS-01 |  | Open | Reorganize docs around pre-release benchmark | Site first explains what is stable, what is experimental, and where to start |
| P4-DOCS-02 |  | Open | Build a concise architecture report from current code | High-level document describes Runtime v2, task contracts, ledgers, mechanisms, agent interface, and limitations |
| P4-DOCS-03 |  | Open | Harden 12-day tutorial workload | Each day requires a nontrivial artifact: experiment log, plot, model, decision rationale, or report |
| P4-DOCS-04 |  | Open | Add three end-to-end notebooks | Reaction-to-assay, reaction-to-purification, and partition-discovery each show planning, execution, spectra, metrics, and reflection |
| P4-DOCS-05 |  | Open | Finalize release checklist page | Includes gates, artifacts, known limitations, private-eval policy, and citation instructions |

## Consolidated And Removed Boards

These files were consolidated into this TODO and removed from the active root
workspace:

- `TODO_PROFESSIONAL.md`
- `TODO_PROFESSIONAL_DEEPENING.md`

The documentation site exposes a concise summary page instead of maintaining a
second active task board. If the site summary disagrees with this file, this
file is authoritative.
