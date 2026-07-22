# ChemWorld System Model

> **This page is the normative source for architectural terminology, trajectory fields, and manuscript boundaries.**
> The authoritative evidence state is `configs/current.json`; implementation does not imply empirical closure.

ChemWorld unifies a **Physical Causal World Substrate**, an **Experimental Interaction Runtime**, and a **Task and
Evaluation Contract** so that search, execution, identification, and adaptation can be studied as one experimental-
intelligence problem. The agent, trainer, model weights, and private agent memory remain outside these three layers.

```text
trainer / pretraining / fine-tuning
                │
                ▼
              Agent
                │ public task, actions, observations, history
                ▼
┌────────────────────────────────────┐
│ Task and Evaluation Contract       │
├────────────────────────────────────┤
│ Experimental Interaction Runtime   │
├────────────────────────────────────┤
│ Physical Causal World Substrate    │
└────────────────────────────────────┘
```

ChemWorld can generate data for an external trainer or host training interactions. It does not update agent weights,
maintain agent beliefs, or select the next experiment for the agent.

## Layer responsibilities

| Layer | Owns | Does not own |
| --- | --- | --- |
| Physical Causal World Substrate | State, dynamics, constitutive laws, equipment, observation generation, constraints, controlled interventions | Task objectives, leaderboard weights, agent beliefs, training |
| Experimental Interaction Runtime | Action validity, transactions, lifecycle, measurements, visible feedback, failures, resource ledgers, trajectories | Agent action selection, silent closeout assistance, cross-task ranking |
| Task and Evaluation Contract | Public goal, action/observation permissions, budgets, termination, scoring, scenario distribution | Runtime physics or hidden-truth disclosure |

The current scoring compiler lives under `chemworld.world.scoring`, but the task layer has authority over objectives
and weights. The runtime executes a task-supplied scoring contract; the physical world does not define the research
objective.

## Physical causal worlds

A world family can be written as

\[
W=(\mathcal X,\mathcal U,T_\omega,O_\omega,C_\omega,\Delta_\omega),
\]

where the terms denote typed physical state, operations, hidden transitions, observation generation, constraints, and
controlled world interventions. Implemented intervention axes include parameters, rate-law form, topology,
constitutive relations, material mappings, and selected apparatus boundaries. Observation noise is configurable, but a
general independently validated sensor-law family is not a current claim.

## Experimental runtime

An Experiment begins from an explicitly initialized sample or process state, contains a sequence of operations and
measurements, and ends in final assay, explicit termination, failure, or budget truncation. Only a contract-valid final
assay is a comparable formal outcome; failures and incomplete runs remain in autonomy denominators.

```text
Campaign
└── Experiment
    └── Operation / Measurement
```

The same runtime exposes three action abstractions:

- **Campaign Design:** select a complete recipe or experiment;
- **Procedure Execution:** select one operation at a time;
- **Process Control:** select bounded equipment setpoints or process-control actions.

The current control interface is a bounded setpoint/process-control abstraction, not a claim of universal high-
frequency continuous control. The runtime validates and records lifecycle semantics but does not choose terminate or
final-assay actions for an autonomous agent.

## Task and evaluation contract

A task specifies the public goal, action and observation permissions, budgets, scoring rules, and world/intervention
distribution. Task endpoints, online shaping, constraints, information efficiency, resources, and procedural autonomy
remain separate; unlike physical quantities are not averaged into one cross-domain intelligence score.

## Canonical entities and identifiers

| Entity | Definition | Trajectory identifier |
| --- | --- | --- |
| Task | Stable public goal, permissions, budget, and scoring contract | `task_id`, `task_contract_hash` |
| World | One hidden physical-law instance | `world_id`, `mechanism_hash` |
| Scenario | Task–World composition plus initial state, interventions, reset/feedback condition, and seed | `scenario_id` |
| Campaign | One agent run on one Task × Scenario × Seed | `campaign_id` |
| Experiment | One initialized physical run within a campaign | `experiment_index` |
| Operation | One state-changing, measurement, or lifecycle action | `operation_id`, `action` |
| Run | Traceable execution instance | `run_id` |

The canonical benchmark cell is **Task × Scenario × Agent × Seed**.

Trajectory v0.1 stored a seed-specific run label in `task_id` and the stable task in `benchmark_task_id`. In v0.2,
`task_id` is the stable task-contract identifier and `run_id` carries the execution label. `benchmark_task_id` remains
a compatibility alias.

## Three outcome layers

Trajectory v0.2 fixes three top-level fields:

| Field | Meaning |
| --- | --- |
| `environment_outcome` | The transaction, physical observation, resource consequence, and lifecycle state actually produced by the world/runtime |
| `agent_visible_observation` | The observation and feedback actually released under this information condition |
| `evaluation_outcome` | The true evaluation endpoint/reward and scoring-contract binding |

Feedback ablations may change only `agent_visible_observation`; they must not rewrite the environment or evaluation
outcomes. The v0.1 aliases `observation`, `reward`, `agent_view`, and `leaderboard_score` remain during migration.

## Bounded completeness

ChemWorld distinguishes:

- **structural completeness:** the hidden-world → action → transition → measurement → feedback → next-experiment
  interaction chain is closed by design;
- **evaluation completeness:** outcomes, constraints, resources, adaptation, and autonomy have explicit contracts, but
  formal cross-method evidence remains incomplete;
- **attribution completeness:** diagnostics are designed to separate under-identifiability, experiment choice,
  feedback use, recovery, and lifecycle failure, but mechanism Gate A remains blocked.

The normative boundary is:

> **ChemWorld targets structural completeness of the experimental-interaction stack across selected physical-
> chemistry archetypes; chemical coverage and numerical fidelity are bounded and explicitly declared, not
> exhaustive.**

## Core, Diagnostic, and Extended

- **Core** is the frozen v0.4 formal comparison scope: partition discovery, reaction-to-crystallization,
  reaction-to-distillation, and flow-reaction optimization.
- **Diagnostic** contains identifiability, no-change, feedback branching, counterfactual, adaptation-decomposition,
  and autonomy protocols. Mechanism v0.2.1 currently starts with crystallization and electrochemistry.
- **Extended** contains the remaining registered tasks, training uses, and demonstrations. Coverage does not grant a
  formal ranking claim.

These are evaluation roles, not separate engines. Changing the formal Core requires a new major protocol; scientific
archetypes must not silently rewrite a frozen scope.

## Mechanism-understanding evidence

1. **Declared:** an auditable mechanism distribution or change probability;
2. **Predictive:** a testable prediction for an unexecuted intervention;
3. **Actionable:** a belief that changes experiment choice and improves recovery or regret under a fixed budget.

Mechanism v0.2.1 primarily covers declared and action diagnostics. An independent predictive probe is a future
protocol feature, not a completed current result.

## Current boundary

The candidate backend and replay controls are operational. Formal method freeze remains blocked, mechanism Gate A
requires recertification after the public contract change, and external Bridge evidence is absent. Documentation and manuscript claims must follow
`configs/current.json` rather than infer scientific readiness from software availability.
