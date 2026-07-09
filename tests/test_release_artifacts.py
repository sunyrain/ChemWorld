from __future__ import annotations

import json
from pathlib import Path

from chemworld.cli import main
from chemworld.eval.baseline_report import generate_baseline_report
from chemworld.eval.paper_artifact import create_paper_artifact
from chemworld.eval.private_artifact import (
    sign_private_eval_results,
    verify_private_eval_artifact,
)


def test_baseline_report_private_signature_and_paper_artifact(tmp_path: Path) -> None:
    report = generate_baseline_report(
        task_ids=["reaction-to-assay"],
        agents=["scripted_chemistry"],
        seeds=[0],
        output_dir=tmp_path / "baseline_report",
    )
    assert report.result_count == 1
    assert (tmp_path / "baseline_report" / "baseline_report.json").exists()
    assert report.leaderboard_rows[0]["agent_name"] == "scripted_chemistry"
    assert report.leaderboard_rows[0]["task_id"] == "reaction-to-assay"

    signed = sign_private_eval_results(
        result_paths=[tmp_path / "baseline_report" / "baseline_results.json"],
        output_path=tmp_path / "private_eval" / "signed.json",
        salt="teacher-secret",
        run_log={"task": "reaction-to-assay"},
    )
    assert signed.result_count == 1
    assert "teacher-secret" not in json.dumps(signed.to_dict())
    assert verify_private_eval_artifact(
        tmp_path / "private_eval" / "signed.json",
        salt="teacher-secret",
    )

    artifact = create_paper_artifact(
        output_dir=tmp_path / "paper_artifact",
        task_ids=["reaction-to-assay"],
        agents=["scripted_chemistry"],
        seeds=[0],
    )
    assert artifact["baseline_report"]["result_count"] == 1
    assert artifact["replay_verified"] is True
    assert (tmp_path / "paper_artifact" / "README.md").exists()
    assert (tmp_path / "paper_artifact" / "environment.md").exists()
    assert (tmp_path / "paper_artifact" / "limitations.md").exists()
    assert (tmp_path / "paper_artifact" / "tasks" / "task_cards.json").exists()
    assert (tmp_path / "paper_artifact" / "tasks" / "task_contracts.json").exists()
    assert (tmp_path / "paper_artifact" / "schemas" / "action_schema.json").exists()
    assert (tmp_path / "paper_artifact" / "dataset_examples" / "dataset_card.json").exists()
    assert (
        tmp_path
        / "paper_artifact"
        / "manifests"
        / "replay_manifest.json"
    ).exists()
    assert (
        tmp_path
        / "paper_artifact"
        / "manifests"
        / "release_manifest.json"
    ).exists()
    assert (tmp_path / "paper_artifact" / "release_checklist.md").exists()
    assert (tmp_path / "paper_artifact" / "scripts" / "reproduce_public_artifact.ps1").exists()
    replay_manifest = json.loads(
        (
            tmp_path
            / "paper_artifact"
            / "manifests"
            / "replay_manifest.json"
        ).read_text(encoding="utf-8")
    )
    assert replay_manifest["verification"]["verified"] is True
    release_checklist = json.loads(
        (
            tmp_path
            / "paper_artifact"
            / "manifests"
            / "release_checklist.json"
        ).read_text(encoding="utf-8")
    )
    assert release_checklist["items"][0]["id"] == "task_contracts"
    assert release_checklist["ready_for_public_claim"] is True


def test_release_artifact_cli_commands(tmp_path: Path, capsys) -> None:
    report_dir = tmp_path / "cli_baselines"
    main(
        [
            "baselines",
            "report",
            "--tasks",
            "reaction-to-assay",
            "--agents",
            "scripted_chemistry",
            "--seeds",
            "0",
            "--output-dir",
            str(report_dir),
        ]
    )
    signed_path = tmp_path / "signed_private_eval.json"
    main(
        [
            "private-eval",
            "sign",
            "--results",
            str(report_dir / "baseline_results.json"),
            "--output",
            str(signed_path),
            "--salt",
            "teacher-secret",
        ]
    )
    main(
        [
            "private-eval",
            "verify",
            "--artifact",
            str(signed_path),
            "--salt",
            "teacher-secret",
        ]
    )
    artifact_dir = tmp_path / "cli_artifact"
    main(
        [
            "artifact",
            "create",
            "--output-dir",
            str(artifact_dir),
            "--tasks",
            "reaction-to-assay",
            "--agents",
            "scripted_chemistry",
            "--seeds",
            "0",
        ]
    )
    output = capsys.readouterr().out
    assert "chemworld-baseline-report-0.2" in output
    assert "signature_valid" in output
    assert "chemworld-paper-artifact-0.1" in output
