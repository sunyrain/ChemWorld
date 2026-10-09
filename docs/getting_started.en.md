# Install, experiment and replay

This page targets the current development runtime, not the frozen paper physics.
Software worlds are not instructions for physical experiments.
[中文](getting_started.md) · [Distribution scope](community_release.md)

## Three entry points

1. **Use current features:** install a wheel built from main in an isolated environment:
   `python -m pip install /absolute/path/to/chemworld_bench-0.2.0-py3-none-any.whl`.
   A new PyPI release/tag has not been authorized. The old published 0.2.0 is not current main.
2. **Develop or run complete examples:** clone Git and use the committed lockfile below.
   Build from Git or a generated sdist, not a GitHub source ZIP.
3. **Reproduce paper results:** use the [independent frozen code and lockfile](https://github.com/sunyrain/ChemWorld-Public/tree/03e8026301c185fd6ba5bdbda7460765d9b3e724).
   Do not replay old trajectories under current physics.

Python 3.11/3.12 are validation targets; the distribution scope lists actual OS
results and unverified combinations. With uv already installed:

```bash
git clone https://github.com/sunyrain/ChemWorld.git
cd ChemWorld
uv sync --locked --extra dev
uv run --no-sync chemworld tasks list
```

## A final assay and your first custom agent

```bash
uv run --no-sync python examples/demo_manual_event_sequence.py
uv run --no-sync python examples/demo_agent_facing_api.py
uv run --no-sync python examples/demo_minimal_agent.py --output runs/minimal-agent.jsonl
uv run --no-sync chemworld verify --submission runs/minimal-agent.jsonl --tolerance 0
uv run --no-sync chemworld evaluate --submission runs/minimal-agent.jsonl
```

Choose a fresh output path: examples refuse to overwrite prior results.
`FourStepAgent` subclasses `BaseAgent` and implements `act(history)`. Replace that
method with your policy; this is a lifecycle example, not an optimizer or a
learned scientific model. The runner invokes reset/update and logs interactions.
It uses no provider key. `terminate` is not a final assay; a committed
`measure` with `instrument="final_assay"` closes the experiment. A low score is
still a result. Replay checks execution, not unrecorded reasoning.

These commands run in a checkout. With a wheel installed, use that environment's
`python`, `chemworld` and `chemworld-lab`. Example sources come with the repository
or sdist; a wheel does not create `examples/` in your current working directory.

## Complete offline research loop

```bash
uv run --no-sync python examples/demo_offline_research.py --output runs/offline-example
```

The [fixed example design](offline_research.md) includes seven episodes, notebook
writing, a host-owned fact ledger, forecasts sealed before held-out execution,
actual prediction errors, one expected rejection, an open batch, a truncated
batch, JSONL export and exact replay in seven new processes. It is a development
demonstration, not a paper rerun. Missing assays stay null, not zero; read
`observed_mask`. Optional Parquet backends are not validated by this JSONL example.

## Provider-free browser Lab

```bash
uv run --no-sync chemworld-lab --no-browser
```

Visit the printed local URL. Select a task, create a session, add materials,
terminate, perform `final_assay`, replay, export/copy JSONL, then close. Close never
inserts an assay. If downloading is blocked, copy the exported text before leaving
the page. Keep the service on loopback; it is not a sandbox or hosted service.
The checkout-only `apps.task_lab.server` is separate, not a wheel entry point.

## Public contract

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
try:
    _, info = env.reset(seed=0)
    print(info["task_id"])
    print(env.unwrapped.action_schema("heat"))
    print(env.unwrapped.available_actions())
finally:
    env.close()
```

`task_info()` declares support; `available_actions()` and `validate_action()` give
current legality. Use schema field names and units. See
[operations](operations.en.md) and the [contribution guide](https://github.com/sunyrain/ChemWorld/blob/main/CONTRIBUTING.md).
