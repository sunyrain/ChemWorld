# ChemWorld-Bench Architecture Report

Date: 2026-07-07

This report summarizes the current ChemWorld-Bench architecture and compares it
against mature Gymnasium-style benchmark ecosystems. The goal is to identify
what is already research-grade, what is merely functional, and what is still
missing before ChemWorld can stand beside strong environment suites rather than
remain a course demo.

## Executive Summary

ChemWorld-Bench now has a real benchmark core:

- a Foundation layer with ontology, state, units, constitution checks, kernels,
  and world-law contracts;
- one unified `ChemWorld` Gym environment with task slices over a shared
  physical-chemical world law;
- a separate `chemworld.models` layer for agent-side belief and surrogate
  interfaces;
- semi-mechanistic reaction dynamics plus a phase/separation module;
- instrument-mediated observations with raw signal, processed estimate, and
  uncertainty fields;
- JSONL trajectories, replay verification, evaluation metrics, baselines, CLI,
  documentation, and a 12-day tutorial sequence.

The strongest current property is that chemical intuition is executable: action
preconditions, non-omniscient observation, measurement cost, non-negativity,
unit metadata, vessel bounds, and safety flags are not just prose. They run in
tests and in trajectory verification.

The biggest remaining gap is not "more UI". It is benchmark hardening:

1. standard Gymnasium environment validation, wrappers, vectorized execution,
   and render modes;
2. environment cards, world generator manifests, and calibrated difficulty
   tiers layered on top of the task registry;
3. a Minari-style offline dataset path for baseline, human, and agent
   trajectories;
4. richer public/private world distributions and more task scenarios under the
   same world law;
5. safety-cost semantics closer to safe RL standards;
6. formal submissions, signed private evaluation, and leaderboard release
   protocol.

## Current Architecture

### Package Layers

| Layer | Current Modules | Role | Status |
| --- | --- | --- | --- |
| Foundation | `chemworld.foundation.*` | Ontology, units, state ledger, constitution, kernels, world-law spec | Strong first version |
| Core | `chemworld.core.*` | Reaction mechanism, phase/separation process, actions, objectives | Strong first world-law implementation |
| Models | `chemworld.models.*` | Belief state and learnable surrogate protocols | Clearer world/model boundary |
| Tasks | `chemworld.tasks` | Task contracts over the shared world law | Strong first registry |
| Gym Env | `chemworld.envs.chemworld_env` | Gymnasium `ChemWorld`, action/observation spaces, reset/step/info | Functional, needs checker/rendering |
| Agents | `chemworld.agents.*` | Random, LHS, greedy, BO, safe BO, scripted, LLM adapter | Good benchmark start |
| Data | `chemworld.data.*` | JSONL schema, logging, validation, anonymization, submission utilities | Good internal format, not yet dataset standard |
| Eval | `chemworld.eval.*` | Metrics, leaderboard, suite runner, replay verifier, explanation scoring | Good local benchmark core |
| Docs/Tutorials | `docs`, `notebooks/tutorials` | Architecture docs, protocol docs, 12-day notebooks | Strong educational/research onboarding |

### Runtime Data Flow

The current environment loop is:

1. user/agent submits an event action;
2. the environment canonicalizes the operation and checks preconditions;
3. the transition kernel updates hidden `WorldState`;
4. reaction ODEs or phase/separation operations evolve species, temperature,
   phase ledgers, cost, risk, and process metrics;
5. constitution checks run after state transitions;
6. the observation kernel generates a non-omniscient instrument observation;
7. the Gym environment returns public observation, reward, termination flags,
   and rich `info`;
8. the logger records a replayable JSONL step;
9. evaluator and verifier compute benchmark metrics.

This is the right direction. The platform is already closer to a benchmark than
to a toy function optimizer because the experiment is stateful, partially
observed, constrained, and replayable.

### Existing Strengths

| Area | Evidence | Why It Matters |
| --- | --- | --- |
| Hidden state separation | `WorldState.to_dict(include_hidden=False)`, `debug_truth` gate | Prevents accidental omniscient agents |
| Event-driven actions | reaction and separation operations including heat, sample, mix, settle, wash, dry, concentrate, measure | Closer to lab workflows than one-shot black-box functions |
| Semi-mechanistic kernel | Arrhenius rates, catalyst/solvent interactions, degradation, coupling impurity, catalyst death | Gives real chemical trade-offs |
| Physical constitution | non-negativity, units, vessel bounds, material conservation, observation cost | Makes "chemical intuition" executable |
| Instrument abstraction | HPLC, GC, UV-vis, final assay | Supports partial observation and measurement design |
| Benchmark records | JSONL with action, observation, preconditions, raw signal, uncertainty, checks | Enables replay, auditing, and human/agent analysis |
| Baseline suite | random, LHS, greedy, GP BO, safe GP BO, scripted chemistry, LLM adapter | Allows comparative claims |
| Tutorials | 12 executed notebooks | Makes the system teachable and reproducible |

## SOTA Gym Environment Patterns

This comparison uses several mature environment families as reference points:

- Gymnasium defines the modern single-agent `Env` API, including `reset`,
  `step`, `terminated`, `truncated`, `info`, action spaces, observation spaces,
  render modes, seeding, wrappers, and vector environments.
- Minari provides a dataset API and CLI for offline RL datasets generated from
  Gymnasium environments.
- PettingZoo provides AEC and parallel APIs for multi-agent environments.
- Safety-Gymnasium makes cost a first-class signal for safe RL.
- MiniGrid demonstrates a compact, configurable, wrapper-rich family of many
  goal-oriented tasks.
- Procgen emphasizes procedurally generated train/test levels to measure
  generalization rather than memorization.
- Brax, ManiSkill, and Isaac Lab emphasize high-throughput parallel simulation,
  hardware acceleration, rich task catalogs, assets, sensors, reproducibility,
  and baseline integration.
- ChemGymRL is the closest chemistry-domain comparator: it uses standard
  Gymnasium APIs for interconnected virtual chemical benches.

## Gap Matrix

| Dimension | SOTA Pattern | ChemWorld Today | Gap | Priority |
| --- | --- | --- | --- | --- |
| Gymnasium compliance | Strict `Env` API, checker, render modes, wrappers, vector env support | API exists, spaces and optional wrappers exist, no formal checker or render modes | Add checker tests, `render_mode`, `make_vec` recipes | P0 |
| Task registry | Many registered tasks with stable IDs and specs | Ten built-in tasks now share one `world_law_id` | Add task cards and calibrated reference scores | P0 |
| Action validity | Action masks/wrappers common in discrete or constrained envs | Optional action-mask wrapper and validator exist | Add recipe compiler validation and richer payload diagnostics | P1 |
| Safety RL semantics | Separate reward and cost channel | Cost/risk in observation and metrics | Add optional Safety-Gymnasium-style wrapper returning cost | P1 |
| Offline datasets | Minari-like HDF5 datasets, metadata, CLI | JSONL trajectories only | Add Minari export/import or HDF5 dataset package | P1 |
| Vectorization | Gymnasium vector envs; Brax/ManiSkill GPU/vector throughput | Single env execution; suite loop exists | Add Sync/Async vector examples and batched recipe runner | P1 |
| Procedural generalization | Procgen-style train/test level distributions | public-dev/test/private split exists | Add world generator manifests, difficulty tiers, held-out families | P1 |
| Task catalog | MiniGrid/Isaac/ManiSkill expose many tasks | Reaction, safety, explanation, partition, purification, and tradeoff tasks exist in one world | Add crystallization, continuous flow, distillation modules under same law | P2 |
| Rendering/inspection | Human/rgb/ansi render, videos, trajectories | Notebook SVGs and JSON records | Add `ansi` render and static state/reaction visualizer | P2 |
| Baseline breadth | RL, IL, offline, model-based, language agents | Search/BO/scripted/LLM adapter | Add SB3/RLlib/CleanRL adapters, offline baselines | P2 |
| Submission protocol | Versioned manifests, locked dependencies, reproducible runs | Local submission bundle schema and validation exist | Add result signing and maintainer review workflow | P1 |
| Private evaluation | Hidden seeds/worlds with audited leaderboard | Placeholder private salt, local evaluator | Add maintainer-only private registry and signed result artifacts | P1 |
| Dataset governance | Dataset cards, licenses, privacy policies | Ethics/data doc and anonymizer | Add dataset cards and release checklist | P1 |
| Multi-agent/human-agent | PettingZoo parallel/AEC patterns | Single-agent env; human+GPT as tutorial concept | Later add human/team/agent planning games | P3 |
| Differentiable/high-throughput sim | Brax/JAX, GPU parallel simulators | SciPy ODE, CPU only | Not urgent; add only after world law stabilizes | P3 |

## What We Are Missing Most

### 1. Task Registry Hardening

ChemWorld now has stable task specs such as:

- `reaction-optimization-standard`
- `reaction-safety-constrained`
- `reaction-to-purification`
- `partition-discovery`
- `purity-yield-tradeoff`
- `public-private-generalization`

Each task defines:

- world law id;
- scenario and initial-state ids;
- allowed operations;
- objective;
- budget;
- world split;
- number of worlds and seeds;
- threshold score;
- allowed instruments;
- safety limits;
- required output fields;
- baseline reference scores.

The next hardening step is to add task cards with reference baseline scores and
difficulty calibration notes.

### 2. Action Masks And Operation Validators

ChemWorld exposes operation-level masks through `ActionMaskWrapper` and
pre-checks event actions with `validate_event_action`. Remaining work is:

- a CLI `chemworld validate-action` helper;
- a recipe-to-event compiler that reports invalid event sequences before
  execution;
- richer diagnostics for numeric payload validity.

These diagnostics help students, BO agents, and LLM planners.

### 3. Standard Dataset Layer

JSONL is excellent for auditability, but research ecosystems increasingly expect
dataset-level metadata, indexing, and sampling. ChemWorld should keep JSONL as
the transparent interchange format and add:

- HDF5/Parquet exports;
- Minari-compatible dataset export where feasible;
- dataset cards;
- trajectory provenance;
- splits for `baseline`, `human-pilot`, `agent-submission`;
- anonymization reports.

This would turn ChemWorld logs into reusable offline world-model learning data.

### 4. Public/Private World Distributions

The split logic is present, but the distribution needs more formalization:

- named generator families;
- parameter ranges and constraints;
- train/test/private manifests;
- difficulty calibration;
- distribution-shift knobs;
- secret salt handling;
- private result signing.

Procgen's lesson is important: a benchmark should make generalization hard by
design, not as an afterthought.

### 5. Safety As A First-Class Objective

ChemWorld has risk, cost, flags, and safety-aware score. The next step is to
expose safety in a way safe RL tools can consume:

- optional `cost` return wrapper;
- cumulative constraint budget;
- per-step violation categories;
- irreversible failure modes;
- safety task suite;
- safe baseline reference table.

This would align the platform with safe-RL benchmark conventions while
preserving ChemWorld's chemistry-specific risk model.

### 6. World-Law Module Expansion

The benchmark should not expand by adding disconnected mini-games. The next
research breadth should come from adding modules to the same `ChemWorld` law
and exposing them through new task slices.

| Candidate Module | Why | Difficulty |
| --- | --- | --- |
| Crystallization | Adds nucleation/growth, particle-size distributions, cooling profiles | Medium-high |
| Continuous flow | Adds residence time, feed control, steady/transient behavior | Medium |
| Distillation | Adds energy/separation trade-offs and staged operation | High |
| Electrochemistry | Adds potential/current control and safety constraints | High |
| Solid handling | Adds drying, filtration, loss, and assay preparation | Medium |

The reaction + phase/separation module is now the first example of this
principle: it broadens tasks without registering a separate extraction world.

## Recommended Architecture Upgrades

### P0: Benchmark Hardening

Current P0 hardening has started with task specs, wrappers, submission bundles,
and explicit `single_experiment` versus `campaign` task semantics. Remaining
P0 work before adding new chemistry:

1. Add Gymnasium environment checker tests.
2. Add task cards with baseline reference scores.
3. Add `ansi` render mode and a deterministic textual state summary.
4. Add maintainer review workflow for submission bundles.
5. Add signed private-eval result artifacts.

### P1: Dataset And Evaluation Infrastructure

1. Add dataset export to HDF5/Parquet and optional Minari bridge.
2. Add dataset cards and privacy release checklist.
3. Add signed evaluation artifacts for private runs.
4. Add world generator manifests with difficulty tiers.
5. Add safety-cost wrapper and safety benchmark suite.

### P2: Research Breadth

1. Add the next physical module under `ChemWorld`, not a standalone game.
2. Add RL library adapters for Stable-Baselines3, CleanRL, and RLlib smoke runs.
3. Add offline imitation/world-model baselines.
4. Add richer mechanism explanation schema with human rubric examples.
5. Add result dashboards as static artifacts, not a web account system.

### P3: Scaling And Advanced Interfaces

1. Add vectorized batch execution for large sweeps.
2. Explore JAX/Numba transition kernels only if CPU ODE becomes a bottleneck.
3. Add PettingZoo-style multi-agent/team environments for human+LLM studies.
4. Add cloud/private-eval automation after the local benchmark contract is
   stable.

## Suggested Next Implementation Slice

The next practical sprint should be small and high leverage:

1. `chemworld.data.datasets`
   - JSONL-to-Parquet export;
   - dataset card template;
   - dataset manifest validation.
2. Task cards
   - reference baseline scores;
   - difficulty calibration notes;
   - expected public/private gap ranges.
3. Tests
   - Gymnasium checker;
   - dataset roundtrip;
   - task-card fixture consistency.

This would close the largest SOTA gap without destabilizing the chemistry
kernel.

## Bottom Line

ChemWorld-Bench now has a credible core: it is not merely a demo. It already has
the right scientific spine: hidden semi-mechanistic worlds, partial observation,
instrument cost, executable constraints, replayable trajectories, baseline
agents, and teaching notebooks.

Against SOTA Gym ecosystems, the missing pieces are mostly benchmark
infrastructure rather than chemistry ambition:

- more formal task specs;
- wrappers and environment checker compliance;
- offline dataset standards;
- stronger public/private generation protocol;
- safety-cost API;
- broader world-law modules and task scenarios;
- submission and private-eval hardening.

The near-term strategy should be: harden the benchmark contract first, then add
new modules only as shared physical chemistry rules. This keeps ChemWorld from
becoming a pile of interesting demos and moves it toward a durable research
platform.

## Sources Consulted

- [Gymnasium Env API](https://gymnasium.farama.org/api/env/)
- [Minari documentation](https://minari.farama.org/)
- [PettingZoo Parallel API](https://pettingzoo.farama.org/api/parallel/)
- [Safety-Gymnasium documentation](https://safety-gymnasium.readthedocs.io/en/latest/)
- [MiniGrid documentation](https://minigrid.farama.org/)
- [Procgen Benchmark](https://openai.com/index/procgen-benchmark/)
- [Brax GitHub repository](https://github.com/google/brax)
- [ManiSkill documentation](https://maniskill.readthedocs.io/en/latest/)
- [Isaac Lab documentation](https://isaac-sim.github.io/IsaacLab/main/)
- [ChemGymRL paper](https://pubs.rsc.org/en/content/articlelanding/2024/dd/d3dd00183k)

