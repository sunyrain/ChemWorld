"""Acceptance checks for asynchronous robotics and observation provenance."""

import tempfile
import time
import unittest
from copy import deepcopy

from .engine import Lab, LabError


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.lab = Lab(self.temp.name)
        self.env = self.lab.environment

    def tearDown(self):
        self.temp.cleanup()

    def run_until(self, predicate, max_steps=1000):
        for _ in range(max_steps):
            if predicate():
                return
            with self.lab.lock:
                self.env.tick(0.5)
        self.fail("command/task did not terminate")

    def command(self, cid, kind, **args):
        return self.env.submit({"command_id": cid, "type": kind, "args": args})

    def binding(self):
        return self.env.bind(
            {
                "binding_id": "mock_temp",
                "asset_id": "reactor_01",
                "physical_id": "MOCK-R01",
                "adapter": "mock",
                "calibration_id": "mock-cal-1",
                "max_age_s": 15,
            }
        )

    def observation(self, **patch):
        data = {
            "observation_id": "obs1",
            "binding_id": "mock_temp",
            "metric": "temperature_c",
            "value": 25,
            "unit": "degC",
            "source_timestamp": time.time(),
            "sequence": 1,
            "quality": "good",
            "calibration_id": "mock-cal-1",
        }
        data.update(patch)
        return data

    def test_transport_custody_is_real_and_roundtrip_preserves_inventory(self):
        before = deepcopy(self.lab.states["sample_tube_01"])
        for target in ["analysis", "preparation"]:
            task = self.env.demo_transport()
            tid = task["id"]
            self.run_until(
                lambda tid=tid: self.env.data["tasks"][tid]["status"] in {"succeeded", "failed"}
            )
            self.assertEqual(
                self.env.data["tasks"][tid]["status"], "succeeded", self.env.data["tasks"][tid]
            )
            self.assertEqual(self.env.data["custody"]["sample_tube_01"], target)
            self.assertEqual(
                self.lab.poses["sample_tube_01"], self.env.station(target)["sample_position_m"]
            )
        self.assertEqual(self.lab.states["sample_tube_01"], before)
        self.assertTrue(
            any(
                e["type"] == "sample.custody" and e["detail"]["holder"] == "robot_01"
                for e in self.env.data["events"]
            )
        )

    def test_routes_avoid_inflated_obstacles_and_detect_changes(self):
        job = self.command("nav1", "robot.navigate", station="analysis")
        p = self.lab.poses["robot_01"][:]
        for q in job["path"]:
            self.assertTrue(self.env.nav.segment_clear(p, q))
            p = q
        before = self.lab.poses["robot_01"][:]
        self.lab.poses["bench_preparation"] = before[:]
        self.env.tick(0.5)
        self.assertEqual(self.env.data["commands"]["nav1"]["status"], "failed")
        self.assertEqual(self.lab.poses["robot_01"], before)
        with self.assertRaises(LabError):
            self.command("bad", "robot.navigate", position_m=[0, -0.65, 0.08])

    def test_idempotency_locks_and_estop(self):
        request = {"command_id": "go", "type": "robot.navigate", "args": {"station": "preparation"}}
        job = self.env.submit(request)
        self.env.tick(0.5)
        self.assertEqual(self.env.submit(request)["id"], job["id"])
        with self.assertRaises(LabError):
            self.command("go", "robot.navigate", station="analysis")
        with self.assertRaises(LabError):
            self.command("other", "robot.navigate", station="analysis")
        with self.assertRaises(LabError):
            self.lab.patch("robot_01", {"speed_m_s": 0.3})
        self.lab.action("robot_01", {"action": "estop"})
        p = self.lab.poses["robot_01"][:]
        self.env.tick(5)
        self.assertEqual(self.lab.poses["robot_01"], p)
        with self.assertRaises(LabError):
            self.command("blocked", "robot.navigate", station="home")
        self.lab.action("robot_01", {"action": "reset_estop"})
        self.command("return", "robot.navigate", station="home")

    def test_grasp_preconditions_and_custody_lock(self):
        with self.assertRaises(LabError):
            self.command("far", "robot.pick", asset_id="sample_tube_01")
        self.lab.poses["robot_01"] = self.env.station("preparation")["dock_m"][:]
        self.lab.patch("sample_tube_01", {"sealed": False})
        with self.assertRaises(LabError):
            self.command("open", "robot.pick", asset_id="sample_tube_01")
        self.lab.patch("sample_tube_01", {"sealed": True})
        self.command("pick", "robot.pick", asset_id="sample_tube_01")
        self.run_until(lambda: self.env.data["commands"]["pick"]["status"] == "succeeded")
        with self.assertRaises(LabError):
            self.lab.action("sample_tube_01", {"action": "move", "position_m": [1, 1, 1]})
        with self.assertRaises(LabError):
            self.lab.patch("sample_tube_01", {"sealed": False})

    def test_observation_provenance_units_and_monotonicity(self):
        self.binding()
        data = self.observation()
        self.env.observe(data)
        self.assertEqual(self.env.observe(data)["id"], "obs1")
        for patch in [
            {"observation_id": "wrong-unit", "unit": "K"},
            {"observation_id": "wrong-cal", "calibration_id": "different"},
            {"observation_id": "future", "source_timestamp": time.time() + 30},
            {"observation_id": "bad-number", "value": float("nan")},
            {"observation_id": "stale-sequence", "sequence": 0},
        ]:
            with self.assertRaises(LabError):
                self.env.observe(self.observation(**patch))
        self.assertEqual(len(self.env.data["observations"]), 1)
        item = self.env.supervision()["comparisons"][0]
        self.assertEqual(item["status"], "aligned")
        self.assertTrue(item["synthetic"])

    def test_supervisor_detects_drift_and_stale_feedback_without_overwriting_state(self):
        self.binding()
        before = deepcopy(self.lab.states["reactor_01"])
        self.env.observe(self.observation(value=50))
        item = self.env.supervision()["comparisons"][0]
        self.assertEqual(item["status"], "diverged")
        self.assertFalse(item["hardware_action_issued"])
        self.assertEqual(self.lab.states["reactor_01"], before)
        self.env.data["observations"]["obs1"]["input"]["source_timestamp"] = time.time() - 60
        self.assertEqual(self.env.supervision()["comparisons"][0]["status"], "stale")
        with self.assertRaises(LabError):
            self.env.submit(
                {
                    "command_id": "real",
                    "type": "robot.navigate",
                    "args": {"station": "home"},
                    "mode": "hardware",
                }
            )

    def test_restart_interrupts_jobs_and_preserves_pairings(self):
        self.binding()
        self.command("inflight", "robot.navigate", station="analysis")
        self.lab.save()
        fresh = Lab(self.temp.name)
        self.assertEqual(fresh.environment.data["commands"]["inflight"]["status"], "interrupted")
        self.assertIn("mock_temp", fresh.environment.data["bindings"])
        self.assertFalse(fresh.states["robot_01"]["active_command_id"])

    def test_generic_task_failure_stops_downstream_steps(self):
        self.env.create_task(
            {
                "task_id": "generic",
                "steps": [
                    {
                        "type": "asset.configure",
                        "args": {
                            "asset_id": "hotplate_01",
                            "parameters": {"target_temperature_c": 40},
                        },
                    },
                    {
                        "type": "asset.action",
                        "args": {
                            "asset_id": "balance_01",
                            "parameters": {"action": "weigh", "sample_id": "sample_tube_01"},
                        },
                    },
                    {
                        "type": "asset.configure",
                        "args": {
                            "asset_id": "hotplate_01",
                            "parameters": {"target_temperature_c": 80},
                        },
                    },
                ],
            }
        )
        self.run_until(
            lambda: self.env.data["tasks"]["generic"]["status"] in {"succeeded", "failed"}
        )
        self.assertEqual(self.env.data["tasks"]["generic"]["status"], "failed")
        self.assertEqual(self.lab.states["hotplate_01"]["target_temperature_c"], 40)


if __name__ == "__main__":
    unittest.main(verbosity=2)
