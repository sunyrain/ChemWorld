from __future__ import annotations

import json

from chemworld.cli import main
from chemworld.data.logging import load_jsonl
from chemworld.data.submission import (
    init_submission_bundle,
    summarize_submission_bundle,
    validate_submission_bundle,
)
from chemworld.eval.metrics import evaluate_records
from chemworld.eval.runner import make_agent, run_agent


def _write_bundle_run(bundle, *, seed: int = 0) -> None:
    trajectory = bundle / "trajectories" / f"seed{seed}.jsonl"
    result = bundle / "results" / f"seed{seed}.json"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=3,
        objective="balanced",
        seed=seed,
        output_path=trajectory,
    )
    records = load_jsonl(trajectory)
    result.write_text(
        json.dumps(evaluate_records(records).to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def test_submission_bundle_init_validate_and_summarize(tmp_path) -> None:
    bundle = tmp_path / "bundle"
    init_submission_bundle(
        bundle,
        agent_name="random",
        agent_family="baseline",
        task_id="reaction-to-assay",
        seeds=[0],
        command=["chemworld", "run", "--task", "reaction-to-assay"],
        dependency_file="pyproject.toml",
    )
    _write_bundle_run(bundle, seed=0)

    validation = validate_submission_bundle(bundle)
    assert validation.valid
    assert validation.trajectory_count == 1
    assert validation.result_count == 1

    summary = summarize_submission_bundle(bundle)
    assert summary["valid"]
    assert summary["seeds"] == [0]
    assert 0.0 <= summary["mean_total_score"] <= 1.0
    assert 0.0 <= summary["mean_safety_risk"] <= 1.0


def test_submission_bundle_validation_rejects_missing_parts(tmp_path) -> None:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    validation = validate_submission_bundle(bundle)
    assert not validation.valid
    assert "missing manifest.json" in validation.errors
    assert any("trajectories" in error for error in validation.errors)


def test_cli_submission_commands(tmp_path, capsys) -> None:
    bundle = tmp_path / "bundle"
    main(
        [
            "submission",
            "init",
            str(bundle),
            "--agent-name",
            "random",
            "--agent-family",
            "baseline",
            "--task-id",
            "reaction-to-assay",
        ]
    )
    _write_bundle_run(bundle, seed=0)
    main(["submission", "validate", str(bundle)])
    main(["submission", "summarize", str(bundle)])
    output = capsys.readouterr().out
    assert "chemworld-submission-bundle-0.1" in output
    assert '"valid": true' in output

