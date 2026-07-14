"""Audit the fail-closed PPO/SAC current-contract integration decision."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATUS = Path("configs/methods/rl_v0.4/rl_current_contract_status.json")
DEFAULT_OUTPUT = Path("workstreams/benchmark_v1/reports/rl-current-contract-integration-v0.4.json")
STATUS_SCHEMA = "chemworld-rl-current-contract-status-0.4"
REPORT_SCHEMA = "chemworld-rl-current-contract-integration-audit-0.4"


class RLCurrentContractIntegrationError(RuntimeError):
    """Raised when current-contract evidence cannot support the declared decision."""


def _load(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RLCurrentContractIntegrationError(f"cannot read {label}: {path}") from exc
    if not isinstance(payload, dict):
        raise RLCurrentContractIntegrationError(f"{label} must be a JSON object")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inside(root: Path, relative: str, label: str) -> Path:
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise RLCurrentContractIntegrationError(f"{label} escapes the repository") from exc
    return path


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=root, text=True, encoding="utf-8"
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise RLCurrentContractIntegrationError(f"git {' '.join(args)} failed") from exc


def _all_contracts_and_replays_exact(report: Mapping[str, Any]) -> bool:
    jobs = report.get("jobs")
    if not isinstance(jobs, list) or len(jobs) != 4:
        return False
    for job in jobs:
        if not isinstance(job, Mapping):
            return False
        for key in ("step0_evaluation", "trained_evaluation"):
            evaluation = job.get(key)
            if not isinstance(evaluation, Mapping) or evaluation.get("exact_replay") is not True:
                return False
            compatibility = evaluation.get("checkpoint_contract_compatibility")
            if (
                not isinstance(compatibility, Mapping)
                or not compatibility
                or not all(value is True for value in compatibility.values())
            ):
                return False
        step0 = job.get("step0_checkpoint")
        trained = job.get("trained_checkpoint")
        if not isinstance(step0, Mapping) or not isinstance(trained, Mapping):
            return False
        hashes = (
            step0.get("checkpoint_sha256"),
            step0.get("checkpoint_contract_sha256"),
            trained.get("checkpoint_sha256"),
            trained.get("manifest_sha256"),
        )
        if not all(isinstance(value, str) and len(value) == 64 for value in hashes):
            return False
    return True


def _historical_archive_is_quarantined(method: str, archive: Mapping[str, Any]) -> bool:
    if method == "ppo":
        return bool(
            archive.get("result_role") == "historical_diagnostic"
            and archive.get("formal_results_present") is False
            and archive.get("benchmark_claim_allowed") is False
            and archive.get("eligible_for_current_runtime_load") is False
            and archive.get("eligible_for_resume") is False
            and archive.get("eligible_for_formal_checkpoint_index") is False
        )
    return bool(
        archive.get("result_role") == "diagnostic_only"
        and archive.get("formal_results_present") is False
        and archive.get("benchmark_claim_allowed") is False
        and archive.get("eligible_for_current_runtime_load") is False
        and archive.get("eligible_for_resume") is False
        and archive.get("eligible_for_formal_checkpoint_index") is False
    )


def build_audit(
    *,
    root: Path,
    status_path: Path,
    source_commit: str,
    origin_main_commit: str,
    source_tree_clean: bool,
) -> dict[str, Any]:
    """Build a machine-readable audit without accessing Bench or reference feedback."""

    status = _load(status_path, "RL current-contract status")
    bindings = status.get("artifact_bindings")
    if not isinstance(bindings, Mapping):
        raise RLCurrentContractIntegrationError("status artifact_bindings must be an object")
    artifacts: dict[str, dict[str, Any]] = {}
    artifact_checks: dict[str, bool] = {}
    for label, binding_raw in bindings.items():
        if not isinstance(binding_raw, Mapping):
            artifact_checks[f"artifact:{label}:binding"] = False
            continue
        path_value = binding_raw.get("path")
        expected = binding_raw.get("sha256")
        if not isinstance(path_value, str) or not isinstance(expected, str):
            artifact_checks[f"artifact:{label}:binding"] = False
            continue
        path = _inside(root, path_value, str(label))
        present = path.is_file()
        actual = _sha256(path) if present else None
        artifact_checks[f"artifact:{label}:present"] = present
        artifact_checks[f"artifact:{label}:digest"] = actual == expected
        if present:
            artifacts[str(label)] = _load(path, str(label))

    required_labels = {
        "rl_method_contract",
        "rl_contract_report",
        "ppo_checkpoint_index",
        "ppo_current_outcome",
        "ppo_current_preflight",
        "ppo_historical_archive",
        "ppo_completed_claim",
        "sac_checkpoint_index",
        "sac_current_outcome",
        "sac_current_preflight",
        "sac_historical_archive",
        "sac_completed_claim",
        "global_method_freeze_snapshot",
    }
    artifact_checks["all_required_binding_labels"] = set(bindings) == required_labels
    contract = artifacts.get("rl_method_contract", {})
    contract_report = artifacts.get("rl_contract_report", {})
    freeze = artifacts.get("global_method_freeze_snapshot", {})
    requirements = cast(Mapping[str, Any], status.get("contract_requirements", {}))
    checks: dict[str, bool] = {
        "status_schema": status.get("schema_version") == STATUS_SCHEMA,
        "task_id": status.get("task_id") == "benchmark-v05-rl-current-contract-integration",
        "declared_selection_failed": status.get("status") == "rl_current_contract_selection_failed",
        "source_is_origin_main": source_commit == origin_main_commit,
        "source_tree_clean": source_tree_clean,
        "rl_contract_remains_contract_only": contract.get("status")
        == "contract_ready_training_pending"
        and contract.get("formal_results_present") is False
        and contract.get("benchmark_claim_allowed") is False,
        "rl_contract_report_controls_ready": contract_report.get("controls_ready") is True
        and contract_report.get("formal_ready_checkpoint_count") == 0
        and contract_report.get("formal_results_present") is False,
        "global_freeze_remains_blocked": freeze.get("status") == "method_freeze_preflight_blocked"
        and freeze.get("bench_unlock_allowed") is False
        and freeze.get("formal_results_present") is False,
        "global_freeze_not_claimed_closed": status.get("global_freeze_boundary", {}).get(
            "global_method_freeze_closed_by_this_claim"
        )
        is False,
        "bench_and_reference_forbidden": status.get("bench_accessed") is False
        and status.get("reference_repositories_used") == []
        and status.get("parent_decision", {}).get("bench_unlock_allowed") is False
        and status.get("parent_decision", {}).get("benchmark_claim_allowed") is False,
    }
    method_evidence: dict[str, Any] = {}
    for method in ("ppo", "sac"):
        index = artifacts.get(f"{method}_checkpoint_index", {})
        outcome = artifacts.get(f"{method}_current_outcome", {})
        preflight = artifacts.get(f"{method}_current_preflight", {})
        archive = artifacts.get(f"{method}_historical_archive", {})
        completed = artifacts.get(f"{method}_completed_claim", {})
        decision = status.get("method_decisions", {}).get(method, {})
        expected_task = (
            "benchmark-v05-rl-adapters--slice-ppo-v048-retrain-dev"
            if method == "ppo"
            else "benchmark-v05-rl-adapters--slice-sac-train-dev"
        )
        method_checks = {
            "decision_selection_failed": isinstance(decision, Mapping)
            and decision.get("status") == "selection_failed"
            and decision.get("method_ready") is False
            and decision.get("selected_checkpoint_count") == 0,
            "index_fail_closed": index.get("schema_version")
            == requirements.get("checkpoint_index_schema")
            and index.get("checkpoints") == []
            and index.get("selected_checkpoint_count") == 0
            and index.get(f"{method}_method_ready") is False
            and index.get("formal_results_present") is False
            and index.get("benchmark_claim_allowed") is False,
            "index_contracts_exact": index.get("required_checkpoint_manifest_schema")
            == requirements.get("checkpoint_manifest_schema")
            and index.get("required_periodic_sidecar_schema")
            == requirements.get("checkpoint_sidecar_schema")
            and index.get("required_observation_contract_hashes")
            == requirements.get("observation_contract_hashes")
            and index.get("shape_only_observation_compatibility_allowed") is False,
            "outcome_negative_not_ready": outcome.get("algorithm") == method
            and outcome.get(f"{method}_method_ready") is False
            and outcome.get("full_matrix", {}).get("executed_training_run_count") == 0
            and outcome.get("full_matrix", {}).get("selected_checkpoint_count") == 0
            and outcome.get("formal_results_present") is False
            and outcome.get("benchmark_claim_allowed") is False
            and outcome.get("bench_accessed") is False
            and outcome.get("reference_search_used") is False,
            "outcome_hash_cross_binding": index.get("current_contract_outcome", {}).get(
                "report_sha256"
            )
            == bindings[f"{method}_current_outcome"]["sha256"],
            "preflight_hash_cross_binding": index.get("current_contract_preflight", {}).get(
                "report_sha256"
            )
            == bindings[f"{method}_current_preflight"]["sha256"],
            "preflight_failed_closed": preflight.get("algorithm") == method
            and preflight.get("full_matrix_allowed") is False
            and preflight.get("gate_assessment", {}).get("passed") is False
            and preflight.get("formal_results_present") is False
            and preflight.get("benchmark_claim_allowed") is False,
            "preflight_contracts_and_replays_exact": _all_contracts_and_replays_exact(preflight),
            "clean_load_evidence": outcome.get("clean_process_load_proof", {}).get("all_loaded")
            is True
            and outcome.get("clean_process_load_proof", {}).get("loaded_checkpoint_count") == 8,
            "historical_archive_quarantined": _historical_archive_is_quarantined(method, archive),
            "claim_completed": completed.get("task_id") == expected_task
            and completed.get("status") == "completed"
            and isinstance(completed.get("completion_summary"), str)
            and bool(completed.get("completion_summary")),
        }
        checks.update({f"{method}:{key}": value for key, value in method_checks.items()})
        method_evidence[method] = {
            "decision": dict(decision) if isinstance(decision, Mapping) else {},
            "preflight_status": preflight.get("status"),
            "preflight_learning_signal_task_count": preflight.get("gate_assessment", {}).get(
                "learning_signal_task_count"
            ),
            "full_matrix_executed_training_run_count": outcome.get("full_matrix", {}).get(
                "executed_training_run_count"
            ),
            "selected_checkpoint_count": index.get("selected_checkpoint_count"),
            "historical_result_role": archive.get("result_role"),
            "completed_claim_path": bindings[f"{method}_completed_claim"]["path"],
        }

    checks.update(artifact_checks)
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "schema_version": REPORT_SCHEMA,
        "status": (
            "rl_current_contract_integration_passed_selection_failed"
            if not failed
            else "rl_current_contract_integration_audit_failed"
        ),
        "task_id": status.get("task_id"),
        "source_commit": source_commit,
        "origin_main_commit": origin_main_commit,
        "source_tree_clean_during_audit": source_tree_clean,
        "status_config_path": status_path.relative_to(root).as_posix(),
        "status_config_sha256": _sha256(status_path),
        "checks": checks,
        "failed_checks": failed,
        "artifact_bindings": status.get("artifact_bindings"),
        "method_evidence": method_evidence,
        "parent_decision": status.get("parent_decision"),
        "evidence_tiers": status.get("evidence_tiers"),
        "global_freeze_boundary": {
            **dict(cast(Mapping[str, Any], status.get("global_freeze_boundary", {}))),
            "snapshot_status": freeze.get("status"),
            "snapshot_source_commit": freeze.get("source_commit"),
            "snapshot_bench_unlock_allowed": freeze.get("bench_unlock_allowed"),
            "snapshot_blocker_count": len(freeze.get("blockers", [])),
        },
        "current_selected_checkpoint_count": 0,
        "referenced_current_checkpoint_manifest_count": 0,
        "current_checkpoint_manifest_verification": "not_applicable_no_selected_checkpoints",
        "preflight_checkpoint_contract_and_replay_evidence_verified": not failed
        and checks.get("ppo:preflight_contracts_and_replays_exact") is True
        and checks.get("sac:preflight_contracts_and_replays_exact") is True,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "bench_accessed": False,
        "reference_search_used": False,
        "reference_repositories_used": [],
        "claim_boundary": (
            "This audit closes RL current-contract readiness as selection_failed. It does not "
            "close the collaborator-owned global method freeze or create formal Bench evidence."
        ),
    }


def _write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dict(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = args.root.resolve()
    status_path = args.status if args.status.is_absolute() else root / args.status
    output_path = args.output if args.output.is_absolute() else root / args.output
    source_commit = _git(root, "rev-parse", "HEAD")
    origin_main_commit = _git(root, "rev-parse", "origin/main")
    source_tree_clean = not _git(root, "status", "--porcelain=v1", "--untracked-files=all")
    report = build_audit(
        root=root,
        status_path=status_path.resolve(),
        source_commit=source_commit,
        origin_main_commit=origin_main_commit,
        source_tree_clean=source_tree_clean,
    )
    _write(output_path.resolve(), report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "failed_checks": report["failed_checks"],
                "source_commit": source_commit,
                "output": str(output_path),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not report["failed_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
