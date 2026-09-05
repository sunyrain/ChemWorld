"""Behavioral acceptance tests, using an isolated API service and temp inventory."""

import concurrent.futures
import json
import math
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from .catalog import ASSETS
from .engine import Lab, LabError
from .server import Handler


class LabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.lab = Lab(self.tmp.name)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.server.lab = self.lab
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.worker.join()
        self.tmp.cleanup()

    def req(self, path, data=None, method=None, expected=200):
        raw = None if data is None else json.dumps(data).encode()
        q = urllib.request.Request(
            self.base + path, data=raw, method=method, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
                q, timeout=4
            ) as r:
                status = r.status
                result = json.load(r)
        except urllib.error.HTTPError as e:
            status = e.code
            result = json.load(e)
        self.assertEqual(status, expected, result)
        return result

    def action(self, id, expected=200, **args):
        return self.req(f"/api/v1/assets/{id}/actions", args, "POST", expected)

    def patch(self, id, expected=200, **args):
        return self.req(f"/api/v1/assets/{id}", args, "PATCH", expected)

    def seed(self, target="beaker_01", amount=100):
        self.patch("water_01", cap_open=True)
        self.action("water_01", action="dispense", target_id=target, amount=amount, unit="ml")

    def test_every_asset_has_working_endpoint_and_generic_actions(self):
        manifest = self.req("/api/v1/assets")
        self.assertEqual(manifest["count"], len(ASSETS))
        spec = self.req("/openapi.json")
        for a in ASSETS:
            with self.subTest(asset=a["id"]):
                id = a["id"]
                path = f"/api/v1/assets/{id}"
                result = self.req(path)
                self.assertEqual(result["id"], id)
                self.assertIn(path, spec["paths"])
                self.assertIn(path + "/actions", spec["paths"])
                self.action(id, action="select")
                self.assertEqual(self.req("/api/v1/state")["selected"], id)
                r = self.action(id, action="set_visible", visible=False)
                self.assertFalse(r["state"]["visible"])
                self.action(id, action="set_visible", visible=True)
                if "move" in a["actions"]:
                    pos = [a["location"][0] + 0.1, *a["location"][1:]]
                    r = self.action(id, action="move", position_m=pos)
                    self.assertEqual(r["position_m"], pos)

    def test_all_typed_fields_and_actions(self):
        self.seed("beaker_01")
        for a in ASSETS:
            with self.subTest(asset=a["id"]):
                id = a["id"]
                if a["fields"]:
                    r = self.patch(id, **{k: v["default"] for k, v in a["fields"].items()})
                    for k, v in a["fields"].items():
                        self.assertEqual(r["state"][k], v["default"])
                for action in a["actions"]:
                    if action in {
                        "move",
                        "set_visible",
                        "select",
                        "dispense",
                        "sample",
                        "navigate",
                        "pick",
                        "place",
                        "home",
                        "estop",
                        "reset_estop",
                    }:
                        continue
                    args = {"action": action}
                    if action in {"measure", "weigh"}:
                        args["sample_id"] = "beaker_01"
                    self.action(id, **args)
        for id in ["reactor_01", "condenser_01", "flask_01"]:
            self.seed(id, 10)
            self.action(id, action="sample")
        for a in ASSETS:
            if a["kind"] == "reagent":
                self.patch(a["id"], cap_open=True)
                self.action(
                    a["id"], action="dispense", target_id="reactor_01", amount=1, unit=a["unit"]
                )

    def test_inventory_is_conserved_and_invalid_transfer_is_atomic(self):
        self.seed(amount=200)
        self.assertEqual(self.lab.states["water_01"]["remaining"], 800)
        self.req(
            "/api/v1/transfers",
            {"source_id": "beaker_01", "target_id": "flask_01", "amount": 50, "unit": "ml"},
            "POST",
        )
        self.assertEqual(self.lab.states["beaker_01"]["volume_ml"], 150)
        self.assertEqual(self.lab.states["flask_01"]["volume_ml"], 50)
        before = self.lab.snapshot()
        for amount, unit in [(300, "ml"), (-1, "ml"), (1, "g")]:
            self.req(
                "/api/v1/transfers",
                {"source_id": "beaker_01", "target_id": "flask_01", "amount": amount, "unit": unit},
                "POST",
                409 if amount == 300 else 422,
            )
            self.assertEqual(self.lab.snapshot(), before)
        self.patch("salt_01", cap_open=True)
        self.action("salt_01", action="dispense", target_id="beaker_01", amount=2.16, unit="g")
        self.assertAlmostEqual(self.lab.states["beaker_01"]["volume_ml"], 151)
        self.assertAlmostEqual(self.lab.states["beaker_01"]["mass_g"], 152.16)
        self.req(
            "/api/v1/transfers",
            {"source_id": "flask_01", "target_id": "waste_aqueous", "amount": 50, "unit": "ml"},
            "POST",
        )
        self.assertEqual(self.lab.states["waste_aqueous"]["volume_ml"], 50)

    def test_concurrent_dispenses_do_not_overdraw_inventory(self):
        self.patch("water_01", cap_open=True)

        def dispense(i):
            try:
                self.lab.transfer(
                    {
                        "source_id": "water_01",
                        "target_id": "waste_aqueous",
                        "amount": 100,
                        "unit": "ml",
                    }
                )
                return True
            except LabError:
                return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            outcomes = list(pool.map(dispense, range(20)))
        self.assertEqual(sum(outcomes), 10)
        self.assertEqual(self.lab.states["water_01"]["remaining"], 0)
        self.assertEqual(self.lab.states["waste_aqueous"]["volume_ml"], 1000)

    def test_validation_and_interlocks(self):
        self.patch("reactor_01", target_temperature_c=201, expected=422)
        self.patch("reactor_01", stir_rpm=True, expected=422)
        self.patch("reactor_01", temperature_c=80, expected=422)
        self.action(
            "water_01", action="dispense", target_id="beaker_01", amount=1, unit="ml", expected=409
        )
        self.patch("hood_01", fan_on=False)
        self.action("reactor_01", action="start", expected=409)
        self.patch("hood_01", fan_on=True)
        self.action("reactor_01", action="start")
        self.patch("hood_01", sash_open_pct=100, expected=409)
        self.action("reactor_01", action="stop")
        for id, key in [("oven_01", "door_open"), ("centrifuge_01", "lid_open")]:
            self.patch(id, **{key: True})
            self.action(id, action="start", expected=409)
            self.patch(id, **{key: False})
            self.action(id, action="start")
            self.patch(id, expected=409, **{key: True})
            self.action(id, action="stop")
        self.req("/api/v1/assets/missing", expected=404)
        self.action("bench_analysis", action="start", expected=422)
        self.action("water_01", action="move", position_m=[0, 0, -1], expected=422)

    def test_measurements_have_provenance_and_export(self):
        self.action("uvvis_01", action="measure", sample_id="beaker_01", expected=409)
        self.seed()
        ids = []
        for id, action in [
            ("balance_01", "weigh"),
            ("ph_01", "measure"),
            ("uvvis_01", "measure"),
            ("ftir_01", "measure"),
        ]:
            result = self.action(id, action=action, sample_id="beaker_01")
            ids.append(result["id"])
            self.assertEqual(result["mode"], "educational_simulation")
            self.assertEqual(result["sample_snapshot"]["volume_ml"], 100)
            if result["kind"] == "spectrum":
                self.assertGreater(len(result["x"]), 100)
                self.assertEqual(len(result["x"]), len(result["y"]))
                self.assertTrue(all(math.isfinite(v) for v in result["y"]))
            with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
                self.base + "/api/v1/results/" + result["id"] + ".csv"
            ) as r:
                self.assertIn(b"educational_simulation", r.read())
        self.assertEqual(len(set(ids)), 4)
        self.action("balance_01", action="tare")
        zero = self.action("balance_01", action="weigh", sample_id="beaker_01")
        self.assertEqual(zero["value"], 0)

    def test_state_persistence_stops_running_devices(self):
        self.seed()
        self.action("hotplate_01", action="start")
        loaded = Lab(self.tmp.name)
        self.assertEqual(loaded.states["beaker_01"]["volume_ml"], 100)
        self.assertFalse(loaded.states["hotplate_01"]["running"])
        self.assertGreater(len(loaded.events), 1)

    def test_temperature_evolves_and_centrifuge_finishes(self):
        self.patch("hotplate_01", target_temperature_c=80)
        self.action("hotplate_01", action="start")
        self.patch("centrifuge_01", duration_s=1)
        self.action("centrifuge_01", action="start")
        self.lab.last_tick -= 1.5
        self.lab.tick()
        self.assertGreater(self.lab.states["hotplate_01"]["temperature_c"], 25)
        self.assertLess(self.lab.states["hotplate_01"]["temperature_c"], 80)
        self.assertFalse(self.lab.states["centrifuge_01"]["running"])

    def test_bench_move_carries_supported_apparatus(self):
        before = self.lab.snapshot()["poses"]
        pos = before["bench_preparation"][:]
        pos[0] += 0.4
        self.action("bench_preparation", action="move", position_m=pos)
        for id in ["hotplate_01", "beaker_01", "bath_01", "flask_01", "rack_01", "centrifuge_01"]:
            self.assertAlmostEqual(self.lab.poses[id][0], before[id][0] + 0.4)
        self.assertEqual(self.lab.poses["uvvis_01"], before["uvvis_01"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LabTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    out = Path(__file__).resolve().parent / "verification"
    out.mkdir(exist_ok=True)
    (out / "api_tests.json").write_text(
        json.dumps(
            {
                "tests": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "success": result.wasSuccessful(),
                "time": time.time(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
