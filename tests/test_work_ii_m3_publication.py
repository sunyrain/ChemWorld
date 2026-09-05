"""An isolated synthetic execution exercises the exported, standalone M3 verifier."""

import hashlib
import json
import runpy
import sys

from scripts import run_work_ii_m3_portability as runner
from scripts.run_work_ii_factorial import read, seal

from chemworld.eval.work_ii_factorial import compile_design, public_packet


def test_synthetic_package_preserves_reuse_failures_privacy_and_numeric_reconstruction(
    tmp_path,
    monkeypatch,
):
    # This fixture never touches the live run or its hidden scores and makes no provider call.
    builder = runpy.run_path(str(runner.ROOT / "paper/tools/build_prior_discovery_supplement.py"))
    protocol = read(runner.PROTOCOL)
    source = runner.load_source(protocol)
    root = tmp_path / "synthetic-execution-not-experimental-data"
    seal(root / "source.json", source)
    seal(root / "protocol.json", protocol)
    seal(root / "release.json", {"tested_commit": "synthetic-fixture", "execution_surface": {}})
    seal(
        root / "physical.json",
        {
            "status": "completed",
            "stop_reason": None,
            "completed": 80,
            "receipts": [
                {
                    "task": world["task"],
                    "cluster_id": world["cluster_id"],
                    "id": f"c{i + 1:02d}",
                    "status": "completed",
                    "replay": {"verified": True},
                }
                for world in protocol["worlds"]
                for i in range(8)
            ],
        },
    )
    for world in protocol["worlds"]:
        packet = compile_design(protocol, world["task"])
        packet["evidence"] = source["public_packets"][world["cluster_id"]]["evidence"]
        seal(
            root / "public" / f"{world['cluster_id']}.json", public_packet(packet, candidates=True)
        )
    monkeypatch.setattr(runner, "check_frozen", lambda root: protocol)

    def provider(root, call_id, model, stage, packet, law, progress, completed, **kwargs):
        failed = completed % 17 == 0
        return {
            "call_id": call_id,
            "thread_id": call_id,
            "status": "schema_failed" if failed else "completed",
            "failure_type": "synthetic_schema_failure" if failed else None,
            "final_payload": {} if failed else {"candidate_id": "c01"},
            "usage": {"input_tokens": 10, "output_tokens": 2},
            "elapsed_s": 1,
            "raw_events": "NEVER_EXPORT_RAW_FIXTURE",
        }

    monkeypatch.setattr(runner, "provider_call", provider)
    runner.run_provider_block(root)
    # Scores are deliberately synthetic; choices have already been sealed.
    seal(
        root / "private_scores.json",
        {
            world["cluster_id"]: {f"c{i + 1:02d}": 0.2 + 0.05 * i for i in range(8)}
            for world in protocol["worlds"]
        },
    )
    report = runner.analyze(root)
    assert report["condition_completed"] == 150
    assert len(report["failures"]) == 20  # ten failures at provider and condition levels
    destination = tmp_path / "synthetic-report.json"
    runner.export_report(root, destination)
    assert "NEVER_EXPORT_RAW_FIXTURE" not in destination.read_text(encoding="utf-8")

    original_load = builder["_load"]
    current = original_load(runner.ROOT / "configs/current.json")
    current["work_ii"]["w2_69_m3_portability"] = {
        "formal_result": True,
        "report": destination.as_posix(),
        "report_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "protocol": runner.PROTOCOL.relative_to(runner.ROOT).as_posix(),
    }

    def fixture_load(path):
        if path == runner.ROOT / "configs/current.json":
            return current
        return original_load(path)

    functions = builder["_m3_files"].__globals__
    monkeypatch.setitem(functions, "_load", fixture_load)
    files = {**builder["_m1_files"](), **builder["_m3_files"]()}
    package = tmp_path / "synthetic-supplement-not-for-publication"
    for name, content in files.items():
        builder["_assert_anonymous"](name, content)
        path = package / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    exported = json.loads((package / "data/m3_portability.json").read_text(encoding="utf-8"))
    assert "source_binding" not in exported
    monkeypatch.setattr(sys, "argv", ["verify_m3.py", "--full"])
    runpy.run_path(str(package / "verify_m3.py"))
