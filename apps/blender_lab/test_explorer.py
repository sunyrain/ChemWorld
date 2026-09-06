"""Exercise public timelines and evidence projections across actual HTTP routes."""

import json
import struct
import unittest
import urllib.error
import urllib.request
from copy import deepcopy
from pathlib import Path

from . import test_lab
from .explorer import evidence_summary

ROOT = Path(__file__).resolve().parent


class ExplorerTests(unittest.TestCase):
    setUp = test_lab.LabTests.setUp
    tearDown = test_lab.LabTests.tearDown
    req = test_lab.LabTests.req

    def test_seek_is_read_only_and_session_history_is_not_mixed(self):
        frames = json.loads((ROOT / "static/demo.json").read_text(encoding="utf-8"))["frames"]
        before = self.lab.snapshot()
        for frame in frames:
            self.req("/api/v1/chemworld/frame", frame)
        self.req("/api/v1/chemworld/frame", frames[-1])
        timeline = self.req("/api/v1/chemworld/timeline")
        self.assertEqual(timeline["frames"], frames)
        self.assertEqual(self.lab.snapshot()["states"], before["states"])
        self.assertEqual(self.lab.revision, before["revision"])
        self.req("/api/v1/chemworld/frame", frames[0], expected=409)
        self.req("/api/v1/chemworld/release", {"session_id": frames[0]["session_id"]})
        new = deepcopy(frames[0])
        new["session_id"] = "new-session"
        self.req("/api/v1/chemworld/frame", new)
        self.assertEqual(self.req("/api/v1/chemworld/timeline")["frames"], [new])

    def test_static_routes_and_published_projection_exclude_private_payloads(self):
        with urllib.request.urlopen(self.base + "/explore", timeout=3) as response:
            self.assertIn("text/html", response.headers["Content-Type"])
            self.assertIn(b"/explorer/explorer.js", response.read())
        for path in ("/explorer/../server.py", "/explorer/../../../../api.md"):
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(self.base + path, timeout=3)
            self.assertEqual(caught.exception.code, 404)
        evidence = self.req("/api/v1/explorer/evidence")
        encoded = json.dumps(evidence)
        for private in (
            "api_key_file",
            "world_seed",
            "source_commit",
            "provider_calls",
            "candidate_scores_after_selections_sealed",
            "scoring_truth",
        ):
            self.assertNotIn(private, encoded)
        self.assertEqual(evidence["diagnostic"]["counts"], {"completed": 117, "failed": 3})
        self.assertEqual(len(evidence["m3"]["world_effects"]), 10)
        self.assertAlmostEqual(evidence["m3"]["primary"]["mean_difference"], -0.1372309348)

    def test_web_geometry_retains_every_catalog_identity(self):
        data = (ROOT / "static/chemlab.glb").read_bytes()
        length = struct.unpack_from("<I", data, 12)[0]
        document = json.loads(data[20 : 20 + length])
        ids = {n.get("extras", {}).get("lab_id") for n in document["nodes"]}
        from .catalog import CATALOG

        self.assertEqual(ids - {None}, set(CATALOG))

    def test_recorded_frames_keep_unknown_measurements_null(self):
        demo = json.loads((ROOT / "static/demo.json").read_text(encoding="utf-8"))
        self.assertEqual(demo["completed"], 8)
        self.assertEqual(demo["statuses"], ["committed"] * 8)
        for frame in demo["frames"]:
            for key, value in frame["observations"].items():
                if key not in {"score", "cost", "safety_risk"} and not frame["observed_mask"].get(
                    key
                ):
                    self.assertIsNone(value)
        self.assertEqual(evidence_summary()["public_information"]["scheduled_pairs"], 40)
