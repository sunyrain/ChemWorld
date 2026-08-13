from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import scripts.evaluate_work_ii_initial_model_pilot as evaluator
from scripts.evaluate_work_ii_initial_model_pilot import (
    _blind_skip_reason,
    _descriptive_interpretation,
    _parametric_controls,
    _rationale_score_match,
    _registered_temperature_direction,
    _render_markdown,
    _scientific_trajectory_complete,
    _supplied_model_distance,
    _temperature_direction_contract,
)

import chemworld.eval.work_ii_blind as blind_evaluator
import chemworld.eval.work_ii_truth as truth_evaluator
from chemworld.eval.provenance import canonical_json_sha256, write_json_atomic
from chemworld.eval.work_ii_execution_mode import (
    build_execution_envelope,
    prepare_execution_context,
)
from chemworld.eval.work_ii_truth import compile_evaluator_truth_query

ROOT = Path(__file__).resolve().parents[1]
AP_SEED2_CONFIGS = (
    "work_ii_reaction_safety_independent_terminal_d1_execution_seed2.json",
    "work_ii_electrochemical_independent_terminal_d1_execution_seed2.json",
)


def _prediction_rows(config: dict[str, object]) -> list[dict[str, object]]:
    checkpoint = config["belief_checkpoint"]
    return [
        {
            "query_id": query["query_id"],
            "metrics": [
                {"metric_id": metric_id, "mean": 0.5}
                for metric_id in query["metric_ids"]
            ],
        }
        for query in checkpoint["held_out_queries"]
    ]


def _synthetic_terminal_triplet(
    root: Path,
    config: dict[str, object],
) -> Path:
    participant = root / "participant"
    world_seed = int(config["world_seed"])
    action_plan = compile_evaluator_truth_query(
        config,
        config["belief_checkpoint"]["held_out_queries"][0],
    )["action_plan"]
    predictions = _prediction_rows(config)
    results = []
    for arm in ("opaque", "aligned_nominal", "misindexed_nominal"):
        recommendation = {
            "selected_experiment_index": 1,
            "selection_rationale": "Selected the highest participant-observed score.",
        }
        experiments = [
            {
                "experiment_index": index,
                "leaderboard_score": 1.0 - index / 100.0,
                "operations": action_plan,
            }
            for index in range(1, 11)
        ]
        summary = {
            "arm": arm,
            "completed": True,
            "formal_result": False,
            "analysis": {
                "complete_experiment_count": 10,
                "right_censored_open_experiment": False,
                "operation_attempt_count": len(action_plan) * 10,
                "resource_rejection_count": 0,
                "belief_snapshots": [
                    {"stage": stage, "predictions": predictions}
                    for stage in config["snapshot_stages"]
                ],
                "experiments": experiments,
                "observed_incumbent_experiment_index": 1,
                "final_recommendation": recommendation,
                "final_recommendation_sha256": canonical_json_sha256(recommendation),
                "prior_reliability_trajectory": (
                    [None] * 5 if arm == "opaque" else [0.7] * 5
                ),
                "suspected_misindexed_fields_trajectory": [[] for _ in range(5)],
            },
            "method_resources": {
                "provider_session_count": 0,
                "logical_codex_turn_count": 0,
                "input_token_count": 0,
                "cached_input_token_count": 0,
                "uncached_input_token_count": 0,
                "output_token_count": 0,
                "input_cache_hit_ratio": None,
                "session_elapsed_s": 0.0,
                "recovered_mcp_tool_failure_count": 0,
                "maximum_consecutive_mcp_tool_failure_count": 0,
                "provider_error_event_count": 0,
            },
            "exact_replay": {"verified": True},
            "qualification": {"passed": True, "failed_checks": []},
        }
        cell_root = participant / f"seed-{world_seed}" / arm
        cell_root.mkdir(parents=True)
        write_json_atomic(cell_root / "summary.json", summary)
        (cell_root / "trajectory.jsonl").write_text("", encoding="utf-8")
        results.append(summary)
    write_json_atomic(
        participant / "matrix_report.json",
        {
            "source_commit": "development-shakedown",
            "task_id": config["task_id"],
            "provider_id": "synthetic-no-provider",
            "model": "none",
            "world_seeds": [world_seed],
            "all_cells_terminal": True,
            "terminal_cell_count": 3,
            "seed_reports": [{"world_seed": world_seed, "results": results}],
        },
    )
    return participant


def _install_zero_provider_replay_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run_agent(**kwargs):
        agent = kwargs["agent"]
        output_path = Path(kwargs["output_path"])
        agent.reset({}, 0)
        rows = []
        history = []
        for _step in range(kwargs["budget"]):
            action = agent.act(history)
            observation = {
                "yield": 0.5,
                "selectivity": 0.5,
                "selective_product_yield": 0.5,
                "electrochemical_selectivity": 0.5,
                "faradaic_efficiency": 0.5,
                "energy_efficiency": 0.5,
                "safety_risk": 0.1,
                "constraint_violations": 0.0,
                "score": 0.5,
            }
            info = {
                "transaction_status": "committed",
                "operation_type": action["operation"],
                "instrument": action.get("instrument"),
            }
            agent.update(action, observation, 0.0, info)
            rows.append(
                {
                    "action": action,
                    "observation": observation,
                    "leaderboard_score": 0.5,
                    **info,
                }
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "".join(json.dumps(row) + "\n" for row in rows),
            encoding="utf-8",
        )
        return []

    class Replay:
        def to_dict(self):
            return {"verified": True, "checked_steps": 1, "mismatches": []}

    monkeypatch.setattr(truth_evaluator, "run_agent", fake_run_agent)
    monkeypatch.setattr(blind_evaluator, "run_agent", fake_run_agent)
    monkeypatch.setattr(
        truth_evaluator, "verify_records", lambda records, tolerance: Replay()
    )
    monkeypatch.setattr(
        blind_evaluator, "verify_records", lambda records, tolerance: Replay()
    )


def _prepare_development_shakedown(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    config_name: str,
) -> tuple[dict[str, object], Path, Path, Path, Path, Path]:
    config = json.loads(
        (ROOT / "configs/benchmark" / config_name).read_text(encoding="utf-8")
    )
    config_path = tmp_path / "configs/benchmark" / config_name
    config_path.parent.mkdir(parents=True)
    write_json_atomic(config_path, config)
    design_path = tmp_path / "configs/benchmark/work_ii_formal_design_v0.2.json"
    write_json_atomic(
        design_path,
        json.loads(
            (ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json").read_text(
                encoding="utf-8"
            )
        ),
    )
    participant = _synthetic_terminal_triplet(tmp_path, config)
    raw_output = tmp_path / "evaluator-raw"
    report_path = tmp_path / "evaluation.json"
    markdown_path = tmp_path / "evaluation.md"
    monkeypatch.setattr(evaluator, "ROOT", tmp_path)
    _install_zero_provider_replay_stub(monkeypatch)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "evaluate_work_ii_initial_model_pilot.py",
            "--participant-run",
            str(participant),
            "--config",
            str(config_path),
            "--design",
            str(design_path),
            "--raw-output",
            str(raw_output),
            "--report",
            str(report_path),
            "--markdown",
            str(markdown_path),
            "--execution-mode",
            "development",
        ],
    )
    return config, participant, raw_output, report_path, markdown_path, config_path


def _cell(
    arm: str,
    *,
    best: float,
    improvement: float,
    reliability: list[float | None],
    challenged: list[list[str]],
) -> dict[str, object]:
    return {
        "prior_arm": arm,
        "best_observed_score": best,
        "effective_pre_error": 0.4,
        "effective_final_error": 0.4 - improvement,
        "checkpoint_improvement": improvement,
        "final_prior_reliability": reliability[-1],
        "prior_reliability_trajectory": reliability,
        "suspected_misindexed_fields_trajectory": challenged,
        "law_summary_error": 0.2,
        "blind_recommendation_gain": 0.0,
        "selected_experiment_index": 2,
        "observed_incumbent_experiment_index": 2,
        "provider_usage": {
            "input_token_count": 100,
            "cached_input_token_count": 80,
            "uncached_input_token_count": 20,
            "output_token_count": 10,
            "session_elapsed_s": 30.0,
            "recovered_mcp_tool_failure_count": 1,
            "provider_error_event_count": 0,
        },
    }


def test_markdown_interpretation_tracks_endpoint_and_prediction_directions() -> None:
    report = {
        "denominators": {
            "participant_cell_count": 3,
            "participant_completed_cell_count": 3,
            "participant_complete_experiment_count": 12,
            "participant_scheduled_experiment_count": 12,
            "participant_checkpoint_count": 12,
            "participant_operation_attempt_count": 74,
            "participant_logical_codex_turn_count": 3,
            "truth_completed_query_count": 4,
            "truth_query_count": 4,
            "truth_exact_replay_count": 4,
            "blind_completed_execution_count": 18,
            "blind_scheduled_execution_count": 18,
        },
        "cluster_contrast": {"H3_primary_contrast": -0.01},
        "cells": [
            _cell(
                "opaque", best=0.58, improvement=0.24, reliability=[None] * 4, challenged=[[]] * 4
            ),
            _cell(
                "aligned_nominal",
                best=0.81,
                improvement=-0.01,
                reliability=[0.7, 0.8],
                challenged=[[]] * 2,
            ),
            _cell(
                "misindexed_nominal",
                best=0.83,
                improvement=-0.02,
                reliability=[0.7, 0.4],
                challenged=[["potential_V"], []],
            ),
        ],
        "report_sha256": "abc",
    }
    report["descriptive_interpretation"] = _descriptive_interpretation(report)

    rendered = _render_markdown(report)

    assert "exceeded the opaque endpoint by 0.2500" in rendered
    assert "Held-out prediction worsened by 0.0200" in rendered
    assert "changed from 0.70 to 0.40" in rendered
    assert "challenged potential_V" in rendered
    assert "remained below the opaque" not in rendered
    assert "300 input tokens (240 cached; 60 uncached)" in rendered


def test_reaction_safety_parametric_controls_and_model_distance() -> None:
    experiment = {
        "operations": [
            {
                "operation": "heat",
                "target_temperature_K": 390.0,
                "duration_s": 1800.0,
            },
            {
                "operation": "heat",
                "target_temperature_K": 420.0,
                "duration_s": 3600.0,
            },
        ]
    }
    model = {
        "model": {
            "claim": {
                "reaction_temperature_K": 420.0,
                "reaction_duration_s": 7200.0,
                "temperature_tolerance_K": 15.0,
                "duration_tolerance_s": 300.0,
            }
        }
    }

    controls = _parametric_controls(experiment, "reaction-safety-constrained")

    assert controls == {
        "heat_stages": [
            {"reaction_temperature_K": 390.0, "reaction_duration_s": 1800.0},
            {"reaction_temperature_K": 420.0, "reaction_duration_s": 3600.0},
        ],
        "reaction_duration_s": 5400.0,
        "reaction_temperature_K": 420.0,
    }
    assert _supplied_model_distance(controls, model) == {
        "reaction_temperature_K": 0.0,
        "reaction_duration_s": 1500.0,
    }

    matched_prior_model = {
        "model": {"claim": {"directional_axis": "reaction_temperature_K"}},
        "context_contract": {
            "approximate_reference_region": {
                "reaction_temperature_K": 420.0,
                "reaction_duration_s": 3300.0,
                "temperature_tolerance_K": 10.0,
                "duration_tolerance_s": 600.0,
            }
        },
    }
    assert _supplied_model_distance(controls, matched_prior_model) == {
        "reaction_temperature_K": 0.0,
        "reaction_duration_s": 1500.0,
    }

    electrochemical_matched_prior = {
        "model": {"claim": {"directional_axis": "controlled_potential_V"}},
        "context_contract": {
            "reference_context": {
                "probe_potential_V": 1.18,
                "probe_current_mA": 70.0,
                "controlled_duration_s": 3540.0,
            }
        },
    }
    assert _supplied_model_distance(
        {"potential_V": 1.05, "current_mA": 75.0, "duration_s": 3600.0},
        electrochemical_matched_prior,
    ) == pytest.approx(
        {
            "controlled_potential_V": 0.13,
            "controlled_current_mA": 5.0,
            "controlled_duration_s": 60.0,
        }
    )


def test_electrochemical_parametric_controls_exclude_probe_duration() -> None:
    experiment = {
        "operations": [
            {
                "operation": "set_potential",
                "potential_V": 1.18,
                "current_mA": 70.0,
            },
            {"operation": "electrolyze", "duration_s": 630.0},
            {
                "operation": "set_potential",
                "potential_V": 1.05,
                "current_mA": 90.0,
            },
            {"operation": "electrolyze", "duration_s": 3540.0},
        ]
    }

    assert _parametric_controls(experiment, "electrochemical-conversion") == {
        "potential_V": 1.05,
        "current_mA": 90.0,
        "duration_s": 3540.0,
    }


def test_rationale_score_match_detects_one_based_incumbent_reference() -> None:
    experiments = [
        {"experiment_index": 9, "leaderboard_score": 0.4150832466018063},
        {"experiment_index": 10, "leaderboard_score": 0.41915356995221154},
    ]
    recommendation = {
        "selected_experiment_index": 9,
        "selection_rationale": (
            "Experiment index 9 delivered the highest participant-visible score (0.41915); "
            "the repeat scored 0.41508."
        ),
    }

    assert _rationale_score_match(recommendation, experiments) == 10


def test_operational_failure_can_retain_a_complete_scientific_trajectory() -> None:
    summary = {
        "completed": False,
        "analysis": {
            "complete_experiment_count": 4,
            "right_censored_open_experiment": False,
        },
        "exact_replay": {"verified": True},
        "qualification": {
            "passed": False,
            "failed_checks": ["provider_operational_limits_reconciled"],
        },
    }

    assert _scientific_trajectory_complete(summary) is True

    summary["analysis"]["complete_experiment_count"] = 10
    assert _scientific_trajectory_complete(summary, 10) is True


def test_blind_skip_reason_never_invents_missing_recommendation() -> None:
    summary = {
        "completed": False,
        "analysis": {
            "complete_experiment_count": 10,
            "right_censored_open_experiment": False,
            "final_recommendation": None,
        },
        "exact_replay": {"verified": True},
    }

    assert _blind_skip_reason(summary, 10) == "missing_committed_final_recommendation"
    summary["analysis"]["complete_experiment_count"] = 0
    assert _blind_skip_reason(summary, 10) == "participant_trajectory_incomplete"


def test_registered_temperature_direction_uses_frozen_aligned_claim() -> None:
    config = {
        "prior_arms": {
            "aligned_nominal": {
                "initial_world_model": {
                    "model": {
                        "claim": {
                            "expected_relation": (
                                "Relative to the stated reference region, the lower-temperature "
                                "side should retain safe balanced performance more reliably than "
                                "the higher-temperature side."
                            )
                        }
                    }
                }
            }
        }
    }

    registered = _registered_temperature_direction(config)

    assert registered["preferred_side"] == "lower_temperature"
    assert registered["source"].endswith("claim.expected_relation")


def test_query_subset_direction_conflict_disables_binary_recovery_scoring() -> None:
    contract = _temperature_direction_contract(
        {"preferred_side": "lower_temperature"},
        {"preferred_side": "higher_temperature"},
    )

    assert contract["status"] == "query_subset_conflict"
    assert contract["recovery_scoring_authorized"] is False


@pytest.mark.parametrize("config_name", AP_SEED2_CONFIGS)
def test_ap_seed2_terminal_d1_zero_provider_evaluator_shakedown(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    config_name: str,
) -> None:
    config, _participant, raw_output, report_path, _markdown_path, _config_path = (
        _prepare_development_shakedown(monkeypatch, tmp_path, config_name)
    )

    assert evaluator.main() == 0
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["status"] == "passed"
    assert report["execution_mode"] == "development"
    assert report["release_eligible"] is False
    assert report["execution_context"] == build_execution_envelope(
        prepare_execution_context(tmp_path, mode="development")
    )
    assert report["task_id"] == config["task_id"]
    assert report["world_seed"] == 2
    assert report["denominators"]["participant_cell_count"] == 3
    assert report["denominators"]["participant_scheduled_experiment_count"] == 30
    assert report["denominators"]["participant_complete_experiment_count"] == 30
    assert report["denominators"]["participant_scheduled_checkpoint_count"] == 15
    assert report["denominators"]["participant_checkpoint_count"] == 15
    assert report["denominators"]["truth_query_count"] == 16
    assert report["denominators"]["truth_completed_query_count"] == 16
    assert report["denominators"]["blind_scheduled_execution_count"] == 18
    assert report["denominators"]["blind_completed_execution_count"] == 18
    assert report["denominators"]["evaluator_provider_call_count"] == 0
    assert report["action_layer"]["status"] == "participant_interpretable"
    assert report["action_layer"]["submitted_recommendations_replaced"] is False
    plans = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((raw_output / "blind").glob("*/plan.json"))
    ]
    assert len(plans) == 3
    assert all(plan["candidate_experiment_indices"] == list(range(1, 11)) for plan in plans)
    assert all(plan["evaluator_provider_call_count"] == 0 for plan in plans)


def test_development_evaluator_fails_closed_on_missing_checkpoint(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config, participant, _raw_output, report_path, _markdown_path, _config_path = (
        _prepare_development_shakedown(monkeypatch, tmp_path, AP_SEED2_CONFIGS[0])
    )
    arm = "opaque"
    summary_path = participant / f"seed-{config['world_seed']}" / arm / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["analysis"]["belief_snapshots"].pop(2)
    write_json_atomic(summary_path, summary)
    matrix_path = participant / "matrix_report.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix["seed_reports"][0]["results"][0] = summary
    write_json_atomic(matrix_path, matrix)

    assert evaluator.main() == 1
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["status"] == "failed_retained"
    assert report["release_eligible"] is False
    assert report["denominators"]["participant_checkpoint_count"] == 14
    assert any(
        failure.get("scope") == "participant_contract"
        and failure.get("prior_arm") == arm
        and "five frozen stages" in str(failure.get("error"))
        for failure in report["failures"]
    )


def test_development_evaluator_rejects_matrix_task_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _config, participant, _raw_output, report_path, _markdown_path, _config_path = (
        _prepare_development_shakedown(monkeypatch, tmp_path, AP_SEED2_CONFIGS[0])
    )
    matrix_path = participant / "matrix_report.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix["task_id"] = "electrochemical-conversion"
    write_json_atomic(matrix_path, matrix)

    with pytest.raises(
        ValueError, match="participant matrix task_id does not match campaign config"
    ):
        evaluator.main()
    assert not report_path.exists()


def test_release_mode_requires_the_canonical_release_manifest(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _config, _participant, _raw_output, _report_path, _markdown_path, _config_path = (
        _prepare_development_shakedown(monkeypatch, tmp_path, AP_SEED2_CONFIGS[0])
    )
    sys.argv[-1] = "release"

    with pytest.raises(ValueError, match="requires a release manifest"):
        evaluator.main()


def test_release_evaluator_embeds_the_validated_execution_envelope(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _config, _participant, _raw_output, report_path, _markdown_path, _config_path = (
        _prepare_development_shakedown(monkeypatch, tmp_path, AP_SEED2_CONFIGS[0])
    )
    manifest_path = tmp_path / "release-manifest.json"
    manifest = {
        "manifest_sha256": "a" * 64,
        "freeze_id": "b" * 64,
        "tested_commit": "c" * 40,
        "execution_surface": {"sha256": "d" * 64},
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    expected_envelope = {
        "execution_mode": "release",
        "evidence_status": "release_candidate",
        "release_eligible": True,
        "c2_admission_authorized": True,
        "tested_commit": "c" * 40,
        "freeze_id": "b" * 64,
        "release_manifest_sha256": "a" * 64,
        "execution_surface_sha256": "d" * 64,
    }
    monkeypatch.setattr(
        evaluator,
        "prepare_execution_context",
        lambda *_args, **_kwargs: type(
            "Context",
            (),
            {
                "execution_mode": "release",
                "release_eligible": True,
                "tested_commit": "c" * 40,
            },
        )(),
    )
    monkeypatch.setattr(
        evaluator, "build_execution_envelope", lambda _context: expected_envelope
    )
    sys.argv.extend(["--release-manifest", str(manifest_path)])

    assert evaluator.main() == 0
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["execution_mode"] == "release"
    assert report["release_eligible"] is True
    assert report["execution_context"] == expected_envelope
