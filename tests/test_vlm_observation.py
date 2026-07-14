from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from chemworld.agents.multimodal import PublicImageArtifact
from chemworld.eval.vlm_observation import (
    SpectrumRenderSpec,
    prepare_vlm_observation,
    render_public_spectrum_packet,
)


def _hplc_packet(*, scale: float = 1.0, secret: str = "target_public") -> dict[str, Any]:
    return {
        "schema_version": "chemworld-public-synthetic-signal-0.2",
        "kind": "hplc_chromatogram",
        "instrument_id": "hplc",
        "time_min": [0.0, 1.0, 2.0, 3.0],
        "intensity": [0.0, 0.3 * scale, 1.0 * scale, 0.1 * scale],
        "peaks": [
            {
                "retention_time_min": 2.0,
                "assignment": secret,
                "analyte_id": secret,
            }
        ],
        "assignments": [{"analyte_id": secret, "assignment": secret}],
        "metadata": {"private-looking-label": secret},
    }


def _ir_packet() -> dict[str, Any]:
    return {
        "kind": "ir_spectrum",
        "instrument_id": "ir",
        "wavenumber_cm-1": [400.0, 1200.0, 2400.0, 4000.0],
        "transmittance": [0.9, 0.3, 0.7, 0.95],
        "peaks": [],
        "assignments": [],
    }


def _context(*, requested: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "contract_version": "chemworld-agent-interaction-0.3",
        "step": 4,
        "task_id": "yield_optimization_v0",
        "decision_stage": "evidence_update",
        "campaign_state": {"remaining_budget": 5},
        "visible_metrics": {"yield": 0.45},
        "latest_spectra": {
            "spectrum_id": "spectrum-current",
            "raw_signal": _hplc_packet(),
        },
        "uncertainty": {},
        "constraint_flags": {},
        "available_operations": ["measure", "terminate"],
        "previous_event_type": "measurement_result",
        "historical_spectrum_catalog": [
            {
                "spectrum_id": "spectrum-not-requested",
                "raw_signal": _ir_packet(),
            }
        ],
        "requested_historical_spectrum": requested or {},
    }


def test_public_image_artifact_rejects_path_traversal() -> None:
    digest = "0" * 64
    with pytest.raises(ValueError, match="traversal-free"):
        PublicImageArtifact(
            artifact_id="image-1",
            spectrum_id="spectrum-1",
            source="current",
            spectrum_kind="hplc_chromatogram",
            disclosure="unassigned",
            media_type="image/png",
            width_px=960,
            height_px=640,
            x_axis_direction="ascending_left_to_right",
            sha256=digest,
            signal_sha256=digest,
            public_packet_sha256=digest,
            render_contract_hash=digest,
            relative_path="../escaped.png",
        )


def test_render_is_byte_deterministic_and_signal_sensitive(tmp_path: Path) -> None:
    first = render_public_spectrum_packet(
        _hplc_packet(),
        artifact_root=tmp_path,
        spectrum_id="spectrum-1",
        source="current",
        channel="hplc",
        disclosure="unassigned",
    )
    second = render_public_spectrum_packet(
        _hplc_packet(),
        artifact_root=tmp_path,
        spectrum_id="spectrum-1",
        source="current",
        channel="hplc",
        disclosure="unassigned",
    )
    changed = render_public_spectrum_packet(
        _hplc_packet(scale=0.8),
        artifact_root=tmp_path,
        spectrum_id="spectrum-1",
        source="current",
        channel="hplc",
        disclosure="unassigned",
    )

    assert first == second
    assert first.sha256 != changed.sha256
    assert first.signal_sha256 != changed.signal_sha256
    assert (tmp_path / first.relative_path).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert first.render_contract_hash == SpectrumRenderSpec().contract_hash
    assert first.x_axis_direction == "ascending_left_to_right"


def test_assigned_and_unassigned_share_curve_but_not_identity(tmp_path: Path) -> None:
    packet = _hplc_packet(secret="public-analyte-A")
    assigned = render_public_spectrum_packet(
        packet,
        artifact_root=tmp_path,
        spectrum_id="spectrum-1",
        source="current",
        channel="hplc",
        disclosure="assigned",
    )
    unassigned = render_public_spectrum_packet(
        packet,
        artifact_root=tmp_path,
        spectrum_id="spectrum-1",
        source="current",
        channel="hplc",
        disclosure="unassigned",
    )

    assert assigned.signal_sha256 == unassigned.signal_sha256
    assert assigned.public_packet_sha256 != unassigned.public_packet_sha256
    assert assigned.sha256 != unassigned.sha256


def test_ir_uses_conventional_descending_axis(tmp_path: Path) -> None:
    artifact = render_public_spectrum_packet(
        _ir_packet(),
        artifact_root=tmp_path,
        spectrum_id="spectrum-ir",
        source="historical",
        channel="ir",
        disclosure="unassigned",
    )
    assert artifact.x_axis_direction == "descending_left_to_right"


def test_history_catalog_is_never_rendered_without_explicit_retrieval(tmp_path: Path) -> None:
    without_request = prepare_vlm_observation(
        _context(),
        artifact_root=tmp_path,
        decision_id="decision-4",
        modality="image_only",
        disclosure="unassigned",
    )
    assert [image.source for image in without_request.images] == ["current"]
    assert all("not-requested" not in image.spectrum_id for image in without_request.images)

    with_request = prepare_vlm_observation(
        _context(
            requested={
                "spectrum_id": "spectrum-requested",
                "status": "retrieved",
                "raw_signal": _ir_packet(),
            }
        ),
        artifact_root=tmp_path,
        decision_id="decision-5",
        modality="image_only",
        disclosure="unassigned",
    )
    assert [image.source for image in with_request.images] == ["current", "historical"]
    assert with_request.images[1].spectrum_id.startswith("spectrum-requested")


def test_image_only_removes_numeric_signal_and_assignment_text(tmp_path: Path) -> None:
    bundle = prepare_vlm_observation(
        _context(),
        artifact_root=tmp_path,
        decision_id="decision-image",
        modality="image_only",
        disclosure="unassigned",
    )
    latest = bundle.prompt_context["latest_spectra"]
    serialized = str(bundle.prompt_context)
    assert latest["available"] is True
    assert latest["image_artifact_ids"] == [bundle.images[0].artifact_id]
    assert "time_min" not in serialized
    assert "target_public" not in serialized
    assert "data:image" not in serialized


def test_numeric_and_combined_modalities_obey_disclosure(tmp_path: Path) -> None:
    numeric = prepare_vlm_observation(
        _context(),
        artifact_root=tmp_path,
        decision_id="decision-numeric",
        modality="numeric_only",
        disclosure="unassigned",
    )
    combined = prepare_vlm_observation(
        _context(),
        artifact_root=tmp_path,
        decision_id="decision-combined",
        modality="image_plus_numeric",
        disclosure="assigned",
    )
    assert numeric.images == ()
    assert numeric.prompt_context["latest_spectra"]["raw_signal"]["assignments"] == []
    assert "target_public" not in str(numeric.prompt_context)
    assert combined.images
    assert combined.prompt_context["latest_spectra"]["raw_signal"]["assignments"]


def test_masked_condition_never_renders_or_exposes_signal(tmp_path: Path) -> None:
    context = _context(
        requested={
            "spectrum_id": "spectrum-requested",
            "status": "retrieved",
            "raw_signal": _ir_packet(),
        }
    )
    original = deepcopy(context)
    bundle = prepare_vlm_observation(
        context,
        artifact_root=tmp_path,
        decision_id="decision-masked",
        modality="image_plus_numeric",
        disclosure="masked",
    )
    assert bundle.images == ()
    assert bundle.prompt_context["latest_spectra"] == {
        "spectrum_condition": "masked",
        "available": False,
    }
    assert "intensity" not in str(bundle.prompt_context)
    assert context == original
    assert not (tmp_path / "vlm_images").exists()


def test_manifest_is_hash_stable_and_contains_no_embedded_bytes(tmp_path: Path) -> None:
    first = prepare_vlm_observation(
        _context(),
        artifact_root=tmp_path,
        decision_id="decision-stable",
        modality="image_plus_numeric",
        disclosure="unassigned",
    )
    second = prepare_vlm_observation(
        _context(),
        artifact_root=tmp_path,
        decision_id="decision-stable",
        modality="image_plus_numeric",
        disclosure="unassigned",
    )
    assert first.manifest_hash == second.manifest_hash
    manifest_text = str(first.to_manifest()).lower()
    assert "base64" not in manifest_text
    assert "data:image" not in manifest_text
    assert str(tmp_path).lower() not in manifest_text
