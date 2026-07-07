# Environment Card

## ChemWorld

`ChemWorld` is the single formal Gymnasium entry point.

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
obs, info = env.reset()
```

The environment exposes:

- shared `world_law_id`;
- scenario card;
- operation cards;
- instrument contracts;
- constitution summary;
- backend spec;
- observation keys;
- task policy.

Rendering:

```bash
chemworld render --task reaction-to-assay --seed 0
```

The current renderer is `ansi` and summarizes campaign, experiment, last
operation, ledger, and visible observations.

## Checker Note

The base environment uses `NaN` to represent not-yet-observed scientific
quantities. Gymnasium's raw env checker does not treat reset-time `NaN` values
as deterministic equivalents, so RL checker smoke tests should wrap the env:

```python
from gymnasium.utils.env_checker import check_env
from chemworld.wrappers import NaNObservationWrapper

env = NaNObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay"))
check_env(env)
```
