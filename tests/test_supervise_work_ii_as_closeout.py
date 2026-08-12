from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import scripts.supervise_work_ii_as_closeout as supervisor


def _roots(tmp_path: Path) -> tuple[Path, Path, Path]:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    external = tmp_path / "external"
    source.mkdir()
    destination.mkdir()
    return source, destination, external


def _summary(source: Path) -> Path:
    path = source / "runs/development/as-run/summary.json"
    path.parent.mkdir(parents=True)
    path.write_text("{}", encoding="utf-8")
    return path


def test_default_dry_run_waits_without_mutation(tmp_path: Path) -> None:
    source, destination, external = _roots(tmp_path)
    status, code = supervisor.supervise_and_record(
        source_root=source,
        source_summary=Path("runs/development/as-run/summary.json"),
        destination_root=destination,
        status_output=external / "status.json",
        event_log=external / "events.jsonl",
        execute=False,
    )

    assert code == 0
    assert status["status"] == "waiting_for_source_summary"
    assert list(destination.iterdir()) == []


def test_dry_run_reports_ready_without_integrating(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source, destination, external = _roots(tmp_path)
    summary = _summary(source)
    monkeypatch.setattr(
        supervisor,
        "integrate_development_result",
        lambda **kwargs: pytest.fail("dry-run must not integrate"),
    )

    status, code = supervisor.supervise_and_record(
        source_root=source,
        source_summary=summary,
        destination_root=destination,
        status_output=external / "status.json",
        event_log=external / "events.jsonl",
        execute=False,
    )

    assert code == 0
    assert status["status"] == "ready_for_execute"


def test_execute_pass_integrates_builds_manifest_and_runs_zero_call_preflight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source, destination, external = _roots(tmp_path)
    summary = _summary(source)
    calls: list[str] = []

    monkeypatch.setattr(
        supervisor,
        "integrate_development_result",
        lambda **kwargs: {
            "status": "integrated_w2_26_input_ready",
            "resource_calibration_candidate_ready": True,
            "provider_execution_authorized": False,
        },
    )

    def build(*args: Any, **kwargs: Any) -> dict[str, Any]:
        calls.append("manifest")
        return {"status": "ready_authorization_blocked"}

    monkeypatch.setattr(supervisor, "build_resource_calibration_execution_manifest", build)
    monkeypatch.setattr(supervisor, "validate_resource_calibration_manifest", lambda *a: [])
    monkeypatch.setattr(
        supervisor,
        "build_resource_calibration_readiness",
        lambda *a: {
            "status": "ready_authorization_blocked",
            "missing_pattern_rounds": [],
            "provider_execution_allowed": False,
            "provider_calls_executed": 0,
        },
    )
    monkeypatch.setattr(supervisor, "validate_resource_calibration_readiness", lambda *a: [])

    status, code = supervisor.supervise_and_record(
        source_root=source,
        source_summary=summary,
        destination_root=destination,
        status_output=external / "status.json",
        event_log=external / "events.jsonl",
        execute=True,
    )

    assert code == 0
    assert status["status"] == "integrated_w2_26_preflight_ready"
    assert status["provider_calls_executed"] == 0
    assert calls == ["manifest"]
    assert (destination / supervisor.DEFAULT_DYNAMIC_MANIFEST).is_file()


def test_scientific_rejection_is_integrated_without_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source, destination, external = _roots(tmp_path)
    summary = _summary(source)
    monkeypatch.setattr(
        supervisor,
        "integrate_development_result",
        lambda **kwargs: {
            "status": "integrated_scientific_rejection_w2_26_blocked",
            "resource_calibration_candidate_ready": False,
            "provider_execution_authorized": False,
        },
    )
    monkeypatch.setattr(
        supervisor,
        "build_resource_calibration_execution_manifest",
        lambda *a, **k: pytest.fail("scientific rejection must not build W2-26"),
    )

    status, code = supervisor.supervise_and_record(
        source_root=source,
        source_summary=summary,
        destination_root=destination,
        status_output=external / "status.json",
        event_log=external / "events.jsonl",
        execute=True,
    )

    assert code == 0
    assert status["status"] == "scientific_rejection_integrated"
    assert status["w2_26_manifest_generated"] is False


def test_validation_failure_fails_closed_and_removes_dynamic_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source, destination, external = _roots(tmp_path)
    summary = _summary(source)
    def integrate(**kwargs: Any) -> dict[str, Any]:
        raw = destination / "runs/development/as-run"
        raw.mkdir(parents=True)
        canonical = {
            "summary": destination / "reports/as-summary.json",
            "package": destination / "configs/as-package.json",
            "d1": destination / "configs/as-d1.json",
        }
        for path in canonical.values():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}", encoding="utf-8")
        return {
            "status": "integrated_w2_26_input_ready",
            "resource_calibration_candidate_ready": True,
            "provider_execution_authorized": False,
            "raw_run": "runs/development/as-run",
            "canonical_summary": "reports/as-summary.json",
            "canonical_package": "configs/as-package.json",
            "canonical_d1_configs": {"candidate": "configs/as-d1.json"},
        }

    monkeypatch.setattr(supervisor, "integrate_development_result", integrate)
    monkeypatch.setattr(
        supervisor,
        "build_resource_calibration_execution_manifest",
        lambda *a, **k: {"status": "ready_authorization_blocked"},
    )
    monkeypatch.setattr(supervisor, "validate_resource_calibration_manifest", lambda *a: [])
    monkeypatch.setattr(
        supervisor,
        "build_resource_calibration_readiness",
        lambda *a: {"status": "not_ready_fail_closed"},
    )
    monkeypatch.setattr(
        supervisor,
        "validate_resource_calibration_readiness",
        lambda *a: ["invalid preflight"],
    )

    status, code = supervisor.supervise_and_record(
        source_root=source,
        source_summary=summary,
        destination_root=destination,
        status_output=external / "status.json",
        event_log=external / "events.jsonl",
        execute=True,
    )

    assert code == 1
    assert status["status"] == "fail_closed"
    assert "invalid preflight" in status["error"]
    assert not (destination / supervisor.DEFAULT_DYNAMIC_MANIFEST).exists()
    assert not (destination / "runs/development/as-run").exists()
    assert not (destination / "reports/as-summary.json").exists()
    assert not (destination / "configs/as-package.json").exists()
    assert not (destination / "configs/as-d1.json").exists()
    persisted = json.loads((external / "status.json").read_text(encoding="utf-8"))
    assert persisted["status"] == "fail_closed"


def test_logs_and_status_must_remain_external(tmp_path: Path) -> None:
    source, destination, _external = _roots(tmp_path)
    with pytest.raises(ValueError, match="outside both repositories"):
        supervisor.supervise_and_record(
            source_root=source,
            source_summary=Path("runs/development/as-run/summary.json"),
            destination_root=destination,
            status_output=destination / "status.json",
            event_log=tmp_path / "events.jsonl",
            execute=False,
        )
