"""Run Gate A or resumable paired campaigns for mechanism adaptation v0.2.1+."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.eval.flagship_diagnostics import FeedbackCondition  # noqa: E402
from chemworld.eval.mechanism_adaptation_execution import (  # noqa: E402
    DEFAULT_GATE_A_PLAN_PATH,
    DEFAULT_LLM_METHODS_PATH,
    DEFAULT_PROTOCOL_PATH,
    load_json_object,
    run_campaign_row,
    run_gate_a,
    run_online_policy_certificate,
    selected_campaign_rows,
)
from chemworld.eval.mechanism_adaptation_pilot import (  # noqa: E402
    build_agent_pilot_report,
    load_campaigns_from_index,
)
from chemworld.eval.mechanism_feedback_audit import (  # noqa: E402
    run_local_feedback_audit,
)
from chemworld.eval.provenance import (  # noqa: E402
    canonical_json_sha256,
    write_json_atomic,
)

DEFAULT_GATE_A_REPORT = (
    ROOT / "workstreams/flagship_tasks/reports/mechanism-adaptation-gate-a-v0.2.5-rc17.json"
)
DEFAULT_ONLINE_POLICY_CERTIFICATE = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "mechanism-adaptation-online-policy-certificate-v0.4-rc17.json"
)
DEFAULT_RUNTIME_ROOT = ROOT / "runs/mechanism-adaptation-v0.2.1"
DEFAULT_PILOT_REPORT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "mechanism-adaptation-agent-pilot-v0.2.1.json"
)
DEFAULT_LOCAL_FEEDBACK_REPORT = (
    DEFAULT_RUNTIME_ROOT / "local-feedback.json"
)
_ONLINE_CERTIFICATE_REFERENCE_FIELDS = (
    "schema_version",
    "certificate_scope",
    "status",
    "gate_pass",
    "required",
    "certificate_present",
    "certificate_sha256",
    "protocol_sha256",
    "gate_a_plan_sha256",
    "execution_contract_binding_sha256",
    "controlled_matched_primary_budget",
    "online_policy_gate_budget",
    "hidden_change_time",
    "policy_received_phase_or_reset_indicator",
    "uses_actual_available_pre_change_history",
    "uses_actual_action_measurement_and_budget_contract",
    "agent_weight_updates_performed",
)


def _write_json(path: Path, payload: Any) -> None:
    write_json_atomic(path, payload)


def _write_immutable_json(path: Path, payload: Any) -> None:
    """Create a formal result exactly once; reruns must use a new versioned path."""

    if path.exists():
        raise FileExistsError(
            f"refusing to overwrite immutable formal result: {path}; "
            "select a new versioned --output path"
        )
    write_json_atomic(path, payload)


def _compact_gate_a_report(
    report: Mapping[str, Any],
    *,
    online_policy_certificate_path: Path | None,
) -> dict[str, Any]:
    """Replace duplicated online trajectories with one hash-bound DAG reference."""

    compacted = dict(report)
    decision = dict(compacted["certificate_decision"])
    certificate = dict(decision["online_policy_feasible_certificate"])
    reference = {
        field: certificate[field]
        for field in _ONLINE_CERTIFICATE_REFERENCE_FIELDS
        if field in certificate
    }
    if online_policy_certificate_path is not None:
        resolved = (
            online_policy_certificate_path
            if online_policy_certificate_path.is_absolute()
            else ROOT / online_policy_certificate_path
        ).resolve()
        try:
            reference["report"] = resolved.relative_to(ROOT).as_posix()
        except ValueError as error:
            raise ValueError(
                "online-policy certificate must be inside the repository"
            ) from error
        standalone_certificate = load_json_object(resolved)
        reference["certificate_sha256"] = canonical_json_sha256(
            standalone_certificate
        )
        reference["certificate_hash_source"] = (
            "standalone_report_canonical_json"
        )
    decision["online_policy_feasible_certificate"] = reference
    compacted["certificate_decision"] = decision
    compacted["online_policy_feasible_certificate"] = reference
    compacted["online_policy_certificate_embedding"] = (
        "canonical_sha256_bound_dag_reference_only"
    )
    return compacted


def _run_gate_a(args: argparse.Namespace) -> int:
    protocol = load_json_object(args.protocol)
    plan = load_json_object(args.gate_a_plan)
    design_audit_path = ROOT / plan["design_validity_precondition"]["report"]
    design_validity_audit = load_json_object(design_audit_path)
    online_policy_certificate = (
        None
        if args.online_policy_certificate is None
        else load_json_object(args.online_policy_certificate)
    )
    print(
        json.dumps(
            {
                "status": "starting",
                "stage": "gate-a",
                "tasks": protocol["design"]["tasks"],
                "budgets": plan["held_out_certificate"]["budgets"],
                "world_seeds_per_family": plan["held_out_certificate"][
                    "world_seeds_per_family"
                ],
                "external_provider_calls": False,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    report = run_gate_a(
        protocol,
        plan,
        online_policy_certificate=online_policy_certificate,
        design_validity_audit=design_validity_audit,
        progress_callback=_print_gate_a_progress,
    )
    report = _compact_gate_a_report(
        report,
        online_policy_certificate_path=args.online_policy_certificate,
    )
    _write_immutable_json(args.output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "gate_a_pass": report["gate_a_pass"],
                "primary_gate_budget": report["primary_gate_budget"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["gate_a_pass"] else 1


def _run_online_policy_certificate(args: argparse.Namespace) -> int:
    protocol = load_json_object(args.protocol)
    plan = load_json_object(args.gate_a_plan)
    design_audit_path = ROOT / plan["design_validity_precondition"]["report"]
    design_validity_audit = load_json_object(design_audit_path)
    print(
        json.dumps(
            {
                "status": "starting",
                "stage": "online-policy-certificate",
                "tasks": protocol["design"]["tasks"],
                "change_time_candidates": plan[
                    "online_policy_feasible_certificate"
                ]["change_time_candidates"],
                "post_change_budget_checkpoints": plan[
                    "online_policy_feasible_certificate"
                ]["post_change_experiment_budget_checkpoints"],
                "online_policy_gate_budget": plan[
                    "online_policy_feasible_certificate"
                ]["online_policy_gate_budget"],
                "external_provider_calls": False,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    report = run_online_policy_certificate(
        protocol,
        plan,
        design_validity_audit=design_validity_audit,
        progress_callback=_print_gate_a_progress,
    )
    _write_immutable_json(args.online_policy_output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "gate_pass": report["gate_pass"],
                "top1_accuracy": report["identifiability_certificate"][
                    "top1_accuracy"
                ],
                "output": str(args.online_policy_output),
            },
            indent=2,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if report["gate_pass"] else 1


def _print_gate_a_progress(event: Mapping[str, Any]) -> None:
    print(json.dumps(dict(event), sort_keys=True), flush=True)


def _run_campaigns(args: argparse.Namespace) -> int:
    protocol = load_json_object(args.protocol)
    methods = load_json_object(args.llm_methods)
    rows = selected_campaign_rows(
        protocol,
        tasks=args.task,
        pair_ids=args.pair_id,
        limit=args.pair_limit,
    )
    summaries = args.runtime_root / "campaigns"
    completed = 0
    reused = 0
    for row in rows:
        path = summaries / _campaign_filename(row, args.feedback_condition)
        if args.resume and path.is_file():
            _validate_resumable_campaign(
                path,
                row=row,
                protocol=protocol,
                feedback_condition=args.feedback_condition,
            )
            reused += 1
            print(json.dumps({"status": "reused", "path": str(path)}), flush=True)
            continue
        print(
            json.dumps(
                {
                    "status": "starting",
                    "pair_id": row["pair_id"],
                    "arm": row["arm"],
                    "task_id": row["task_id"],
                    "feedback_condition": args.feedback_condition,
                }
            ),
            flush=True,
        )
        result = run_campaign_row(
            protocol,
            row,
            output_root=args.runtime_root,
            llm_methods=methods,
            method_id=args.method_id,
            spectrum_disclosure=args.spectrum_disclosure,
            feedback_condition=args.feedback_condition,
            progress_callback=_print_campaign_progress,
        )
        _write_json(path, result)
        completed += 1
    index = {
        "schema_version": "chemworld-mechanism-adaptation-campaign-index-0.2.1",
        "protocol_id": protocol["protocol_id"],
        "selected_row_count": len(rows),
        "selected_pair_count": len({row["pair_id"] for row in rows}),
        "completed_this_invocation": completed,
        "reused_this_invocation": reused,
        "feedback_condition": args.feedback_condition,
        "campaign_paths": [
            str(summaries / _campaign_filename(row, args.feedback_condition))
            for row in rows
        ],
        "formal_result": False,
    }
    _write_json(args.runtime_root / "campaign-index.json", index)
    print(json.dumps(index, indent=2, sort_keys=True))
    return 0


def _print_campaign_progress(
    phase: str,
    record: Any,
    trace: list[dict[str, Any]],
) -> None:
    if record.event_type != "experiment_end" and record.step % 10 != 0:
        return
    status = trace[-1].get("status") if trace else None
    print(
        json.dumps(
            {
                "status": "progress",
                "phase": phase,
                "step": record.step,
                "event_type": record.event_type,
                "complete_experiment_count": record.method_resources.get(
                    "complete_experiment_count"
                ),
                "leaderboard_score": record.info.get("leaderboard_score"),
                "decision_status": status,
            }
        ),
        flush=True,
    )


def _build_pilot_report(args: argparse.Namespace) -> int:
    protocol = load_json_object(args.protocol)
    index_path = args.runtime_root / "campaign-index.json"
    campaigns = load_campaigns_from_index(index_path, root=ROOT)
    report = build_agent_pilot_report(protocol, campaigns, root=ROOT, replay=True)
    _write_json(args.pilot_report, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "gate_0": report["gate_0"]["status"],
                "gate_b": report["gate_b"]["status"],
                "gate_c": report["gate_c"]["status"],
                "gate_d": report["gate_d"]["status"],
                "gate_e": report["gate_e"]["status"],
                "output": str(args.pilot_report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["gate_0"]["status"] == "passed" else 1


def _run_local_feedback(args: argparse.Namespace) -> int:
    protocol = load_json_object(args.protocol)
    methods = load_json_object(args.llm_methods)
    campaigns = load_campaigns_from_index(
        args.runtime_root / "campaign-index.json",
        root=ROOT,
    )
    changed = next(
        (
            campaign
            for campaign in campaigns
            if campaign.get("matrix_row", {}).get("arm") == "changed"
        ),
        None,
    )
    if changed is None:
        raise RuntimeError("local feedback audit requires one changed campaign")
    iid_records = _load_jsonl_records(changed["iid"]["trajectory_path"])
    shifted_records = _load_jsonl_records(changed["shifted"]["trajectory_path"])
    print(
        json.dumps(
            {
                "status": "starting",
                "stage": "local-feedback",
                "pair_id": changed["matrix_row"]["pair_id"],
                "provider_repeats": args.provider_repeats,
                "condition_count": 4,
                "external_provider_calls": True,
            }
        ),
        flush=True,
    )
    report = run_local_feedback_audit(
        protocol,
        changed["matrix_row"],
        iid_records=iid_records,
        shifted_records=shifted_records,
        llm_methods=methods,
        repository_root=ROOT,
        method_id=args.method_id,
        spectrum_disclosure=args.spectrum_disclosure,
        provider_repeats=args.provider_repeats,
        target_shifted_experiment=args.target_shifted_experiment,
    )
    _write_json(args.local_feedback_report, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "net_local_feedback_effect": report["metrics"]["feedback_effect"][
                    "net_feedback_effect"
                ],
                "provider_billed_cost_usd": report["resources"][
                    "provider_billed_cost_usd"
                ],
                "output": str(args.local_feedback_report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _load_jsonl_records(raw_path: str) -> list[dict[str, Any]]:
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    if not records or not all(isinstance(item, dict) for item in records):
        raise ValueError(f"trajectory is empty or invalid: {path}")
    return records


def _validate_resumable_campaign(
    path: Path,
    *,
    row: dict[str, Any],
    protocol: dict[str, Any],
    feedback_condition: FeedbackCondition = "true_feedback",
) -> None:
    payload = load_json_object(path)
    expected_protocol = hashlib.sha256(
        json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if payload.get("protocol_sha256") != expected_protocol:
        raise RuntimeError(f"refusing stale campaign protocol binding: {path}")
    if payload.get("matrix_row") != row:
        raise RuntimeError(f"refusing stale campaign matrix-row binding: {path}")
    observed_condition = payload.get("feedback_condition", "true_feedback")
    if observed_condition != feedback_condition:
        raise RuntimeError(f"refusing stale campaign feedback-condition binding: {path}")
    for phase in ("iid", "shifted"):
        phase_payload = payload.get(phase)
        if not isinstance(phase_payload, dict):
            raise RuntimeError(f"resumable campaign lacks {phase} phase: {path}")
        trajectory_path = Path(str(phase_payload.get("trajectory_path") or ""))
        if not trajectory_path.is_absolute():
            trajectory_path = ROOT / trajectory_path
        if not trajectory_path.is_file():
            raise RuntimeError(f"resumable campaign trajectory is missing: {trajectory_path}")
        observed = hashlib.sha256(trajectory_path.read_bytes()).hexdigest()
        if observed != phase_payload.get("trajectory_sha256"):
            raise RuntimeError(f"resumable campaign trajectory digest is stale: {trajectory_path}")


def _campaign_filename(
    row: dict[str, Any],
    feedback_condition: FeedbackCondition,
) -> str:
    suffix = "" if feedback_condition == "true_feedback" else f"--{feedback_condition}"
    return f"{row['pair_id']}--{row['arm']}{suffix}.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=(
            "gate-a",
            "online-policy-certificate",
            "campaign",
            "pilot-report",
            "local-feedback",
        ),
        default="gate-a",
        help="Gate A is environment-only; campaign makes external provider calls.",
    )
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--gate-a-plan", type=Path, default=DEFAULT_GATE_A_PLAN_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_GATE_A_REPORT)
    parser.add_argument(
        "--online-policy-output",
        type=Path,
        default=DEFAULT_ONLINE_POLICY_CERTIFICATE,
    )
    parser.add_argument(
        "--online-policy-certificate",
        type=Path,
        default=None,
        help=(
            "Separately generated, protocol/plan-bound online-policy-feasible Gate A "
            "certificate. Omission leaves full Gate A fail-closed and pending."
        ),
    )
    parser.add_argument("--llm-methods", type=Path, default=DEFAULT_LLM_METHODS_PATH)
    parser.add_argument("--runtime-root", type=Path, default=DEFAULT_RUNTIME_ROOT)
    parser.add_argument("--pilot-report", type=Path, default=DEFAULT_PILOT_REPORT)
    parser.add_argument(
        "--local-feedback-report",
        type=Path,
        default=DEFAULT_LOCAL_FEEDBACK_REPORT,
    )
    parser.add_argument("--method-id", default="live_llm_b")
    parser.add_argument(
        "--spectrum-disclosure", choices=("assigned", "unassigned", "masked"), default="assigned"
    )
    parser.add_argument(
        "--feedback-condition",
        choices=(
            "true_feedback",
            "permuted_feedback",
            "delayed_feedback",
            "critical_measurement_deleted",
        ),
        default="true_feedback",
        help="Agent-visible feedback intervention; environment state and scoring remain unchanged.",
    )
    parser.add_argument("--task", action="append")
    parser.add_argument("--pair-id", action="append")
    parser.add_argument("--pair-limit", type=int)
    parser.add_argument("--provider-repeats", type=int, default=3)
    parser.add_argument("--target-shifted-experiment", type=int, default=2)
    parser.add_argument("--resume", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.stage == "gate-a":
        return _run_gate_a(args)
    if args.stage == "online-policy-certificate":
        return _run_online_policy_certificate(args)
    if args.stage == "campaign":
        return _run_campaigns(args)
    if args.stage == "pilot-report":
        return _build_pilot_report(args)
    return _run_local_feedback(args)


if __name__ == "__main__":
    raise SystemExit(main())
