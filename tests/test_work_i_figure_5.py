from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.render_work_i_figure_5 import (
    EXPECTED_OPERATION_SIGNATURE,
    MANIFEST_PATH,
    OUTPUT_DIR,
    OUTPUT_STEM,
    load_figure_inputs,
    manifest_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


def _manifest() -> dict[str, object]:
    payload = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_example_is_the_frozen_seven_operation_lifecycle() -> None:
    inputs = load_figure_inputs(ROOT)
    demonstration = inputs["demonstration"]
    assert tuple(demonstration["operation_signature"]) == EXPECTED_OPERATION_SIGNATURE
    assert demonstration["operation_count"] == 7
    assert demonstration["cell_id"] == "cell-01"
    assert demonstration["arm"] == "opaque"
    assert demonstration["world_seed"] == 0
    assert demonstration["final_score"] == pytest.approx(0.5306862436116384)
    assert demonstration["diagnostic_policy"] == [
        {"instrument": "uvvis", "operation_index_in_batch": 5}
    ]


def test_campaign_receipt_preserves_closure_resources_and_units() -> None:
    receipt = load_figure_inputs(ROOT)["receipt"]
    assert receipt["verified"] is True
    assert receipt["trajectory_event_alignment_verified"] is True
    assert (
        receipt["expected_batches"],
        receipt["closed_batches"],
        receipt["final_assays"],
        receipt["discarded_batches"],
    ) == (6, 6, 6, 0)
    assert receipt["operation_attempts"] == 69
    assert receipt["nonfinal_instrument_uses"] == 17
    assert receipt["stocks_used"] == {
        "reagent_mol": pytest.approx(0.24),
        "solvent_L": pytest.approx(0.48),
    }
    assert receipt["report_only"]["process_time_s"] == pytest.approx(140400.0)


def test_full_g2_v04_accounting_and_replay_gates_are_exact() -> None:
    inputs = load_figure_inputs(ROOT)
    assert inputs["totals"] == {
        "closed_lifecycles": 60,
        "operation_attempts": 815,
        "nonfinal_measurements": 164,
        "invalid_operations": 0,
    }
    ledger = inputs["ledger_g2"]
    assert ledger["final_assays"] == 60
    assert ledger["provider_sessions"] == 60
    assert ledger["all_cells_complete"] is True
    assert ledger["all_exact_replays_verified"] is True
    assert ledger["all_pairs_physically_matched"] is True


def test_manifest_binds_sources_outputs_and_counting_boundary() -> None:
    manifest = _manifest()
    assert manifest["manifest_sha256"] == manifest_sha256(manifest)
    assert manifest["figure_id"] == "F5"
    assert manifest["owner_task"] == "W1-P06"
    assert manifest["evidence_census"] == {
        "worlds": 5,
        "information_arms": 2,
        "campaign_cells": 10,
        "closed_lifecycles": 60,
        "final_assays": 60,
        "explicit_discards": 0,
        "accepted_primitive_operations": 815,
        "nonfinal_measurements": 164,
        "invalid_or_rejected_operations": 0,
        "provider_sessions": 60,
        "right_censored_lifecycles": 0,
        "example_operation_count": 7,
    }
    assert manifest["claim_boundary"]["example_is_descriptive"] is True
    assert manifest["claim_boundary"]["operations_as_independent_samples"] is False
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
    assert "Primitive-control agents expose" not in svg
    assert pdf.startswith(b"%PDF") and b"/FontFile2" in pdf
    assert int.from_bytes(png[16:20], "big") == 2124
    assert int.from_bytes(png[20:24], "big") == 1560

    tampered = deepcopy(manifest)
    tampered["claim_boundary"]["operations_as_independent_samples"] = True
    assert tampered["manifest_sha256"] != manifest_sha256(tampered)
