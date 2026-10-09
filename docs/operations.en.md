# Operations and instruments

Use the current public schema, not guessed laboratory verbs:

```python
{"operation": "heat", "target_temperature_K": 350.0,
 "duration_s": 1200.0, "stirring_speed_rpm": 800.0}
```

`target_temperature_K` is the jacket setpoint, not an instantaneous measured
sample temperature. `heat`/`wait` continue the current vessel's process. `quench`
does not create a new batch. `cool`, `stir`, `crystallize` and `filter` are not
standalone action IDs: use the task's actual operations, such as
`cool_crystallize` and `filter_crystals`.

`add_solvent` can accumulate allowed finite-catalog mixtures; some task contracts
restrict pure media. `add_reagent` is the declared premixed feed; `add_component`
selects a public `feed_catalog` component. Resources use actual molar input.
Do not infer hidden species names or assume every first material choice locks all
future additions. New vessel/port and persistent-control operations are available
only under their declared task/composition contracts.

For every state, inspect `task_info()`, `action_schema(operation)`,
`available_actions()` and `validate_action(action)`. Registry membership is not
task permission, and task permission is not current-state legality. Never
hard-code the action vector length or silently clip out-of-range values.

Executable instrument IDs are `hplc`, `gc`, `uvvis`, `ph_meter`, `final_assay`;
some full-process contracts additionally permit `particle_size`. Read
`allowed_instruments`. IR/NMR-like features inside a synthetic spectral packet
are **not** separate `measure` instrument IDs. Model-library availability does
not create a new agent action.

End a process with `terminate`, then request
`{"operation": "measure", "instrument": "final_assay"}`. Neither an open record,
a cancelled session nor a budget truncation is a completed final assay. Missing
values remain null; read masks. A negative result is retained as an assay, not
deleted. Native replay reconstructs actions and observations, not reasoning.

Start with [the executable examples](getting_started.en.md). These virtual model
operations are not physical laboratory instructions.
