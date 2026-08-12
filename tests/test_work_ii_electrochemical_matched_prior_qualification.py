from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest
from scripts.run_work_ii_electrochemical_matched_prior_qualification import (
    _d1_config,
    _prepare_execution,
    _resolve_output_paths,
    _validate_source_execution_context,
)

from chemworld.eval.work_ii_electrochemical_matched_prior_qualification import (
    GRID_COORDINATES,
    analyze_matched_prior_world,
    build_public_priors,
    rounded_reference_context,
    select_reference_candidate,
    surface_design,
)

ROOT = Path(__file__).resolve().parents[1]


def _source_report() -> dict:
    optimum = [0.625, 0.375, 0.02, 0.86, 0.80, 0.51, 0.62, 0.80, 0.98]
    candidate = [0.625, 0.375, 0.02, 0.78, 0.76, 0.58, 0.60, 0.78, 0.98]
    return {
        "analysis": {"oracle_optimum": {"vector": optimum, "score": 0.84}},
        "validation_candidates": [
            {"candidate_rank": 1, "vector": optimum, "oracle_score": 0.84},
            {"candidate_rank": 2, "vector": candidate, "oracle_score": 0.82},
        ],
    }


def _context() -> dict:
    return {
        "electrolyte_profile": 1,
        "solvent": 1,
        "reagent_amount_mol": 0.01,
        "probe_potential_V": 1.0,
        "probe_current_mA": 60.0,
        "probe_duration_s": 600.0,
        "controlled_duration_s": 1800.0,
    }


def test_electrochemical_surface_uses_frozen_36_85_checkerboard() -> None:
    selected = select_reference_candidate(_source_report())
    context = rounded_reference_context(selected["vector"])
    rows = surface_design(context)

    assert len(rows) == 121
    assert len(GRID_COORDINATES) == 11
    assert sum(row["split"] == "fit" for row in rows) == 36
    assert sum(row["split"] == "held_out" for row in rows) == 85
    assert all(0.6 <= row["controlled_potential_V"] <= 1.8 for row in rows)
    assert all(0.001 <= row["controlled_current_mA"] <= 220.0 for row in rows)


def test_baseline_preserving_potential_reflection_passes_synthetic_surface() -> None:
    rows = []
    for row in surface_design(_context()):
        potential = float(row["potential_coordinate"])
        current = float(row["current_coordinate"])
        score = 0.62 - 0.24 * (potential - 0.5) - 0.04 * (current - 0.5) ** 2
        rows.append(
            {
                **row,
                "status": "completed",
                "safe": True,
                "score": score,
                "safety_risk": 0.05,
            }
        )

    analysis = analyze_matched_prior_world(
        rows,
        validation_sigma=0.001,
        reference_context=_context(),
        world_token="electrochemical-conversion:synthetic",
    )

    assert analysis["passed"] is True
    assert analysis["selected_reflection"]["axis"] == "potential"
    assert analysis["selected_reflection"]["baseline_maximum_score_gap"] == pytest.approx(0.0)
    assert analysis["selected_reflection"]["blind_error_margin"] >= 0.05
    assert analysis["prior_matching"]["passed"] is True
    assert analysis["leakage_audit"]["passed"] is True


def test_public_priors_differ_only_in_directional_claim() -> None:
    priors = build_public_priors(
        {"axis": "potential", "aligned_preferred_side": "lower_controlled_potential"},
        reference_context=_context(),
    )

    left = json.loads(json.dumps(priors["supplied_a"], sort_keys=True))
    right = json.loads(json.dumps(priors["supplied_b"], sort_keys=True))
    left["model"]["claim"].pop("expected_relation")
    right["model"]["claim"].pop("expected_relation")
    assert left == right


def test_generated_d1_config_uses_electrochemical_k10_pattern() -> None:
    base = json.loads(
        (
            ROOT / "configs/benchmark/work_ii_electrochemical_parametric_initial_model_pilot.json"
        ).read_text(encoding="utf-8")
    )
    world_package = {
        "world_seed": 0,
        "reference_context": _context(),
        "prior_arms": {"opaque": {}, "aligned_nominal": {}, "misindexed_nominal": {}},
        "held_out_queries": [],
        "world_package_sha256": "a" * 64,
    }
    config = _d1_config(base, world_package)

    campaign = config["campaign"]
    assert campaign["complete_experiments"] == 10
    assert campaign["operation_attempt_limit"] == 110
    assert campaign["operation_repeat_limits"] == {"electrolyze": 20}
    assert campaign["process_time_limit_s"] == pytest.approx(45_000.0)
    assert campaign["process_time_policy"]["required_stage_max_s"] == pytest.approx(36_000.0)
    assert campaign["process_time_policy"]["repeat_allowance_s"] == pytest.approx(9_000.0)
    assert campaign["process_time_policy"]["quench_transfer_allowance_s"] == pytest.approx(0.0)
    assert config["qualification"]["execution_authorized"] is False
    assert config["qualification"]["formal_r5_authorized"] is False
    assert config["execution_context"]["execution_mode"] == "development"


def test_electrochemical_q2_rejects_cross_freeze_release_upstream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import scripts.run_work_ii_electrochemical_matched_prior_qualification as runner

    context, envelope = _prepare_execution(Namespace())
    release_context = context.__class__(
        mode=context.mode.RELEASE,
        evidence_status="release_candidate",
        release_eligible=True,
        c2_admission_authorized=True,
        tested_commit="a" * 40,
        freeze_id="b" * 64,
        release_manifest_sha256="c" * 64,
        execution_surface_sha256="d" * 64,
    )
    monkeypatch.setattr(runner, "validate_execution_envelope", lambda *_args: ["mismatch"])
    with pytest.raises(ValueError, match="same release freeze"):
        _validate_source_execution_context(
            {"execution_context": envelope}, release_context
        )


def test_electrochemical_development_q2_marks_legacy_upstream() -> None:
    context, _ = _prepare_execution(Namespace())
    assert _validate_source_execution_context({}, context) == (None, True)


def test_electrochemical_runner_development_preparation_avoids_git(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import chemworld.eval.work_ii_execution_mode as execution_mode

    def unexpected(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("development electrochemical Q2 used release provenance")

    monkeypatch.setattr(execution_mode, "git_worktree_dirty", unexpected)
    monkeypatch.setattr(execution_mode, "git_source_commit", unexpected)
    monkeypatch.setattr(execution_mode, "work_ii_material_tree_sha256", unexpected)
    _, envelope = _prepare_execution(Namespace())
    assert envelope["execution_mode"] == "development"
    assert envelope["freeze_id"] is None


def test_electrochemical_q2_development_defaults_outputs_under_run_root(
    tmp_path: Path,
) -> None:
    context, _ = _prepare_execution(Namespace())
    root, summary, package, d1 = _resolve_output_paths(
        Namespace(output_root=tmp_path, summary=None, package=None, d1_config=None),
        context,
    )
    assert root == tmp_path
    assert {summary, package, d1} == {
        tmp_path / "summary.json",
        tmp_path / "package.json",
        tmp_path / "d1.json",
    }
