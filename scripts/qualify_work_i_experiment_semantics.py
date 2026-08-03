"""Qualify transaction, resource, failure, and instrument semantics for Work I."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401  # register the environment
from chemworld.agents.task_recipes import (
    task_recipe_dimension,
    task_recipe_from_unit_vector,
)
from chemworld.campaign_resources import (
    CampaignResourceCard,
    CampaignResourceLedger,
    campaign_resource_event_id,
)
from chemworld.foundation.world_fork_runtime import PUBLIC_TRANSACTION_STATUS_SEMANTICS
from chemworld.runtime.domain_service_registry import DomainServiceRegistry
from chemworld.runtime.kernel_registry import OperationKernelRegistry, affected_ledgers
from chemworld.runtime.transactions import StatePatch, TransactionManager, WorldEvent
from chemworld.tasks import list_tasks
from chemworld.world.instruments import instrument_contracts
from chemworld.world.operations import INSTRUMENTS, OPERATION_TYPES, operation_contracts

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.json"
DEFAULT_MARKDOWN = ROOT / "workstreams/arxiv_v1/reports/work-i-experiment-semantics-v0.1.md"


def _sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _physical_projection(env: Any) -> dict[str, Any]:
    state = env._state.to_dict(include_hidden=True)
    keys = (
        "volume_L",
        "temperature_K",
        "pressure_Pa",
        "phase",
        "vessel_id",
        "terminated",
        "quenched",
        "species_amounts",
        "phases",
        "vessels",
        "equipment",
        "thermal",
    )
    return {key: state[key] for key in keys}


def _env(task_id: str, **kwargs: Any) -> gym.Env:
    return gym.make(
        "ChemWorld",
        task_id=task_id,
        seed=0,
        observation_noise_mode="keyed",
        observation_seed_override=0,
        observation_noise_namespace="chemworld-work-i-semantics",
        **kwargs,
    )


def _collect_committed_probes() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    operation_probes: dict[str, dict[str, Any]] = {}
    instrument_probes: dict[str, dict[str, Any]] = {}
    for task in list_tasks():
        env = _env(task.task_id)
        try:
            env.reset(seed=0)
            raw = env.unwrapped
            task_info = raw.task_info()
            recipe = task_recipe_from_unit_vector(
                task_info,
                np.full(task_recipe_dimension(task_info), 0.5, dtype=float),
            )
            for action in recipe["steps"]:
                before_terminated = bool(raw._state.terminated)
                _, _, _, _, info = env.step(action)
                operation = str(action["operation"])
                if info.get("transaction_status") == "committed":
                    operation_probes.setdefault(
                        operation,
                        {
                            "task_id": task.task_id,
                            "action": action,
                            "transaction_status": info.get("transaction_status"),
                            "rollback_reason": info.get("rollback_reason"),
                            "kernel_id": info.get("kernel_id"),
                        },
                    )
                    instrument = action.get("instrument")
                    if operation == "measure" and isinstance(instrument, str):
                        instrument_probes.setdefault(
                            instrument,
                            {
                                "task_id": task.task_id,
                                "action": action,
                                "state_terminated_before_measurement": before_terminated,
                                "transaction_status": info.get("transaction_status"),
                                "cost_delta": info.get("cost_delta"),
                                "sample_delta": info.get("sample_delta"),
                            },
                        )
        finally:
            env.close()

    # Complete-experiment midpoint recipes intentionally omit these optional
    # primitives, so qualify them in a valid prepared reaction vessel.
    env = _env("reaction-to-assay")
    try:
        env.reset(seed=0)
        setup = (
            {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0},
            {"operation": "add_reagent", "amount_mol": 0.01},
        )
        for action in setup:
            env.step(action)
        for action in (
            {"operation": "wait", "duration_s": 60.0, "stirring_speed_rpm": 300.0},
            {"operation": "sample", "sample_volume_L": 0.0001},
        ):
            _, _, _, _, info = env.step(action)
            operation_probes[str(action["operation"])] = {
                "task_id": "reaction-to-assay",
                "action": action,
                "transaction_status": info.get("transaction_status"),
                "rollback_reason": info.get("rollback_reason"),
                "kernel_id": info.get("kernel_id"),
            }
    finally:
        env.close()
    return operation_probes, instrument_probes


def _collect_failure_probes() -> dict[str, dict[str, Any]]:
    tasks = list_tasks()
    task_for_operation = {
        operation: next(task.task_id for task in tasks if operation in task.allowed_operations)
        for operation in OPERATION_TYPES
    }
    probes: dict[str, dict[str, Any]] = {}
    for operation in OPERATION_TYPES:
        task_id = task_for_operation[operation]
        env = _env(task_id)
        try:
            env.reset(seed=0)
            raw = env.unwrapped
            before = _physical_projection(raw)
            before_ledger = raw._state.ledger.to_dict()
            _, _, _, _, info = env.step({"operation": operation})
            after = _physical_projection(raw)
            after_ledger = raw._state.ledger.to_dict()
            probes[operation] = {
                "task_id": task_id,
                "probe_action": {"operation": operation},
                "transaction_status": info.get("transaction_status"),
                "rollback_reason": info.get("rollback_reason"),
                "physical_state_unchanged": before == after,
                "penalty_cost_delta": after_ledger["cost"] - before_ledger["cost"],
                "penalty_risk_delta": after_ledger["risk"] - before_ledger["risk"],
                "event_types": [event["event_type"] for event in info.get("world_events", ())],
                "passed": (
                    info.get("transaction_status") in {"validation_failed", "rolled_back"}
                    and before == after
                ),
            }
        finally:
            env.close()
    return probes


def _constitution_rollback_probe() -> dict[str, Any]:
    env = _env("reaction-to-assay")
    try:
        env.reset(seed=0)
        raw = env.unwrapped
        original = raw._state
        candidate = original.replace(volume_L=-1.0)
        result = TransactionManager(raw.constitution).commit(
            state=original,
            operation_type="adversarial_negative_volume",
            events=(WorldEvent("candidate", "adversarial_negative_volume"),),
            patches=(
                StatePatch(
                    patch_type="replace_state",
                    affected_ledgers=("species", "phases", "process"),
                    state=candidate,
                ),
            ),
        )
        return {
            "transaction_status": result.transaction_status,
            "rollback_reason": result.rollback_reason,
            "candidate_volume_L": candidate.volume_L,
            "result_volume_L": result.state.volume_L,
            "original_volume_L": original.volume_L,
            "penalty_cost_delta": result.state.ledger.cost - original.ledger.cost,
            "penalty_risk_delta": result.state.ledger.risk - original.ledger.risk,
            "event_types": [event.event_type for event in result.events],
            "passed": (
                result.transaction_status == "rolled_back"
                and result.rollback_reason == "constitution_failed"
                and result.state.volume_L == original.volume_L
                and any(event.event_type == "transaction_rollback" for event in result.events)
            ),
        }
    finally:
        env.close()


def _resource_probe() -> dict[str, Any]:
    ledger_card = CampaignResourceCard(
        card_id="work-i-semantics-ledger-probe",
        operation_attempt_limit=1,
        vessel_start_limit=1,
        final_assay_limit=1,
        nonfinal_instrument_use_limit=1,
        stock_limits={"reagent_mol": 0.05, "solvent_L": 0.05},
        per_instrument_limits=dict.fromkeys(INSTRUMENTS, 1),
        metadata={"purpose": "work-i-semantic-qualification"},
    )
    ledger = CampaignResourceLedger(ledger_card)
    first_id = campaign_resource_event_id("work-i-resource-probe", 1)
    second_id = campaign_resource_event_id("work-i-resource-probe", 2)
    first_action = {"operation": "add_solvent", "volume_L": 0.025, "solvent": 0}
    second_action = {"operation": "add_reagent", "amount_mol": 0.01}
    first = ledger.preflight(first_id, first_action, starts_vessel=True)
    ledger.record_outcome(
        first_id,
        first_action,
        {"transaction_status": "committed", "operation_committed": True},
        starts_vessel=True,
    )
    second = ledger.preflight(second_id, second_action)
    ledger.record_outcome(
        second_id,
        second_action,
        {
            "transaction_status": "campaign_resource_rejected",
            "operation_committed": False,
        },
    )
    snapshot = ledger.snapshot()
    restored = CampaignResourceLedger.from_snapshot(snapshot).snapshot()

    environment_card = CampaignResourceCard(
        card_id="work-i-semantics-environment-probe",
        operation_attempt_limit=2,
        vessel_start_limit=1,
        final_assay_limit=1,
        nonfinal_instrument_use_limit=1,
        stock_limits={"reagent_mol": 0.05, "solvent_L": 0.025},
        per_instrument_limits=dict.fromkeys(INSTRUMENTS, 1),
        metadata={"purpose": "work-i-semantic-environment-integration"},
    )
    env = _env(
        "electrochemical-conversion",
        campaign_resource_card=environment_card,
    )
    try:
        env.reset(seed=0)
        _, _, _, _, accepted_info = env.step(first_action)
        _, _, _, _, rejected_info = env.step(
            {"operation": "add_solvent", "volume_L": 0.001, "solvent": 1}
        )
    finally:
        env.close()
    state = snapshot["state"]
    return {
        "ledger_card": ledger_card.to_dict(),
        "environment_card": environment_card.to_dict(),
        "first_preflight": first.to_dict(),
        "second_preflight": second.to_dict(),
        "ledger_state": state,
        "snapshot_roundtrip_exact": restored == snapshot,
        "environment_statuses": [
            accepted_info.get("transaction_status"),
            rejected_info.get("transaction_status"),
        ],
        "environment_rejection_reason": rejected_info.get("rollback_reason"),
        "passed": (
            first.allowed
            and not second.allowed
            and second.rejection_reasons == ("operation_attempt_limit",)
            and state["operation_attempts"] == 1
            and state["vessel_starts"] == 1
            and state["stocks_used"] == {"solvent_L": 0.025}
            and restored == snapshot
            and accepted_info.get("transaction_status") == "committed"
            and rejected_info.get("transaction_status") == "campaign_resource_rejected"
            and rejected_info.get("campaign_resource_rejection_reasons")
            == ["stock_limit:solvent_L"]
        ),
    }


def build_report() -> dict[str, Any]:
    contracts = operation_contracts()
    kernels = OperationKernelRegistry.default()
    services = DomainServiceRegistry.default()
    services.validate_operation_coverage()
    committed, instrument_probes = _collect_committed_probes()
    failures = _collect_failure_probes()
    constitution = _constitution_rollback_probe()
    resource = _resource_probe()
    operation_rows = []
    for operation in OPERATION_TYPES:
        contract = contracts[operation]
        kernel = kernels.get(operation)
        commit_probe = committed.get(operation)
        failure_probe = failures[operation]
        operation_rows.append(
            {
                "operation_id": operation,
                "module": contract.module,
                "kind": contract.kind,
                "required_fields": list(contract.required_fields),
                "preconditions": list(contract.preconditions),
                "kernel_id": kernel.kernel_id,
                "kernel_version": kernel.kernel_version,
                "domain_service_id": services.service_id_for_operation(operation),
                "affected_ledgers": list(affected_ledgers(operation)),
                "committed_probe": commit_probe,
                "failure_probe": failure_probe,
                "passed": (
                    commit_probe is not None
                    and commit_probe["transaction_status"] == "committed"
                    and failure_probe["passed"]
                ),
            }
        )

    instrument_rows = []
    for instrument_id in INSTRUMENTS:
        contract = instrument_contracts()[instrument_id]
        probe = instrument_probes.get(instrument_id)
        cost_matches = (
            probe is not None
            and abs(float(probe["cost_delta"]) - contract.cost) <= 1.0e-12
        )
        sample_matches = (
            probe is not None
            and abs(float(probe["sample_delta"]) - contract.sample_consumption_L) <= 1.0e-12
        )
        terminal_semantics_match = (
            probe is not None
            and bool(probe["state_terminated_before_measurement"])
            == contract.requires_terminated
        )
        instrument_rows.append(
            {
                "instrument_id": instrument_id,
                "cost": contract.cost,
                "latency_s": contract.latency_s,
                "sample_consumption_L": contract.sample_consumption_L,
                "destructive": contract.destructive,
                "requires_terminated": contract.requires_terminated,
                "probe": probe,
                "cost_delta_matches_contract": cost_matches,
                "sample_delta_matches_contract": sample_matches,
                "terminal_precondition_matches_contract": terminal_semantics_match,
                "latency_semantics": "declared_scheduling_latency_not_process_state_time",
                "passed": bool(
                    probe is not None
                    and probe["transaction_status"] == "committed"
                    and cost_matches
                    and sample_matches
                    and terminal_semantics_match
                ),
            }
        )

    observed_statuses = sorted(
        {
            "committed",
            constitution["transaction_status"],
            resource["environment_statuses"][1],
            *(probe["transaction_status"] for probe in failures.values()),
        }
    )
    declared_statuses = [item["status"] for item in PUBLIC_TRANSACTION_STATUS_SEMANTICS]
    gates = {
        "all_28_operation_contracts_routed": (
            len(operation_rows) == 28
            and all(row["kernel_id"] and row["domain_service_id"] for row in operation_rows)
        ),
        "all_28_operations_commit_in_valid_context": all(
            row["committed_probe"] is not None
            and row["committed_probe"]["transaction_status"] == "committed"
            for row in operation_rows
        ),
        "all_28_invalid_probes_preserve_physical_state": all(
            row["failure_probe"]["passed"] for row in operation_rows
        ),
        "constitution_failure_rolls_back_atomically": constitution["passed"],
        "all_5_instruments_charge_declared_cost_and_sample": all(
            row["passed"] for row in instrument_rows
        ),
        "campaign_hard_limits_and_replay_qualified": resource["passed"],
        "public_failure_status_vocabulary_matches_runtime": set(observed_statuses)
        == set(declared_statuses),
    }
    core: dict[str, Any] = {
        "schema_version": "chemworld-work-i-experiment-semantics-qualification-0.1",
        "operation_rows": operation_rows,
        "instrument_rows": instrument_rows,
        "failure_semantics": {
            "declared_transaction_statuses": list(PUBLIC_TRANSACTION_STATUS_SEMANTICS),
            "observed_statuses": observed_statuses,
            "invalid_probe_status_counts": dict(
                sorted(Counter(row["transaction_status"] for row in failures.values()).items())
            ),
            "constitution_rollback_probe": constitution,
            "physical_mutation_policy": (
                "candidate physical state commits only on committed; failures preserve the "
                "pre-action physical state and may apply a declared process penalty"
            ),
        },
        "resource_semantics": resource,
        "summary_counts": {
            "operation_contract_count": len(operation_rows),
            "operation_valid_commit_pass_count": sum(
                row["committed_probe"] is not None
                and row["committed_probe"]["transaction_status"] == "committed"
                for row in operation_rows
            ),
            "operation_invalid_state_preservation_pass_count": sum(
                row["failure_probe"]["passed"] for row in operation_rows
            ),
            "instrument_contract_count": len(instrument_rows),
            "instrument_probe_pass_count": sum(row["passed"] for row in instrument_rows),
            "transaction_status_count": len(declared_statuses),
        },
        "gates": gates,
        "passed": all(gates.values()),
        "claim_boundary": {
            "typed_operation_transaction_semantics": True,
            "campaign_resource_accounting_semantics": True,
            "failure_and_rollback_semantics": True,
            "synthetic_instrument_cost_semantics": True,
            "real_instrument_calibration_claim": False,
            "physical_laboratory_safety_claim": False,
        },
    }
    digest = _sha256(core)
    return {
        **core,
        "qualification_id": f"chemworld-work-i-experiment-semantics-{digest[:16]}",
        "qualification_sha256": digest,
    }


def build_markdown(report: dict[str, Any]) -> str:
    summary = report["summary_counts"]
    lines = [
        "# Work I Experimental Semantics Qualification",
        "",
        f"Qualification: `{report['qualification_id']}`  ",
        f"SHA-256: `{report['qualification_sha256']}`",
        "",
        "## Overall qualification",
        "",
        "| Semantic surface | Qualified result |",
        "| --- | --- |",
        (
            f"| Typed operations | {summary['operation_valid_commit_pass_count']}/"
            f"{summary['operation_contract_count']} committed in a valid context; "
            f"{summary['operation_invalid_state_preservation_pass_count']}/"
            f"{summary['operation_contract_count']} invalid probes preserved physical state |"
        ),
        (
            f"| Instruments | {summary['instrument_probe_pass_count']}/"
            f"{summary['instrument_contract_count']} matched declared cost, sample consumption, "
            "and terminal precondition |"
        ),
        (
            "| Resources | hard preflight limits, attempt charging, committed-only "
            "stock debits, and snapshot replay passed |"
        ),
        (
            "| Failures | validation, precondition/constitution rollback, and resource "
            "rejection remain distinct and replayable |"
        ),
        "",
        "## Operation qualification table",
        "",
        "| Operation | Module | Kind | Valid | Invalid status | Physical state kept |",
        "| --- | --- | --- | ---: | --- | ---: |",
    ]
    for row in report["operation_rows"]:
        lines.append(
            f"| `{row['operation_id']}` | `{row['module']}` | `{row['kind']}` | "
            f"{row['committed_probe']['transaction_status'] == 'committed'} | "
            f"`{row['failure_probe']['transaction_status']}` | "
            f"{row['failure_probe']['physical_state_unchanged']} |"
        )
    lines.extend(
        [
            "",
            "## Instrument qualification table",
            "",
            (
                "| Instrument | Cost | Latency (s) | Sample (L) | Destructive | "
                "Requires termination | Probe passed |"
            ),
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in report["instrument_rows"]:
        lines.append(
            f"| `{row['instrument_id']}` | {row['cost']:.3f} | {row['latency_s']:.0f} | "
            f"{row['sample_consumption_L']:.6f} | {row['destructive']} | "
            f"{row['requires_terminated']} | {row['passed']} |"
        )
    lines.extend(
        [
            "",
            "## Transaction and resource interpretation",
            "",
            "Only `committed` applies a candidate physical transition. `validation_failed`, "
            "`rolled_back`, and `campaign_resource_rejected` retain the pre-action physical "
            "state while preserving the declared attempt or process penalty in the audit trail. "
            "The campaign ledger reserves attempts before execution, debits stocks and vessel or "
            "instrument counts only for committed outcomes, hashes every event, and round-trips "
            "exactly from its snapshot.",
            "",
            "Instrument latency is a declared scheduling quantity, not elapsed physical process "
            "time. These are synthetic instrument and executable-world semantics; the table does "
            "not claim calibration against physical laboratory devices or real-world safety.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    json_text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    markdown_text = build_markdown(report)
    if args.check:
        if args.json_output.read_text(encoding="utf-8") != json_text:
            raise SystemExit("machine semantics report does not match deterministic rebuild")
        if args.markdown_output.read_text(encoding="utf-8") != markdown_text:
            raise SystemExit("human semantics report does not match deterministic rebuild")
    else:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json_text, encoding="utf-8")
        args.markdown_output.write_text(markdown_text, encoding="utf-8")
    print(
        json.dumps(
            {
                **report["summary_counts"],
                "qualification_sha256": report["qualification_sha256"],
                "passed": report["passed"],
            },
            sort_keys=True,
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
