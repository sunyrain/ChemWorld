# ChemWorld Master TODO

Last consolidated: 2026-07-09

This is the single active TODO for ChemWorld. Older detailed boards
(`TODO_PROFESSIONAL.md` and `TODO_PROFESSIONAL_DEEPENING.md`) are reference
archives only. New work should be claimed, updated, completed, and counted in
this file.

Current board size:

- 58 active items total.
- 4 items done.
- 54 items remaining: 51 open, 3 claimed.
- First release target: finish P0 and P1, which currently leaves 16 items.
- Full pre-release package target: finish P0, P1, P2, and P4, which currently
  leaves 27 items.
- Professional deepening backlog: 27 items, including 3 already claimed by
  `liyijun`.

## Current Position

ChemWorld is now a unified `ChemWorld` Gymnasium environment with Runtime v2,
typed ledgers, mechanism-driven reaction integration, task contracts, agent-facing
views, replay verification, dataset export hooks, and a published MkDocs site.

The next phase is not to add more surface area. The next phase is to harden a
small pre-release benchmark until outside users can trust, reproduce, and submit
against it.

## Work Rules For Fast Iteration

- Pull `origin/main` before claiming work.
- Claim exactly one concrete item by setting `Owner` and `Status`, then push.
- If remote `TODO.md` changes while you are working, pull immediately and
  update your local plan.
- Finish one item, update this file, run relevant gates, commit, and push before
  starting another.
- If working alone, claiming can be skipped for very short tasks, but the
  completed item still needs an owner in this table before commit.
- Do not mark a proxy/lite implementation as professional.
- Do not copy source code from reference repositories.
- Every completed item should include code, tests, docs or a short note saying
  why docs are not needed.

Status vocabulary:

| Status | Meaning |
| --- | --- |
| Open | Ready to claim |
| Claimed | Owner reserved the task and pushed the claim |
| Active | Implementation is in progress |
| Review | Pushed and waiting for review |
| Done | Complete, tested, documented, and pushed |
| Blocked | Explicit blocker with handoff note |

## Progress Summary

Fresh consolidated board counts:

| Area | Total | Done | Open | Claimed | Remaining | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P0 Pre-release benchmark hardening | 12 | 2 | 10 | 0 | 10 | Highest priority |
| P1 Runtime and environment consistency | 8 | 2 | 6 | 0 | 6 | Needed before public benchmark claims |
| P2 Agent-facing interaction and datasets | 6 | 0 | 6 | 0 | 6 | Required for RL/BO/LLM users |
| P3 Professional physchem deepening | 27 | 0 | 24 | 3 | 27 | Concrete slices from the deepening roadmap |
| P4 Docs, notebooks, and release packaging | 5 | 0 | 5 | 0 | 5 | Keep site useful but do not let docs outrun code |
| Total active board | 58 | 4 | 51 | 3 | 54 | First target: finish P0/P1 |

Priority interpretation:

1. Benchmark credibility requires P0 first.
2. Public trust requires P1 immediately after or alongside P0.
3. Agent usability requires P2 after the pre-release contract is stable.
4. Site, notebooks, and release packaging should track code, not outrun it.
5. P3 is the long professional-physics backlog; only pull from it when it
   directly improves a benchmark task or replaces a declared proxy/lite gap.

Historical implementation already completed:

- unified `ChemWorld` entrypoint and task registry;
- Runtime v2 transactional kernel architecture;
- mechanism compiler and compiled reaction integrator;
- typed phase, species, vessel, equipment, process, and instrument ledgers;
- role-based spectra and public observation contracts;
- task/profile/scoring/observation hashes in replay records;
- dataset export hardening;
- agent-facing API and wrappers;
- major physchem lite/professional-candidate slices across properties, EOS,
  reactions, reactors, separations, transport, spectroscopy, thermochemistry,
  and electrochemistry;
- GitHub Pages documentation deployment.

## P0: Pre-Release Benchmark Hardening

Goal: make three core tasks credible as a small benchmark release.

Recommended first tasks:

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P0-BENCH-01 | Codex | Done | Freeze the three-task pre-release contract | Task cards specify objective, budget, allowed operations, instruments, seeds, score metrics, safety limits, maturity tags, and expected qualitative behavior |
| P0-BENCH-02 |  | Open | Build official seed suite | Public-dev/public-test seed lists and hidden-eval salt policy are documented and loaded by CLI |
| P0-BENCH-03 | Codex | Done | Generate official baseline table | `chemworld baselines report` runs random, scripted, BO, safe BO, ToolUsingLLMStub, and LLMReplay across frozen task seeds; `baseline_summary_table.json` and docs report mean, stderr, invalid rate, final-assay count, and AUC |
| P0-BENCH-04 |  | Open | Calibrate BO budgets and initial samples | BO agents enter acquisition phase under default benchmark budgets and are stronger than random without saturating score |
| P0-BENCH-05 |  | Open | Lock golden trajectories | Scripted trajectories for the three core tasks compare observations, reward/info, transaction metadata, and final metrics |
| P0-BENCH-06 |  | Open | Audit scoring contracts | `obs["score"]`, final assay metrics, `leaderboard_score`, and task score contract recomputation agree |
| P0-BENCH-07 |  | Open | Harden replay verifier | Verify catches tampered mechanism hash, scoring hash, profile hash, reward, observation, and transaction summary |
| P0-BENCH-08 |  | Open | Build one valid submission bundle example | `manifest.json`, trajectories, results, explanations, dependency notes, and reproducible command all validate |
| P0-BENCH-09 |  | Open | Build local teacher/student evaluation smoke | Teacher-side validate -> verify -> evaluate -> summarize works on one simulated student sandbox |
| P0-BENCH-10 |  | Open | Produce benchmark paper artifact skeleton | Includes task contracts, baseline report, dataset card, replay manifest, and release checklist |
| P0-BENCH-11 |  | Open | Add CI-like local release command | One documented command runs lint, type check, tests, docs build, audit script, and baseline smoke |
| P0-BENCH-12 |  | Open | Write pre-release limitations statement | Clearly states virtual semi-mechanistic scope, model maturity, non-real-predictor boundary, and known proxy/lite surfaces |

## P1: Runtime And Environment Consistency

Goal: ensure actions, ledgers, observations, spectra, scoring, logs, and docs tell
the same story.

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P1-CONSIST-01 | Codex | Done | Run and document environment self-consistency audit | Full audit covers 14 formal tasks over seeds 0/1/2 with complete task/profile/mechanism/scoring/observation hash coverage, replay verification, and documented warnings |
| P1-CONSIST-02 | Codex | Done | Spectra-metric semantic alignment | Downstream final assay spectra now use selected-phase public species calibration; full audit reports zero spectra failures and zero spectra warnings |
| P1-CONSIST-03 |  | Open | Action affordance consistency | `available_actions`, action mask, validator, task policy, and operation registry agree for every task |
| P1-CONSIST-04 |  | Open | Invalid action atomicity | Schema/task/precondition failures do not mutate material ledgers and record explicit process/cost penalties where appropriate |
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
physical-chemistry slices. These are concrete tasks distilled from
`TODO_PROFESSIONAL_DEEPENING.md`.

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

Goal: make the project legible without letting docs outrun tested behavior.

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P4-DOCS-01 |  | Open | Reorganize docs around pre-release benchmark | Site first explains what is stable, what is experimental, and where to start |
| P4-DOCS-02 |  | Open | Build a concise architecture report from current code | High-level document describes Runtime v2, task contracts, ledgers, mechanisms, agent interface, and limitations |
| P4-DOCS-03 |  | Open | Harden 12-day tutorial workload | Each day requires a nontrivial artifact: experiment log, plot, model, decision rationale, or report |
| P4-DOCS-04 |  | Open | Add three end-to-end notebooks | Reaction-to-assay, reaction-to-purification, and partition-discovery each show planning, execution, spectra, metrics, and reflection |
| P4-DOCS-05 |  | Open | Finalize release checklist page | Includes gates, artifacts, known limitations, private-eval policy, and citation instructions |

## Recommended Next Sprint

Do these in order:

1. `P0-BENCH-04` calibrate BO budgets and initial samples.
2. `P1-CONSIST-03` audit action affordance consistency.
3. `P0-BENCH-08` publish a valid submission bundle example.
4. `P0-BENCH-02` build official seed suite.
5. `P1-CONSIST-04` audit invalid action atomicity.

Rationale: these five items convert ChemWorld from a rich internal prototype into
a benchmark that an outside researcher can understand, run, and compare against.

## Archived Detailed Boards

- `TODO_PROFESSIONAL.md`: broad professional-grade module roadmap and completed
  first professional slices.
- `TODO_PROFESSIONAL_DEEPENING.md`: detailed physchem deepening slices and
  reference-reading contract.
- Git history before 2026-07-09 preserves the long historical `TODO.md`.
