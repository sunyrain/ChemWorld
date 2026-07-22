from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.build_report_lifecycle_index import build_report_lifecycle_index


def _write(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_report_lifecycle_classifies_every_report_once(tmp_path: Path) -> None:
    current_path = "workstreams/a/reports/current.json"
    external_path = "workstreams/a/reports/external.json"
    superseded_path = "workstreams/a/reports/old.json"
    archive_path = "workstreams/a/reports/archive/diagnostic.json"
    historical_path = "workstreams/a/reports/other.json"
    for path in (
        current_path,
        external_path,
        superseded_path,
        archive_path,
        historical_path,
    ):
        _write(tmp_path / path, {"path": path})
    policy = {
        "schema_version": "chemworld-report-lifecycle-policy-0.1",
        "report_glob": "workstreams/*/reports/**/*.json",
        "categories": ["current", "historical", "superseded", "external"],
        "external_paths": [external_path],
        "superseded_paths": [superseded_path],
        "default_noncurrent_category": "historical",
    }
    current = {
        "evidence_dag": {
            "nodes": {
                "current": {"path": current_path},
                "report_lifecycle_index": {
                    "path": "workstreams/report-lifecycle-index-v0.1.json"
                },
            },
        }
    }
    report = build_report_lifecycle_index(
        root=tmp_path,
        policy=policy,
        current=current,
        source_commit="test-source",
        source_tree_dirty=False,
    )
    by_path = {item["path"]: item for item in report["reports"]}
    assert by_path[current_path]["category"] == "current"
    assert by_path[external_path]["category"] == "external"
    assert by_path[superseded_path]["category"] == "superseded"
    assert by_path[archive_path]["classification_reason"] == "archive_directory"
    assert by_path[historical_path]["category"] == "historical"
    assert report["all_reports_classified_exactly_once"] is True
    assert report["deletion_authorized"] is False


def test_report_lifecycle_rejects_missing_explicit_path(tmp_path: Path) -> None:
    policy = {
        "schema_version": "chemworld-report-lifecycle-policy-0.1",
        "report_glob": "workstreams/*/reports/**/*.json",
        "categories": ["current", "historical", "superseded", "external"],
        "external_paths": ["workstreams/a/reports/missing.json"],
        "superseded_paths": [],
        "default_noncurrent_category": "historical",
    }
    with pytest.raises(ValueError, match="paths are missing"):
        build_report_lifecycle_index(
            root=tmp_path,
            policy=policy,
            current={"evidence_dag": {"nodes": {}}},
            source_commit="test-source",
            source_tree_dirty=False,
        )
