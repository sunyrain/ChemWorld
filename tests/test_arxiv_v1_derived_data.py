from __future__ import annotations

import csv
import json
from pathlib import Path

from chemworld.eval.arxiv_v1_derived_data import canonical_sha256

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "benchmark" / "releases" / "chemworld-serious-v1"
DERIVED = RELEASE / "arxiv-v1-derived-data.json"


def _load_derived() -> dict[str, object]:
    return json.loads(DERIVED.read_text(encoding="utf-8"))


def test_derived_data_is_self_hashed_and_contains_no_absolute_source_paths() -> None:
    data = _load_derived()
    declared = data.pop("derived_data_sha256")
    assert declared == canonical_sha256(data)
    sources = data["sources"]
    assert isinstance(sources, dict)
    for source in sources.values():
        if source is None:
            continue
        path = source["path"]
        assert isinstance(path, str)
        assert not Path(path).is_absolute()
        assert ":" not in path


def test_derived_g0_and_g2_v04_accounting_matches_audited_totals() -> None:
    data = _load_derived()
    assert data["paper_scope"]["g0_nonduplicated_physical_experiments"] == 29580
    task_rows = data["g0"]["task_arm_rows"]
    assert len([row for row in task_rows if row["arm"] in {"opaque", "nominal", "misindexed"}]) == 6
    assert len([row for row in task_rows if row["arm"] == "derived_contrasts"]) == 2
    cells = data["g2_v0_4"]["cell_rows"]
    assert len(cells) == 10
    assert sum(row["completed_vessels"] for row in cells) == 60
    assert sum(row["operation_count"] for row in cells) == 815
    assert sum(row["invalid_operation_count"] for row in cells) == 0
    assert all(len(row["final_score_sequence"]) == 6 for row in cells)


def test_csv_views_are_generated_from_the_same_derived_rows() -> None:
    data = _load_derived()
    table_dir = RELEASE / "tables"
    expectations = {
        "g0-task-arm.csv": len(data["g0"]["task_arm_rows"]),
        "g0-world-arm.csv": len(data["g0"]["world_arm_rows"]),
        "g0-baselines.csv": len(data["g0"]["baseline_rows"]),
        "g2-v0.4-cells.csv": len(data["g2_v0_4"]["cell_rows"]),
        "g2-v0.4-paired-worlds.csv": len(data["g2_v0_4"]["paired_world_rows"]),
    }
    for name, expected in expectations.items():
        with (table_dir / name).open(encoding="utf-8", newline="") as handle:
            assert len(list(csv.DictReader(handle))) == expected


def test_figure_manifest_is_bound_to_derived_data_and_never_fakes_figure_5() -> None:
    data = _load_derived()
    manifest = json.loads((RELEASE / "figure-manifest.json").read_text(encoding="utf-8"))
    declared = manifest.pop("manifest_sha256")
    assert declared == canonical_sha256(manifest)
    assert manifest["derived_data_sha256"] == data["derived_data_sha256"]
    assert manifest["figure_5_rendered"] is (data["g2_v0_5"] is not None)
    file_paths = {row["path"] for row in manifest["files"]}
    assert any("figure-1-" in path for path in file_paths)
    assert any("figure-4-" in path for path in file_paths)
    assert any("figure-6-" in path for path in file_paths)
    assert any("figure-5-" in path for path in file_paths) is manifest["figure_5_rendered"]
