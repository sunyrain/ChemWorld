from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import scripts.integrate_work_ii_as_development_result as integration

from chemworld.eval.provenance import file_sha256


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _source(tmp_path: Path, *, passed: bool) -> tuple[Path, Path, dict[str, Any]]:
    root = tmp_path / "source"
    run = root / "runs/development/a-s-complete"
    package = run / "q2-package.json"
    _write(package, {"package_sha256": "p" * 64})
    generated: dict[str, Any] = {}
    if passed:
        for candidate_id in integration.CANDIDATE_IDS:
            path = run / f"{candidate_id}-d1.json"
            _write(
                path,
                {
                    "candidate_id": candidate_id,
                    "qualification": {"q0_q1_q2_passed": True},
                },
            )
            generated[candidate_id] = {
                "path": path.relative_to(root).as_posix(),
                "sha256": file_sha256(path),
                "execution_authorized": False,
            }
    summary = {
        "formal_result": False,
        "provider_call_count": 0,
        "participant_session_count": 0,
        "all_candidates_passed": passed,
        "generated_package": {
            "path": package.relative_to(root).as_posix(),
            "sha256": file_sha256(package),
            "package_sha256": "p" * 64,
        },
        "participant_d1_configs_generated": generated,
        "summary_sha256": "source",
    }
    summary_path = run / "summary.json"
    _write(summary_path, summary)
    return root, summary_path, summary


def _patch_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        integration,
        "CANONICAL_SUMMARY",
        Path("workstreams/flagship_tasks/reports/as-summary.json"),
    )
    monkeypatch.setattr(
        integration,
        "CANONICAL_PACKAGE",
        Path("configs/benchmark/as-package.json"),
    )
    monkeypatch.setattr(
        integration,
        "CANONICAL_D1",
        {
            candidate_id: Path(f"configs/benchmark/{candidate_id}-d1.json")
            for candidate_id in integration.CANDIDATE_IDS
        },
    )


def test_integrates_passed_development_run_without_authorizing_execution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_root, source_summary, _ = _source(tmp_path, passed=True)
    destination = tmp_path / "destination"
    _patch_paths(monkeypatch)
    calls: list[tuple[Path, bool]] = []

    def validate(root: Path, summary: dict[str, Any], **kwargs: Any) -> list[str]:
        calls.append((root, kwargs["deep_validate_world_reports"]))
        return []

    monkeypatch.setattr(integration, "validate_summary", validate)
    result = integration.integrate_development_result(
        source_root=source_root,
        source_summary=source_summary,
        destination_root=destination,
    )

    assert result["status"] == "integrated_w2_26_input_ready"
    assert result["provider_execution_authorized"] is False
    assert result["formal_r5_authorized"] is False
    assert calls[0] == (source_root.resolve(), True)
    assert calls[1][1] is False
    assert calls[1][0] == destination.resolve()
    published = json.loads(
        (destination / integration.CANONICAL_SUMMARY).read_text(encoding="utf-8")
    )
    assert published["generated_package"]["path"] == integration.CANONICAL_PACKAGE.as_posix()
    assert set(published["participant_d1_configs_generated"]) == set(
        integration.CANDIDATE_IDS
    )
    for path in integration.CANONICAL_D1.values():
        config = json.loads((destination / path).read_text(encoding="utf-8"))
        assert config["qualification"]["q2_passed"] is True
    assert (destination / "runs/development/a-s-complete/summary.json").is_file()


def test_complete_scientific_rejection_is_retained_but_does_not_unlock_w2_26(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_root, source_summary, _ = _source(tmp_path, passed=False)
    destination = tmp_path / "destination"
    _patch_paths(monkeypatch)
    monkeypatch.setattr(integration, "validate_summary", lambda *args, **kwargs: [])

    result = integration.integrate_development_result(
        source_root=source_root,
        source_summary=source_summary,
        destination_root=destination,
    )

    assert result["status"] == "integrated_scientific_rejection_w2_26_blocked"
    assert result["resource_calibration_candidate_ready"] is False
    assert result["canonical_d1_configs"] == {}
    assert not any((destination / path).exists() for path in integration.CANONICAL_D1.values())


def test_source_validation_failure_writes_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_root, source_summary, _ = _source(tmp_path, passed=True)
    destination = tmp_path / "destination"
    _patch_paths(monkeypatch)
    monkeypatch.setattr(
        integration, "validate_summary", lambda *args, **kwargs: ["receipt tamper"]
    )

    with pytest.raises(ValueError, match="receipt tamper"):
        integration.integrate_development_result(
            source_root=source_root,
            source_summary=source_summary,
            destination_root=destination,
        )
    assert not (destination / "runs/development/a-s-complete").exists()
    assert not (destination / integration.CANONICAL_SUMMARY).exists()
    assert not (destination / integration.CANONICAL_PACKAGE).exists()
    assert not any((destination / path).exists() for path in integration.CANONICAL_D1.values())


def test_destination_validation_failure_writes_no_partial_canonical_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_root, source_summary, _ = _source(tmp_path, passed=True)
    destination = tmp_path / "destination"
    _patch_paths(monkeypatch)
    calls = 0

    def validate(*args: Any, **kwargs: Any) -> list[str]:
        nonlocal calls
        calls += 1
        return [] if calls == 1 else ["rewritten binding mismatch"]

    monkeypatch.setattr(integration, "validate_summary", validate)
    with pytest.raises(ValueError, match="rewritten binding mismatch"):
        integration.integrate_development_result(
            source_root=source_root,
            source_summary=source_summary,
            destination_root=destination,
        )

    assert not (destination / "runs/development/a-s-complete").exists()
    assert not (destination / integration.CANONICAL_SUMMARY).exists()
    assert not (destination / integration.CANONICAL_PACKAGE).exists()
    assert not any((destination / path).exists() for path in integration.CANONICAL_D1.values())


def test_integration_is_write_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_root, source_summary, _ = _source(tmp_path, passed=True)
    destination = tmp_path / "destination"
    _patch_paths(monkeypatch)
    monkeypatch.setattr(integration, "validate_summary", lambda *args, **kwargs: [])

    integration.integrate_development_result(
        source_root=source_root,
        source_summary=source_summary,
        destination_root=destination,
    )
    with pytest.raises(FileExistsError, match="overwrite"):
        integration.integrate_development_result(
            source_root=source_root,
            source_summary=source_summary,
            destination_root=destination,
        )
