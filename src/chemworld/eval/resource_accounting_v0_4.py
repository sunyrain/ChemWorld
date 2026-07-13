"""Fail-closed, cross-family resource accounting for formal benchmark runs."""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
from typing import Any, Literal, TypeGuard, cast

from chemworld.eval.interaction_strata import RESOURCE_AXES
from chemworld.eval.method_protocol import (
    METHOD_RESOURCE_LEDGER_VERSION,
    METHOD_RESOURCE_USAGE_VERSION,
)

RESOURCE_ACCOUNTING_VERSION = "chemworld-resource-accounting-0.4"
RESOURCE_AGGREGATION_VERSION = "chemworld-resource-aggregation-0.4"
PROVIDER_PRICING_VERSION = "chemworld-provider-pricing-0.4"
PROVIDER_RECEIPT_VERSION = "chemworld-provider-receipt-0.4"
CLASSIC_COMPUTE_EVENT_VERSION = "chemworld-classic-compute-event-0.4"
RL_TRAINING_RESOURCE_VERSION = "chemworld-rl-training-resource-0.4"

ResourceProfile = Literal[
    "classic_recipe",
    "operation_baseline",
    "rl_evaluation",
    "live_llm_evaluation",
]
MethodKind = Literal["classic", "rl", "live_llm"]

RESOURCE_DIMENSIONS = {
    "complete_experiment_count": "count",
    "operation_count": "count",
    "measurement_count": "count",
    "decision_count": "count",
    "provider_request_count": "count",
    "provider_retry_count": "count",
    "input_token_count": "token",
    "output_token_count": "token",
    "monetary_cost_usd": "USD",
    "fit_count": "count",
    "acquisition_optimization_count": "count",
    "training_environment_step_count": "environment_step",
    "cpu_time_s": "second",
    "gpu_time_s": "second",
    "wall_time_s": "second",
}

_COUNT_AXES = tuple(
    axis
    for axis in RESOURCE_AXES
    if RESOURCE_DIMENSIONS[axis] in {"count", "token", "environment_step"}
)
_FLOAT_AXES = tuple(axis for axis in RESOURCE_AXES if axis not in _COUNT_AXES)
_PROVIDER_PROVENANCE_FIELDS = {
    "provider",
    "model_id",
    "model_snapshot_or_access_date",
    "prompt_hash",
    "request_parameters",
    "tokenizer_or_provider_usage_source",
}


class ResourceAccountingError(RuntimeError):
    """Raised when aggregation inputs are ambiguous rather than merely incomplete."""


def canonical_sha256(payload: Mapping[str, Any]) -> str:
    """Return a deterministic JSON digest for a resource-control object."""

    encoded = json.dumps(
        payload,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def bind_pricing_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Create a digest-bound immutable provider pricing snapshot."""

    snapshot = dict(payload)
    snapshot.setdefault("schema_version", PROVIDER_PRICING_VERSION)
    snapshot.pop("pricing_version_sha256", None)
    snapshot["pricing_version_sha256"] = canonical_sha256(snapshot)
    return snapshot


def audit_cell_resource_accounting(
    records: Sequence[Mapping[str, Any]],
    *,
    cell_identity_sha256: str,
    method_id: str,
    method_kind: MethodKind,
    resource_profile: ResourceProfile,
    provider_receipts: Sequence[Mapping[str, Any]] = (),
    pricing_snapshot: Mapping[str, Any] | None = None,
    classic_compute_events: Sequence[Mapping[str, Any]] = (),
    classic_compute_required: bool = False,
    rl_checkpoint_sha256: str | None = None,
) -> dict[str, Any]:
    """Reconcile one retained trajectory into the preregistered 15 resource axes.

    Evidence defects are returned as an accounting-failure report so the cell can
    remain in the statistical denominator.  Unknown monetary cost is represented
    by ``None`` and is never silently converted to zero.
    """

    reasons: list[str] = []
    axes = _empty_axes()
    ledger: Mapping[str, Any] = {}
    usage: Mapping[str, Any] = {}

    if not _is_sha256(cell_identity_sha256):
        reasons.append("cell_identity_invalid")
    if not method_id.strip():
        reasons.append("method_id_missing")
    expected_profiles = {
        "classic": {"classic_recipe", "operation_baseline"},
        "rl": {"rl_evaluation"},
        "live_llm": {"live_llm_evaluation"},
    }
    if resource_profile not in expected_profiles[method_kind]:
        reasons.append("method_kind_resource_profile_mismatch")

    if not records or not all(isinstance(record, Mapping) for record in records):
        reasons.append("trajectory_empty_or_invalid")
    else:
        axes["operation_count"] = len(records)
        axes["decision_count"] = len(records)
        axes["measurement_count"] = sum(
            _is_measurement(record.get("action")) for record in records
        )
        candidate = records[-1].get("method_resources")
        if isinstance(candidate, Mapping):
            ledger = candidate
        else:
            reasons.append("final_method_ledger_missing")

    if ledger:
        _audit_legacy_ledger(ledger, records=records, reasons=reasons)
        complete_count = ledger.get("complete_experiment_count")
        if _is_nonnegative_int(complete_count):
            axes["complete_experiment_count"] = complete_count
        else:
            axes["complete_experiment_count"] = None
        run_wall = ledger.get("run_wall_time_s")
        axes["wall_time_s"] = _finite_or_none(run_wall)
        if axes["wall_time_s"] is None:
            reasons.append("evaluation_wall_time_invalid")
        usage_payload = ledger.get("agent_usage")
        if isinstance(usage_payload, Mapping):
            usage = usage_payload
        else:
            reasons.append("agent_usage_missing")

    if usage:
        _audit_legacy_usage(usage, method_kind=method_kind, reasons=reasons)
        axes["cpu_time_s"] = _finite_or_none(usage.get("cpu_time_s"))
        axes["gpu_time_s"] = _finite_or_none(usage.get("gpu_time_s"))
        for axis in ("cpu_time_s", "gpu_time_s"):
            if axes[axis] is None:
                reasons.append(f"{axis}_invalid")
        training_steps = usage.get("training_environment_step_count")
        if not _is_nonnegative_int(training_steps):
            axes["training_environment_step_count"] = None
            reasons.append("training_environment_step_count_invalid")
        elif training_steps != 0:
            axes["training_environment_step_count"] = training_steps
            reasons.append("training_resources_mixed_into_evaluation_cell")

    classic_summary = _audit_classic_events(
        classic_compute_events,
        cell_identity_sha256=cell_identity_sha256,
        resource_profile=resource_profile,
        required=classic_compute_required,
        evaluation_cpu_time_s=axes["cpu_time_s"],
        evaluation_wall_time_s=axes["wall_time_s"],
        reasons=reasons,
    )
    axes["fit_count"] = classic_summary["fit_count"]
    axes["acquisition_optimization_count"] = classic_summary[
        "acquisition_optimization_count"
    ]

    provider_summary = _audit_provider_receipts(
        provider_receipts,
        pricing_snapshot=pricing_snapshot,
        expected_decision_count=axes["decision_count"],
        method_kind=method_kind,
        legacy_usage=usage,
        reasons=reasons,
    )
    for axis in (
        "provider_request_count",
        "provider_retry_count",
        "input_token_count",
        "output_token_count",
        "monetary_cost_usd",
    ):
        axes[axis] = provider_summary[axis]

    if method_kind == "rl":
        if not _is_sha256(rl_checkpoint_sha256):
            reasons.append("rl_checkpoint_binding_missing")
    elif rl_checkpoint_sha256 is not None:
        reasons.append("non_rl_cell_declares_rl_checkpoint")

    _validate_axes(axes, reasons=reasons)
    unique_reasons = sorted(set(reasons))
    complete = not unique_reasons
    return {
        "schema_version": RESOURCE_ACCOUNTING_VERSION,
        "status": "complete" if complete else "accounting_failure",
        "accounting_complete": complete,
        "retained_in_statistical_denominator": True,
        "cell_identity_sha256": cell_identity_sha256,
        "method_id": method_id,
        "method_kind": method_kind,
        "resource_profile": resource_profile,
        "rl_checkpoint_sha256": rl_checkpoint_sha256,
        "axes": axes,
        "axis_dimensions": dict(RESOURCE_DIMENSIONS),
        "provider_accounting": provider_summary,
        "classic_compute_accounting": classic_summary,
        "failure_reasons": unique_reasons,
        "cross_resource_scalarization": None,
    }


def audit_rl_training_resource(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a checkpoint-level training ledger kept outside evaluation cells."""

    reasons: list[str] = []
    if payload.get("schema_version") != RL_TRAINING_RESOURCE_VERSION:
        reasons.append("training_resource_schema_invalid")
    training_run_id = payload.get("training_run_id")
    checkpoint = payload.get("checkpoint_sha256")
    source_manifest = payload.get("source_manifest_sha256")
    if not isinstance(training_run_id, str) or not training_run_id.strip():
        reasons.append("training_run_id_missing")
    if not _is_sha256(checkpoint):
        reasons.append("checkpoint_sha256_invalid")
    if not _is_sha256(source_manifest):
        reasons.append("source_manifest_sha256_invalid")
    if payload.get("accounting_complete") is not True:
        reasons.append("training_resource_declared_incomplete")

    requested = payload.get("requested_training_environment_step_count")
    actual = payload.get("training_environment_step_count")
    if not _is_nonnegative_int(requested) or requested <= 0:
        reasons.append("requested_training_steps_invalid")
    if not _is_nonnegative_int(actual) or actual <= 0:
        reasons.append("training_steps_invalid")
    if _is_nonnegative_int(requested) and _is_nonnegative_int(actual) and requested != actual:
        reasons.append("training_step_budget_mismatch")

    resource_values: dict[str, int | float | None] = {
        "training_environment_step_count": actual if _is_nonnegative_int(actual) else None,
        "cpu_time_s": _finite_or_none(payload.get("cpu_time_s")),
        "gpu_time_s": _finite_or_none(payload.get("gpu_time_s")),
        "wall_time_s": _finite_or_none(payload.get("wall_time_s")),
    }
    for axis in ("cpu_time_s", "gpu_time_s", "wall_time_s"):
        if resource_values[axis] is None:
            reasons.append(f"training_{axis}_invalid")
    unique_reasons = sorted(set(reasons))
    complete = not unique_reasons
    return {
        "schema_version": RL_TRAINING_RESOURCE_VERSION,
        "status": "complete" if complete else "accounting_failure",
        "accounting_complete": complete,
        "training_run_id": training_run_id,
        "checkpoint_sha256": checkpoint,
        "source_manifest_sha256": source_manifest,
        "resources": resource_values,
        "failure_reasons": unique_reasons,
        "reported_separately_from_evaluation": True,
    }


def aggregate_resource_accounting(
    cell_reports: Sequence[Mapping[str, Any]],
    *,
    matrix_elapsed_wall_time_s: float,
    rl_training_reports: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Aggregate unique evaluation cells without summing parallel wall time.

    Additive evaluation axes are summed once per unique cell.  Matrix wall time
    is the externally observed elapsed duration, while the sum of cell wall
    times is retained under a diagnostic field and never substituted for it.
    RL training artifacts are deduplicated by checkpoint and reported in a
    separate section instead of being allocated repeatedly to evaluation cells.
    """

    if not _is_nonnegative_finite(matrix_elapsed_wall_time_s):
        raise ResourceAccountingError("matrix elapsed wall time must be finite and non-negative")
    identities: set[str] = set()
    failure_reasons: list[str] = []
    evaluation = _empty_axes()
    evaluation["wall_time_s"] = float(matrix_elapsed_wall_time_s)
    summed_cell_wall = 0.0
    referenced_checkpoints: set[str] = set()

    for report in cell_reports:
        identity = report.get("cell_identity_sha256")
        if not isinstance(identity, str) or identity in identities:
            raise ResourceAccountingError("cell resource reports must have unique identities")
        identities.add(identity)
        if report.get("schema_version") != RESOURCE_ACCOUNTING_VERSION:
            failure_reasons.append(f"cell:{identity}:schema_invalid")
        if report.get("accounting_complete") is not True:
            failure_reasons.append(f"cell:{identity}:accounting_incomplete")
        axes = report.get("axes")
        if not isinstance(axes, Mapping) or set(axes) != set(RESOURCE_AXES):
            failure_reasons.append(f"cell:{identity}:axes_invalid")
            continue
        for axis in RESOURCE_AXES:
            value = axes.get(axis)
            if value is None:
                failure_reasons.append(f"cell:{identity}:{axis}_missing")
                continue
            if axis == "wall_time_s":
                summed_cell_wall += float(value)
            else:
                evaluation[axis] = _sum_axis(evaluation[axis], value, axis=axis)
        checkpoint = report.get("rl_checkpoint_sha256")
        if checkpoint is not None:
            if not _is_sha256(checkpoint):
                failure_reasons.append(f"cell:{identity}:rl_checkpoint_invalid")
            else:
                referenced_checkpoints.add(checkpoint)

    training_by_checkpoint: dict[str, Mapping[str, Any]] = {}
    training_totals: dict[str, int | float] = {
        "training_environment_step_count": 0,
        "cpu_time_s": 0.0,
        "gpu_time_s": 0.0,
        "wall_time_s": 0.0,
    }
    training_run_ids: set[str] = set()
    for report in rl_training_reports:
        checkpoint = report.get("checkpoint_sha256")
        run_id = report.get("training_run_id")
        if not isinstance(checkpoint, str) or checkpoint in training_by_checkpoint:
            raise ResourceAccountingError("RL training reports must be unique by checkpoint")
        if not isinstance(run_id, str) or run_id in training_run_ids:
            raise ResourceAccountingError("RL training reports must have unique training run ids")
        training_by_checkpoint[checkpoint] = report
        training_run_ids.add(run_id)
        if report.get("accounting_complete") is not True:
            failure_reasons.append(f"checkpoint:{checkpoint}:training_accounting_incomplete")
            continue
        if checkpoint not in referenced_checkpoints:
            failure_reasons.append(f"checkpoint:{checkpoint}:training_report_unreferenced")
            continue
        resources = report.get("resources")
        if not isinstance(resources, Mapping):
            failure_reasons.append(f"checkpoint:{checkpoint}:training_resources_missing")
            continue
        for axis in training_totals:
            value = resources.get(axis)
            if value is None:
                failure_reasons.append(f"checkpoint:{checkpoint}:{axis}_missing")
            else:
                training_totals[axis] += value

    for checkpoint in sorted(referenced_checkpoints - set(training_by_checkpoint)):
        failure_reasons.append(f"checkpoint:{checkpoint}:training_report_missing")

    unique_reasons = sorted(set(failure_reasons))
    complete = not unique_reasons
    return {
        "schema_version": RESOURCE_AGGREGATION_VERSION,
        "status": "complete" if complete else "accounting_failure",
        "accounting_complete": complete,
        "cell_count": len(identities),
        "evaluation_resource_totals": evaluation,
        "evaluation_axis_dimensions": dict(RESOURCE_DIMENSIONS),
        "summed_cell_wall_time_s_diagnostic_only": summed_cell_wall,
        "matrix_elapsed_wall_time_s": float(matrix_elapsed_wall_time_s),
        "parallel_wall_time_sum_used_as_elapsed": False,
        "rl_training_resource_totals_separate": training_totals,
        "unique_rl_checkpoint_count": len(training_by_checkpoint),
        "rl_training_charged_per_evaluation_cell": False,
        "failure_reasons": unique_reasons,
        "cross_resource_scalarization": None,
    }


def _audit_legacy_ledger(
    ledger: Mapping[str, Any],
    *,
    records: Sequence[Mapping[str, Any]],
    reasons: list[str],
) -> None:
    if ledger.get("schema_version") != METHOD_RESOURCE_LEDGER_VERSION:
        reasons.append("method_ledger_schema_invalid")
    if ledger.get("accounting_complete") is not True:
        reasons.append("method_ledger_declared_incomplete")
    operation_count = ledger.get("operation_count")
    if not _is_nonnegative_int(operation_count) or operation_count != len(records):
        reasons.append("method_ledger_operation_count_incoherent")
    complete_count = ledger.get("complete_experiment_count")
    if not _is_nonnegative_int(complete_count):
        reasons.append("method_ledger_experiment_count_invalid")
    decision = _finite_or_none(ledger.get("decision_wall_time_s"))
    update = _finite_or_none(ledger.get("update_wall_time_s"))
    run = _finite_or_none(ledger.get("run_wall_time_s"))
    if decision is None or update is None or run is None:
        reasons.append("method_ledger_time_invalid")
    elif decision + update > run + 1e-9:
        reasons.append("method_ledger_component_time_exceeds_elapsed")


def _audit_legacy_usage(
    usage: Mapping[str, Any], *, method_kind: MethodKind, reasons: list[str]
) -> None:
    if usage.get("schema_version") != METHOD_RESOURCE_USAGE_VERSION:
        reasons.append("agent_usage_schema_invalid")
    if usage.get("accounting_complete") is not True:
        reasons.append("agent_usage_declared_incomplete")
    if not isinstance(usage.get("usage_source"), str) or not usage["usage_source"].strip():
        reasons.append("agent_usage_source_missing")
    for field in (
        "model_call_count",
        "input_token_count",
        "output_token_count",
        "training_environment_step_count",
    ):
        if not _is_nonnegative_int(usage.get(field)):
            reasons.append(f"agent_usage_{field}_invalid")
    for field in ("monetary_cost_usd", "cpu_time_s", "gpu_time_s"):
        if _finite_or_none(usage.get(field)) is None:
            reasons.append(f"agent_usage_{field}_invalid")
    if method_kind == "live_llm":
        provenance = usage.get("model_provenance")
        if not isinstance(provenance, Mapping) or not _PROVIDER_PROVENANCE_FIELDS.issubset(
            provenance
        ):
            reasons.append("online_model_provenance_incomplete")


def _audit_classic_events(
    events: Sequence[Mapping[str, Any]],
    *,
    cell_identity_sha256: str,
    resource_profile: ResourceProfile,
    required: bool,
    evaluation_cpu_time_s: int | float | None,
    evaluation_wall_time_s: int | float | None,
    reasons: list[str],
) -> dict[str, Any]:
    fit_count = 0
    acquisition_count = 0
    event_ids: set[str] = set()
    cpu_component = 0.0
    wall_component = 0.0
    if events and resource_profile != "classic_recipe":
        reasons.append("classic_compute_events_on_nonclassic_profile")
    for event in events:
        if event.get("schema_version") != CLASSIC_COMPUTE_EVENT_VERSION:
            reasons.append("classic_compute_event_schema_invalid")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id.strip() or event_id in event_ids:
            reasons.append("classic_compute_event_id_duplicate_or_missing")
        else:
            event_ids.add(event_id)
        if event.get("cell_identity_sha256") != cell_identity_sha256:
            reasons.append("classic_compute_event_cell_mismatch")
        kind = event.get("event_kind")
        if kind == "fit":
            fit_count += 1
        elif kind == "acquisition_optimization":
            acquisition_count += 1
        else:
            reasons.append("classic_compute_event_kind_invalid")
        cpu = _finite_or_none(event.get("cpu_time_s"))
        wall = _finite_or_none(event.get("wall_time_s"))
        if cpu is None or wall is None:
            reasons.append("classic_compute_event_time_invalid")
        else:
            cpu_component += cpu
            wall_component += wall
    if required and (fit_count == 0 or acquisition_count == 0):
        reasons.append("required_classic_fit_or_acquisition_event_missing")
    if evaluation_cpu_time_s is not None and cpu_component > evaluation_cpu_time_s + 1e-9:
        reasons.append("classic_component_cpu_exceeds_evaluation_cpu")
    if evaluation_wall_time_s is not None and wall_component > evaluation_wall_time_s + 1e-9:
        reasons.append("classic_component_wall_exceeds_evaluation_elapsed")
    return {
        "schema_version": CLASSIC_COMPUTE_EVENT_VERSION,
        "fit_count": fit_count,
        "acquisition_optimization_count": acquisition_count,
        "event_count": len(events),
        "component_cpu_time_s": cpu_component,
        "component_wall_time_s": wall_component,
        "component_times_already_in_evaluation_totals": True,
    }


def _audit_provider_receipts(
    receipts: Sequence[Mapping[str, Any]],
    *,
    pricing_snapshot: Mapping[str, Any] | None,
    expected_decision_count: int | float | None,
    method_kind: MethodKind,
    legacy_usage: Mapping[str, Any],
    reasons: list[str],
) -> dict[str, Any]:
    if method_kind != "live_llm":
        if receipts or pricing_snapshot is not None:
            reasons.append("provider_evidence_on_offline_method")
        for field in (
            "model_call_count",
            "input_token_count",
            "output_token_count",
            "monetary_cost_usd",
        ):
            value = legacy_usage.get(field, 0)
            if value != 0:
                reasons.append("offline_method_has_provider_usage")
                break
        return {
            "schema_version": PROVIDER_RECEIPT_VERSION,
            "provider_request_count": 0,
            "provider_retry_count": 0,
            "input_token_count": 0,
            "output_token_count": 0,
            "monetary_cost_usd": 0.0,
            "pricing_version_sha256": None,
            "failed_request_count": 0,
            "prompt_cache_hit_token_count": 0,
            "prompt_cache_miss_token_count": 0,
            "duplicate_request_charged": False,
        }

    pricing, pricing_digest = _validate_pricing_snapshot(pricing_snapshot, reasons=reasons)
    request_ids: set[str] = set()
    attempts_by_decision: dict[int, list[int]] = defaultdict(list)
    input_tokens = 0
    output_tokens = 0
    cache_hit_tokens = 0
    cache_miss_tokens = 0
    failed_requests = 0
    recomputed_cost = Decimal("0")
    billed_cost = Decimal("0")
    cost_known = pricing is not None

    for receipt in receipts:
        if receipt.get("schema_version") != PROVIDER_RECEIPT_VERSION:
            reasons.append("provider_receipt_schema_invalid")
        request_id = receipt.get("request_id")
        if not isinstance(request_id, str) or not request_id.strip() or request_id in request_ids:
            reasons.append("provider_request_id_duplicate_or_missing")
        else:
            request_ids.add(request_id)
        decision_index = receipt.get("logical_decision_index")
        attempt_index = receipt.get("attempt_index")
        if not _is_positive_int(decision_index) or not _is_positive_int(attempt_index):
            reasons.append("provider_decision_or_attempt_index_invalid")
        else:
            attempts_by_decision[decision_index].append(attempt_index)
        status = receipt.get("status")
        if status not in {"succeeded", "failed"}:
            reasons.append("provider_receipt_status_invalid")
        failed_requests += int(status == "failed")
        if receipt.get("usage_complete") is not True:
            reasons.append("provider_usage_missing")
            cost_known = False
        if receipt.get("billable") is not True:
            reasons.append("provider_request_unbillable")
            cost_known = False
        if receipt.get("usage_source") != "provider_response":
            reasons.append("provider_usage_source_invalid")
        if pricing is not None:
            if receipt.get("provider") != pricing.get("provider"):
                reasons.append("provider_receipt_provider_mismatch")
            if receipt.get("model_id") != pricing.get("model_id"):
                reasons.append("provider_receipt_model_mismatch")
            if receipt.get("pricing_version_sha256") != pricing_digest:
                reasons.append("provider_receipt_pricing_version_mismatch")
                cost_known = False
        input_count = receipt.get("input_token_count")
        output_count = receipt.get("output_token_count")
        hit_count = receipt.get("input_cache_hit_token_count")
        miss_count = receipt.get("input_cache_miss_token_count")
        if not all(
            _is_nonnegative_int(value)
            for value in (input_count, output_count, hit_count, miss_count)
        ):
            reasons.append("provider_receipt_token_count_invalid")
            cost_known = False
            continue
        input_count_value = cast(int, input_count)
        output_count_value = cast(int, output_count)
        hit_count_value = cast(int, hit_count)
        miss_count_value = cast(int, miss_count)
        if hit_count_value + miss_count_value != input_count_value:
            reasons.append("provider_cache_token_breakdown_incoherent")
            cost_known = False
        input_tokens += input_count_value
        output_tokens += output_count_value
        cache_hit_tokens += hit_count_value
        cache_miss_tokens += miss_count_value
        billed = _decimal_or_none(receipt.get("billed_cost_usd"))
        if billed is None or billed < 0:
            reasons.append("provider_billed_cost_missing_or_invalid")
            cost_known = False
        else:
            billed_cost += billed
        if pricing is not None:
            expected_cost = _provider_cost(
                cache_hit_tokens=hit_count_value,
                cache_miss_tokens=miss_count_value,
                output_tokens=output_count_value,
                pricing=pricing,
            )
            if expected_cost is None:
                reasons.append("provider_pricing_rate_invalid")
                cost_known = False
            else:
                recomputed_cost += expected_cost
                if billed is not None and abs(expected_cost - billed) > Decimal("1e-12"):
                    reasons.append("provider_billed_cost_mismatch")
                    cost_known = False

    decision_count = int(expected_decision_count or 0)
    expected_decisions = set(range(1, decision_count + 1))
    if set(attempts_by_decision) != expected_decisions:
        reasons.append("provider_receipts_do_not_cover_every_logical_decision")
    for attempts in attempts_by_decision.values():
        if sorted(attempts) != list(range(1, len(attempts) + 1)):
            reasons.append("provider_retry_sequence_incoherent")
    retry_count = sum(max(len(attempts) - 1, 0) for attempts in attempts_by_decision.values())
    if not receipts:
        reasons.append("provider_receipts_missing")
        cost_known = False
    if recomputed_cost != billed_cost:
        reasons.append("provider_total_bill_mismatch")
        cost_known = False

    legacy_bindings = {
        "model_call_count": len(receipts),
        "input_token_count": input_tokens,
        "output_token_count": output_tokens,
    }
    for field, expected in legacy_bindings.items():
        if legacy_usage.get(field) != expected:
            reasons.append(f"provider_{field}_ledger_mismatch")
    legacy_cost = _decimal_or_none(legacy_usage.get("monetary_cost_usd"))
    if legacy_cost is None or abs(legacy_cost - billed_cost) > Decimal("1e-12"):
        reasons.append("provider_monetary_cost_ledger_mismatch")
        cost_known = False

    return {
        "schema_version": PROVIDER_RECEIPT_VERSION,
        "provider_request_count": len(receipts),
        "provider_retry_count": retry_count,
        "input_token_count": input_tokens,
        "output_token_count": output_tokens,
        "monetary_cost_usd": float(billed_cost) if cost_known else None,
        "pricing_version_sha256": pricing_digest,
        "failed_request_count": failed_requests,
        "prompt_cache_hit_token_count": cache_hit_tokens,
        "prompt_cache_miss_token_count": cache_miss_tokens,
        "duplicate_request_charged": False,
    }


def _validate_pricing_snapshot(
    snapshot: Mapping[str, Any] | None, *, reasons: list[str]
) -> tuple[Mapping[str, Any] | None, str | None]:
    if not isinstance(snapshot, Mapping):
        reasons.append("provider_pricing_snapshot_missing")
        return None, None
    if snapshot.get("schema_version") != PROVIDER_PRICING_VERSION:
        reasons.append("provider_pricing_schema_invalid")
    if snapshot.get("currency") != "USD":
        reasons.append("provider_pricing_currency_invalid")
    for field in ("provider", "model_id", "access_date"):
        if not isinstance(snapshot.get(field), str) or not str(snapshot[field]).strip():
            reasons.append(f"provider_pricing_{field}_missing")
    supplied = snapshot.get("pricing_version_sha256")
    unsigned = dict(snapshot)
    unsigned.pop("pricing_version_sha256", None)
    computed = canonical_sha256(unsigned)
    if supplied != computed:
        reasons.append("provider_pricing_digest_mismatch")
        return None, computed
    for field in (
        "input_cache_hit_per_million_usd",
        "input_cache_miss_per_million_usd",
        "output_per_million_usd",
    ):
        value = _decimal_or_none(snapshot.get(field))
        if value is None or value < 0:
            reasons.append(f"provider_pricing_{field}_invalid")
            return None, computed
    return snapshot, computed


def _provider_cost(
    *,
    cache_hit_tokens: int,
    cache_miss_tokens: int,
    output_tokens: int,
    pricing: Mapping[str, Any],
) -> Decimal | None:
    hit_rate = _decimal_or_none(pricing.get("input_cache_hit_per_million_usd"))
    miss_rate = _decimal_or_none(pricing.get("input_cache_miss_per_million_usd"))
    output_rate = _decimal_or_none(pricing.get("output_per_million_usd"))
    if hit_rate is None or miss_rate is None or output_rate is None:
        return None
    return (
        Decimal(cache_hit_tokens) * hit_rate
        + Decimal(cache_miss_tokens) * miss_rate
        + Decimal(output_tokens) * output_rate
    ) / Decimal(1_000_000)


def _validate_axes(axes: Mapping[str, Any], *, reasons: list[str]) -> None:
    if set(axes) != set(RESOURCE_AXES):
        reasons.append("resource_axis_set_mismatch")
        return
    for axis in _COUNT_AXES:
        value = axes[axis]
        if value is not None and not _is_nonnegative_int(value):
            reasons.append(f"resource_axis_{axis}_invalid")
    for axis in _FLOAT_AXES:
        value = axes[axis]
        if value is not None and not _is_nonnegative_finite(value):
            reasons.append(f"resource_axis_{axis}_invalid")


def _empty_axes() -> dict[str, int | float | None]:
    return {
        axis: (0 if axis in _COUNT_AXES else 0.0)
        for axis in RESOURCE_AXES
    }


def _sum_axis(current: Any, value: Any, *, axis: str) -> int | float:
    if axis in _COUNT_AXES:
        if not _is_nonnegative_int(current) or not _is_nonnegative_int(value):
            raise ResourceAccountingError(f"invalid count axis during aggregation: {axis}")
        return current + value
    if not _is_nonnegative_finite(current) or not _is_nonnegative_finite(value):
        raise ResourceAccountingError(f"invalid float axis during aggregation: {axis}")
    return float(current) + float(value)


def _is_measurement(action: Any) -> int:
    return int(isinstance(action, Mapping) and action.get("operation") == "measure")


def _is_sha256(value: Any) -> TypeGuard[str]:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _is_nonnegative_int(value: Any) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_positive_int(value: Any) -> TypeGuard[int]:
    return _is_nonnegative_int(value) and value > 0


def _is_nonnegative_finite(value: Any) -> TypeGuard[int | float]:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and value >= 0
    )


def _finite_or_none(value: Any) -> float | None:
    return float(value) if _is_nonnegative_finite(value) else None


def _decimal_or_none(value: Any) -> Decimal | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return result if result.is_finite() else None


__all__ = [
    "CLASSIC_COMPUTE_EVENT_VERSION",
    "PROVIDER_PRICING_VERSION",
    "PROVIDER_RECEIPT_VERSION",
    "RESOURCE_ACCOUNTING_VERSION",
    "RESOURCE_AGGREGATION_VERSION",
    "RESOURCE_DIMENSIONS",
    "RL_TRAINING_RESOURCE_VERSION",
    "ResourceAccountingError",
    "aggregate_resource_accounting",
    "audit_cell_resource_accounting",
    "audit_rl_training_resource",
    "bind_pricing_snapshot",
    "canonical_sha256",
]
