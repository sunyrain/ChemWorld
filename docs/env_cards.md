# Environment Card

## ChemWorld

`ChemWorld` is the single formal Gymnasium entry point.

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
obs, info = env.reset()
```

Task diversity is expressed through `task_id`, not through separate environment
names.

## Reset Info

`reset()` returns public task and runtime metadata, including:

- `world_law_id`;
- `task_id`;
- `scenario_id`;
- `initial_state_id`;
- `mechanism_id`;
- `mechanism_hash`;
- `task_contract_hash`;
- `runtime_profile_hash`;
- `scoring_contract_hash`;
- `observation_contract_hash`;
- `kernel_maturity`;
- `physics_maturity`;
- `proxy_allowed`;
- operation cards;
- instrument cards;
- backend spec;
- constitution summary.

Agents may use these fields for planning and reproducibility. They do not
contain hidden species amounts, hidden rate constants, or private mechanism
parameters.

## Step Contract

Each `step(action)` applies one executable operation:

```python
obs, reward, terminated, truncated, info = env.step(
    {"operation": "measure", "instrument": "hplc"}
)
```

The Gymnasium five-tuple remains standard. ChemWorld adds benchmark-specific
signals in `info`, including:

- `raw_signal`;
- `processed_estimate`;
- `uncertainty`;
- `observed_keys`;
- `observed_mask`;
- `cost`;
- `cost_components`;
- `constraint_flags`;
- `leaderboard_score`;
- `kernel_id`;
- `domain_service_id`;
- `world_events`;
- `state_patches_summary`.

## Rendering

The current renderer is `ansi`:

```bash
chemworld render --task reaction-to-assay --seed 0
```

It summarizes campaign state, experiment index, last operation, public ledger
state, and visible observations. It is intended for debugging and teaching,
not as a graphical lab interface.

## Checker Note

Scientific quantities that have not been measured are represented as `NaN` in
Gym arrays and `null` in JSONL. Gymnasium's raw env checker does not treat
reset-time `NaN` values as deterministic equivalents, so checker smoke tests
should wrap the env:

```python
from gymnasium.utils.env_checker import check_env
from chemworld.wrappers import NaNObservationWrapper

env = NaNObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay"))
check_env(env)
```

## Self-Consistency Gate

Use the environment audit script to check that task info, ledgers,
observations, spectra, scoring, logs, and replay remain aligned:

```bash
python scripts/audit_environment_consistency.py --tasks all --seeds 0 1 2
```

The audit writes JSON and CSV summaries under `runs/audit/`.

## Maturity Boundary

`ChemWorld` is a benchmark environment. Some task slices use proxy process
models and are marked as such. Release claims should report the maturity fields
from reset info and trajectory records rather than treating all tasks as
equally validated physical simulations.
