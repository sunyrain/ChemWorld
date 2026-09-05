"""Virtual device state machine. Educational signals, not predictive chemistry."""

import json
import math
import os
import threading
import time
import uuid
from copy import deepcopy
from pathlib import Path

from .catalog import ASSETS, CATALOG, VERSION, public_asset


class LabError(Exception):
    def __init__(self, message, status=422):
        super().__init__(message)
        self.status = status


def finite(value, label, low=None, high=None):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise LabError(f"{label} must be a finite number")
    if (low is not None and value < low) or (high is not None and value > high):
        raise LabError(f"{label} outside allowed range [{low}, {high}]")
    return float(value)


def exact_keys(data, allowed):
    if not isinstance(data, dict):
        raise LabError("Expected a JSON object")
    extra = set(data) - set(allowed)
    if extra:
        raise LabError("Unknown fields: " + ", ".join(sorted(extra)))


class Lab:
    def __init__(self, data_dir):
        self.dir = Path(data_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.revision = 0
        self.states = {a["id"]: deepcopy(a["initial_state"]) for a in ASSETS}
        self.poses = {a["id"]: list(a["location"]) for a in ASSETS}
        self.results = {}
        self.events = []
        self.selected = "reactor_01"
        self.last_tick = time.monotonic()
        self.bridge = {"connected": False, "applied_revision": -1}
        self.last_bridge = 0
        state_file = self.dir / "state.json"
        if state_file.exists():
            data = json.loads(state_file.read_text(encoding="utf-8"))
            if data.get("version") == "1.0.0" and set(data["states"]) == set(self.states) - {
                "robot_01",
                "sample_tube_01",
            }:
                backup = self.dir / "state.before_environment_v1.json"
                if not backup.exists():
                    backup.write_text(state_file.read_text(encoding="utf-8"), encoding="utf-8")
                data["states"] = {**self.states, **data["states"]}
                data["poses"] = {**self.poses, **data["poses"]}
                data["version"] = VERSION
            if data.get("version") != VERSION or set(data["states"]) != set(self.states):
                raise RuntimeError(
                    "State/catalog version mismatch; "
                    "keep the old state and use a new data directory"
                )
            self.states = data["states"]
            self.poses = data["poses"]
            self.revision = data["revision"]
            self.results = data.get("results", {})
            self.events = data.get("events", [])
            # Do not restart heating after a server restart.
            for s in self.states.values():
                if "running" in s:
                    s["running"] = False
                    s["status"] = "idle"
        from .lab_environment import Environment

        self.environment = Environment(self)
        from .projection import ProjectionStore

        self.projection = ProjectionStore()
        self.record("server", "started", {})
        self.save()

    def save(self):
        data = {
            "version": VERSION,
            "revision": self.revision,
            "states": self.states,
            "poses": self.poses,
            "results": self.results,
            "events": self.events[-500:],
        }
        temp = self.dir / "state.tmp"
        temp.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
        )
        os.replace(temp, self.dir / "state.json")

    def record(self, asset_id, operation, detail):
        self.revision += 1
        event = {
            "revision": self.revision,
            "time": time.time(),
            "asset_id": asset_id,
            "operation": operation,
            "detail": deepcopy(detail),
        }
        self.events.append(event)
        self.events = self.events[-500:]
        with (self.dir / "events.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")

    def require(self, id):
        if not isinstance(id, str):
            raise LabError("asset id must be a string")
        if id not in CATALOG:
            raise LabError(f"Unknown asset: {id}", 404)
        return CATALOG[id], self.states[id]

    def get(self, id):
        with self.lock:
            a, s = self.require(id)
            return dict(
                **public_asset(a),
                state=deepcopy(s),
                position_m=self.poses[id][:],
                revision=self.revision,
            )

    def snapshot(self):
        with self.lock:
            return {
                "version": VERSION,
                "revision": self.revision,
                "selected": self.selected,
                "states": deepcopy(self.states),
                "poses": deepcopy(self.poses),
            }

    def patch(self, id, data):
        with self.lock:
            a, s = self.require(id)
            self.environment.guard(id, "configure")
            exact_keys(data, a["fields"])
            if not data:
                raise LabError("No writable fields supplied")
            for key, value in data.items():
                field = a["fields"][key]
                if field["type"] == "boolean":
                    if type(value) is not bool:
                        raise LabError(key + " must be boolean")
                else:
                    finite(value, key, field["minimum"], field["maximum"])
            if (
                a["kind"] == "hood"
                and (
                    data.get("fan_on") is False
                    or data.get("sash_open_pct", s["sash_open_pct"]) > 60
                )
                and any(
                    st.get("running") and CATALOG[k].get("hood") == id
                    for k, st in self.states.items()
                )
            ):
                raise LabError("Stop the reactor before changing ventilation to this state", 409)
            if s.get("running") and (data.get("door_open") or data.get("lid_open")):
                raise LabError("Stop the device before opening its door/lid", 409)
            s.update(data)
            self.record(id, "configure", data)
            self.save()
            return self.get(id)

    def action(self, id, data):
        with self.lock:
            a, s = self.require(id)
            if not isinstance(data, dict):
                raise LabError("Expected a JSON object")
            action = data.get("action")
            if action not in a["actions"]:
                raise LabError(f"Unsupported action {action!r}; supported: {a['actions']}")
            self.environment.guard(id, action)
            if a["kind"] == "mobile_manipulator" and action not in {
                "inspect",
                "select",
                "set_visible",
            }:
                return self.environment.robot_action(data)
            args = {k: v for k, v in data.items() if k != "action"}
            if action == "dispense":
                exact_keys(args, ["target_id", "amount", "unit"])
                return self.transfer(dict(source_id=id, **args))
            if action in {"measure", "weigh", "sample"}:
                return self.measure(id, action, args)
            allowed = {"move": ["position_m"], "set_visible": ["visible"]}.get(action, [])
            exact_keys(args, allowed)
            if action == "start":
                if s.get("door_open") or s.get("lid_open"):
                    raise LabError("Close the door/lid before starting", 409)
                if a.get("hood"):
                    hood = self.states[a["hood"]]
                    if not hood["fan_on"] or hood["sash_open_pct"] > 60:
                        raise LabError("Reactor requires ventilation on and sash <= 60%", 409)
                s.update(running=True, status="running")
                if a["kind"] == "centrifuge":
                    s["remaining_s"] = s["duration_s"]
            elif action == "stop":
                s.update(running=False, status="idle")
            elif action == "tare":
                s["reading"] = "0.0000 g"
                s["tare_g"] = s.get("last_mass_g", 0)
            elif action == "select":
                self.selected = id
            elif action == "set_visible":
                if type(args.get("visible")) is not bool:
                    raise LabError("visible must be boolean")
                s["visible"] = args["visible"]
            elif action == "move":
                pos = args.get("position_m")
                if not isinstance(pos, list) or len(pos) != 3:
                    raise LabError("position_m must contain x, y, z")
                for i, v in enumerate(pos):
                    finite(v, "position_m", -20 if i < 2 else 0, 20)
                delta = [pos[i] - self.poses[id][i] for i in range(3)]
                self.poses[id] = pos[:]

                def move_children(parent):
                    for child in ASSETS:
                        support = child.get("support")
                        if child.get("portable"):
                            station = self.environment.data["custody"].get(child["id"])
                            support = (
                                self.environment.definition["stations"]
                                .get(station, {})
                                .get("support")
                            )
                        if support == parent:
                            self.poses[child["id"]] = [
                                v + delta[i] for i, v in enumerate(self.poses[child["id"]])
                            ]
                            move_children(child["id"])

                move_children(id)
            self.record(id, action, args)
            self.save()
            return self.get(id)

    def transfer(self, data):
        with self.lock:
            exact_keys(data, ["source_id", "target_id", "amount", "unit"])
            src, dst = data.get("source_id"), data.get("target_id")
            a, s = self.require(src)
            b, t = self.require(dst)
            self.environment.guard(src, "transfer")
            self.environment.guard(dst, "transfer")
            if src == dst:
                raise LabError("Source and target must differ")
            amount = finite(data.get("amount"), "amount", 0.0001, 10000)
            unit = data.get("unit")
            if b["kind"] not in {"reactor", "vessel", "waste"}:
                raise LabError("Target must be a vessel, reactor, or waste container")
            if a["kind"] == "reagent":
                if unit != a["unit"]:
                    raise LabError(f"Expected unit {a['unit']}")
                if not s["cap_open"]:
                    raise LabError("Open the reagent cap first", 409)
                if amount > s["remaining"]:
                    raise LabError("Insufficient reagent inventory", 409)
                volume = amount if unit == "ml" else amount / a["density"]
                mass = amount if unit == "g" else amount * a["density"]
                additions = [
                    {
                        "reagent_id": src,
                        "amount": amount,
                        "unit": unit,
                        "volume_ml": volume,
                        "mass_g": mass,
                    }
                ]
            elif a["kind"] in {"reactor", "vessel"}:
                if unit != "ml":
                    raise LabError("Vessel transfers use ml")
                if amount > s["volume_ml"]:
                    raise LabError("Insufficient vessel contents", 409)
                ratio = amount / s["volume_ml"]
                additions = [
                    dict(
                        c,
                        amount=c["amount"] * ratio,
                        volume_ml=c["volume_ml"] * ratio,
                        mass_g=c["mass_g"] * ratio,
                    )
                    for c in s["contents"]
                ]
                volume, mass = amount, s["mass_g"] * ratio
            else:
                raise LabError("Source cannot dispense")
            if t["volume_ml"] + volume > b["capacity_ml"] + 1e-8:
                raise LabError("Target capacity exceeded", 409)
            # All validation happens before either inventory is changed.
            if a["kind"] == "reagent":
                s["remaining"] = round(s["remaining"] - amount, 6)
            else:
                s["volume_ml"] = max(0, s["volume_ml"] - volume)
                s["mass_g"] = max(0, s["mass_g"] - mass)
                s["contents"] = [
                    dict(
                        c,
                        amount=c["amount"] * (1 - ratio),
                        volume_ml=c["volume_ml"] * (1 - ratio),
                        mass_g=c["mass_g"] * (1 - ratio),
                    )
                    for c in s["contents"]
                    if c["amount"] * (1 - ratio) > 1e-8
                ]
            t["volume_ml"] += volume
            t["mass_g"] += mass
            for addition in additions:
                existing = next(
                    (c for c in t["contents"] if c["reagent_id"] == addition["reagent_id"]), None
                )
                if existing:
                    for k in ("amount", "volume_ml", "mass_g"):
                        existing[k] += addition[k]
                else:
                    t["contents"].append(addition)
            self.record(src, "transfer", data)
            self.save()
            return {
                "revision": self.revision,
                "source": self.get(src),
                "target": self.get(dst),
                "transferred_volume_ml": volume,
            }

    def measure(self, id, action, args):
        a, s = self.require(id)
        exact_keys(args, [] if action == "sample" else ["sample_id"])
        sample_id = id if action == "sample" else args.get("sample_id")
        b, sample = self.require(sample_id)
        if b["kind"] not in {"reactor", "vessel"} or sample["volume_ml"] <= 0:
            raise LabError("Measurement requires a non-empty vessel", 409)
        result = {
            "id": "result_" + uuid.uuid4().hex[:12],
            "asset_id": id,
            "sample_id": sample_id,
            "timestamp": time.time(),
            "mode": "educational_simulation",
            "method": action,
            "disclaimer": (
                "Synthetic educational output; "
                "not a validated analytical result or chemical prediction."
            ),
            "sample_snapshot": deepcopy(sample),
        }
        if action == "sample":
            result.update(
                kind="composition",
                volume_ml=sample["volume_ml"],
                mass_g=sample["mass_g"],
                contents=deepcopy(sample["contents"]),
            )
        elif a["kind"] == "balance":
            mass = sample["mass_g"]
            value = round(mass - s.get("tare_g", 0), 4)
            result.update(
                kind="mass",
                value=value,
                unit="g",
                model="Sum of tracked constituent masses, excluding vessel tare",
            )
            s.update(reading=f"{value:.4f} g", last_mass_g=mass)
        elif a["kind"] == "ph_meter":
            masses = {c["reagent_id"]: c["mass_g"] for c in sample["contents"]}
            value = round(
                max(
                    2,
                    min(
                        10,
                        7
                        - 0.7 * masses.get("citrate_01", 0)
                        + 0.35 * masses.get("bicarbonate_01", 0),
                    ),
                ),
                2,
            )
            result.update(
                kind="pH",
                value=value,
                unit="pH",
                model="Illustrative composition-to-pH mapping, not acid-base equilibrium",
            )
            s["reading"] = f"pH {value:.2f}"
        elif a["kind"] in {"uvvis", "ftir"}:
            uv = a["kind"] == "uvvis"
            xs = list(range(200, 901, 5)) if uv else list(range(400, 4001, 20))
            fraction = (
                sum(
                    c["volume_ml"]
                    for c in sample["contents"]
                    if c["reagent_id"] in {"cuso4_01", "indicator_01"}
                )
                / sample["volume_ml"]
            )
            peaks = (
                [(610, 75, 1.3 * fraction + 0.1), (280, 28, 0.25)]
                if uv
                else [(3350, 160, 42), (1650, 70, 30), (1100, 50, 24)]
            )
            ys = [
                round(
                    (
                        0.02
                        + sum(
                            amp * math.exp(-0.5 * ((x - center) / width) ** 2)
                            for center, width, amp in peaks
                        )
                    )
                    * s.get("path_length_cm", 1)
                    if uv
                    else 98
                    - sum(
                        amp * math.exp(-0.5 * ((x - center) / width) ** 2)
                        for center, width, amp in peaks
                    ),
                    5,
                )
                for x in xs
            ]
            result.update(
                kind="spectrum",
                x=xs,
                y=ys,
                x_unit="nm" if uv else "cm^-1",
                y_unit="AU" if uv else "%T",
                model="Synthetic Gaussian demonstration bands; no molecular identification",
            )
            s["reading"] = "SCAN COMPLETE"
        else:
            raise LabError("Measurement not supported")
        self.results[result["id"]] = result
        if "last_result_id" in s:
            s["last_result_id"] = result["id"]
        s["status"] = "ready"
        self.record(id, action, {"sample_id": sample_id, "result_id": result["id"]})
        self.save()
        return deepcopy(result)

    def tick(self):
        with self.lock:
            now = time.monotonic()
            dt = min(2, now - self.last_tick)
            self.last_tick = now
            changed = False
            for id, s in self.states.items():
                if "temperature_c" in s:
                    target = s["target_temperature_c"] if s["running"] else 25
                    old = s["temperature_c"]
                    s["temperature_c"] = round(old + (target - old) * (1 - math.exp(-dt / 20)), 3)
                    changed |= s["temperature_c"] != old
                if CATALOG[id]["kind"] == "centrifuge" and s["running"]:
                    s["remaining_s"] = round(max(0, s["remaining_s"] - dt), 2)
                    if not s["remaining_s"]:
                        s.update(running=False, status="complete")
                    changed = True
            if changed:
                self.revision += 1
                self.save()
            if self.environment.tick(dt):
                self.revision += 1
                self.save()

    def health(self):
        with self.lock:
            return {
                "service": "ChemLab API",
                "integration": "chemworld-blender-1",
                "version": VERSION,
                "asset_count": len(ASSETS),
                "revision": self.revision,
                "simulation": True,
                "bridge": dict(self.bridge, connected=time.time() - self.last_bridge < 5),
            }
