from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.audit_work_i_publication_figures import (
    PUBLICATION_DIR,
    REPORT_JSON_PATH,
    REPORT_MD_PATH,
    PublicationFigureAuditError,
    audit_publication_figures,
    audit_sha256,
    build_markdown_report,
    validate_bound_file,
)

ROOT = Path(__file__).resolve().parents[1]


def _committed_audit() -> dict[str, Any]:
    payload = json.loads((ROOT / REPORT_JSON_PATH).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_p01_resolves_exactly_six_canonical_publication_figures() -> None:
    audit = audit_publication_figures(ROOT)
    assert audit["status"] == "PASS"
    assert [(row["figure_id"], row["owner_task"]) for row in audit["figures"]] == [
        ("F1", "W1-P02"),
        ("F2", "W1-P03"),
        ("F3", "W1-P09"),
        ("F4", "W1-P05"),
        ("F5", "W1-P06"),
        ("F6", "W1-P07"),
    ]
    assert audit["aggregate"]["canonical_assets_passed"] == 18
    assert audit["aggregate"]["figures_with_pending_result_panels"] == 0
    assert audit["figures"][2]["pending_result_panels"] == []
    assert audit["figures"][2]["original_owner_task"] == "W1-P04"
    assert audit["figures"][2]["manifest_status"] == "frozen_latent_gate_failure_display"
    assert audit["aggregate"]["legacy_unmanifested_assets_excluded"] == 12
    assert all(
        path.startswith(PUBLICATION_DIR.as_posix()) for path in audit["legacy_unmanifested_assets"]
    )


def test_every_format_passes_the_frozen_publication_criteria() -> None:
    audit = audit_publication_figures(ROOT)
    for figure in audit["figures"]:
        outputs = {row["format"]: row for row in figure["outputs"]}
        assert list(outputs) == ["svg", "pdf", "png"]
        svg = outputs["svg"]["properties"]
        assert svg["text_is_editable"] is True
        assert svg["text_element_count"] > 0
        assert svg["embedded_image_count"] == 0
        assert (svg["width_points"], svg["height_points"]) == pytest.approx((509.76, 374.4))
        pdf = outputs["pdf"]["properties"]
        assert pdf["page_count"] == 1
        assert pdf["embedded_truetype_font_stream_count"] > 0
        assert (pdf["width_points"], pdf["height_points"]) == pytest.approx((509.76, 374.4))
        png = outputs["png"]["properties"]
        assert (png["width_pixels"], png["height_pixels"]) == (2124, 1560)
        assert (png["dpi_x"], png["dpi_y"]) == pytest.approx((299.9994, 299.9994))


def test_committed_reports_match_the_deterministic_self_hashed_rebuild() -> None:
    committed = _committed_audit()
    rebuilt = audit_publication_figures(ROOT)
    assert committed == rebuilt
    assert committed["audit_sha256"] == audit_sha256(committed)
    assert (ROOT / REPORT_MD_PATH).read_text(encoding="utf-8") == build_markdown_report(rebuilt)
    assert len(committed["source_bindings"]) == 8
    tampered = deepcopy(committed)
    tampered["aggregate"]["canonical_assets_passed"] = 17
    assert tampered["audit_sha256"] != audit_sha256(tampered)


def test_bound_asset_hash_tampering_fails_closed(tmp_path: Path) -> None:
    audit = audit_publication_figures(ROOT)
    png = audit["figures"][0]["outputs"][2]
    source = ROOT / png["path"]
    tampered = tmp_path / source.name
    tampered.write_bytes(source.read_bytes() + b"tamper")
    with pytest.raises(PublicationFigureAuditError, match="byte count mismatch"):
        validate_bound_file(tampered, png["sha256"], png["bytes"])
