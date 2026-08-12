from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.check_package_import_boundaries import BASELINE_PATH, audit, scan

ROOT = Path(__file__).resolve().parents[1]


def test_current_import_boundary_matches_reviewed_baseline() -> None:
    regressions, resolved = audit(ROOT)

    assert regressions == []
    assert resolved == []


def test_scan_reports_upward_imports(tmp_path: Path) -> None:
    module = tmp_path / "src" / "chemworld" / "foundation" / "sample.py"
    module.parent.mkdir(parents=True)
    module.write_text(
        "from chemworld.world.scenario import ScenarioSpec\nimport chemworld.providers.deepseek\n",
        encoding="utf-8",
    )

    assert scan(tmp_path) == {"src/chemworld/foundation/sample.py": ["providers", "world"]}


def test_scan_ignores_allowed_downward_imports(tmp_path: Path) -> None:
    module = tmp_path / "src" / "chemworld" / "runtime" / "sample.py"
    module.parent.mkdir(parents=True)
    module.write_text(
        "from chemworld.foundation import WorldState\n"
        "from chemworld.physchem.specs import PropertyCorrelation\n"
        "from chemworld.world.parameters import ChemWorldParameters\n",
        encoding="utf-8",
    )

    assert scan(tmp_path) == {}


def test_audit_rejects_new_upward_import(tmp_path: Path) -> None:
    module = tmp_path / "src" / "chemworld" / "world" / "sample.py"
    module.parent.mkdir(parents=True)
    module.write_text("from chemworld.eval.metrics import score\n", encoding="utf-8")
    baseline = tmp_path / BASELINE_PATH
    baseline.parent.mkdir(parents=True)
    baseline.write_text("{}\n", encoding="utf-8")

    regressions, resolved = audit(tmp_path)

    assert regressions == ["src/chemworld/world/sample.py: chemworld.eval"]
    assert resolved == []


def test_audit_fails_closed_when_baseline_is_missing(tmp_path: Path) -> None:
    (tmp_path / "src" / "chemworld").mkdir(parents=True)

    with pytest.raises(RuntimeError, match="unable to load import-boundary baseline"):
        audit(tmp_path)


def test_baseline_is_machine_readable() -> None:
    baseline = json.loads((ROOT / BASELINE_PATH).read_text(encoding="utf-8"))

    assert baseline
