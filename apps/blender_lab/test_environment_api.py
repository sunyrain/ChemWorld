"""Exercise SDK and adapters through an isolated HTTP server."""

import unittest

from . import test_lab
from .adapters import MockTemperatureAdapter, UnconfiguredHardwareAdapter
from .environment_client import EnvironmentClient


class EnvironmentHTTPTests(unittest.TestCase):
    setUp = test_lab.LabTests.setUp
    tearDown = test_lab.LabTests.tearDown

    def test_command_lifecycle_and_idempotency_over_http(self):
        client = EnvironmentClient(self.base)
        self.assertEqual(len(client.describe()["assets"]), 36)
        revision = client.observe()["simulation"]["revision"]
        job = client.step("robot.navigate", {"station": "preparation"}, "http-nav", revision)
        self.assertEqual(job["status"], "running")
        with self.lab.lock:
            for _ in range(20):
                self.lab.environment.tick(0.5)
        self.assertEqual(client.wait(job["id"], timeout=1)["status"], "succeeded")
        repeated = client.step("robot.navigate", {"station": "preparation"}, "http-nav", revision)
        self.assertEqual(repeated["status"], "succeeded")
        with self.assertRaises(ValueError):
            client.step("robot.navigate", {"station": "analysis"}, "http-nav")

    def test_mock_feedback_is_marked_and_does_not_change_simulator(self):
        client = EnvironmentClient(self.base)
        before = client.get("reactor_01")["state"]
        mock = MockTemperatureAdapter(client, offset=8)
        binding = mock.bind()
        self.assertEqual(binding["calibration_status"], "declared_not_verified")
        data = mock.publish_once()[0]
        self.assertTrue(data["synthetic"])
        self.assertEqual(client.publish(**data["input"])["id"], data["id"])
        comparison = client.supervision()["comparisons"][0]
        self.assertEqual(comparison["status"], "diverged")
        self.assertFalse(comparison["hardware_action_issued"])
        self.assertEqual(client.get("reactor_01")["state"], before)
        driver = UnconfiguredHardwareAdapter("ros2")
        with self.assertRaises(NotImplementedError):
            driver.execute({"action": "move"})

    def test_task_and_observation_validation_over_http(self):
        client = EnvironmentClient(self.base)
        task = client.task([{"type": "robot.navigate", "args": {"station": "home"}}], "http-task")
        with self.lab.lock:
            self.lab.environment.tick(0.5)
            self.lab.environment.tick(0.5)
        record = client.request("/api/v1/environment/tasks/" + task["id"])
        self.assertEqual(record["status"], "succeeded")
        mock = MockTemperatureAdapter(client)
        mock.bind()
        data = next(mock.observations())
        data["unit"] = "K"
        with self.assertRaises(ValueError):
            client.publish(**data)
        with self.assertRaises(ValueError):
            client.request(
                "/api/v1/environment/commands",
                {
                    "command_id": "physical",
                    "type": "robot.navigate",
                    "args": {"station": "home"},
                    "mode": "hardware",
                },
            )


if __name__ == "__main__":
    unittest.main()
