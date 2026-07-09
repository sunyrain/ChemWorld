# Campaign Model

ChemWorld logs benchmark interaction at three nested levels:

```text
Campaign
  -> Experiment
      -> Operation
```

This distinction is important because Bayesian optimization, Latin hypercube
search, greedy search, and leaderboard agents often run many independent
experiments under one finite budget.

## Campaign

A campaign is one full benchmark run for one task and seed. It owns:

- `campaign_id`;
- `task_id`;
- `scenario_id`;
- `mechanism_hash`;
- global operation budget;
- experiment records;
- aggregate best-score, safety, cost, and sample-efficiency metrics.

In `campaign` tasks, the Gym episode continues until the global budget is
exhausted or a task-level terminal condition is reached.

## Experiment

An experiment is one attempt inside a campaign. It owns:

- `experiment_index`;
- initial state id;
- operation sequence;
- final-assay event if one occurs;
- terminal score and process summary.

For recipe-space optimizers, one recipe normally corresponds to one
experiment. `final_assay` closes that experiment and starts the next experiment
inside the same campaign.

## Operation

An operation is one executable laboratory action:

- `add_reagent`;
- `heat`;
- `measure`;
- `distill`;
- `electrolyze`;
- `terminate`;
- and other registered operations.

Every operation record includes:

- `operation_id`;
- `operation_type`;
- action payload;
- precondition results;
- affected ledgers;
- state-delta summary;
- world events;
- constitution checks;
- observation packet;
- reward, cost, and leaderboard-score fields when applicable.

## Episode Modes

ChemWorld uses two episode semantics.

| Mode | Final-assay behavior | Intended use |
| --- | --- | --- |
| `single_experiment` | `final_assay` terminates the Gym episode | teaching workflows, one complete procedure, downstream process tasks |
| `campaign` | `final_assay` closes the current experiment but does not terminate the campaign | BO, LHS, greedy search, public leaderboard optimization |

In both modes, `final_assay` requires a terminated or assay-ready experiment
state. Repeated final assays inside the same single experiment are rejected by
preconditions.

## Replay Contract

Replay verification restores:

- task id;
- scenario id;
- seed;
- mechanism hash;
- task/runtime/scoring/observation contract hashes;
- action sequence.

The verifier then recomputes observations, rewards, and constitution reports.
A mismatch in mechanism or contract hashes is a reproducibility failure rather
than a warning.
