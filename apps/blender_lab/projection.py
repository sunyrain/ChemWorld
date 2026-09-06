"""Single-view ownership and ordered public frames; no chemical state writes."""

import json
import re
import threading
import time
from copy import deepcopy

from .engine import LabError, exact_keys

FRAME_KEYS = {
    "schema_version",
    "session_id",
    "step",
    "source",
    "task_id",
    "operation",
    "status",
    "observations",
    "observed_mask",
    "campaign",
    "instrument",
    "asset_id",
    "mapping_status",
    "report_text",
    "physical_control_enabled",
}


class ProjectionStore:
    def __init__(self):
        self.lock = threading.RLock()
        self.frame = None
        self.owner = None
        self.received_at = None

    def snapshot(self):
        with self.lock:
            return {
                "frame": deepcopy(self.frame),
                "active_session_id": self.owner,
                "received_at": self.received_at,
                "physical_control_enabled": False,
            }

    def publish(self, frame):
        with self.lock:
            exact_keys(frame, FRAME_KEYS)
            if set(frame) != FRAME_KEYS:
                raise LabError("Incomplete public frame")
            if (
                frame["schema_version"] != "chemworld-blender-public-1"
                or frame["source"] != "chemworld_public_api"
                or frame["physical_control_enabled"] is not False
            ):
                raise LabError("Only public ChemWorld presentation frames are supported")
            sid = frame["session_id"]
            if not isinstance(sid, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,96}", sid):
                raise LabError("Invalid session_id")
            if type(frame["step"]) is not int or frame["step"] < 0:
                raise LabError("step must be a non-negative integer")
            if not all(
                isinstance(frame[k], dict) for k in ("observations", "observed_mask", "campaign")
            ):
                raise LabError("Invalid public observation maps")
            if any(type(v) is not bool for v in frame["observed_mask"].values()):
                raise LabError("Observation mask values must be boolean")
            for key, value in frame["observations"].items():
                if value is not None and (
                    type(value) not in {int, float}
                    or not (
                        frame["observed_mask"].get(key) or key in {"score", "cost", "safety_risk"}
                    )
                ):
                    raise LabError("Unmeasured values must be null")
            json.dumps(frame, allow_nan=False)
            if self.owner not in {None, sid}:
                raise LabError(
                    "Another session owns this scene; release it or use a separate port", 409
                )
            if self.owner == sid and self.frame is not None:
                if frame["step"] < self.frame["step"]:
                    raise LabError("Out-of-order public frame", 409)
                if frame["step"] == self.frame["step"]:
                    if frame != self.frame:
                        raise LabError("Step already published with different contents", 409)
                    return self.snapshot()
            self.owner = sid
            self.frame = deepcopy(frame)
            self.received_at = time.time()
            return self.snapshot()

    def release(self, data):
        with self.lock:
            exact_keys(data, ["session_id"])
            if data.get("session_id") != self.owner:
                raise LabError("Session does not own this scene", 409)
            self.owner = None
            return self.snapshot()
