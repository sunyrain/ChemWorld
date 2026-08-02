from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.arxiv_v1_derived_data import (
    ArxivV1DerivedDataError,
    _g2_v05_rows,
    canonical_sha256,
    file_sha256,
)

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "benchmark" / "releases" / "chemworld-serious-v1"
DERIVED = RELEASE / "arxiv-v1-derived-data.json"
INTERPRETATION_POLICY = ROOT / (
    "configs/benchmark/"
    "g2_autonomous_electrochemical_material_seed1_seed3_r5_v0.5_"
    "interpretation_policy.json"
)


def _load_derived() -> dict[str, object]:
    return json.loads(DERIVED.read_text(encoding="utf-8"))


def _terminal_g2_audit() -> dict[str, object]:
    policy = json.loads(INTERPRETATION_POLICY.read_text(encoding="utf-8"))
    fallback = policy["classification"]["branch_precedence"][-1]
    audit: dict[str, object] = {
        "schema_version": "chemworld-autonomous-material-trajectory-replication-audit-0.1",
        "status": "completed_audited_fresh_trajectory_replication",
        "matrix": {
            "completed_cell_count": 20,
            "right_censored_cell_count": 0,
            "all_attempt_selection_policies_verified": True,
            "all_physical_pairs_verified": True,
            "all_terminal_cells_resource_replay_verified": True,
        },
        "paired_trajectories": [],
        "within_world_descriptive_aggregates": [],
        "interpretation": {
            "mapping_policy": {
                "sha256": file_sha256(INTERPRETATION_POLICY),
                "schema_version": policy["schema_version"],
                "status": policy["status"],
            },
            "selected_branch": {
                "branch_id": fallback["branch_id"],
                "manuscript_language": fallback["manuscript_language"],
            },
        },
    }
    audit["audit_sha256"] = canonical_sha256(audit)
    return audit


def _rehash_audit(audit: dict[str, object]) -> None:
    audit.pop("audit_sha256", None)
    audit["audit_sha256"] = canonical_sha256(audit)


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
    complete_pairs = [
        row for row in data["g2_v0_5"]["paired_trajectories"] if row["pair_complete"]
    ]
    assert len(complete_pairs) == 8
    for row in complete_pairs:
        contrast = row["nominal_minus_opaque"]
        assert contrast["terminal_final_score"] == contrast["final_score_sequence"][-1]


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


def test_generated_release_text_is_lf_stable_and_figure_hashes_match() -> None:
    manifest_path = RELEASE / "figure-manifest.json"
    display_path = ROOT / "paper/experimental_intelligence_v1_display_items.md"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for path in (DERIVED, manifest_path, display_path):
        assert b"\r\n" not in path.read_bytes()
    for row in manifest["files"]:
        path = ROOT / row["path"]
        assert file_sha256(path) == row["sha256"]
        if path.suffix == ".svg":
            assert b"\r\n" not in path.read_bytes()


def test_terminal_g2_rows_require_the_frozen_interpretation_binding() -> None:
    audit = _terminal_g2_audit()
    assert _g2_v05_rows(audit)["interpretation"]["selected_branch"]["branch_id"]

    missing = deepcopy(audit)
    missing.pop("interpretation")
    _rehash_audit(missing)
    with pytest.raises(ArxivV1DerivedDataError, match="interpretation block"):
        _g2_v05_rows(missing)


def test_terminal_g2_rows_reject_a_posthoc_branch_rewrite() -> None:
    audit = _terminal_g2_audit()
    audit["interpretation"]["selected_branch"]["manuscript_language"] = "better story"
    _rehash_audit(audit)
    with pytest.raises(ArxivV1DerivedDataError, match="language differs"):
        _g2_v05_rows(audit)
