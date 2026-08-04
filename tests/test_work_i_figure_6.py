from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from scripts.render_work_i_figure_6 import (
    DISCORDANT_PAIR_IDS,
    MANIFEST_PATH,
    OUTPUT_DIR,
    OUTPUT_STEM,
    _sign_discordant_pair_ids,
    load_figure_inputs,
    manifest_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _manifest() -> dict[str, Any]:
    payload = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_fresh_matched_design_retains_right_censoring() -> None:
    inputs = load_figure_inputs(ROOT)
    pairs = inputs["pairs"]
    complete = inputs["complete_pairs"]
    assert len(pairs) == 10
    assert len(complete) == 8
    censored = [row for row in pairs if not row["pair_complete"]]
    assert [(row["world_seed"], row["trajectory_replicate_id"]) for row in censored] == [
        (1, "r01"),
        (3, "r05"),
    ]
    assert inputs["matrix"]["right_censored_cell_ids"] == ["cell-001", "cell-019"]


def test_best_versus_raw_terminal_endpoint_diagnostic_is_two_of_eight() -> None:
    complete = load_figure_inputs(ROOT)["complete_pairs"]
    assert _sign_discordant_pair_ids(complete) == DISCORDANT_PAIR_IDS
    lookup = {
        (row["world_seed"], row["trajectory_replicate_id"]): row["nominal_minus_opaque"]
        for row in complete
    }
    assert lookup[(1, "r03")]["best_final_score"] < 0 < lookup[(1, "r03")]["terminal_final_score"]
    assert lookup[(3, "r01")]["best_final_score"] < 0 < lookup[(3, "r01")]["terminal_final_score"]


def test_threshold_classification_is_supporting_and_descriptive() -> None:
    inputs = load_figure_inputs(ROOT)
    assert inputs["core_classes"].count("mixed") == 6
    assert inputs["core_classes"].count("directionally_positive") == 1
    assert inputs["core_classes"].count("directionally_negative") == 1
    interpretation = inputs["interpretation"]
    assert interpretation["descriptive_only"] is True
    assert interpretation["development_trajectory_included"] is False
    assert interpretation["provider_sampling_seed_controlled"] is False
    assert interpretation["general_world_effect_allowed"] is False


def test_manifest_binds_sources_outputs_and_claim_boundary() -> None:
    manifest = _manifest()
    assert manifest["manifest_sha256"] == manifest_sha256(manifest)
    assert manifest["figure_id"] == "F6"
    assert manifest["owner_task"] == "W1-P07"
    assert manifest["evidence_census"] == {
        "selected_worlds": 2,
        "fresh_replicates_per_world": 5,
        "planned_matched_pairs": 10,
        "complete_matched_pairs": 8,
        "right_censored_pairs": 2,
        "planned_cells": 20,
        "completed_cells": 18,
        "right_censored_cells": 2,
        "planned_vessel_opportunities": 120,
        "executed_vessels": 114,
        "completed_final_assays": 112,
        "accepted_primitive_operations": 1615,
        "best_vs_raw_terminal_sign_discordant_pairs": 2,
        "world_by_core_metric_classifications": 8,
        "mixed_world_by_core_metric_classifications": 6,
    }
    assert manifest["claim_boundary"]["population_level_material_information_claim"] is False
    assert manifest["claim_boundary"]["right_censored_pairs_retained"] is True
    assert len(manifest["source_bindings"]) == 8
    for binding in manifest["source_bindings"]:
        assert _sha256(ROOT / binding["path"]) == binding["sha256"]

    outputs = manifest["outputs"]
    assert [row["format"] for row in outputs] == ["svg", "pdf", "png"]
    for row in outputs:
        path = ROOT / row["path"]
        assert path.stat().st_size == row["bytes"]
        assert _sha256(path) == row["sha256"]

    output_dir = ROOT / OUTPUT_DIR
    svg = (output_dir / f"{OUTPUT_STEM}.svg").read_text(encoding="utf-8")
    pdf = (output_dir / f"{OUTPUT_STEM}.pdf").read_bytes()
    png = (output_dir / f"{OUTPUT_STEM}.png").read_bytes()
    assert "<text" in svg
    assert "Fresh trajectories reveal process structure" not in svg
    assert "r01" not in svg
    assert "r05" not in svg
    assert "rep. 1" in svg
    assert "rep. 5" in svg
    assert pdf.startswith(b"%PDF") and b"/FontFile2" in pdf
    assert int.from_bytes(png[16:20], "big") == 2124
    assert int.from_bytes(png[20:24], "big") == 1560

    tampered = deepcopy(manifest)
    tampered["claim_boundary"]["population_level_material_information_claim"] = True
    assert tampered["manifest_sha256"] != manifest_sha256(tampered)
