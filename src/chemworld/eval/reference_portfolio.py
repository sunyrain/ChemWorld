"""Fail-closed planning and evidence freezing for independent references."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.reference_regret import (
    load_reference_regret_protocol,
    reference_regret_protocol_sha256,
)
from chemworld.eval.result_artifacts import validate_verified_evaluation_result
from chemworld.physchem.mechanism_library import configuration_root

REFERENCE_PORTFOLIO_PLAN_VERSION = "chemworld-reference-portfolio-plan-0.1"
REFERENCE_PORTFOLIO_EVIDENCE_VERSION = "chemworld-reference-portfolio-evidence-0.1"
REFERENCE_PORTFOLIO_AUDIT_VERSION = "chemworld-reference-portfolio-audit-0.1"
DEFAULT_REFERENCE_PORTFOLIO_PLAN_PATH = (
    configuration_root() / "benchmark" / "reference_portfolio_vnext.json"
)
ROOT = Path(__file__).resolve().parents[3]


class ReferencePortfolioError(ValueError):
    """Raised when a reference-search plan or evidence set fails closed."""


def load_reference_portfolio_plan(
    path: str | Path = DEFAULT_REFERENCE_PORTFOLIO_PLAN_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReferencePortfolioError("reference portfolio plan must be a JSON object")
    return payload


def reference_portfolio_plan_sha256(plan: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(plan, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def build_reference_run_plan(
    plan: Mapping[str, Any],
    reference_protocol: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    protocol = dict(reference_protocol or load_reference_regret_protocol())
    _validate_plan(plan, protocol)
    namespace = str(plan["builder_seed_namespace"])
    runs: list[dict[str, Any]] = []
    for task_id in protocol["formal_task_ids"]:
        for benchmark_seed in protocol["seed_ids"]:
            for replicate_id in plan["replicate_ids"]:
                run_key = f"{task_id}:seed{int(benchmark_seed)}:{replicate_id}"
                runs.append(
                    {
                        "run_id": hashlib.sha256(
                            f"{namespace}\0{run_key}".encode()
                        ).hexdigest(),
                        "task_id": str(task_id),
                        "benchmark_seed": int(benchmark_seed),
                        "replicate_id": str(replicate_id),
                        "builder_seed": _derived_seed(namespace, run_key),
                        "builder_id": str(plan["builder_id"]),
                        "source_split": str(plan["source_split"]),
                        "evaluation_policy": str(plan["evaluation_policy"]),
                        "experiment_budget": int(plan["experiment_budget"]),
                    }
                )
    return runs


def audit_reference_portfolio(
    plan: Mapping[str, Any],
    *,
    reference_protocol: Mapping[str, Any] | None = None,
    evidence_manifest: Mapping[str, Any] | None = None,
    workspace_root: str | Path = ROOT,
) -> dict[str, Any]:
    protocol = dict(reference_protocol or load_reference_regret_protocol())
    runs = build_reference_run_plan(plan, protocol)
    plan_digest = reference_portfolio_plan_sha256(plan)
    protocol_digest = reference_regret_protocol_sha256(protocol)
    dependencies = _dependency_evidence(plan, ROOT)
    probes = _adversarial_probes(plan, protocol, runs)
    checks = {
        "candidate_is_non_claiming": plan.get("benchmark_claim_allowed") is False,
        "formal_results_flag_is_false": plan.get("formal_results_present") is False,
        "reference_protocol_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "reference_is_not_oracle": protocol.get("reference_semantics", {}).get("is_oracle")
        is False,
        "builder_role_matches_protocol": plan.get("builder_role")
        == protocol.get("independence_policy", {}).get("reference_builder_role"),
        "source_split_matches_protocol": plan.get("source_split")
        == protocol.get("independence_policy", {}).get("reference_source_split"),
        "builder_excluded_from_evaluated_methods": plan.get("builder_id")
        not in set(plan.get("evaluated_method_ids", ())),
        "run_ids_unique": len({item["run_id"] for item in runs}) == len(runs),
        "builder_seeds_unique": len({item["builder_seed"] for item in runs})
        == len(runs),
        "dependencies_ready": bool(dependencies)
        and all(item["ready"] for item in dependencies.values()),
        "adversarial_probes_pass": bool(probes) and all(probes.values()),
    }
    controls_ready = all(checks.values())
    estimates: list[dict[str, Any]] = []
    evidence_complete = False
    evidence_digest = None
    if evidence_manifest is not None:
        evidence_digest = _canonical_sha256(evidence_manifest)
        estimates = freeze_reference_estimates(
            plan,
            protocol,
            evidence_manifest,
            workspace_root=workspace_root,
        )
        evidence_complete = True
    expected_reference_cells = (
        len(protocol["formal_task_ids"])
        * len(protocol["seed_ids"])
        * len(protocol["metrics"])
    )
    status = (
        "controls_ready_candidate_evidence_complete"
        if controls_ready and evidence_complete
        else "controls_ready_evidence_missing"
        if controls_ready
        else "controls_failed"
    )
    return {
        "schema_version": REFERENCE_PORTFOLIO_AUDIT_VERSION,
        "plan_id": plan.get("plan_id"),
        "plan_sha256": plan_digest,
        "reference_protocol_id": protocol.get("protocol_id"),
        "reference_protocol_sha256": protocol_digest,
        "status": status,
        "controls_ready": controls_ready,
        "evidence_supplied": evidence_manifest is not None,
        "evidence_complete": evidence_complete,
        "evidence_manifest_sha256": evidence_digest,
        "planned_source_run_count": len(runs),
        "expected_reference_cell_count": expected_reference_cells,
        "candidate_reference_record_count": len(estimates),
        "source_count_per_task_seed": len(plan["replicate_ids"]),
        "checks": checks,
        "adversarial_probes": probes,
        "dependencies": dependencies,
        "formal_results_present": False,
        "parent_task_complete": False,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "remaining_release_gates": list(plan.get("remaining_release_gates", ())),
    }


def freeze_reference_estimates(
    plan: Mapping[str, Any],
    reference_protocol: Mapping[str, Any],
    evidence_manifest: Mapping[str, Any],
    *,
    workspace_root: str | Path = ROOT,
) -> list[dict[str, Any]]:
    """Validate a complete candidate manifest and derive reference records.

    Returned records remain candidate evidence. Promoting them to formal evidence
    requires a new frozen protocol and is deliberately outside this function.
    """

    runs = build_reference_run_plan(plan, reference_protocol)
    rows = _validate_evidence_structure(plan, reference_protocol, evidence_manifest, runs)
    values: dict[tuple[str, int, str], list[tuple[float, str]]] = {}
    root = Path(workspace_root).resolve()
    for row in rows:
        result_path = _resolve_workspace_path(root, row.get("result_path"))
        expected_result_digest = _sha256(row.get("result_sha256"), "result_sha256")
        if _file_sha256(result_path) != expected_result_digest:
            raise ReferencePortfolioError("result artifact digest mismatch")
        result = json.loads(result_path.read_text(encoding="utf-8"))
        if not isinstance(result, dict):
            raise ReferencePortfolioError("result artifact must be a JSON object")
        try:
            validate_verified_evaluation_result(result, replay=True)
        except (OSError, TypeError, ValueError) as exc:
            raise ReferencePortfolioError(f"result artifact replay failed: {exc}") from exc
        _validate_result_binding(plan, row, result)
        layered = result["score_replay"]["layered_evaluation"]
        trajectory_digest = _sha256(row.get("trajectory_sha256"), "trajectory_sha256")
        if result.get("trajectory_sha256") != trajectory_digest:
            raise ReferencePortfolioError("trajectory digest does not match result artifact")
        for metric_id in reference_protocol["metrics"]:
            metric = layered.get(metric_id)
            if not isinstance(metric, dict):
                raise ReferencePortfolioError(f"result is missing layered metric {metric_id!r}")
            value = _finite(metric.get("best"), f"{metric_id}.best")
            cell = (str(row["task_id"]), int(row["benchmark_seed"]), str(metric_id))
            values.setdefault(cell, []).append((value, trajectory_digest))

    confidence = float(plan["uncertainty_policy"]["confidence_level"])
    samples = int(plan["uncertainty_policy"]["bootstrap_samples"])
    bootstrap_seed = int(plan["uncertainty_policy"]["bootstrap_seed"])
    protocol_digest = reference_regret_protocol_sha256(reference_protocol)
    estimates = []
    for cell in sorted(values):
        task_id, seed, metric_id = cell
        source_values = [item[0] for item in values[cell]]
        digests = [item[1] for item in values[cell]]
        estimate = max(source_values)
        interval = _best_of_portfolio_interval(
            source_values,
            confidence_level=confidence,
            samples=samples,
            seed=_derived_seed(str(bootstrap_seed), f"{task_id}\0{seed}\0{metric_id}"),
        )
        estimates.append(
            {
                "schema_version": reference_protocol["reference_record_schema_version"],
                "protocol_sha256": protocol_digest,
                "task_id": task_id,
                "seed": seed,
                "metric_id": metric_id,
                "estimate": estimate,
                "interval_lower": interval[0],
                "interval_upper": interval[1],
                "confidence_level": confidence,
                "is_oracle": False,
                "builder_id": plan["builder_id"],
                "source_split": plan["source_split"],
                "frozen_before_method_scoring": True,
                "source_count": len(source_values),
                "trajectory_digests": sorted(digests),
                "result_schema_version": reference_protocol["result_schema_version"],
                "score_replay_binding_version": reference_protocol[
                    "score_replay_binding_version"
                ],
                "replay_verified": True,
                "candidate_evidence_only": True,
            }
        )
    return estimates


def _validate_plan(plan: Mapping[str, Any], protocol: Mapping[str, Any]) -> None:
    if plan.get("schema_version") != REFERENCE_PORTFOLIO_PLAN_VERSION:
        raise ReferencePortfolioError("unsupported reference portfolio plan schema")
    if plan.get("benchmark_claim_allowed") is not False:
        raise ReferencePortfolioError("candidate portfolio plan must be non-claiming")
    if plan.get("formal_results_present") is not False:
        raise ReferencePortfolioError("candidate portfolio plan cannot declare formal results")
    builder_id = str(plan.get("builder_id") or "")
    if not builder_id:
        raise ReferencePortfolioError("builder_id is required")
    evaluated = [str(item) for item in plan.get("evaluated_method_ids", ())]
    if builder_id in evaluated:
        raise ReferencePortfolioError("reference builder overlaps an evaluated method")
    if len(set(evaluated)) != len(evaluated):
        raise ReferencePortfolioError("evaluated method ids must be unique")
    independence = protocol.get("independence_policy", {})
    if plan.get("builder_role") != independence.get("reference_builder_role"):
        raise ReferencePortfolioError("reference builder role does not match protocol")
    if plan.get("source_split") != independence.get("reference_source_split"):
        raise ReferencePortfolioError("reference source split does not match protocol")
    if plan.get("evaluation_policy") != "vnext_risk_cost":
        raise ReferencePortfolioError("reference runs must use vnext_risk_cost")
    replicates = [str(item) for item in plan.get("replicate_ids", ())]
    if not replicates or len(set(replicates)) != len(replicates):
        raise ReferencePortfolioError("replicate ids must be non-empty and unique")
    minimum = int(plan.get("minimum_sources_per_cell", 0))
    if minimum < 1 or minimum > len(replicates):
        raise ReferencePortfolioError("minimum source count is inconsistent with replicates")
    if int(plan.get("experiment_budget", 0)) <= 0:
        raise ReferencePortfolioError("experiment budget must be positive")
    uncertainty = plan.get("uncertainty_policy", {})
    confidence = float(uncertainty.get("confidence_level", 0.0))
    if uncertainty.get("method") != "best_of_portfolio_replica_bootstrap":
        raise ReferencePortfolioError("unsupported reference uncertainty method")
    if not 0.0 < confidence < 1.0:
        raise ReferencePortfolioError("confidence level must be in (0, 1)")
    if int(uncertainty.get("bootstrap_samples", 0)) < 100:
        raise ReferencePortfolioError("bootstrap sample count is too small")


def _validate_evidence_structure(
    plan: Mapping[str, Any],
    protocol: Mapping[str, Any],
    manifest: Mapping[str, Any],
    runs: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    policy = plan["evidence_policy"]
    if manifest.get("schema_version") != policy["manifest_schema_version"]:
        raise ReferencePortfolioError("unsupported reference evidence manifest schema")
    if manifest.get("status") != "complete":
        raise ReferencePortfolioError("reference evidence manifest is not complete")
    if manifest.get("plan_sha256") != reference_portfolio_plan_sha256(plan):
        raise ReferencePortfolioError("reference evidence plan digest mismatch")
    if manifest.get("reference_protocol_sha256") != reference_regret_protocol_sha256(protocol):
        raise ReferencePortfolioError("reference evidence protocol digest mismatch")
    if manifest.get("builder_id") != plan["builder_id"]:
        raise ReferencePortfolioError("reference evidence builder mismatch")
    if manifest.get("source_split") != plan["source_split"]:
        raise ReferencePortfolioError("reference evidence source split mismatch")
    if manifest.get("frozen_before_method_scoring") is not True:
        raise ReferencePortfolioError("reference evidence was not frozen before method scoring")
    raw_rows = manifest.get("records")
    if not isinstance(raw_rows, list):
        raise ReferencePortfolioError("reference evidence records must be a list")
    rows = [dict(item) for item in raw_rows if isinstance(item, Mapping)]
    if len(rows) != len(raw_rows):
        raise ReferencePortfolioError("reference evidence record must be an object")
    expected = {str(item["run_id"]): item for item in runs}
    observed: dict[str, dict[str, Any]] = {}
    for row in rows:
        run_id = str(row.get("run_id") or "")
        if run_id not in expected:
            raise ReferencePortfolioError("reference evidence contains an unknown run")
        if run_id in observed:
            raise ReferencePortfolioError("reference evidence contains a duplicate run")
        planned = expected[run_id]
        for field in (
            "task_id",
            "benchmark_seed",
            "replicate_id",
            "builder_seed",
            "builder_id",
            "source_split",
        ):
            if row.get(field) != planned.get(field):
                raise ReferencePortfolioError(f"reference evidence {field} mismatch")
        if row.get("builder_id") in set(plan["evaluated_method_ids"]):
            raise ReferencePortfolioError("reference evidence uses an evaluated method identity")
        _sha256(row.get("builder_implementation_sha256"), "builder_implementation_sha256")
        _sha256(row.get("result_sha256"), "result_sha256")
        _sha256(row.get("trajectory_sha256"), "trajectory_sha256")
        observed[run_id] = row
    missing = sorted(set(expected) - set(observed))
    if missing:
        raise ReferencePortfolioError("reference evidence coverage is incomplete")
    return [observed[str(item["run_id"])] for item in runs]


def _validate_result_binding(
    plan: Mapping[str, Any],
    row: Mapping[str, Any],
    result: Mapping[str, Any],
) -> None:
    policy = plan["evidence_policy"]
    if result.get("result_schema_version") != policy["result_schema_version"]:
        raise ReferencePortfolioError("result schema does not match portfolio policy")
    binding = result.get("score_replay")
    if not isinstance(binding, Mapping):
        raise ReferencePortfolioError("result is missing score/replay binding")
    if binding.get("schema_version") != policy["score_replay_binding_version"]:
        raise ReferencePortfolioError("score/replay schema does not match portfolio policy")
    layered = binding.get("layered_evaluation")
    if not isinstance(layered, Mapping) or layered.get("task_id") != row["task_id"]:
        raise ReferencePortfolioError("result task does not match planned reference run")
    records = load_jsonl(Path(str(result["trajectory_path"])))
    first = records[0]
    if int(first.get("seed", -1)) != int(row["benchmark_seed"]):
        raise ReferencePortfolioError("trajectory world seed does not match benchmark seed")
    if first.get("world_split") != row["source_split"]:
        raise ReferencePortfolioError("trajectory split does not match reference-search split")
    metadata = first.get("agent_metadata", {})
    if not isinstance(metadata, Mapping) or metadata.get("agent_name") != row["builder_id"]:
        raise ReferencePortfolioError("trajectory builder identity mismatch")
    observed_builder_seed = metadata.get("reference_builder_seed", metadata.get("seed"))
    if int(observed_builder_seed) != int(row["builder_seed"]):
        raise ReferencePortfolioError("trajectory builder seed mismatch")
    if metadata.get("evaluation_policy") != plan["evaluation_policy"]:
        raise ReferencePortfolioError("trajectory evaluation policy mismatch")
    resources = result.get("resource_usage")
    if not isinstance(resources, Mapping):
        raise ReferencePortfolioError("result is missing the method resource ledger")
    if resources.get("schema_version") != "chemworld-resource-usage-0.2":
        raise ReferencePortfolioError("result has an unsupported resource ledger")
    if int(resources.get("complete_experiment_count", -1)) != int(
        plan["experiment_budget"]
    ):
        raise ReferencePortfolioError("result does not consume the frozen experiment budget")
    ledger = resources.get("method_ledger")
    if not isinstance(ledger, Mapping) or ledger.get("accounting_complete") is not True:
        raise ReferencePortfolioError("result resource accounting is incomplete")


def _adversarial_probes(
    plan: Mapping[str, Any],
    protocol: Mapping[str, Any],
    runs: Sequence[Mapping[str, Any]],
) -> dict[str, bool]:
    plan_digest = reference_portfolio_plan_sha256(plan)
    protocol_digest = reference_regret_protocol_sha256(protocol)
    rows = [
        {
            **dict(run),
            "builder_implementation_sha256": "1" * 64,
            "result_path": f"candidate/{run['run_id']}.json",
            "result_sha256": "2" * 64,
            "trajectory_sha256": "3" * 64,
        }
        for run in runs
    ]
    base = {
        "schema_version": REFERENCE_PORTFOLIO_EVIDENCE_VERSION,
        "status": "complete",
        "plan_sha256": plan_digest,
        "reference_protocol_sha256": protocol_digest,
        "builder_id": plan["builder_id"],
        "source_split": plan["source_split"],
        "frozen_before_method_scoring": True,
        "records": rows,
    }

    def rejected(changed: Mapping[str, Any], message: str) -> bool:
        try:
            _validate_evidence_structure(plan, protocol, changed, runs)
        except ReferencePortfolioError as exc:
            return message in str(exc)
        return False

    missing = copy.deepcopy(base)
    missing["records"] = missing["records"][:-1]
    duplicate = copy.deepcopy(base)
    duplicate["records"].append(copy.deepcopy(duplicate["records"][0]))
    unknown = copy.deepcopy(base)
    unknown["records"][0]["run_id"] = "0" * 64
    plan_mismatch = copy.deepcopy(base)
    plan_mismatch["plan_sha256"] = "0" * 64
    protocol_mismatch = copy.deepcopy(base)
    protocol_mismatch["reference_protocol_sha256"] = "0" * 64
    split_mismatch = copy.deepcopy(base)
    split_mismatch["source_split"] = "bench"
    builder_mismatch = copy.deepcopy(base)
    builder_mismatch["builder_id"] = "random"
    not_frozen = copy.deepcopy(base)
    not_frozen["frozen_before_method_scoring"] = False
    return {
        "missing_run_rejected": rejected(missing, "coverage is incomplete"),
        "duplicate_run_rejected": rejected(duplicate, "duplicate run"),
        "unknown_run_rejected": rejected(unknown, "unknown run"),
        "plan_digest_mismatch_rejected": rejected(plan_mismatch, "plan digest mismatch"),
        "protocol_digest_mismatch_rejected": rejected(
            protocol_mismatch, "protocol digest mismatch"
        ),
        "source_split_mismatch_rejected": rejected(split_mismatch, "source split mismatch"),
        "builder_mismatch_rejected": rejected(builder_mismatch, "builder mismatch"),
        "late_freeze_rejected": rejected(not_frozen, "not frozen before method scoring"),
    }


def _dependency_evidence(
    plan: Mapping[str, Any], workspace_root: Path
) -> dict[str, dict[str, Any]]:
    root = workspace_root.resolve()
    evidence = {}
    for evidence_id, relative in plan.get("dependencies", {}).items():
        path = _resolve_workspace_path(root, relative)
        exists = path.is_file()
        ready = exists
        if exists and path.suffix == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            if "controls_ready" in payload:
                ready = payload.get("controls_ready") is True
            if "completion_summary" in payload:
                ready = payload.get("status") == "completed"
        evidence[str(evidence_id)] = {
            "path": str(relative),
            "exists": exists,
            "ready": ready,
            "sha256": _file_sha256(path) if exists else None,
        }
    return evidence


def _best_of_portfolio_interval(
    values: Sequence[float],
    *,
    confidence_level: float,
    samples: int,
    seed: int,
) -> list[float]:
    if not values:
        raise ReferencePortfolioError("cannot bootstrap an empty reference portfolio")
    rng = random.Random(seed)
    count = len(values)
    maxima = sorted(
        max(values[rng.randrange(count)] for _ in range(count)) for _ in range(samples)
    )
    tail = (1.0 - confidence_level) / 2.0
    return [_quantile(maxima, tail), _quantile(maxima, 1.0 - tail)]


def _quantile(values: Sequence[float], probability: float) -> float:
    position = probability * (len(values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper or values[lower] == values[upper]:
        return float(values[lower])
    weight = position - lower
    return float(values[lower] * (1.0 - weight) + values[upper] * weight)


def _derived_seed(namespace: str, key: str) -> int:
    digest = hashlib.sha256(f"{namespace}\0{key}".encode()).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF


def _resolve_workspace_path(root: Path, value: Any) -> Path:
    relative = Path(str(value or ""))
    if not str(value or "") or relative.is_absolute() or ".." in relative.parts:
        raise ReferencePortfolioError("evidence path must be workspace-relative")
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ReferencePortfolioError("evidence path escapes workspace") from exc
    if not resolved.is_file():
        raise ReferencePortfolioError(f"evidence file does not exist: {relative}")
    return resolved


def _sha256(value: Any, field: str) -> str:
    text = str(value or "")
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise ReferencePortfolioError(f"{field} must be a lowercase SHA-256 digest")
    return text


def _finite(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise ReferencePortfolioError(f"{field} must be finite")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ReferencePortfolioError(f"{field} must be finite") from exc
    if not math.isfinite(number):
        raise ReferencePortfolioError(f"{field} must be finite")
    return number


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


__all__ = [
    "DEFAULT_REFERENCE_PORTFOLIO_PLAN_PATH",
    "REFERENCE_PORTFOLIO_AUDIT_VERSION",
    "REFERENCE_PORTFOLIO_EVIDENCE_VERSION",
    "REFERENCE_PORTFOLIO_PLAN_VERSION",
    "ReferencePortfolioError",
    "audit_reference_portfolio",
    "build_reference_run_plan",
    "freeze_reference_estimates",
    "load_reference_portfolio_plan",
    "reference_portfolio_plan_sha256",
]
