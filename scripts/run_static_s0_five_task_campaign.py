"""Plan or execute the qualified five-task, five-world S0 development campaign."""

from __future__ import annotations

import argparse
import copy
import json
import statistics
import subprocess
import sys
import threading
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import (
    canonical_json_sha256,
    git_source_commit,
    git_worktree_dirty,
    write_json_atomic,
)
from chemworld.eval.static_optimization_baselines import run_baseline_cell
from chemworld.eval.static_optimization_postrun import (
    replay_static_optimization_receipt,
    replay_static_optimization_validation,
)
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)
from chemworld.tasks import get_task

try:
    from scripts.qualify_static_s0_five_tasks import (
        _participant_protocol,
        _task_protocol,
    )
except ModuleNotFoundError:
    from qualify_static_s0_five_tasks import _participant_protocol, _task_protocol

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "configs/benchmark/static_s0_five_task_campaign_20x5_v0.2_dev.json"
DEFAULT_OUTPUT = ROOT / "runs/dev/static-s0-five-task-campaign-20x5-v0.2"


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return payload


def _repo_path(value: object) -> Path:
    path = (ROOT / str(value)).resolve()
    path.relative_to(ROOT)
    return path


def _seeded_protocol(protocol: Mapping[str, Any], world_seed: int) -> dict[str, Any]:
    seeded = copy.deepcopy(dict(protocol))
    seeded["world_policy"]["world_seed"] = int(world_seed)
    return seeded


def _full_protocol(
    plan: Mapping[str, Any],
    qualification_plan: Mapping[str, Any],
    task_id: str,
    *,
    kind: str,
) -> dict[str, Any]:
    protocol = _task_protocol(qualification_plan, task_id)
    protocol.pop("development_seed_policy", None)
    protocol["schema_version"] = (
        "chemworld-static-scientific-optimization-protocol-five-task-0.1-s0-dev"
    )
    protocol["protocol_id"] = f"{plan['campaign_id']}--{kind}--{task_id}"
    protocol["freeze_id"] = f"{plan['campaign_id']}--{kind}--{task_id}--20x5"
    protocol["status"] = "postqualification_multiseed_development"
    protocol["world_policy"]["evaluation_world_seeds"] = list(plan["world_seeds"])
    protocol["algorithm_seeds"] = list(plan["algorithm_seeds"])
    protocol["candidate_order_seed"] = 0
    protocol["scientific_campaign_budget"] = {
        "exploration_experiments": int(plan["campaign"]["exploration_experiments"]),
        "horizon_visible": bool(plan["campaign"]["horizon_visible"]),
        "final_synthesis_after_exploration": kind == "participant",
    }
    protocol["horizon"] = int(plan["campaign"]["exploration_experiments"])
    protocol["validation_budget"] = {
        "incumbent_replicates": int(plan["campaign"]["incumbent_validation_replicates"]),
        "recommendation_replicates": int(plan["campaign"]["recommendation_validation_replicates"]),
        "independent_observation_seeds": True,
        "paired_observation_seeds_across_targets": True,
        "feedback_returned_to_agent": False,
    }
    if kind == "participant":
        participant = plan["participant"]
        protocol["method_config_path"] = participant["method_config_path"]
        protocol["method_ids"] = [participant["method_id"]]
        protocol["final_synthesis"] = {
            "enabled": True,
            "calls": 1,
            "executes_experiment": False,
            "allow_tested_recommendation": True,
            "allow_interpolated_recommendation": True,
            "allow_extrapolated_recommendation_within_bounds": True,
            "requires_structured_world_claims": False,
            "validation_feedback_returned_to_agent": False,
            "list_item_limit": 16,
            "list_item_limit_visible_to_model": True,
        }
        protocol["reward_contract"]["final_selection"] = "committed_model_final_recommendation"
    elif kind == "baseline":
        protocol["final_synthesis"] = {
            "enabled": False,
            "calls": 0,
            "mode": "deterministic_best_observed_selection",
            "executes_experiment": False,
            "validation_feedback_returned_to_agent": False,
        }
        protocol["reward_contract"]["final_selection"] = "best_observed_completed_experiment"
    else:
        raise ValueError(f"unsupported campaign kind: {kind}")
    noise_namespace_base = str(
        plan.get("observation_noise_namespace_base", plan["campaign_id"])
    )
    protocol["observation_noise_namespace"] = f"{noise_namespace_base}--{task_id}"
    validate_static_optimization_protocol(protocol)
    return protocol


def _validate_plan(
    plan: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, dict[str, dict[str, Any]]]]:
    if plan.get("status") != "postqualification_multiseed_development_pending_execution":
        raise ValueError("five-task campaign is not an executable frozen candidate")
    if plan.get("world_seeds") != [0, 1, 2, 3, 4]:
        raise ValueError("five-task campaign world seeds must be exactly 0 through 4")
    if plan.get("development_world_seed") != 0:
        raise ValueError("five-task campaign development world seed must be 0")
    if plan.get("held_out_world_seeds") != [1, 2, 3, 4]:
        raise ValueError("five-task campaign held-out world seeds must be exactly 1 through 4")
    if plan.get("execution_world_seeds") != [1, 2, 3, 4]:
        raise ValueError("five-task campaign must execute only held-out world seeds 1 through 4")
    if (
        plan.get("execution_contract", {}).get("import_qualified_development_seed0")
        is not True
    ):
        raise ValueError("five-task campaign must import the qualified development seed 0")
    if plan.get("algorithm_seeds") != [0]:
        raise ValueError("five-task campaign must use the paired algorithm seed 0")
    task_ids = list(plan["task_ids"])
    if len(task_ids) != 5 or len(set(task_ids)) != 5:
        raise ValueError("five-task campaign must contain exactly five distinct tasks")
    qualification_path = _repo_path(plan["qualification_plan_path"])
    qualification_plan = _load_object(qualification_path)
    if canonical_json_sha256(qualification_plan) != plan["qualification_plan_sha256"]:
        raise ValueError("qualification plan hash mismatch")
    if qualification_plan["task_ids"] != task_ids:
        raise ValueError("campaign task order differs from its qualification plan")
    if list(plan["baseline_algorithm_ids"]) != list(qualification_plan["algorithms"]):
        raise ValueError("campaign baseline suite differs from its qualification suite")
    methods = _load_object(_repo_path(plan["participant"]["method_config_path"]))
    if list(methods["methods"]) != [plan["participant"]["method_id"]]:
        raise ValueError("participant method binding is ambiguous")
    protocols = {
        kind: {
            task_id: _full_protocol(
                plan,
                qualification_plan,
                task_id,
                kind=kind,
            )
            for task_id in task_ids
        }
        for kind in ("baseline", "participant")
    }
    return qualification_plan, protocols


def _verify_qualification(
    plan: Mapping[str, Any],
    report_path: Path,
    *,
    source_commit: str,
) -> dict[str, Any]:
    report = _load_object(report_path)
    if report.get("qualified") is not True or report.get("multi_seed_release_allowed") is not True:
        raise RuntimeError("single-seed qualification did not release multi-seed execution")
    if report.get("source_tree_dirty") is not False:
        raise RuntimeError("qualification report is not bound to a clean source tree")
    qualified_source_commit = str(report.get("source_commit", ""))
    source_compatibility: dict[str, Any] = {
        "mode": "exact_source_commit",
        "qualified_source_commit": qualified_source_commit,
        "campaign_source_commit": source_commit,
        "changed_paths": [],
    }
    if qualified_source_commit != source_commit:
        compatibility = plan.get("qualification_source_compatibility")
        if not isinstance(compatibility, Mapping):
            raise RuntimeError("qualification report source commit differs from campaign source")
        if compatibility.get("qualified_source_commit") != qualified_source_commit:
            raise RuntimeError("qualification source-compatibility commit mismatch")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", qualified_source_commit, source_commit],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if ancestor.returncode != 0:
            raise RuntimeError("qualification source is not an ancestor of campaign source")
        changed = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                f"{qualified_source_commit}..{source_commit}",
                "--",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        changed_paths = sorted(
            line.strip().replace("\\", "/")
            for line in changed.stdout.splitlines()
            if line.strip()
        )
        allowed_paths = sorted(
            str(path).replace("\\", "/")
            for path in compatibility.get("allowed_changed_paths", [])
        )
        disallowed = sorted(set(changed_paths) - set(allowed_paths))
        if disallowed:
            raise RuntimeError(
                "qualification-sensitive source changed after seed-0 release: "
                + ", ".join(disallowed)
            )
        source_compatibility = {
            "mode": "ancestor_with_exact_changed_path_allowlist",
            "qualified_source_commit": qualified_source_commit,
            "campaign_source_commit": source_commit,
            "changed_paths": changed_paths,
            "allowed_changed_paths": allowed_paths,
            "no_disallowed_paths_changed": True,
        }
    if report.get("qualification_plan_sha256") != plan["qualification_plan_sha256"]:
        raise RuntimeError("qualification report plan hash mismatch")
    if report.get("task_ids") != plan["task_ids"]:
        raise RuntimeError("qualification report task scope mismatch")
    verified = copy.deepcopy(report)
    verified["_campaign_source_compatibility"] = source_compatibility
    return verified


def _summary(values: list[float]) -> dict[str, float | int | None]:
    return {
        "count": len(values),
        "mean": statistics.fmean(values) if values else None,
        "sample_standard_deviation": (statistics.stdev(values) if len(values) > 1 else None),
        "minimum": min(values) if values else None,
        "maximum": max(values) if values else None,
    }


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _run_logged(command: list[str], output: Path, log_name: str) -> None:
    output.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    write_json_atomic(
        output / log_name,
        {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        },
    )
    if result.returncode != 0:
        raise RuntimeError(f"campaign subprocess failed ({result.returncode}): {' '.join(command)}")


def _run_baseline_cell(
    *,
    plan: Mapping[str, Any],
    base_protocol: Mapping[str, Any],
    task_id: str,
    world_seed: int,
    algorithm_id: str,
    output: Path,
) -> dict[str, Any]:
    protocol = _seeded_protocol(base_protocol, world_seed)
    receipt_path = (
        output / "baselines" / task_id / f"world-{world_seed:02d}" / f"{algorithm_id}_seed0.json"
    )
    protocol_hash = canonical_json_sha256(protocol)
    if receipt_path.is_file():
        receipt = _load_object(receipt_path)
        if receipt.get("protocol_sha256") != protocol_hash:
            raise RuntimeError(f"stale baseline receipt: {receipt_path}")
        reused = True
    else:
        receipt = run_baseline_cell(
            protocol=protocol,
            algorithm_id=algorithm_id,
            algorithm_seed=0,
        )
        write_json_atomic(receipt_path, receipt)
        reused = False
    exploration = replay_static_optimization_receipt(receipt, protocol)
    validation = replay_static_optimization_validation(receipt)
    if not exploration["verified"] or not validation["verified"]:
        raise RuntimeError(f"baseline exact replay failed: {receipt_path}")
    return {
        "kind": "baseline",
        "task_id": task_id,
        "world_seed": world_seed,
        "method_id": algorithm_id,
        "primary_score": float(receipt["primary_score"]),
        "best_exploration_score": max(float(value) for value in receipt["scores"]),
        "completed_experiment_count": int(receipt["completed_experiment_count"]),
        "validation_experiment_count": sum(
            len(receipt["validation"][target]["replicates"])
            for target in ("incumbent", "recommendation")
        ),
        "exact_replay": True,
        "reused": reused,
        "receipt_sha256": canonical_json_sha256(receipt),
        "receipt_path": str(receipt_path),
    }


def _participant_complete(
    output: Path,
    *,
    protocol_hash: str,
    method_hash: str,
    world_seed: int,
    provider: str,
) -> bool:
    report_path = output / "report.json"
    if not report_path.is_file():
        return False
    report = _load_object(report_path)
    return bool(
        report.get("protocol_sha256") == protocol_hash
        and report.get("method_config_sha256") == method_hash
        and report.get("completed_cell_count") == report.get("cell_count") == 1
        and report.get("method_failure_cell_count") == 0
        and report.get("provider_mode") == provider
        and report.get("completed_experiment_count") == report.get("planned_experiment_count") == 20
        and int(report.get("execution_seed", -1)) == world_seed
    )


def _run_participant_cell(
    *,
    plan: Mapping[str, Any],
    protocol_path: Path,
    base_protocol: Mapping[str, Any],
    method_path: Path,
    method_hash: str,
    task_id: str,
    world_seed: int,
    output: Path,
    provider: str,
) -> dict[str, Any]:
    seeded = _seeded_protocol(base_protocol, world_seed)
    protocol_hash = canonical_json_sha256(seeded)
    cell_output = output / "participants" / task_id / f"world-{world_seed:02d}"
    reused = _participant_complete(
        cell_output,
        protocol_hash=protocol_hash,
        method_hash=method_hash,
        world_seed=world_seed,
        provider=provider,
    )
    if not reused:
        if (cell_output / "report.json").exists() or (cell_output / "receipts").exists():
            raise RuntimeError(
                "incomplete participant output exists; use the explicit continuation "
                f"workflow before retrying: {cell_output}"
            )
        command = [
            sys.executable,
            "scripts/run_static_optimization_s0.py",
            "--protocol",
            str(protocol_path),
            "--llm-methods",
            str(method_path),
            "--output",
            str(cell_output),
            "--provider",
            provider,
        ]
        if provider != "mock":
            command.extend(
                [
                    "--allow-external-provider",
                    "--confirm-protocol-sha256",
                    protocol_hash,
                    "--confirm-method-sha256",
                    method_hash,
                ]
            )
        command.extend(
            [
                "--world-seed",
                str(world_seed),
                "--task",
                task_id,
                "--method-id",
                str(plan["participant"]["method_id"]),
            ]
        )
        _run_logged(command, cell_output, "execution_run_log.json")
    audit_command = [
        sys.executable,
        "scripts/audit_static_optimization_s0.py",
        "--protocol",
        str(protocol_path),
        "--run-root",
        str(cell_output),
        "--output",
        str(cell_output / "postrun_audit.json"),
        "--world-seed",
        str(world_seed),
    ]
    _run_logged(audit_command, cell_output, "execution_audit_log.json")
    report = _load_object(cell_output / "report.json")
    audit = _load_object(cell_output / "postrun_audit.json")
    if audit.get("replay", {}).get("all_verified") is not True:
        raise RuntimeError(f"participant exact replay failed: {cell_output}")
    cell = report["cells"][0]
    validation = cell["validation"]
    return {
        "kind": "participant",
        "task_id": task_id,
        "world_seed": world_seed,
        "method_id": plan["participant"]["method_id"],
        "primary_score": float(validation["primary_validated_recommendation_score_mean"]),
        "validated_incumbent_score": float(validation["validated_incumbent_score_mean"]),
        "recommendation_gain_over_incumbent": float(
            validation["recommendation_gain_over_incumbent_mean"]
        ),
        "best_exploration_score": max(float(value) for value in cell["scores"]),
        "completed_experiment_count": int(cell["completed_experiment_count"]),
        "validation_experiment_count": int(cell["completed_validation_experiment_count"]),
        "provider_call_count": int(report["provider_call_count"]),
        "exact_replay": True,
        "postrun_audit_passed": True,
        "reused": reused,
        "report_sha256": canonical_json_sha256(report),
        "report_path": str(cell_output / "report.json"),
    }


def _qualified_development_seed0_results(
    plan: Mapping[str, Any],
    *,
    qualification_plan: Mapping[str, Any],
    qualification_report: Mapping[str, Any],
    selection: str,
) -> list[dict[str, Any]]:
    artifact_root = _repo_path(plan["qualification_artifact_root"])
    results: list[dict[str, Any]] = []
    for task_id in plan["task_ids"]:
        task_report = qualification_report["tasks"][task_id]
        if task_report.get("qualified") is not True:
            raise RuntimeError(f"qualification seed 0 is not qualified for {task_id}")
        if selection in {"baselines", "all"}:
            protocol = _task_protocol(qualification_plan, task_id)
            if canonical_json_sha256(protocol) != task_report["protocol_sha256"]:
                raise RuntimeError(f"qualification baseline protocol drift: {task_id}")
            exploration_replays = {
                str(replay["method_id"]): replay
                for replay in task_report["exploration_replays"]
            }
            validation_replays = {
                str(replay["cell_id"]).split(":", maxsplit=1)[0]: replay
                for replay in task_report["validation_replays"]
            }
            for algorithm_id in plan["baseline_algorithm_ids"]:
                method_id = f"{algorithm_id}_seed0"
                receipt_path = (
                    artifact_root
                    / task_id
                    / "receipts"
                    / f"{algorithm_id}_seed0.json"
                )
                receipt = _load_object(receipt_path)
                if (
                    canonical_json_sha256(receipt)
                    != task_report["receipt_sha256"][method_id]
                ):
                    raise RuntimeError(
                        f"qualification baseline receipt drift: {receipt_path}"
                    )
                exploration = replay_static_optimization_receipt(receipt, protocol)
                validation = replay_static_optimization_validation(receipt)
                if (
                    not exploration["verified"]
                    or not validation["verified"]
                    or exploration_replays[method_id].get("verified") is not True
                    or validation_replays[method_id].get("verified") is not True
                ):
                    raise RuntimeError(
                        f"qualification baseline replay failed: {receipt_path}"
                    )
                results.append(
                    {
                        "kind": "baseline",
                        "task_id": task_id,
                        "world_seed": 0,
                        "method_id": algorithm_id,
                        "primary_score": float(receipt["primary_score"]),
                        "best_exploration_score": max(
                            float(value) for value in receipt["scores"]
                        ),
                        "completed_experiment_count": int(
                            receipt["completed_experiment_count"]
                        ),
                        "validation_experiment_count": sum(
                            len(receipt["validation"][target]["replicates"])
                            for target in ("incumbent", "recommendation")
                        ),
                        "exact_replay": True,
                        "reused": True,
                        "seed_role": "development_qualification",
                        "provenance": "qualified_seed0_import",
                        "receipt_sha256": canonical_json_sha256(receipt),
                        "receipt_path": str(receipt_path),
                    }
                )
        if selection in {"participants", "all"}:
            participant = task_report["participant"]
            if participant.get("qualified") is not True or not all(
                value is True for value in participant["checks"].values()
            ):
                raise RuntimeError(
                    f"qualification participant checks failed for {task_id}"
                )
            report_path = Path(str(participant["report_path"])).resolve()
            report_path.relative_to(artifact_root)
            report = _load_object(report_path)
            if canonical_json_sha256(report) != participant["report_sha256"]:
                raise RuntimeError(
                    f"qualification participant report drift: {report_path}"
                )
            protocol = _participant_protocol(qualification_plan, task_id)
            cell = report["cells"][0]
            exploration = replay_static_optimization_receipt(cell, protocol)
            validation_replay = replay_static_optimization_validation(cell)
            if not exploration["verified"] or not validation_replay["verified"]:
                raise RuntimeError(
                    f"qualification participant replay failed: {report_path}"
                )
            validation = cell["validation"]
            results.append(
                {
                    "kind": "participant",
                    "task_id": task_id,
                    "world_seed": 0,
                    "method_id": plan["participant"]["method_id"],
                    "primary_score": float(
                        validation["primary_validated_recommendation_score_mean"]
                    ),
                    "validated_incumbent_score": float(
                        validation["validated_incumbent_score_mean"]
                    ),
                    "recommendation_gain_over_incumbent": float(
                        validation["recommendation_gain_over_incumbent_mean"]
                    ),
                    "best_exploration_score": max(
                        float(value) for value in cell["scores"]
                    ),
                    "completed_experiment_count": int(
                        cell["completed_experiment_count"]
                    ),
                    "validation_experiment_count": int(
                        cell["completed_validation_experiment_count"]
                    ),
                    "provider_call_count": int(report["provider_call_count"]),
                    "exact_replay": True,
                    "postrun_audit_passed": True,
                    "reused": True,
                    "seed_role": "development_qualification",
                    "provenance": "qualified_seed0_import",
                    "report_sha256": canonical_json_sha256(report),
                    "report_path": str(report_path),
                }
            )
    return results


def _build_report(
    plan: Mapping[str, Any],
    *,
    qualification_report: Mapping[str, Any],
    source_commit: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    task_reports: dict[str, Any] = {}
    for task_id in plan["task_ids"]:
        task = get_task(task_id)
        task_results = [item for item in results if item["task_id"] == task_id]
        methods: dict[str, Any] = {}
        for method_id in sorted({str(item["method_id"]) for item in task_results}):
            rows = [item for item in task_results if item["method_id"] == method_id]
            rows.sort(key=lambda item: item["world_seed"])
            held_out_rows = [
                item
                for item in rows
                if item["world_seed"] in plan["held_out_world_seeds"]
            ]
            development_rows = [
                item
                for item in rows
                if item["world_seed"] == plan["development_world_seed"]
            ]
            methods[method_id] = {
                "kind": rows[0]["kind"],
                "world_seeds": [item["world_seed"] for item in rows],
                "blind_validated_score": _summary([float(item["primary_score"]) for item in rows]),
                "held_out_blind_validated_score": _summary(
                    [float(item["primary_score"]) for item in held_out_rows]
                ),
                "development_seed0_blind_validated_score": _summary(
                    [float(item["primary_score"]) for item in development_rows]
                ),
                "best_exploration_score": _summary(
                    [float(item["best_exploration_score"]) for item in rows]
                ),
                "recommendation_gain_over_incumbent": _summary(
                    [
                        float(item["recommendation_gain_over_incumbent"])
                        for item in rows
                        if "recommendation_gain_over_incumbent" in item
                    ]
                ),
                "all_exact_replay": all(item["exact_replay"] for item in rows),
                "rows": rows,
            }
        method_means = [
            float(method["blind_validated_score"]["mean"]) for method in methods.values()
        ]
        task_reports[task_id] = {
            "task_contract_hash": task.contract_hash,
            "threshold": task.threshold,
            "methods": methods,
            "threshold_reached_by_any_method_mean": (max(method_means) >= task.threshold),
            "participant_held_out_mean_reaches_threshold": (
                float(
                    methods[str(plan["participant"]["method_id"])][
                        "held_out_blind_validated_score"
                    ]["mean"]
                )
                >= task.threshold
            ),
        }
    expected_result_count = (
        len(plan["task_ids"]) * len(plan["world_seeds"]) * (len(plan["baseline_algorithm_ids"]) + 1)
    )
    report = {
        "schema_version": "chemworld-static-s0-five-task-campaign-report-0.2-dev",
        "campaign_id": plan["campaign_id"],
        "campaign_plan_sha256": canonical_json_sha256(plan),
        "qualification_report_sha256": qualification_report["report_sha256"],
        "qualification_source_compatibility": qualification_report[
            "_campaign_source_compatibility"
        ],
        "source_commit": source_commit,
        "source_tree_dirty_at_completion": git_worktree_dirty(ROOT),
        "formal_result": False,
        "benchmark_claim_allowed": False,
        "world_seeds": list(plan["world_seeds"]),
        "development_world_seed": int(plan["development_world_seed"]),
        "held_out_world_seeds": list(plan["held_out_world_seeds"]),
        "algorithm_seeds": list(plan["algorithm_seeds"]),
        "result_count": len(results),
        "expected_result_count": expected_result_count,
        "all_cells_completed": len(results) == expected_result_count,
        "all_exact_replay": all(item["exact_replay"] for item in results),
        "all_tasks_reach_threshold_by_method_mean": all(
            task["threshold_reached_by_any_method_mean"] for task in task_reports.values()
        ),
        "all_tasks_participant_held_out_mean_reaches_threshold": all(
            task["participant_held_out_mean_reaches_threshold"]
            for task in task_reports.values()
        ),
        "imported_qualified_seed0_result_count": sum(
            item.get("provenance") == "qualified_seed0_import" for item in results
        ),
        "participant_provider_call_count": sum(
            int(item.get("provider_call_count", 0))
            for item in results
            if item["kind"] == "participant"
        ),
        "tasks": task_reports,
        "claim_boundary": plan["claim_boundary"],
    }
    report["completed"] = bool(
        report["all_cells_completed"]
        and report["all_exact_replay"]
        and not report["source_tree_dirty_at_completion"]
    )
    report["report_sha256"] = canonical_json_sha256(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--qualification-report", type=Path)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--selection",
        choices=("baselines", "participants", "all"),
        default="all",
    )
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument(
        "--preflight-mock",
        action="store_true",
        help="Run one 20-round mock participant cell per task and exact audits.",
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-campaign-sha256")
    args = parser.parse_args()
    plan = _load_object(args.plan)
    _qualification_plan, protocols = _validate_plan(plan)
    campaign_hash = canonical_json_sha256(plan)
    planned = {
        "campaign_id": plan["campaign_id"],
        "campaign_plan_sha256": campaign_hash,
        "selection": args.selection,
        "world_seeds": plan["world_seeds"],
        "development_world_seed": plan["development_world_seed"],
        "held_out_world_seeds": plan["held_out_world_seeds"],
        "execution_world_seeds": plan["execution_world_seeds"],
        "task_ids": plan["task_ids"],
        "participant_world_cells": (
            len(plan["task_ids"]) * len(plan["world_seeds"])
            if args.selection in {"participants", "all"}
            else 0
        ),
        "participant_cells_imported_from_qualification": (
            len(plan["task_ids"])
            if args.selection in {"participants", "all"}
            else 0
        ),
        "participant_cells_to_execute": (
            len(plan["task_ids"]) * len(plan["execution_world_seeds"])
            if args.selection in {"participants", "all"}
            else 0
        ),
        "baseline_cells": (
            len(plan["task_ids"]) * len(plan["world_seeds"]) * len(plan["baseline_algorithm_ids"])
            if args.selection in {"baselines", "all"}
            else 0
        ),
    }
    if args.preflight_mock:
        if args.execute:
            raise ValueError("--preflight-mock and --execute are mutually exclusive")
        if args.max_workers <= 0:
            raise ValueError("--max-workers must be positive")
        output = args.output_root.resolve() / "preflight-mock"
        method_path = _repo_path(plan["participant"]["method_config_path"])
        method_hash = canonical_json_sha256(_load_object(method_path))
        futures = {}
        results: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            for task_id in plan["task_ids"]:
                protocol_path = output / "protocols" / f"participant--{task_id}.json"
                write_json_atomic(protocol_path, protocols["participant"][task_id])
                future = executor.submit(
                    _run_participant_cell,
                    plan=plan,
                    protocol_path=protocol_path,
                    base_protocol=protocols["participant"][task_id],
                    method_path=method_path,
                    method_hash=method_hash,
                    task_id=task_id,
                    world_seed=0,
                    output=output,
                    provider="mock",
                )
                futures[future] = task_id
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(
                    json.dumps(
                        {
                            "preflight_completed": futures[future],
                            "score": result["primary_score"],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
        preflight = {
            "schema_version": ("chemworld-static-s0-five-task-participant-preflight-0.1-dev"),
            "campaign_id": plan["campaign_id"],
            "campaign_plan_sha256": campaign_hash,
            "method_config_sha256": method_hash,
            "task_ids": list(plan["task_ids"]),
            "world_seed": 0,
            "completed_task_count": len(results),
            "twenty_rounds_per_task": all(
                result["completed_experiment_count"] == 20 for result in results
            ),
            "six_blind_validations_per_task": all(
                result["validation_experiment_count"] == 6 for result in results
            ),
            "all_exact_replay": all(result["exact_replay"] for result in results),
            "all_postrun_audits_passed": all(result["postrun_audit_passed"] for result in results),
            "passed": len(results) == len(plan["task_ids"])
            and all(result["exact_replay"] for result in results),
            "results": sorted(results, key=lambda item: item["task_id"]),
        }
        preflight["report_sha256"] = canonical_json_sha256(preflight)
        write_json_atomic(output / "preflight_report.json", preflight)
        print(
            json.dumps(
                {
                    "output": str(output / "preflight_report.json"),
                    "passed": preflight["passed"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
        return 0 if preflight["passed"] else 1
    if not args.execute:
        print(json.dumps(planned, indent=2, sort_keys=True))
        return 0
    if args.confirm_campaign_sha256 != campaign_hash:
        raise RuntimeError("execution requires the exact canonical campaign SHA-256")
    if args.max_workers <= 0:
        raise ValueError("--max-workers must be positive")
    if git_worktree_dirty(ROOT):
        raise RuntimeError("five-task campaign execution requires a clean source tree")
    source_commit = git_source_commit(ROOT)
    qualification_report_path = args.qualification_report or _repo_path(
        plan["qualification_report_default_path"]
    )
    qualification_report = _verify_qualification(
        plan,
        qualification_report_path,
        source_commit=source_commit,
    )
    output = args.output_root.resolve()
    protocol_paths: dict[str, dict[str, Path]] = {kind: {} for kind in ("baseline", "participant")}
    for kind in protocol_paths:
        for task_id, protocol in protocols[kind].items():
            path = output / "protocols" / f"{kind}--{task_id}.json"
            write_json_atomic(path, protocol)
            protocol_paths[kind][task_id] = path
    method_path = _repo_path(plan["participant"]["method_config_path"])
    method_hash = canonical_json_sha256(_load_object(method_path))
    jobs: list[tuple[str, dict[str, Any]]] = []
    results = _qualified_development_seed0_results(
        plan,
        qualification_plan=_qualification_plan,
        qualification_report=qualification_report,
        selection=args.selection,
    )
    if args.selection in {"baselines", "all"}:
        for task_id in plan["task_ids"]:
            for world_seed in plan["execution_world_seeds"]:
                for algorithm_id in plan["baseline_algorithm_ids"]:
                    jobs.append(
                        (
                            "baseline",
                            {
                                "plan": plan,
                                "base_protocol": protocols["baseline"][task_id],
                                "task_id": task_id,
                                "world_seed": world_seed,
                                "algorithm_id": algorithm_id,
                                "output": output,
                            },
                        )
                    )
    if args.selection in {"participants", "all"}:
        for task_id in plan["task_ids"]:
            for world_seed in plan["execution_world_seeds"]:
                jobs.append(
                    (
                        "participant",
                        {
                            "plan": plan,
                            "protocol_path": protocol_paths["participant"][task_id],
                            "base_protocol": protocols["participant"][task_id],
                            "method_path": method_path,
                            "method_hash": method_hash,
                            "task_id": task_id,
                            "world_seed": world_seed,
                            "output": output,
                            "provider": str(plan["participant"]["provider"]),
                        },
                    )
                )
    status_lock = threading.Lock()
    execution_status: dict[str, Any] = {
        "schema_version": "chemworld-static-s0-five-task-execution-status-0.1-dev",
        "campaign_id": plan["campaign_id"],
        "campaign_plan_sha256": campaign_hash,
        "selection": args.selection,
        "max_workers": int(args.max_workers),
        "started_at": _utc_now(),
        "updated_at": _utc_now(),
        "jobs": {},
        "summary": {},
    }
    for item in results:
        job_id = (
            f"{item['kind']}:{item['task_id']}:world-{int(item['world_seed']):02d}:"
            f"{item['method_id']}"
        )
        execution_status["jobs"][job_id] = {
            "kind": item["kind"],
            "task_id": item["task_id"],
            "world_seed": int(item["world_seed"]),
            "method_id": item["method_id"],
            "state": "completed",
            "provenance": item.get("provenance", "existing_exact_receipt"),
            "started_at": None,
            "completed_at": execution_status["started_at"],
        }
    job_specs: list[tuple[str, dict[str, Any], str]] = []
    for kind, kwargs in jobs:
        method_id = (
            kwargs["algorithm_id"]
            if kind == "baseline"
            else plan["participant"]["method_id"]
        )
        job_id = (
            f"{kind}:{kwargs['task_id']}:world-{int(kwargs['world_seed']):02d}:"
            f"{method_id}"
        )
        execution_status["jobs"][job_id] = {
            "kind": kind,
            "task_id": kwargs["task_id"],
            "world_seed": int(kwargs["world_seed"]),
            "method_id": method_id,
            "state": "queued",
            "provenance": "held_out_execution",
            "started_at": None,
            "completed_at": None,
        }
        job_specs.append((kind, kwargs, job_id))

    def _write_execution_status() -> None:
        states = [
            str(item["state"]) for item in execution_status["jobs"].values()
        ]
        execution_status["updated_at"] = _utc_now()
        execution_status["summary"] = {
            state: states.count(state)
            for state in ("queued", "running", "completed", "failed")
        }
        write_json_atomic(output / "execution_status.json", execution_status)

    def _execute_observable_job(
        kind: str,
        kwargs: dict[str, Any],
        job_id: str,
    ) -> dict[str, Any]:
        with status_lock:
            execution_status["jobs"][job_id]["state"] = "running"
            execution_status["jobs"][job_id]["started_at"] = _utc_now()
            _write_execution_status()
        try:
            result = (
                _run_baseline_cell(**kwargs)
                if kind == "baseline"
                else _run_participant_cell(**kwargs)
            )
        except Exception as exc:
            with status_lock:
                execution_status["jobs"][job_id]["state"] = "failed"
                execution_status["jobs"][job_id]["completed_at"] = _utc_now()
                execution_status["jobs"][job_id]["error"] = (
                    f"{type(exc).__name__}: {exc}"
                )
                _write_execution_status()
            raise
        with status_lock:
            execution_status["jobs"][job_id]["state"] = "completed"
            execution_status["jobs"][job_id]["completed_at"] = _utc_now()
            execution_status["jobs"][job_id]["primary_score"] = result[
                "primary_score"
            ]
            _write_execution_status()
        return result

    with status_lock:
        _write_execution_status()
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(
                _execute_observable_job,
                kind,
                kwargs,
                job_id,
            ): (kind, kwargs["task_id"], kwargs["world_seed"])
            for kind, kwargs, job_id in job_specs
        }
        for future in as_completed(futures):
            kind, task_id, world_seed = futures[future]
            result = future.result()
            results.append(result)
            print(
                json.dumps(
                    {
                        "completed": f"{kind}:{task_id}:world-{world_seed:02d}",
                        "method_id": result["method_id"],
                        "score": result["primary_score"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    results.sort(
        key=lambda item: (
            item["task_id"],
            item["kind"],
            item["method_id"],
            item["world_seed"],
        )
    )
    if args.selection == "all":
        report = _build_report(
            plan,
            qualification_report=qualification_report,
            source_commit=source_commit,
            results=results,
        )
        write_json_atomic(output / "campaign_report.json", report)
        print(
            json.dumps(
                {
                    "output": str(output / "campaign_report.json"),
                    "completed": report["completed"],
                    "result_count": report["result_count"],
                    "all_tasks_reach_threshold_by_method_mean": report[
                        "all_tasks_reach_threshold_by_method_mean"
                    ],
                },
                sort_keys=True,
            ),
            flush=True,
        )
        return 0 if report["completed"] else 1
    partial = {
        "schema_version": "chemworld-static-s0-five-task-campaign-partial-0.2-dev",
        "campaign_id": plan["campaign_id"],
        "campaign_plan_sha256": campaign_hash,
        "selection": args.selection,
        "source_commit": source_commit,
        "results": results,
    }
    write_json_atomic(output / f"{args.selection}_partial_report.json", partial)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
