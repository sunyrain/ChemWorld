# ChemWorld TODO List

Last updated: 2026-07-09

This file is the only active project board for ChemWorld. The older root files
`TODO_PROFESSIONAL.md` and `TODO_PROFESSIONAL_DEEPENING.md`, plus their docs
copies, are reference archives. Do not use them as live task boards.

## Current Count

| Scope | Total | Done | Active | Claimed | Open | Remaining |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 Pre-release benchmark hardening | 12 | 3 | 0 | 0 | 9 | 9 |
| P1 Runtime and environment consistency | 8 | 2 | 0 | 0 | 6 | 6 |
| P2 Agent-facing interaction and datasets | 6 | 0 | 0 | 0 | 6 | 6 |
| P3 Professional physchem deepening | 27 | 0 | 0 | 3 | 24 | 27 |
| P4 Docs, notebooks, site, release packaging | 5 | 0 | 0 | 0 | 5 | 5 |
| Total | 58 | 5 | 0 | 3 | 50 | 53 |

Immediate release target:

- Finish P0 and P1 first: 15 remaining items.
- Finish P0, P1, P2, and P4 for a usable public pre-release package: 26
  remaining items.
- P3 is the long professional-physics backlog: 27 remaining items. Pull from it
  only when it directly strengthens a benchmark task or replaces a declared
  proxy/lite limitation.

## Current Position

ChemWorld currently has:

- one formal Gymnasium entrypoint: `gym.make("ChemWorld", task_id=...)`;
- a unified task registry and shared `world_law_id`;
- Runtime v2 with transactional records, typed ledgers, mechanism compilation,
  operation kernels, domain services, observation kernels, scoring contracts,
  replay verification, and task/profile/mechanism/scoring hashes;
- agent-facing views for RL/tool JSON/lab report usage;
- dataset export hooks and submission bundle infrastructure;
- a published MkDocs site;
- selected professional-candidate physchem slices, but not a fully rigorous
  process simulator.

The current bottleneck is not feature count. The bottleneck is benchmark trust:
stable task contracts, calibrated baselines, replay/audit strength, submission
examples, and clear limitations.

## Work Rules

- Work from `main`.
- Pull before starting a task.
- Claim or mark exactly one item `Active` before doing nontrivial work.
- Update this file immediately when a task is completed.
- Push after every completed item.
- Do not mark proxy/lite work as professional.
- Do not copy source code from reference repositories.
- Each done item must include code, tests, docs, or an explicit note that docs
  are unnecessary.

Status meanings:

| Status | Meaning |
| --- | --- |
| Open | Ready to start |
| Claimed | Reserved by an owner, implementation not started |
| Active | Implementation in progress |
| Review | Pushed and waiting for review |
| Done | Complete, tested, documented where needed, and pushed |
| Blocked | Explicit blocker recorded in the task note |

## P0: Pre-Release Benchmark Hardening

Goal: make the first public benchmark small, reproducible, and credible.

Frozen core tasks:

- `reaction-to-assay`
- `reaction-to-purification`
- `partition-discovery`

| ID | Owner | Status | Task | Exit Criteria |
| --- | --- | --- | --- | --- |
| P0-BENCH-01 | Codex | Done | Freeze the three-task pre-release contract | Task cards specify objective, budget, allowed operations, instruments, seeds, score metrics, safety limits, maturity tags, and expected qualitative behavior |
| P0-BENCH-02 |  | Open | Build official seed suite | Public-dev/public-test seed lists and hidden-eval salt policy are documented and loaded by CLI |
| P0-BENCH-03 | Codex | Done | Generate official baseline table | `chemworld baselines report` runs random, scripted, BO, safe BO, ToolUsingLLMStub, and LLMReplay across frozen task seeds; `baseline_summary_table.json` and docs report mean, stderr, invalid rate, final-assay count, and AUC |
| P0-BENCH-04 | Codex | Done | Calibrate BO budgets and initial samples | BO acquisition diagnostics are recorded in agent traces, metrics, baseline summaries, tests, and docs; GP-BO/safe GP-BO enter acquisition under default budgets and outperform random without saturating score |
| P0-BENCH-05 |  | Open | Lock golden trajectories | Scripted trajectories for the three core tasks compare observations, reward/info, transaction metadata, and final metrics |
| P0-BENCH-06 |  | Open | Audit scoring contracts | `obs["score"]`, final assay metrics, `leaderboard_score`, and task score contract recomputation agree |
| P0-BENCH-07 |  | Open | Harden replay verifier | Verify catches tampered mechanism hash, scoring hash, profile hash, reward, observation, and transaction summary |
| P0-BENCH-08 |  | Open | Build one valid submission bundle example | `manifest.json`, trajectories, results, explanations, dependency notes, and reproducible command all validate |
| P0-BENCH-09 |  | Open | Build local teacher/student evaluation smoke | Teacher-side validate -> verify -> evaluate -> summarize works on one simulated student sandbox |
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
physical-chemistry slices. These are long-horizon tasks, not blockers for the
first benchmark pre-release unless a task contract depends on them.

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

## Recommended Next Sprint

Do these next, in order:

1. `P1-CONSIST-03`: audit action affordance consistency.
2. `P0-BENCH-08`: publish a valid submission bundle example.
3. `P0-BENCH-02`: build the official seed suite.
4. `P1-CONSIST-04`: audit invalid action atomicity.
5. `P0-BENCH-05`: lock golden trajectories.

This sequence reduces the highest public benchmark risk first: baseline
credibility, agent-facing action clarity, submission reproducibility, seed
policy, and invalid-action trust.

## Deprecated Boards

These files are no longer active planning surfaces:

- `TODO_PROFESSIONAL.md`
- `TODO_PROFESSIONAL_DEEPENING.md`
- `docs/professional_todo.md`
- `docs/professional_deepening_todo.md`

They remain useful as historical references, but all new planning and progress
accounting should happen in this file.
