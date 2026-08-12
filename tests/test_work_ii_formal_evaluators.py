from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

import chemworld.eval.work_ii_formal_evaluators as orchestration
from chemworld.eval.provenance import canonical_json_sha256, file_sha256, write_json_atomic
from chemworld.eval.work_ii_blind import build_blind_evaluation_plan

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATHS = (
    "configs/benchmark/work_ii_campaign_pilot.json",
    "configs/benchmark/work_ii_crystallization_campaign.json",
    "configs/benchmark/work_ii_distillation_campaign.json",
    "configs/benchmark/work_ii_partition_campaign.json",
    "configs/benchmark/work_ii_safety_campaign.json",
)


def _contract() -> dict[str, Any]:
    return {
        "participant_complete_experiments_per_cell": 4,
        "candidate_experiment_indices": [1, 2, 3, 4],
        "participant_final_recommendations_per_cell": 1,
        "blind_targets_per_cell": [
            "observed_incumbent",
            "participant_final_recommendation",
        ],
        "blind_replicates_per_target": 3,
        "paired_noise_within_replicate": True,
        "participant_feedback_from_blind_evaluator": False,
        "evaluator_provider_calls": 0,
        "evaluator_trajectory_separate_from_participant": True,
        "evaluator_resources_excluded_from_participant_ledger": True,
    }


def _formal_cells() -> list[dict[str, Any]]:
    config_task_ids = {
        path: json.loads((ROOT / path).read_text(encoding="utf-8"))["task_id"]
        for path in CONFIG_PATHS
    }
    locus_configs = {
        "A_E": CONFIG_PATHS,
        "A_P": CONFIG_PATHS[:2],
        "A_S": CONFIG_PATHS[-2:],
    }
    arms = ("opaque", "aligned_nominal", "misindexed_nominal")
    cells: list[dict[str, Any]] = []
    for locus_index, (locus, config_paths) in enumerate(locus_configs.items(), start=1):
        for task_index, config_path in enumerate(config_paths, start=1):
            for world_index in range(1, 6):
                cluster_id = (
                    f"work-ii-public-{locus.lower()}-{task_index:02d}-{world_index:02d}"
                )
                for arm_index, arm in enumerate(arms, start=1):
                    cell: dict[str, Any] = {
                        "cell_id": f"{cluster_id}-arm-{arm_index:02d}",
                        "world_cluster_id": cluster_id,
                        "c2_locus": locus,
                        "task_id": config_task_ids[config_path],
                        "world_seed": locus_index * 100_000 + task_index * 100 + world_index,
                        "prior_arm": arm,
                        "campaign_config_path": config_path,
                        "campaign_config_sha256": file_sha256(ROOT / config_path),
                        "complete_experiment_count": {
                            "A_E": 8,
                            "A_P": 10,
                            "A_S": 12,
                        }[locus],
                        "participant_final_recommendation_count": 1,
                        "blind_validation_target_count": 2,
                        "blind_replicates_per_target": 3,
                        "blind_validation_execution_count": 6,
                    }
                    cell["cell_key_sha256"] = canonical_json_sha256(cell)
                    cells.append(cell)
    return cells


def _summary(cell: dict[str, Any], manifest_sha256: str) -> dict[str, Any]:
    recommendation = {
        "selected_experiment_index": 2,
        "selection_rationale": "frozen participant choice",
    }
    return {
        "formal_result": True,
        "formal_preflight_sha256": manifest_sha256,
        "formal_cell": cell,
        "completed": True,
        "qualification": {"passed": True},
        "exact_replay": {"verified": True},
        "analysis": {
            "experiments": [
                {
                    "experiment_index": index,
                    "leaderboard_score": 0.8 if index == 2 else 0.1,
                    "operations": [
                        {"operation": "wait", "duration_s": index},
                        {"operation": "measure", "instrument": "final_assay"},
                    ],
                }
                for index in range(1, int(cell["complete_experiment_count"]) + 1)
            ],
            "final_recommendation": recommendation,
            "final_recommendation_sha256": canonical_json_sha256(recommendation),
            "observed_incumbent_experiment_index": 2,
        },
    }


def _terminal_receipts(
    execution_root: Path,
    cells: list[dict[str, Any]],
    manifest_sha256: str,
) -> dict[str, dict[str, Any]]:
    completed_cell = cells[0]
    session_root = execution_root / "attempts" / completed_cell["cell_key_sha256"]
    session_root.mkdir(parents=True)
    summary = _summary(completed_cell, manifest_sha256)
    plan = build_blind_evaluation_plan(
        completed_cell,
        summary,
        orchestration.effective_blind_evaluator_contract(
            completed_cell,
            _contract(),
        ),
    )
    plan_path = session_root / "blind_evaluation_plan.json"
    write_json_atomic(plan_path, plan)
    summary["blind_evaluation_plan"] = {
        "sha256": file_sha256(plan_path),
        "plan_sha256": plan["plan_sha256"],
    }
    summary_path = session_root / "summary.json"
    write_json_atomic(summary_path, summary)

    receipts: dict[str, dict[str, Any]] = {}
    for index, cell in enumerate(cells):
        state = "completed" if index == 0 else (
            "right_censored" if index % 2 else "failed"
        )
        reason = {
            "completed": "scientific_completed_qualified_campaign",
            "right_censored": "method_right_censored_failure_after_accepted_operation",
            "failed": "method_failed_unscorable_before_first_operation",
        }[state]
        result: dict[str, Any] = {"completed": state == "completed"}
        if state == "completed":
            result.update(
                {
                    "summary": {
                        "path": summary_path.relative_to(execution_root).as_posix(),
                        "sha256": file_sha256(summary_path),
                    },
                    "blind_evaluation_plan": {
                        "path": plan_path.relative_to(execution_root).as_posix(),
                        "sha256": file_sha256(plan_path),
                    },
                }
            )
        receipt: dict[str, Any] = {
            "cell_key_sha256": cell["cell_key_sha256"],
            "cell": cell,
            "state": state,
            "reason_code": reason,
            "result": result,
            "result_sha256": canonical_json_sha256(result),
        }
        receipt["receipt_sha256"] = canonical_json_sha256(receipt)
        receipts[cell["cell_key_sha256"]] = receipt
    return receipts


def _fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cells = _formal_cells()
    manifest: dict[str, Any] = {
        "formal_execution_allowed": True,
        "preflight_sha256": "f" * 64,
        "blind_evaluator_contract": _contract(),
        "cells": cells,
    }
    execution_root = tmp_path / "participant"
    execution_root.mkdir()
    write_json_atomic(execution_root / "execution_manifest.json", manifest)
    receipts = _terminal_receipts(execution_root, cells, manifest["preflight_sha256"])

    class FakeStore:
        def __init__(self, root: Path, supplied_manifest: dict[str, Any]) -> None:
            assert root == execution_root / "store"
            assert supplied_manifest == manifest

        def audit(self) -> dict[str, Any]:
            return {"complete": True, "audit_sha256": "a" * 64}

        def load_terminal(self, key: str) -> dict[str, Any]:
            return deepcopy(receipts[key])

    monkeypatch.setattr(orchestration, "validate_formal_preflight", lambda _: [])
    monkeypatch.setattr(orchestration, "validate_formal_bindings", lambda *_: [])
    monkeypatch.setattr(orchestration, "WorkIIFormalCellStore", FakeStore)
    monkeypatch.setattr(
        orchestration,
        "build_formal_evaluator_source_binding",
        lambda *_, **__: {
            "source_commit": "c" * 40,
            "material_roots": ["test"],
            "material_tree_sha256": "d" * 64,
            "source_binding_sha256": "e" * 64,
        },
    )
    return manifest, execution_root, receipts


def _fake_truth_executor(counter: dict[str, int]):
    def execute(plan, config, output_root):
        del config
        counter["truth"] += 1
        output_root.mkdir(parents=True)
        write_json_atomic(output_root / "plan.json", plan)
        receipts = []
        truth = {}
        for query in plan["queries"]:
            query_root = output_root / "queries" / query["query_id"]
            query_root.mkdir(parents=True)
            trajectory = query_root / "trajectory.jsonl"
            trajectory.write_text("{}\n", encoding="utf-8")
            values = dict.fromkeys(query["metric_ids"], 0.5)
            truth[query["query_id"]] = values
            receipts.append(
                {
                    "execution_index": query["execution_index"],
                    "execution_id": query["execution_id"],
                    "query_id": query["query_id"],
                    "metric_ids": query["metric_ids"],
                    "action_plan_sha256": query["action_plan_sha256"],
                    "observation_coordinate_sha256": query[
                        "observation_coordinate_sha256"
                    ],
                    "evaluator_provider_call_count": 0,
                    "participant_operation_denominator_impact": 0,
                    "participant_feedback_emitted": False,
                    "status": "completed",
                    "truth": values,
                    "operation_attempt_count": 1,
                    "trajectory": {
                        "path": trajectory.relative_to(output_root).as_posix(),
                        "sha256": file_sha256(trajectory),
                    },
                    "exact_replay": {"verified": True},
                }
            )
        report = {
            "schema_version": "chemworld-work-ii-evaluator-truth-report-0.1",
            "formal_result": True,
            "formal_preflight_sha256": plan["formal_preflight_sha256"],
            "plan_sha256": plan["plan_sha256"],
            "world_cluster_id": plan["world_cluster_id"],
            "task_id": plan["task_id"],
            "world_seed": plan["world_seed"],
            "status": "completed",
            "truth_query_count": len(receipts),
            "completed_truth_query_count": len(receipts),
            "failed_truth_query_count": 0,
            "truth_query_metric_count": sum(len(item["metric_ids"]) for item in receipts),
            "completed_truth_query_metric_count": sum(
                len(item["metric_ids"]) for item in receipts
            ),
            "evaluator_provider_call_count": 0,
            "participant_operation_denominator_impact": 0,
            "participant_feedback_emitted": False,
            "truth": truth,
            "receipts": receipts,
        }
        report["report_sha256"] = canonical_json_sha256(report)
        write_json_atomic(output_root / "report.json", report)
        return report

    return execute


def _fake_blind_executor(counter: dict[str, int]):
    def execute(plan, config, output_root):
        del config
        counter["blind"] += 1
        output_root.mkdir(parents=True)
        write_json_atomic(output_root / "plan.json", plan)
        receipts = []
        for execution in plan["executions"]:
            execution_root = (
                output_root
                / "executions"
                / orchestration.blind_execution_directory_name(execution)
            )
            execution_root.mkdir(parents=True)
            trajectory = execution_root / "trajectory.jsonl"
            trajectory.write_text("{}\n", encoding="utf-8")
            receipt = {
                "schema_version": "chemworld-work-ii-blind-evaluation-report-0.1",
                "execution_id": execution["execution_id"],
                "target": execution["target"],
                "replicate_index": execution["replicate_index"],
                "paired_noise_id_sha256": execution["paired_noise_id_sha256"],
                "action_plan_sha256": execution["action_plan_sha256"],
                "evaluator_provider_call_count": 0,
                "participant_operation_denominator_impact": 0,
                "participant_feedback_emitted": False,
                "status": "completed",
                "leaderboard_score": 0.75,
                "operation_attempt_count": 1,
                "trajectory": {
                    "path": trajectory.relative_to(output_root).as_posix(),
                    "sha256": file_sha256(trajectory),
                },
                "exact_replay": {"verified": True},
            }
            receipt["receipt_sha256"] = canonical_json_sha256(receipt)
            write_json_atomic(execution_root / "receipt.json", receipt)
            receipts.append(receipt)
        report = {
            "schema_version": "chemworld-work-ii-blind-evaluation-report-0.1",
            "formal_result": True,
            "cell_id": plan["cell_id"],
            "cell_key_sha256": plan["cell_key_sha256"],
            "plan_sha256": plan["plan_sha256"],
            "status": "completed",
            "scheduled_execution_count": 6,
            "completed_execution_count": 6,
            "failed_execution_count": 0,
            "evaluator_provider_call_count": 0,
            "participant_operation_denominator_impact": 0,
            "participant_feedback_emitted": False,
            "target_score_means": {
                "observed_incumbent": 0.75,
                "participant_final_recommendation": 0.75,
            },
            "recommendation_gain_over_incumbent": 0.0,
            "receipt_sha256": [receipt["receipt_sha256"] for receipt in receipts],
        }
        report["report_sha256"] = canonical_json_sha256(report)
        write_json_atomic(output_root / "report.json", report)
        return report

    return execute


def test_c2_roster_requires_only_canonical_locus_and_exact_135_cells() -> None:
    cells = _formal_cells()
    clusters = orchestration._cluster_schedule(cells)
    assert len(cells) == 135
    assert len(clusters) == 45

    missing_locus = deepcopy(cells)
    missing_locus[0].pop("c2_locus")
    with pytest.raises(ValueError, match="c2_locus must be exactly"):
        orchestration._cluster_schedule(missing_locus)

    alias_only = deepcopy(cells)
    alias_only[0]["locus"] = alias_only[0].pop("c2_locus")
    with pytest.raises(ValueError, match="c2_locus must be exactly"):
        orchestration._cluster_schedule(alias_only)

    missing_cell = cells[:-1]
    with pytest.raises(ValueError, match="formal arm triplet is incomplete"):
        orchestration._cluster_schedule(missing_cell)


def test_formal_evaluator_orchestration_retains_exact_denominators_and_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest, execution_root, _ = _fixture(tmp_path, monkeypatch)
    calls = {"truth": 0, "blind": 0}
    monkeypatch.setattr(orchestration, "execute_evaluator_truth_plan", _fake_truth_executor(calls))
    monkeypatch.setattr(orchestration, "execute_blind_evaluation_plan", _fake_blind_executor(calls))

    output_root = tmp_path / "evaluators"
    summary = orchestration.execute_formal_evaluators(
        ROOT,
        manifest,
        execution_root,
        output_root,
    )

    assert calls == {"truth": 45, "blind": 1}
    assert summary["status"] == "terminal_with_retained_failures"
    assert summary["provider_call_count"] == 0
    denominators = summary["denominators"]
    assert denominators["participant_session_count"] == 135
    assert denominators["participant_terminal_session_count"] == 135
    assert denominators["participant_state_counts"] == {
        "completed": 1,
        "right_censored": 67,
        "failed": 67,
    }
    assert {
        locus: (
            row["observed_task_count"],
            row["observed_cluster_count"],
            row["observed_cell_count"],
        )
        for locus, row in denominators["c2_roster"].items()
    } == {
        "A_E": (5, 25, 75),
        "A_P": (2, 10, 30),
        "A_S": (2, 10, 30),
    }
    assert denominators["truth_cluster_count"] == 45
    assert denominators["truth_scheduled_execution_count"] == 180
    assert denominators["truth_completed_execution_count"] == 180
    assert denominators["truth_failed_execution_count"] == 0
    assert denominators["truth_scheduled_query_metric_count"] == 600
    assert denominators["truth_completed_query_metric_count"] == 600
    assert denominators["blind_session_count"] == 135
    assert denominators["blind_evaluable_session_count"] == 1
    assert denominators["blind_scheduled_target_count"] == 270
    assert denominators["blind_scheduled_execution_count"] == 810
    assert denominators["blind_launched_execution_count"] == 6
    assert denominators["blind_completed_execution_count"] == 6
    assert denominators["blind_failed_or_unstarted_execution_count"] == 804
    assert summary["failure_count"] == 134
    assert {failure["stage"] for failure in summary["failures"]} == {
        "participant_session"
    }
    assert len(list((output_root / "truth").glob("*/report.json"))) == 45
    assert len(list((output_root / "blind").glob("*/report.json"))) == 1
    assert summary["summary_sha256"] == canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )


def test_resume_reuses_only_fully_validated_evaluator_units(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest, execution_root, _ = _fixture(tmp_path, monkeypatch)
    calls = {"truth": 0, "blind": 0}
    monkeypatch.setattr(orchestration, "execute_evaluator_truth_plan", _fake_truth_executor(calls))
    monkeypatch.setattr(orchestration, "execute_blind_evaluation_plan", _fake_blind_executor(calls))
    output_root = tmp_path / "evaluators"
    orchestration.execute_formal_evaluators(ROOT, manifest, execution_root, output_root)

    resumed = orchestration.execute_formal_evaluators(
        ROOT,
        manifest,
        execution_root,
        output_root,
        resume=True,
    )

    assert calls == {"truth": 45, "blind": 1}
    assert resumed["resume_audit"] == {
        "reused_truth_cluster_count": 45,
        "new_truth_cluster_count": 0,
        "reused_blind_session_count": 1,
        "new_blind_session_count": 0,
    }


def test_resume_fails_closed_before_execution_when_existing_trajectory_changed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest, execution_root, _ = _fixture(tmp_path, monkeypatch)
    calls = {"truth": 0, "blind": 0}
    monkeypatch.setattr(orchestration, "execute_evaluator_truth_plan", _fake_truth_executor(calls))
    monkeypatch.setattr(orchestration, "execute_blind_evaluation_plan", _fake_blind_executor(calls))
    output_root = tmp_path / "evaluators"
    orchestration.execute_formal_evaluators(ROOT, manifest, execution_root, output_root)
    truth_trajectory = next((output_root / "truth").glob("*/queries/*/trajectory.jsonl"))
    truth_trajectory.write_text('{"tampered": true}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="trajectory is missing or changed"):
        orchestration.execute_formal_evaluators(
            ROOT,
            manifest,
            execution_root,
            output_root,
            resume=True,
        )

    assert calls == {"truth": 45, "blind": 1}
