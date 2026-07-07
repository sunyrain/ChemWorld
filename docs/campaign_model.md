# Campaign Model

ChemWorld logs three nested levels:

- Campaign: one full benchmark run for a task and seed.
- Experiment: one recipe or experimental attempt inside a campaign.
- Operation: one executable laboratory action.

In campaign tasks, `final_assay` closes the current experiment but does not end
the whole campaign. In single-experiment tasks, `final_assay` terminates the
episode.

Every trajectory record includes:

- `campaign_id`
- `experiment_index`
- `operation_id`
- `scenario_id`
- `initial_state_id`

This makes replay and evaluation robust when a campaign contains many final
assays.
