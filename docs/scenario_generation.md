# Scenario Generation

ChemWorld treats a task as a slice of one shared physical-chemical world, not as
an independent game. A scenario is the hidden parameter and initial-state family
behind that slice.

## Contract

Each scenario declares:

- `scenario_id`
- `world_law_id`
- `family`
- `split`
- `difficulty`
- `hidden_parameter_seed`
- `initial_state_seed`
- `initial_state_id`
- `parameter_profile`
- `allowed_module_tags`
- `expected_qualitative_behavior`

The default generator is deterministic: the same scenario, split, profile, and
seed reconstruct the same hidden world. `hidden_parameter_seed` and
`parameter_profile` shift the hidden kinetic/partition parameters;
`initial_state_seed` controls reproducible initial-state jitter for scenarios
that need it. Public and private splits share the same mechanism family but use
different hidden parameters.

## CLI

```bash
chemworld scenarios list
chemworld scenarios show reaction-to-purification
```

Use `chemworld tasks card <task_id>` to see the scenario card attached to a
benchmark task.
