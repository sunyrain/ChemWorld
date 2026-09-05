"""Environment-level commands, sample custody and read-only digital-twin supervision."""

import json
import math
import os
import re
import time
import uuid
from copy import deepcopy
from pathlib import Path

from .catalog import ASSETS, CATALOG
from .engine import LabError, exact_keys, finite
from .navigation import Navigator

ROOT = Path(__file__).resolve().parent
TERMINAL = {"succeeded", "failed", "cancelled", "interrupted"}
COMMAND_TYPES = {
    "robot.navigate",
    "robot.pick",
    "robot.place",
    "asset.configure",
    "asset.action",
    "transfer",
}


def identifier(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}", value):
        raise LabError(label + " must be a stable identifier (1-96 ASCII characters)")
    return value


def vector(value, label):
    if not isinstance(value, list) or len(value) != 3:
        raise LabError(label + " requires [x,y,z]")
    return [finite(v, label, -20, 20) for v in value]


def robot_tcp(pose, state, extension=None):
    """Cartesian tool centre used consistently by the simulator and visual arm."""
    yaw = math.radians(state["base_yaw_deg"])
    home = [pose[0] - 0.16 * math.sin(yaw), pose[1] + 0.16 * math.cos(yaw), pose[2] + 0.86]
    t = state["arm_extension"] if extension is None else extension
    target = state["arm_target_m"]
    return [home[i] * (1 - t) + target[i] * t for i in range(3)]


class Environment:
    def __init__(self, lab):
        self.lab = lab
        self.definition = json.loads((ROOT / "environment.json").read_text(encoding="utf-8"))
        self.nav = Navigator(lab, self.definition)
        self.path = lab.dir / "environment_state.json"
        self.data = {
            "schema_version": "1.0",
            "revision": 0,
            "commands": {},
            "tasks": {},
            "bindings": {},
            "observations": {},
            "latest": {},
            "custody": {"sample_tube_01": "preparation"},
            "events": [],
        }
        self.internal = False
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
            for bucket in ["commands", "tasks"]:
                for item in self.data[bucket].values():
                    if item["status"] not in TERMINAL:
                        item.update(
                            status="interrupted",
                            reason="Service restarted; effects will not be replayed",
                            finished_at=time.time(),
                        )
        state = lab.states["robot_01"]
        state.update(active_command_id="", status="estopped" if state["estopped"] else "idle")
        self.event("environment.started", {"restart_policy": "interrupt"})
        self.save()

    def save(self):
        temp = self.path.with_suffix(".tmp")
        temp.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
        )
        os.replace(temp, self.path)

    def event(self, kind, detail):
        self.data["revision"] += 1
        e = {
            "sequence": self.data["revision"],
            "time": time.time(),
            "type": kind,
            "detail": deepcopy(detail),
        }
        self.data["events"].append(e)
        self.data["events"] = self.data["events"][-500:]
        with (self.lab.dir / "environment_events.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    def guard(self, id, operation):
        if self.internal:
            return
        robot = self.lab.states["robot_01"]
        if id == robot.get("held_asset_id") and operation not in {"select", "inspect", "sample"}:
            raise LabError("Sample is held by robot; place it before modifying it", 409)
        job = self.data["commands"].get(robot.get("active_command_id"))
        if (
            job
            and id in job.get("resources", [])
            and operation not in {"select", "inspect", "estop"}
        ):
            raise LabError("Resource reserved by active command " + job["id"], 409)

    def describe(self):
        result = deepcopy(self.definition)
        result["assets"] = [
            {
                "id": a["id"],
                "kind": a["kind"],
                "capabilities": a["actions"],
                "writable_fields": a["fields"],
                "frame": "lab_world",
                "support": a.get("support"),
                "portable": a.get("portable", False),
            }
            for a in ASSETS
        ]
        return result

    def snapshot(self):
        with self.lab.lock:
            robot = deepcopy(self.lab.states["robot_01"])
            return {
                "environment_id": self.definition["environment_id"],
                "schema_version": "1.0",
                "timestamp": time.time(),
                "revision": self.data["revision"],
                "simulation": self.lab.snapshot(),
                "robot": robot,
                "custody": deepcopy(self.data["custody"]),
                "commands": deepcopy(list(self.data["commands"].values())[-100:]),
                "tasks": deepcopy(list(self.data["tasks"].values())[-100:]),
                "supervision": self.supervision(),
                "hardware_dispatch_enabled": False,
            }

    def validate_command(self, data):
        exact_keys(data, ["command_id", "type", "args", "mode", "expected_revision"])
        cid = identifier(data.get("command_id"), "command_id")
        if data.get("type") not in COMMAND_TYPES:
            raise LabError("Unknown command type")
        if data.get("mode", "simulation") != "simulation":
            raise LabError(
                "Only simulation execution is implemented; hardware output is not configured", 409
            )
        if not isinstance(data.get("args"), dict):
            raise LabError("args must be an object")
        if "expected_revision" in data and type(data["expected_revision"]) is not int:
            raise LabError("expected_revision must be an integer")
        return cid

    def submit(self, data):
        with self.lab.lock:
            cid = self.validate_command(data)
            signature = json.dumps(data, sort_keys=True, allow_nan=False)
            previous = self.data["commands"].get(cid)
            if previous:
                if previous["request_json"] != signature:
                    raise LabError("command_id already used for different parameters", 409)
                return deepcopy(previous)
            if "expected_revision" in data and data["expected_revision"] != self.lab.revision:
                raise LabError("Stale simulation revision", 409)
            kind = data["type"]
            args = data["args"]
            job = {
                "id": cid,
                "type": kind,
                "args": deepcopy(args),
                "mode": "simulation",
                "status": "accepted",
                "accepted_at": time.time(),
                "request_json": signature,
                "resources": [],
                "result": None,
            }
            if kind.startswith("robot."):
                self.prepare_robot(job)
                job.update(status="running", started_at=time.time())
                self.lab.states["robot_01"].update(
                    active_command_id=cid,
                    status="navigating" if kind == "robot.navigate" else "manipulating",
                )
            else:
                # Record and persist acceptance before executing a mutating operation.
                self.data["commands"][cid] = job
                self.event("command.accepted", {"command_id": cid})
                self.save()
                self.internal = True
                try:
                    if kind in {"asset.configure", "asset.action"}:
                        exact_keys(args, ["asset_id", "parameters"])
                        aid = args.get("asset_id")
                        self.lab.require(aid)
                        self.internal = False
                        self.guard(
                            aid,
                            "configure"
                            if kind.endswith("configure")
                            else args.get("parameters", {}).get("action"),
                        )
                        self.internal = True
                        if aid == "robot_01":
                            raise LabError("Use robot commands for the mobile manipulator")
                        job["result"] = (
                            self.lab.patch(aid, args.get("parameters"))
                            if kind.endswith("configure")
                            else self.lab.action(aid, args.get("parameters"))
                        )
                    elif kind == "transfer":
                        self.internal = False
                        job["result"] = self.lab.transfer(args)
                        self.internal = True
                    job.update(status="succeeded", finished_at=time.time())
                except (LabError, TypeError, ValueError) as e:
                    job.update(status="failed", reason=str(e), finished_at=time.time())
                finally:
                    self.internal = False
            self.data["commands"][cid] = job
            self.event("command." + job["status"], {"command_id": cid, "type": kind})
            self.lab.record("environment", "command", {"command_id": cid, "status": job["status"]})
            self.lab.save()
            self.save()
            return deepcopy(job)

    def station(self, name):
        if not isinstance(name, str) or name not in self.definition["stations"]:
            raise LabError("Unknown station")
        return self.definition["stations"][name]

    def prepare_robot(self, job):
        state = self.lab.states["robot_01"]
        pose = self.lab.poses["robot_01"]
        args = job["args"]
        if state["estopped"]:
            raise LabError("Robot is emergency-stopped; reset before commanding", 409)
        if state["active_command_id"]:
            raise LabError("Robot already has an active command", 409)
        if not self.nav.clear(pose):
            raise LabError("Robot footprint currently obstructed", 409)
        job["resources"] = ["robot_01"]
        if state["held_asset_id"]:
            job["resources"].append(state["held_asset_id"])
        if job["type"] == "robot.navigate":
            exact_keys(args, ["station", "position_m"])
            if ("station" in args) == ("position_m" in args):
                raise LabError("Specify station or position_m, exactly one")
            station = self.station(args["station"]) if "station" in args else None
            goal = station["dock_m"] if station else vector(args["position_m"], "position_m")
            if abs(goal[2] - 0.08) > 1e-5:
                raise LabError("Mobile base must remain on the floor at z=0.08 m")
            job.update(
                path=self.nav.path(pose, goal),
                waypoint=0,
                goal=goal[:],
                final_yaw_deg=station["yaw_deg"] if station else None,
            )
            return
        exact_keys(args, ["asset_id"] if job["type"] == "robot.pick" else ["station"])
        if job["type"] == "robot.pick":
            aid = args.get("asset_id")
            asset, sample = self.lab.require(aid)
            if state["held_asset_id"]:
                raise LabError("Gripper already holds a sample", 409)
            if not asset.get("portable") or not sample.get("sealed"):
                raise LabError(
                    "Pick requires a portable sample with a declared grasp profile and closed cap",
                    409,
                )
            target = self.lab.poses[aid][:]
            support = self.data["custody"].get(aid)
            station = self.station(support)
            if math.dist(pose, station["dock_m"]) > 0.12:
                raise LabError("Navigate to the sample station before picking", 409)
            target = [target[i] + asset["grasp_offset_m"][i] for i in range(3)]
            job.update(asset_id=aid)
            job["resources"].append(aid)
        else:
            aid = state["held_asset_id"]
            if not aid:
                raise LabError("Gripper is empty", 409)
            station = self.station(args.get("station"))
            if "sample_position_m" not in station:
                raise LabError("Station has no sample handoff surface")
            if math.dist(pose, station["dock_m"]) > 0.12:
                raise LabError("Navigate to destination station before placing", 409)
            if any(v == args["station"] and k != aid for k, v in self.data["custody"].items()):
                raise LabError("Handoff position is occupied", 409)
            target = [
                station["sample_position_m"][i] + CATALOG[aid]["grasp_offset_m"][i]
                for i in range(3)
            ]
            job.update(asset_id=aid, place_position=station["sample_position_m"][:])
        if math.dist(target, [pose[0], pose[1] + 0.08, pose[2] + 0.84]) > 0.86:
            raise LabError("Sample is outside configured arm reach", 409)
        job.update(elapsed_s=0.0, grasp_done=False)
        state.update(arm_target_m=target, arm_extension=0.0)

    def robot_action(self, data):
        action = data.get("action")
        if action in {"estop", "reset_estop"}:
            exact_keys(data, ["action"])
            state = self.lab.states["robot_01"]
            if action == "estop":
                cid = state["active_command_id"]
                if cid:
                    self.finish(self.data["commands"][cid], "cancelled", "Emergency stop requested")
                for task in self.data["tasks"].values():
                    if task["status"] not in TERMINAL:
                        task.update(status="cancelled", reason="Emergency stop requested")
                state.update(estopped=True, status="estopped")
            else:
                state.update(estopped=False, status="idle")
            self.event("robot." + action, {})
            self.lab.record("robot_01", action, {})
            self.lab.save()
            self.save()
            return self.lab.get("robot_01")
        if action == "home":
            exact_keys(data, ["action"])
            args = {"station": "home"}
            kind = "navigate"
        else:
            args = {k: v for k, v in data.items() if k != "action"}
            kind = action
        return self.submit(
            {"command_id": "robot_" + uuid.uuid4().hex[:16], "type": "robot." + kind, "args": args}
        )

    def create_task(self, data):
        with self.lab.lock:
            exact_keys(data, ["task_id", "steps"])
            tid = identifier(data.get("task_id"), "task_id")
            steps = data.get("steps")
            if not isinstance(steps, list) or not 1 <= len(steps) <= 50:
                raise LabError("steps must contain 1-50 commands")
            for i, step in enumerate(steps):
                exact_keys(step, ["type", "args"])
                self.validate_command(dict(command_id=f"{tid}:{i}", **step))
            old = self.data["tasks"].get(tid)
            if old:
                if old["steps"] != steps:
                    raise LabError("task_id already used for another plan", 409)
                return deepcopy(old)
            if any(t["status"] not in TERMINAL for t in self.data["tasks"].values()):
                raise LabError("Another environment task is active", 409)
            task = {
                "id": tid,
                "steps": deepcopy(steps),
                "status": "queued",
                "step_index": 0,
                "accepted_at": time.time(),
            }
            self.data["tasks"][tid] = task
            self.event("task.queued", {"task_id": tid})
            self.save()
            return deepcopy(task)

    def finish(self, job, status="succeeded", reason=None):
        job.update(status=status, finished_at=time.time())
        if reason:
            job["reason"] = reason
        state = self.lab.states["robot_01"]
        state.update(active_command_id="", status="idle" if status == "succeeded" else "stopped")
        self.event("command." + status, {"command_id": job["id"], "reason": reason})

    def tick(self, dt):
        state = self.lab.states["robot_01"]
        pose = self.lab.poses["robot_01"]
        changed = False
        job = self.data["commands"].get(state["active_command_id"])
        if job and job["status"] == "running":
            changed = True
            if job["type"] == "robot.navigate":
                distance = state["speed_m_s"] * dt
                while distance > 0 and job["waypoint"] < len(job["path"]):
                    target = job["path"][job["waypoint"]]
                    remaining = math.dist(pose, target)
                    if not self.nav.segment_clear(pose, target):
                        self.finish(job, "failed", "Route obstructed after planning")
                        break
                    if remaining < 1e-6:
                        job["waypoint"] += 1
                        continue
                    step = min(distance, remaining)
                    fraction = step / remaining
                    state["base_yaw_deg"] = math.degrees(
                        math.atan2(-(target[0] - pose[0]), target[1] - pose[1])
                    )
                    pose[:] = [pose[i] + (target[i] - pose[i]) * fraction for i in range(3)]
                    state["wheel_angle_deg"] += math.degrees(step / 0.095)
                    distance -= step
                    if remaining <= step + 1e-8:
                        job["waypoint"] += 1
                if job["status"] == "running" and job["waypoint"] == len(job["path"]):
                    if job["final_yaw_deg"] is not None:
                        state["base_yaw_deg"] = job["final_yaw_deg"]
                    self.finish(job)
            else:
                job["elapsed_s"] += dt
                t = min(1, job["elapsed_s"] / 4)
                state["arm_extension"] = 2 * t if t < 0.5 else 2 * (1 - t)
                if t >= 0.5 and not job["grasp_done"]:
                    aid = job["asset_id"]
                    if job["type"] == "robot.pick":
                        state.update(held_asset_id=aid, gripper_open=False)
                        self.data["custody"][aid] = "robot_01"
                    else:
                        state.update(held_asset_id="", gripper_open=True)
                        self.lab.poses[aid] = job["place_position"][:]
                        self.data["custody"][aid] = job["args"]["station"]
                    job["grasp_done"] = True
                    self.event(
                        "sample.custody",
                        {
                            "asset_id": aid,
                            "holder": self.data["custody"][aid],
                            "command_id": job["id"],
                        },
                    )
                if t >= 1:
                    self.finish(job)
            state["battery_pct"] = max(0, state["battery_pct"] - dt * 0.001)
        if state["held_asset_id"]:
            aid = state["held_asset_id"]
            tcp = robot_tcp(pose, state)
            self.lab.poses[aid] = [tcp[i] - CATALOG[aid]["grasp_offset_m"][i] for i in range(3)]
        for task in self.data["tasks"].values():
            if task["status"] in TERMINAL:
                continue
            index = task["step_index"]
            cid = f"{task['id']}:{index}"
            current = self.data["commands"].get(cid)
            if current and current["status"] == "succeeded":
                task["step_index"] += 1
                index += 1
                cid = f"{task['id']}:{index}"
                current = None
                changed = True
            if current and current["status"] in TERMINAL:
                task.update(
                    status="failed",
                    reason=current.get("reason", current["status"]),
                    finished_at=time.time(),
                )
                self.event("task.failed", {"task_id": task["id"]})
                changed = True
            elif index >= len(task["steps"]):
                task.update(status="succeeded", finished_at=time.time())
                self.event("task.succeeded", {"task_id": task["id"]})
                changed = True
            elif current is None:
                try:
                    self.submit(dict(command_id=cid, **task["steps"][index]))
                    task["status"] = "running"
                except LabError as e:
                    task.update(status="failed", reason=str(e), finished_at=time.time())
                    self.event("task.failed", {"task_id": task["id"], "reason": str(e)})
                changed = True
        if changed:
            self.save()
        return changed

    def bind(self, data):
        with self.lab.lock:
            exact_keys(
                data,
                ["binding_id", "asset_id", "physical_id", "adapter", "calibration_id", "max_age_s"],
            )
            bid = identifier(data.get("binding_id"), "binding_id")
            self.lab.require(data.get("asset_id"))
            identifier(data.get("physical_id"), "physical_id")
            identifier(data.get("calibration_id"), "calibration_id")
            if (
                data.get("adapter") not in self.definition["adapters"]
                or data["adapter"] == "simulation"
            ):
                raise LabError("Unknown observation adapter")
            finite(data.get("max_age_s", 15), "max_age_s", 1, 3600)
            old = self.data["bindings"].get(bid)
            if old:
                if old["definition"] != data:
                    raise LabError(
                        "Binding is immutable; create a new binding_id after recalibration", 409
                    )
                return deepcopy(old)
            binding = {
                "id": bid,
                "definition": deepcopy(data),
                "created_at": time.time(),
                "calibration_status": "declared_not_verified",
                "hardware_dispatch_enabled": False,
            }
            self.data["bindings"][bid] = binding
            self.event("binding.created", {"binding_id": bid})
            self.save()
            return deepcopy(binding)

    def observe(self, data):
        with self.lab.lock:
            exact_keys(
                data,
                [
                    "observation_id",
                    "binding_id",
                    "metric",
                    "value",
                    "unit",
                    "source_timestamp",
                    "sequence",
                    "quality",
                    "calibration_id",
                ],
            )
            oid = identifier(data.get("observation_id"), "observation_id")
            previous = self.data["observations"].get(oid)
            if previous:
                if previous["input"] != data:
                    raise LabError("observation_id conflict", 409)
                return deepcopy(previous)
            binding = self.data["bindings"].get(data.get("binding_id"))
            if not binding:
                raise LabError("Unknown binding", 404)
            spec = binding["definition"]
            metric = data.get("metric")
            metric_spec = self.definition["metrics"].get(metric)
            if not metric_spec or metric not in self.lab.states[spec["asset_id"]]:
                raise LabError("Metric is not declared for this asset")
            if data.get("unit") != metric_spec["unit"]:
                raise LabError("Unit mismatch; adapter must normalize to " + metric_spec["unit"])
            finite(data.get("value"), "value")
            timestamp = finite(data.get("source_timestamp"), "source_timestamp", 0, time.time() + 5)
            if type(data.get("sequence")) is not int or data["sequence"] < 0:
                raise LabError("sequence must be a non-negative integer")
            if data.get("quality") not in {"good", "uncertain", "bad"}:
                raise LabError("quality must be good, uncertain or bad")
            if data.get("calibration_id") != spec["calibration_id"]:
                raise LabError("Calibration identity mismatch", 409)
            key = spec["asset_id"] + ":" + metric + ":" + binding["id"]
            old = self.data["observations"].get(self.data["latest"].get(key, ""))
            if old and (
                data["sequence"] <= old["input"]["sequence"]
                or timestamp < old["input"]["source_timestamp"]
            ):
                raise LabError("Out-of-order observation", 409)
            observation = {
                "id": oid,
                "input": deepcopy(data),
                "received_at": time.time(),
                "asset_id": spec["asset_id"],
                "source_kind": "mock"
                if spec["adapter"] == "mock"
                else "manual"
                if spec["adapter"] == "manual"
                else "external_unverified",
                "synthetic": spec["adapter"] == "mock",
            }
            self.data["observations"][oid] = observation
            self.data["latest"][key] = oid
            self.event("observation.received", {"observation_id": oid, "binding_id": binding["id"]})
            self.save()
            return deepcopy(observation)

    def supervision(self):
        comparisons = []
        for oid in self.data["latest"].values():
            observation = self.data["observations"][oid]
            data = observation["input"]
            binding = self.data["bindings"][data["binding_id"]]["definition"]
            metric = data["metric"]
            spec = self.definition["metrics"][metric]
            state = self.lab.states[binding["asset_id"]]
            age = max(0, time.time() - data["source_timestamp"])
            eligible = age <= binding.get("max_age_s", 15) and data["quality"] == "good"
            delta = data["value"] - state[metric]
            status = (
                "stale"
                if age > binding.get("max_age_s", 15)
                else "invalid_quality"
                if data["quality"] != "good"
                else "diverged"
                if abs(delta) > spec["tolerance"]
                else "aligned"
            )
            comparisons.append(
                {
                    "asset_id": binding["asset_id"],
                    "binding_id": data["binding_id"],
                    "metric": metric,
                    "unit": spec["unit"],
                    "desired": state.get(spec.get("target", "")),
                    "simulated": state[metric],
                    "observed": data["value"],
                    "observed_minus_simulated": delta,
                    "tolerance": spec["tolerance"],
                    "age_s": round(age, 3),
                    "quality": data["quality"],
                    "calibration_id": data["calibration_id"],
                    "source_kind": observation["source_kind"],
                    "synthetic": observation["synthetic"],
                    "status": status,
                    "eligible_for_comparison": eligible,
                    "recommendation": "continue observing"
                    if status == "aligned"
                    else "hold dependent physical steps and inspect",
                    "hardware_action_issued": False,
                }
            )
        return {
            "mode": "shadow_read_only",
            "bindings": deepcopy(list(self.data["bindings"].values())),
            "comparisons": comparisons,
            "physical_control_enabled": False,
        }

    def demo_transport(self):
        station = self.data["custody"]["sample_tube_01"]
        if station == "robot_01":
            raise LabError(
                "Place the currently held sample before starting a new transport demo", 409
            )
        destination = "analysis" if station == "preparation" else "preparation"
        return self.create_task(
            {
                "task_id": "transport_" + uuid.uuid4().hex[:10],
                "steps": [
                    {"type": "robot.navigate", "args": {"station": station}},
                    {"type": "robot.pick", "args": {"asset_id": "sample_tube_01"}},
                    {"type": "robot.navigate", "args": {"station": destination}},
                    {"type": "robot.place", "args": {"station": destination}},
                    {"type": "robot.navigate", "args": {"station": "home"}},
                ],
            }
        )
