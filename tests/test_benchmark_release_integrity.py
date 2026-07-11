from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from scripts.build_benchmark_release import _write_trajectory_archive
from scripts.check_frozen_benchmark import verify_release_bundle

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "benchmark" / "releases" / "chemworld-serious-v1"


def test_stale_public_bundle_is_candidate_but_not_a_frozen_release() -> None:
    strict = verify_release_bundle(ROOT, RELEASE)
    candidate = verify_release_bundle(ROOT, RELEASE, allow_candidate=True)

    assert strict["passed"] is False
    assert strict["strict_release_ready"] is False
    assert strict["release_claim_allowed"] is False
    assert "task_contract_freshness" in strict["freshness_failures"]
    assert "source_commit_binding" in strict["freshness_failures"]
    assert candidate["passed"] is True
    assert candidate["structural_integrity_passed"] is True
    assert candidate["release_claim_allowed"] is False
    assert candidate["candidate_waivers"] == candidate["freshness_failures"]
    digest_check = next(
        check
        for check in candidate["checks"]
        if check["check_id"] == "embedded_evidence_digests"
    )
    assert {
        result["match_mode"] for result in digest_check["observed"].values()
    } in ({"raw_bytes"}, {"legacy_git_crlf_text"})


def test_legacy_v1_digest_is_stable_across_git_line_endings(tmp_path: Path) -> None:
    copied = tmp_path / "release"
    shutil.copytree(RELEASE, copied)
    source_line_endings = set()
    for filename in (
        "baseline_summary.json",
        "benchmark_validation.json",
        "response_surface_audit.json",
    ):
        path = copied / filename
        payload = path.read_bytes()
        normalized_lf = payload.replace(b"\r\n", b"\n")
        uses_crlf = payload != normalized_lf
        source_line_endings.add("crlf" if uses_crlf else "lf")
        alternate = normalized_lf if uses_crlf else normalized_lf.replace(b"\n", b"\r\n")
        assert alternate != payload
        path.write_bytes(alternate)

    assert len(source_line_endings) == 1

    report = verify_release_bundle(ROOT, copied, allow_candidate=True)

    assert report["passed"] is True
    digest_check = next(
        check
        for check in report["checks"]
        if check["check_id"] == "embedded_evidence_digests"
    )
    expected_mode = "legacy_git_crlf_text" if source_line_endings == {"crlf"} else "raw_bytes"
    assert {
        result["match_mode"] for result in digest_check["observed"].values()
    } == {expected_mode}


def test_candidate_mode_never_waives_evidence_tampering(tmp_path: Path) -> None:
    copied = tmp_path / "release"
    shutil.copytree(RELEASE, copied)
    summary_path = copied / "baseline_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["rows"][0]["mean_total_score"] = 999.0
    summary_path.write_text(json.dumps(summary), encoding="utf-8")

    report = verify_release_bundle(ROOT, copied, allow_candidate=True)
    assert report["passed"] is False
    assert report["structural_integrity_passed"] is False
    assert "embedded_evidence_digests" in report["structural_failures"]


def test_trajectory_archive_is_complete_and_deterministic(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    report_dir = run_dir / "baseline_report"
    report_dir.mkdir(parents=True)
    rows = []
    for seed in (1, 0):
        trajectory = tmp_path / f"seed-{seed}.jsonl"
        trajectory.write_text(f'{{"seed": {seed}}}\n', encoding="utf-8")
        digest = hashlib.sha256(trajectory.read_bytes()).hexdigest()
        rows.append(
            {
                "task_id": "task-a",
                "agent_name": "agent-a",
                "seed": seed,
                "trajectory_path": str(trajectory),
                "trajectory_sha256": digest,
                "verified": True,
            }
        )
    (report_dir / "baseline_results.json").write_text(
        json.dumps(rows),
        encoding="utf-8",
    )

    left = _write_trajectory_archive(run_dir=run_dir, output_dir=tmp_path / "left")
    right = _write_trajectory_archive(run_dir=run_dir, output_dir=tmp_path / "right")

    assert left["count"] == 2
    assert left["archive_sha256"] == right["archive_sha256"]
    assert left["index_sha256"] == right["index_sha256"]
    with zipfile.ZipFile(tmp_path / "left" / "trajectories.zip") as archive:
        assert archive.namelist() == [
            "trajectories/task-a/agent-a/seed-0.jsonl",
            "trajectories/task-a/agent-a/seed-1.jsonl",
        ]
