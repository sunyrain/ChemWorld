from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest
from scripts.run_work_ii_matched_prior_qualification import (
    _d1_config,
    _prepare_execution,
    _resolve_output_paths,
    _validate_source_execution_context,
)

from chemworld.eval.work_ii_matched_prior_qualification import (
    analyze_matched_prior_world,
    audit_public_priors,
    audit_supplied_prior_matching,
    rounded_reference_context,
    select_reference_candidate,
    surface_design,
)

ROOT = Path(__file__).resolve().parents[1]


def test_development_q2_accepts_development_or_release_upstream() -> None:
    context, envelope = _prepare_execution(Namespace())
    assert _validate_source_execution_context(
        {"execution_context": envelope}, context
    ) == (envelope, False)
    release_upstream = {
        **envelope,
        "execution_mode": "release",
        "evidence_status": "release_candidate",
        "release_eligible": True,
        "c2_admission_authorized": True,
        "tested_commit": "a" * 40,
        "freeze_id": "b" * 64,
        "release_manifest_sha256": "c" * 64,
        "execution_surface_sha256": "d" * 64,
    }
    assert _validate_source_execution_context(
        {"execution_context": release_upstream}, context
    ) == (release_upstream, False)


def test_development_q2_marks_legacy_upstream_and_release_rejects_it() -> None:
    development_context, _ = _prepare_execution(Namespace())
    assert _validate_source_execution_context({}, development_context) == (None, True)
    release_context = development_context.__class__(
        mode=development_context.mode.RELEASE,
        evidence_status="release_candidate",
        release_eligible=True,
        c2_admission_authorized=True,
        tested_commit="a" * 40,
        freeze_id="b" * 64,
        release_manifest_sha256="c" * 64,
        execution_surface_sha256="d" * 64,
    )
    with pytest.raises(ValueError, match="release Q2 source lacks"):
        _validate_source_execution_context({}, release_context)


def test_reaction_d1_remains_provider_unauthorized_and_mode_labelled() -> None:
    base = json.loads(
        (
            ROOT
            / "configs/benchmark/"
            "work_ii_reaction_safety_parametric_initial_model_pilot.json"
        ).read_text(encoding="utf-8")
    )
    world_package = {
        "world_seed": 0,
        "reference_context": {},
        "prior_arms": {"opaque": {}, "aligned_nominal": {}, "misindexed_nominal": {}},
        "held_out_queries": [],
        "world_package_sha256": "a" * 64,
    }
    config = _d1_config(base, world_package, legacy_source_evidence=True)
    assert config["qualification"]["execution_authorized"] is False
    assert config["execution_context"]["execution_mode"] == "development"
    assert config["legacy_source_evidence"] is True


def test_reaction_q2_development_defaults_all_outputs_under_run_root(
    tmp_path: Path,
) -> None:
    context, _ = _prepare_execution(Namespace())
    root, summary, package, d1 = _resolve_output_paths(
        Namespace(output_root=tmp_path, summary=None, package=None, d1_config=None),
        context,
    )
    assert (root, summary, package, d1) == (
        tmp_path,
        tmp_path / "summary.json",
        tmp_path / "package.json",
        tmp_path / "d1.json",
    )


def _source_report() -> dict:
    return {
        "analysis": {
            "oracle_optimum": {
                "score": 0.45,
                "vector": [0.80, 0.20, 0.10, 0.20, 0.375, 0.70, 0.625, 0.30],
            }
        },
        "validation_candidates": [
            {
                "candidate_rank": 1,
                "oracle_score": 0.45,
                "vector": [0.80, 0.20, 0.10, 0.20, 0.375, 0.70, 0.625, 0.30],
            },
            {
                "candidate_rank": 2,
                "oracle_score": 0.44,
                "vector": [0.78, 0.22, 0.10, 0.20, 0.375, 0.70, 0.625, 0.30],
            },
            {
                "candidate_rank": 3,
                "oracle_score": 0.43,
                "vector": [0.76, 0.24, 0.20, 0.35, 0.375, 0.76, 0.625, 0.36],
            },
        ],
    }


def test_reference_candidate_uses_first_non_optimum_context() -> None:
    selected = select_reference_candidate(_source_report())
    assert selected["candidate_rank"] == 3
    assert selected["score_gap"] == pytest.approx(0.02)
    assert selected["non_target_distance"] > 0.05


def test_surface_design_is_frozen_checkerboard() -> None:
    selected = select_reference_candidate(_source_report())
    context = rounded_reference_context(selected["vector"])
    rows = surface_design(context)
    assert len(rows) == 121
    assert sum(row["split"] == "fit" for row in rows) == 36
    assert sum(row["split"] == "held_out" for row in rows) == 85
    assert rows[0]["temperature_K"] == 370.0
    assert rows[0]["duration_s"] == 300.0
    assert rows[-1]["temperature_K"] == 470.0
    assert rows[-1]["duration_s"] == 6300.0


def test_matched_prior_analysis_passes_identifiable_synthetic_surface() -> None:
    selected = select_reference_candidate(_source_report())
    context = rounded_reference_context(selected["vector"])
    rows = []
    for design in surface_design(context):
        x_value = (design["temperature_K"] - 420.0) / 50.0
        y_value = (design["duration_s"] - 3300.0) / 3000.0
        score = 0.34 + 0.08 * x_value - 0.02 * y_value + 0.01 * x_value * y_value
        risk = 0.18 + 0.025 * x_value + 0.015 * y_value
        rows.append(
            {
                **design,
                "status": "completed",
                "safe": True,
                "score": score,
                "safety_risk": risk,
            }
        )
    analysis = analyze_matched_prior_world(
        rows,
        validation_sigma=0.001,
        reference_context=context,
        world_token="synthetic-world",
    )
    assert analysis["passed"] is True
    assert analysis["selected_reflection"]["axis"] == "temperature"
    assert analysis["selected_reflection"]["disagreement_fraction"] >= 0.25
    assert analysis["selected_reflection"]["low_side_support"] >= 3
    assert analysis["selected_reflection"]["high_side_support"] >= 3
    assert len(analysis["held_out_queries"]) == 16
    assert analysis["blind_identification"]["identified_aligned_law"] is True


def test_public_supplied_priors_are_matched_and_identity_free() -> None:
    selected = select_reference_candidate(_source_report())
    context = rounded_reference_context(selected["vector"])
    rows = []
    for design in surface_design(context):
        x_value = (design["temperature_K"] - 420.0) / 50.0
        y_value = (design["duration_s"] - 3300.0) / 3000.0
        rows.append(
            {
                **design,
                "status": "completed",
                "safe": True,
                "score": 0.34 + 0.08 * x_value - 0.02 * y_value,
                "safety_risk": 0.18 + 0.02 * x_value + 0.01 * y_value,
            }
        )
    analysis = analyze_matched_prior_world(
        rows,
        validation_sigma=0.001,
        reference_context=context,
        world_token="synthetic-world",
    )
    priors = analysis["public_priors"]
    matching = audit_supplied_prior_matching(priors["supplied_a"], priors["supplied_b"])
    assert matching["passed"] is True
    assert matching["difference_paths"] == ["model.claim.expected_relation"]
    assert audit_public_priors(priors)["passed"] is True
