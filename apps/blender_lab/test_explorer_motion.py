"""Check authored routes and reach against scene geometry, without executing Core."""

import json
import math
from pathlib import Path
from types import SimpleNamespace

from .build_explorer_motion import build_motion
from .catalog import ASSETS, CATALOG
from .navigation import Navigator

ROOT = Path(__file__).resolve().parent


def test_choreography_matches_demo_and_all_routes_clear_the_robot_footprint():
    motion = build_motion()
    saved = json.loads((ROOT / "static/replay-motion.json").read_text(encoding="utf-8"))
    assert motion == saved
    definition = json.loads((ROOT / "environment.json").read_text(encoding="utf-8"))
    nav = Navigator(
        SimpleNamespace(poses={a["id"]: list(a["location"]) for a in ASSETS}), definition
    )
    for segment in motion["segments"]:
        assert nav.segment_clear(segment["from"]["position"], segment["to"]["position"])
        end = segment["to"]
        if end["extension"] == 1:
            # The web arm shoulder is 0.84 m above the base, offset 0.08 m forward.
            shoulder = [end["position"][0], end["position"][1] + 0.08, end["position"][2] + 0.84]
            assert math.dist(shoulder, end["target"]) <= CATALOG["robot_01"]["reach_m"]
    assert len(motion["stepEnds"]) == 9
    assert motion["source"] == "authored_illustration"
    assert motion["research_evidence"] is False


def test_reaction_handoff_sits_on_its_bench_and_does_not_change_service_custody():
    motion = build_motion()
    bench = CATALOG["bench_reaction"]
    point = motion["stations"]["reaction"]["sample_position_m"]
    assert all(abs(point[i] - bench["location"][i]) < bench["size"][i] / 2 for i in (0, 1))
    assert point[2] == bench["size"][2]
    definition = json.loads((ROOT / "environment.json").read_text(encoding="utf-8"))
    assert "sample_position_m" not in definition["stations"]["reaction"]
