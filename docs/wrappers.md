# Wrappers And Validity Signals

ChemWorld wrappers are optional Gymnasium wrappers. They do not change the core
environment contract.

## ActionMaskWrapper

`ActionMaskWrapper` adds operation-level validity signals to `info`:

- `valid_operations`: operation names whose current preconditions pass;
- `action_mask`: boolean mask aligned with `operation_types`;
- `operation_types`: ordered operation names;
- `invalid_reasons`: per-operation invalid reason summaries.

Example:

```python
import gymnasium as gym
import chemworld
from chemworld.wrappers import ActionMaskWrapper

env = ActionMaskWrapper(gym.make("ChemWorld", budget=12, seed=0))
obs, info = env.reset(seed=0)
print(info["valid_operations"])
```

The mask is produced by the shared `OperationValidator`, which combines task
allowed operations and physical constitution preconditions. Numeric payload
ranges remain the responsibility of action spaces, `ActionCodec`, and
constitution checks.

## SafetyCostWrapper

`SafetyCostWrapper` adds safe-RL style cost fields to `info` without changing
Gymnasium's five-value return:

- `cost_signal`;
- `cost_components`;
- `constraint_budget_remaining`.

Cost components are derived from unsafe operation, high cost, failed
preconditions, and failed constitution checks.

## NaNObservationWrapper

`NaNObservationWrapper` converts dict observations with missing `NaN` values
into RL-friendly vectors:

```python
from chemworld.wrappers import NaNObservationWrapper

env = NaNObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay"))
obs, info = env.reset()
```

The vector is:

```text
filled_values + observed_mask
```

Missing values are replaced by a configurable sentinel, defaulting to `-1.0`.

## Event Validation Helper

Use `validate_event_action(action, env)` to pre-check an event action against the
current state. This helper delegates to the same `OperationValidator` used by
the environment and wrappers.

