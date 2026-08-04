from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.audit_work_i_figure_integration import (
    FIGURES,
    MANIFEST_PATH,
    FigureIntegrationError,
    _ordered_positions,
    build_integration_manifest,
    manifest_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _committed() -> dict[str, Any]:
    payload = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_final_inventory_binds_six_figures_and_eighteen_assets() -> None:
    manifest = _committed()
    assert manifest == build_integration_manifest(ROOT)
    assert manifest["manifest_sha256"] == manifest_sha256(manifest)
    assert manifest["status"] == "PASS"
    assert manifest["canonical_figure_count"] == 6
    assert manifest["canonical_asset_count"] == 18
    assert manifest["caption_titles"] == [title for _, _, title in FIGURES]
    assert [row["figure_id"] for row in manifest["figures"]] == [
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
    ]
    assert sum(len(row["outputs"]) for row in manifest["figures"]) == 18


def test_f3_is_finalized_as_a_failed_gate_not_a_point_estimate() -> None:
    manifest = _committed()
    f3 = manifest["figures"][2]
    assert f3["owner_task"] == "W1-P09"
    assert f3["original_owner_task"] == "W1-P04"
    assert f3["manifest_status"] == "frozen_latent_gate_failure_display"
    assert f3["pending_result_panels"] == []
    assert manifest["latent_terminal_disposition"] == {
        "figure_id": "F3",
        "formal_gate_passed": False,
        "main_text_point_estimates_reported": False,
        "resolved_shadow_receipts": 6,
        "unresolved_shadow_receipts": 30,
        "finite_population_bounds_reported": True,
    }


def test_manifest_hash_and_caption_order_fail_closed() -> None:
    manifest = _committed()
    tampered = deepcopy(manifest)
    tampered["canonical_asset_count"] = 17
    assert tampered["manifest_sha256"] != manifest_sha256(tampered)
    with pytest.raises(FigureIntegrationError, match="order"):
        _ordered_positions("second first", ["first", "second"], "test captions")
