"""Standard-library client for the generic laboratory environment."""

import time
import uuid

from .client import ChemLabClient

PREFIX = "/api/v1/environment"
TERMINAL = {"succeeded", "failed", "cancelled", "interrupted"}


class EnvironmentClient(ChemLabClient):
    def describe(self):
        return self.request(PREFIX)

    def observe(self):
        return self.request(PREFIX + "/state")

    def step(self, kind, args, command_id=None, expected_revision=None):
        data = {
            "command_id": command_id or "cmd_" + uuid.uuid4().hex,
            "type": kind,
            "args": args,
            "mode": "simulation",
        }
        if expected_revision is not None:
            data["expected_revision"] = expected_revision
        return self.request(PREFIX + "/commands", data)

    def command(self, command_id):
        return self.request(PREFIX + "/commands/" + command_id)

    def wait(self, command_id, timeout=120):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.command(command_id)
            if result["status"] in TERMINAL:
                return result
            time.sleep(0.25)
        raise TimeoutError("Outcome unknown; query the original command_id before retrying")

    def task(self, steps, task_id=None):
        return self.request(
            PREFIX + "/tasks", {"task_id": task_id or "task_" + uuid.uuid4().hex, "steps": steps}
        )

    def transport_demo(self):
        return self.request(PREFIX + "/demo/transport", {})

    def bind(self, **definition):
        return self.request(PREFIX + "/bindings", definition)

    def publish(self, **observation):
        return self.request(PREFIX + "/observations", observation)

    def supervision(self):
        return self.request(PREFIX + "/supervision")
