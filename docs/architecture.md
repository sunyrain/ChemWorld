# Architecture

ChemWorld-Bench is organized as a layered Python package around one registered
environment, `ChemWorld`. Task diversity is expressed as slices of the same
physical-chemical world law rather than separate environments.

## Foundation

`chemworld.foundation` is the reusable Chemical World Model base layer:

- ontology primitives for substances, phases, vessels, instruments, operations,
  reactions, and state variables;
- lightweight canonical units and conversions;
- hidden `WorldState`, public `Observation`, and experiment `Ledger`;
- executable `PhysicalConstitution` checks for non-negativity, units, material
  conservation, observation non-omniscience, measurement cost, preconditions,
  vessel bounds, and risk;
- transition and observation kernel protocols.

Learnable world-model interfaces live in `chemworld.models`, not in
`chemworld.foundation`. This keeps the boundary clear: foundation defines the
world law; models define agent-side beliefs about that world.

The foundation separates three epistemic layers:

- hidden state: species amounts, catalyst activity, physical state, and hidden
  world parameters;
- observation: public instrument readouts, raw signals, processed estimates, and
  uncertainty;
- belief state: the learner or agent's local world model inferred from
  trajectory records.

This separation is central to the benchmark. Agents can act on observations and
beliefs, but cannot read hidden state except in explicit developer/debug runs.

## Runtime V2

`chemworld.runtime` is now the execution center. The Gym environment delegates
chemistry to a transactional runtime instead of carrying operation-specific
branches.

The runtime is organized around:

- `TaskRuntimeProfile`, which declares the operations, instruments, kernels, and
  capabilities required by one task slice;
- `MechanismCompiler`, which compiles mechanism YAML into a `CompiledMechanism`
  with species indexes, a stoichiometric matrix, observable mappings, score
  bindings, and a mechanism hash;
- `OperationKernelRegistry`, which maps allowed operation types to typed kernels
  for the current profile rather than requiring every known ChemWorld operation
  globally;
- `ChemWorldDomainServices`, which owns reaction, thermal, phase, separation,
  instrument, and scoring calculations used by operation kernels;
- `TransactionManager`, which applies state patches atomically, runs
  constitution checks, and records rollback/penalty events when a candidate
  state violates physical constraints.

Operation kernels return `WorldEvent` and `StatePatch` records. The transaction
manager commits those patches to typed ledgers only after validation. This keeps
material ledgers auditable: invalid actions can add process penalties without
silently changing hidden material state.

The active backend remains `semi_mechanistic`, but it is now a runtime service
implementation rather than the conceptual center of the package. Backend
metadata still lives in `chemworld.backends`, separating the shared world law
from the fidelity used to advance hidden state.

Mechanisms are no longer fixed to a single `A/P/B/D/E` reaction family. Each
scenario binds to a mechanism card, such as `simple_batch_reaction`,
`reaction_extraction`, `reactive_distillation_lite`, `pfr_hotspot`, or
`electrochemical_conversion`. The runtime records `mechanism_id` and
`mechanism_hash` in reset info and trajectory logs so replay can fail fast when
the mechanism artifact changes.

Typed ledgers in `WorldState` expose species definitions, phase material
amounts, vessel bounds, equipment attachment, per-vessel heat ledgers, and
process cost/risk/time. During the current migration, the legacy scalar state is
adapted into typed ledgers so phase totals remain synchronized with the hidden
material state.

## Task Registry

`chemworld.tasks` defines benchmark contracts over the shared world law. Each
`TaskSpec` fixes:

- `world_law_id`;
- scenario and initial-state ids;
- split, budget, seeds, objective, and threshold;
- allowed operations and instruments;
- observation and termination policies;
- success metrics and difficulty.

The official entrypoint is:

```python
gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
```

Each task can also emit a task card through `chemworld tasks card <task_id>`.
Task cards are the release-facing benchmark contract and include motivation,
allowed operations, instruments, seed policy, metrics, failure modes, and
baseline reference-score slots.

## Gym API

`chemworld.envs` exposes `ChemWorld` through Gymnasium. Each `step()` is an
executable operation such as `add_reagent`, `heat`, `wait`, `measure`, or
`terminate`. The environment does not expose hidden species amounts or hidden
rate parameters unless explicitly constructed with `debug_truth=True`.

`ChemWorldEnv.step()` is intentionally thin:

1. canonicalize the action;
2. validate schema, task policy, instrument policy, and preconditions;
3. dispatch the action to `ChemWorldRuntime`;
4. observe through the instrument observation kernel;
5. compute reward/cost/info;
6. update campaign bookkeeping and return the Gymnasium five-tuple.

Action handling is split into an explicit abstraction layer:

- `ActionCodec`: converts semantic event JSON to canonical actions and stable
  numeric vectors;
- `OperationValidator`: combines task policy and physical preconditions into a
  single validation result;
- wrappers read validator output instead of duplicating validation logic.

Failed action preconditions return non-informative observations with empty
`observed_keys`, no instrument cost, no sample consumption, and an explicit
`error_message`. `final_assay` is a terminal scoring measurement: it requires a
terminated reaction state, ends the episode, and can only create one
`leaderboard_score`.

Task-aware wrappers can add operation masks and safety-cost signals without
changing the Gymnasium five-tuple API.

## Observation Kernel

Instrument observations are represented as:

- `raw_signal`: teaching- and research-facing instrument signal packets such as
  UV-vis spectra, HPLC/GC chromatograms, IR/NMR proxy spectra, or a final-assay
  multi-instrument packet;
- `processed_estimate`: derived estimates such as yield, selectivity,
  conversion, byproduct signal, degradation warning, purity, recovery, or phase
  partition metrics;
- `uncertainty`: per-estimate measurement noise metadata;
- `observed_mask`: the explicit mask distinguishing measured values from
  unknown values.

Gym observations still expose the stable numeric observation keys. Missing
values are represented as `NaN` in Gym arrays and `null` in trajectory JSONL.

## Agents

`chemworld.agents` contains official baselines:

- random search;
- Latin hypercube search;
- greedy local perturbation;
- Gaussian-process Bayesian optimization;
- random-forest expected improvement;
- safety-constrained Bayesian optimization;
- LLM planner adapter and deterministic replay agent.

## Evaluation

`chemworld.eval` computes performance, sample efficiency, safety-aware scores,
and leaderboard aggregates from JSONL trajectories.

Evaluation now also contains a transparent mechanism-explanation rubric. This
rubric is intentionally simple: it checks whether a submitted explanation covers
temperature trade-offs, degradation, byproducts/selectivity, catalyst-solvent
interactions, concentration/safety, uncertainty, and a next experiment. It is a
stable first-pass artifact score, not a replacement for expert review.

## Data

`chemworld.data` defines the trajectory schema, logging utilities, dataset
export, submission bundles, and anonymization helpers for human pilot studies.
Runtime v2 trajectory records include `mechanism_id`, `mechanism_hash`,
`kernel_id`, `kernel_version`, `affected_ledgers`, `world_events`,
`state_patches_summary`, `transaction_status`, and `rollback_reason`.
