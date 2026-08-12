from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.check_package_research_boundary import BASELINE_PATH, audit, scan

ROOT = Path(__file__).resolve().parents[1]


def test_current_package_boundary_matches_reviewed_baseline() -> None:
    regressions, resolved = audit(ROOT)

    assert regressions == []
    assert resolved == []


def test_scan_reports_repository_only_literal_family(tmp_path: Path) -> None:
    module = tmp_path / "src" / "chemworld" / "sample.py"
    module.parent.mkdir(parents=True)
    module.write_text('PATH = "workstreams/example/report.json"\n', encoding="utf-8")

    assert scan(tmp_path) == {"src/chemworld/sample.py": ["workstreams/"]}


def test_audit_rejects_new_package_dependency(tmp_path: Path) -> None:
    module = tmp_path / "src" / "chemworld" / "sample.py"
    module.parent.mkdir(parents=True)
    module.write_text('PATH = "scripts/build_report.py"\n', encoding="utf-8")
    baseline = tmp_path / BASELINE_PATH
    baseline.parent.mkdir(parents=True)
    baseline.write_text("{}\n", encoding="utf-8")

    regressions, resolved = audit(tmp_path)

    assert regressions == ["src/chemworld/sample.py: scripts/"]
    assert resolved == []


def test_audit_fails_closed_when_baseline_is_missing(tmp_path: Path) -> None:
    (tmp_path / "src" / "chemworld").mkdir(parents=True)

    with pytest.raises(RuntimeError, match="unable to load boundary baseline"):
        audit(tmp_path)


def test_baseline_is_machine_readable() -> None:
    baseline = json.loads((ROOT / BASELINE_PATH).read_text(encoding="utf-8"))

    assert len(baseline) == 34
