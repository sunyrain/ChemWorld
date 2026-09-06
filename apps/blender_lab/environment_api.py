"""REST contract for the lab environment, independent of the Blender renderer."""

from copy import deepcopy

from .engine import LabError, exact_keys

PREFIX = "/api/v1/environment"


def dispatch_environment(env, method, path, body=None):
    route = path[len(PREFIX) :]
    with env.lab.lock:
        if method == "GET":
            if route == "":
                return env.describe()
            if route == "/state":
                return env.snapshot()
            if route == "/supervision":
                return env.supervision()
            if route == "/events":
                return {"events": deepcopy(env.data["events"])}
            if route == "/bindings":
                return {"bindings": deepcopy(list(env.data["bindings"].values()))}
            if route == "/commands":
                return {"commands": deepcopy(list(env.data["commands"].values()))}
            if route == "/tasks":
                return {"tasks": deepcopy(list(env.data["tasks"].values()))}
            for prefix, bucket in [("/commands/", "commands"), ("/tasks/", "tasks")]:
                if route.startswith(prefix):
                    item = env.data[bucket].get(route[len(prefix) :])
                    if item:
                        return deepcopy(item)
                    raise LabError("Item not found", 404)
        elif method == "POST":
            data = body()
            if route == "/commands":
                return env.submit(data)
            if route == "/tasks":
                return env.create_task(data)
            if route == "/bindings":
                return env.bind(data)
            if route == "/observations":
                return env.observe(data)
            if route == "/demo/transport":
                exact_keys(data, [])
                return env.demo_transport()
        raise LabError("Environment endpoint/method not found", 404)


def extend_openapi(paths, operation):
    string = {"type": "string"}
    obj = {"type": "object"}

    def schema(properties, required=None):
        return {
            "type": "object",
            "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False,
        }

    command = schema(
        {
            "command_id": string,
            "type": {
                "enum": [
                    "robot.navigate",
                    "robot.pick",
                    "robot.place",
                    "asset.configure",
                    "asset.action",
                    "transfer",
                ]
            },
            "args": obj,
            "mode": {"const": "simulation"},
            "expected_revision": {"type": "integer"},
        },
        ["command_id", "type", "args"],
    )
    task = schema(
        {
            "task_id": string,
            "steps": {
                "type": "array",
                "minItems": 1,
                "maxItems": 50,
                "items": schema({"type": string, "args": obj}),
            },
        }
    )
    binding = schema(
        {
            "binding_id": string,
            "asset_id": string,
            "physical_id": string,
            "adapter": {"enum": ["manual", "mock", "sila2", "opcua", "ros2"]},
            "calibration_id": string,
            "max_age_s": {"type": "number", "minimum": 1, "maximum": 3600},
        },
        ["binding_id", "asset_id", "physical_id", "adapter", "calibration_id"],
    )
    observation = schema(
        {
            "observation_id": string,
            "binding_id": string,
            "metric": {"enum": ["temperature_c", "stir_rpm", "volume_ml", "mass_g"]},
            "value": {"type": "number"},
            "unit": string,
            "source_timestamp": {"type": "number"},
            "sequence": {"type": "integer", "minimum": 0},
            "quality": {"enum": ["good", "uncertain", "bad"]},
            "calibration_id": string,
        }
    )
    for route, summary in [
        ("", "Environment geometry, frames, constraints and capabilities"),
        ("/state", "Unified environment observation with separate simulated and observed state"),
        ("/supervision", "Read-only shadow comparison and drift/staleness decisions"),
        ("/events", "Environment journal"),
        ("/commands", "Command lifecycle records"),
        ("/tasks", "Generic sequential task plans"),
        ("/bindings", "Immutable device pairing records"),
    ]:
        paths[PREFIX + route] = {"get": operation(summary)}
    for route, summary, payload in [
        ("/commands", "Submit an idempotent simulation command", command),
        ("/tasks", "Submit a generic task plan", task),
        ("/bindings", "Pair a virtual asset with a declared physical identity", binding),
        (
            "/observations",
            "Ingest timestamped measurements without changing simulated or desired state",
            observation,
        ),
        ("/demo/transport", "Move the sealed example sample between stations", schema({})),
    ]:
        paths.setdefault(PREFIX + route, {})["post"] = operation(summary, payload)
    for route, param in [("commands", "command_id"), ("tasks", "task_id")]:
        paths[PREFIX + "/" + route + "/{" + param + "}"] = {
            "parameters": [{"in": "path", "name": param, "required": True, "schema": string}],
            "get": operation("Inspect lifecycle and result"),
        }
