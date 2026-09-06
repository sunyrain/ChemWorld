# Blender laboratory and automation assistant

The optional local application in `apps/blender_lab/` adds an editable laboratory, a mobile
manipulator, explicit carrier transport, and generic environment contracts. The installable adapter
is `chemworld.interfaces.blender`.

## Integration boundary

ChemWorld Core remains the experimental executor: it owns actions, public observations, budgets,
rewards, and exact replay. `BlenderObserver` reads public observation views and sends display frames
to the local Blender service. Student Lab, LLM runs, and classical runs share an opt-in hook. Unknown
measurements stay `null`; hidden world state and evaluator provenance are not sent to the viewer.
Presentation failure never retries a Core action and is exposed through `projection_error`.

Scene logistics are explicit workflow operations. The original ChemLab educational simulator has
separate inventory and synthetic measurements. The sealed demonstration carrier is not yet a Core
aliquot. The integrated example waits for transport between sampling and measurement. General Task
Lab actions update the public display only. UV–Vis, FTIR, and pH have instrument models; other
instruments appear as reports.

## Start locally

From the source checkout, substitute the actual Blender executable:

```powershell
uv sync --extra dev --python 3.12
uv run --no-sync python -m apps.blender_lab --blender "C:\path\to\blender.exe"
$env:CHEMWORLD_BLENDER_URL = "http://127.0.0.1:8877"
uv run --no-sync python -m apps.task_lab.server --port 8876
```

The Blender service uses port 8877; Task Lab uses 8876. Press **N** in Blender's 3D view. The
**ChemWorld** tab shows public experiment state; **自动化** controls the carrier and robot camera.
Motion is service-driven and does not need timeline playback. Use the launcher to connect the native
bridge. The app and scene require a checkout, while the Python observer ships in the package.

```powershell
uv run --no-sync python examples/demo_blender_workflow.py --output runs/blender_lab/my-demo/trajectory.jsonl
uv run --no-sync chemworld verify --constitution --submission runs/blender_lab/my-demo/trajectory.jsonl
```

Use a new output path for every run. Failed runs remain available. Each service port accepts one
active Core session; closing the session releases it and retains its final display.

## Physical pairing roadmap

The environment defines asset identities, nominal coordinates, capabilities, sample custody, command
lifecycles, normalized observations, and read-only discrepancy supervision. Future integration should
proceed through identity, spatial/sensor calibration, read-only data, shadow execution, then validated
bounded control. Physical sample identities and public measurement contracts still need to be mapped
to Core. Current supervision compares demo scene values and does not inject observations into Core.

There are no physical drivers, verified motion calibration, full-arm collision checks, or validated
contact dynamics. SiLA 2, OPC UA, and ROS 2 adapters are placeholders. Software integration tests do
not establish physical transfer validity.

See the [application guide](https://github.com/sunyrain/ChemWorld/tree/main/apps/blender_lab) and
[environment contract](https://github.com/sunyrain/ChemWorld/blob/main/apps/blender_lab/ENVIRONMENT.md)
for SDK examples, HTTP routes, ownership recovery, and development validation. The
[real-world roadmap](real_world_bridge.md) retains its separate evidence requirements.
