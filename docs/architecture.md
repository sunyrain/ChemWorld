# Architecture

ChemWorld-Bench is organized as a layered Python package.

## Foundation

`chemworld.foundation` is the reusable Chemical World Model base layer:

- ontology primitives for substances, phases, vessels, instruments, operations,
  reactions, and state variables;
- lightweight canonical units and conversions;
- hidden `WorldState`, public `Observation`, and experiment `Ledger`;
- executable `PhysicalConstitution` checks for non-negativity, units, material
  conservation, observation non-omniscience, measurement cost, preconditions,
  vessel bounds, and risk;
- transition and observation kernel protocols;
- surrogate and belief-state interfaces for local world-model learning.

The foundation separates three epistemic layers:

- hidden state: species amounts, catalyst activity, physical state, and hidden
  world parameters;
- observation: public instrument readouts, raw signals, processed estimates, and
  uncertainty;
- belief state: the learner or agent's local world model inferred from
  trajectory records.

This separation is central to the benchmark. Agents can act on observations and
beliefs, but cannot read hidden state except in explicit developer/debug runs.

## Core

`chemworld.core` owns the scientific abstraction:

- recipe-space utilities used by optimization baselines;
- hidden world parameter generation across public and private splits;
- semi-mechanistic event transition kernels;
- objective scoring.

The current world family uses five reactions:

- `A -> P`, target product formation;
- `A -> B`, byproduct formation;
- `P -> D`, target product degradation.
- `A + P -> E`, coupled impurity formation;
- `Cat_active -> Cat_dead`, catalyst deactivation.

Rates follow Arrhenius temperature dependence and are modified by catalyst,
solvent, concentration, catalyst activity, and stirring speed. The transition
kernel also updates temperature through a simplified energy balance, plus cost,
sampling, pressure proxy, and safety risk ledgers.

## Gym API

`chemworld.envs` exposes `BatchReactorWorld` through Gymnasium. Each `step()`
is an executable operation such as `add_reagent`, `heat`, `wait`, `measure`, or
`terminate`. The environment does not expose hidden species amounts or hidden
rate parameters unless explicitly constructed with `debug_truth=True`.

`BatchReactorWorld` integrates ODE dynamics for `A -> P`, `A -> B`,
`P -> D`, `A + P -> E`, and `Cat_active -> Cat_dead`, with a simplified energy
balance and instrument observation kernel.

Failed action preconditions return non-informative observations with empty
`observed_keys`, no instrument cost, no sample consumption, and an explicit
`error_message`. `final_assay` is a terminal scoring measurement: it requires a
terminated reaction state, ends the episode, and can only create one
`leaderboard_score`.

## Observation Kernel

Instrument observations are represented as:

- `raw_signal`: teaching- and research-facing instrument signal packets such as
  UV-vis spectra, HPLC peaks, GC peaks, or a final-assay packet;
- `processed_estimate`: derived estimates such as yield, selectivity,
  conversion, byproduct signal, or degradation warning;
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

`chemworld.data` defines the trajectory schema, logging utilities, and
anonymization helpers for human pilot studies.
