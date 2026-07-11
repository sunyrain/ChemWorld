"""Independent best-known references and signed-regret controls."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from statistics import fmean, median
from typing import Any

from chemworld.eval.result_artifacts import (
    EVALUATION_RESULT_SCHEMA_VERSION,
    SCORE_REPLAY_BINDING_VERSION,
)
from chemworld.physchem.mechanism_library import configuration_root

REFERENCE_REGRET_PROTOCOL_VERSION = "chemworld-reference-regret-protocol-0.1"
REFERENCE_REGRET_AUDIT_VERSION = "chemworld-reference-regret-audit-0.1"
REFERENCE_ESTIMATE_VERSION = "chemworld-reference-estimate-0.1"
METHOD_SCORE_OBSERVATION_VERSION = "chemworld-method-score-observation-0.1"
DEFAULT_REFERENCE_REGRET_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "reference_regret_vnext.json"
)
ROOT = Path(__file__).resolve().parents[3]


class ReferenceRegretError(ValueError):
    """Raised when reference-regret evidence fails closed."""


def load_reference_regret_protocol(
    path: str | Path = DEFAULT_REFERENCE_REGRET_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReferenceRegretError("reference-regret protocol must be a JSON object")
    return payload


def reference_regret_protocol_sha256(protocol: Mapping[str, Any]) -> str:
    """Return a semantic digest of the complete protocol payload."""

    return hashlib.sha256(
        json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def evaluate_reference_regret(
    protocol: Mapping[str, Any],
    reference_records: Sequence[Mapping[str, Any]],
    method_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Validate a complete evidence grid and compute signed paired regret.

    A negative regret is intentionally retained: a best-known reference is an
    estimate, not an oracle or an upper bound.
    """

    _validate_protocol_shape(protocol)
    protocol_digest = reference_regret_protocol_sha256(protocol)
    expected_cells = _expected_cells(protocol)
    reference_index, reference_digests, builder_ids = _index_references(
        protocol,
        reference_records,
        protocol_digest=protocol_digest,
        expected_cells=expected_cells,
    )
    method_index, method_digests, method_ids = _index_methods(
        protocol,
        method_records,
        protocol_digest=protocol_digest,
        expected_cells=expected_cells,
    )
    missing_references = sorted(expected_cells - set(reference_index))
    if missing_references:
        raise ReferenceRegretError(
            f"reference coverage incomplete: missing {len(missing_references)} cells"
        )
    if not method_ids:
        raise ReferenceRegretError("method evidence is empty")
    missing_methods = {}
    for method_id in method_ids:
        observed_cells = {
            (task_id, seed, metric_id)
            for indexed_method, task_id, seed, metric_id in method_index
            if indexed_method == method_id
        }
        missing_methods[method_id] = sorted(expected_cells - observed_cells)
    incomplete = {key: value for key, value in missing_methods.items() if value}
    if incomplete:
        details = ", ".join(f"{key}={len(value)}" for key, value in sorted(incomplete.items()))
        raise ReferenceRegretError(f"method coverage incomplete: {details}")
    overlap = reference_digests & method_digests
    if overlap:
        raise ReferenceRegretError("reference and evaluated-method trajectories overlap")
    if builder_ids & method_ids:
        raise ReferenceRegretError("reference builder identity overlaps an evaluated method")

    paired: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for (method_id, task_id, seed, metric_id), method in sorted(method_index.items()):
        reference = reference_index[(task_id, seed, metric_id)]
        direction = str(protocol["metrics"][metric_id]["direction"])
        estimate = float(reference["estimate"])
        score = float(method["value"])
        lower = float(reference["interval_lower"])
        upper = float(reference["interval_upper"])
        if direction == "maximize":
            signed_regret = estimate - score
            interval = [lower - score, upper - score]
        else:
            signed_regret = score - estimate
            interval = [score - upper, score - lower]
        item = {
            "method_id": method_id,
            "task_id": task_id,
            "seed": seed,
            "metric_id": metric_id,
            "reference_estimate": estimate,
            "method_value": score,
            "signed_regret": signed_regret,
            "reference_uncertainty_regret_interval": interval,
            "method_exceeds_reference": signed_regret < 0.0,
            "reference_is_oracle": False,
            "reference_trajectory_digests": list(reference["trajectory_digests"]),
            "method_trajectory_sha256": method["trajectory_sha256"],
        }
        paired.append(item)
        grouped[(method_id, task_id, metric_id)].append(item)

    bootstrap = protocol["uncertainty_policy"]
    summaries: dict[str, dict[str, dict[str, Any]]] = defaultdict(lambda: defaultdict(dict))
    for (method_id, task_id, metric_id), items in sorted(grouped.items()):
        regrets = [float(item["signed_regret"]) for item in items]
        lower_bounds = [
            float(item["reference_uncertainty_regret_interval"][0]) for item in items
        ]
        upper_bounds = [
            float(item["reference_uncertainty_regret_interval"][1]) for item in items
        ]
        summaries[method_id][task_id][metric_id] = {
            "paired_seed_count": len(regrets),
            "mean_signed_regret": fmean(regrets),
            "median_signed_regret": median(regrets),
            "paired_seed_bootstrap_interval": _paired_bootstrap_interval(
                regrets,
                confidence_level=float(bootstrap["confidence_level"]),
                samples=int(bootstrap["bootstrap_samples"]),
                seed=_group_seed(int(bootstrap["bootstrap_seed"]), method_id, task_id, metric_id),
            ),
            "reference_uncertainty_mean_endpoint_interval": [
                fmean(lower_bounds),
                fmean(upper_bounds),
            ],
            "method_exceeds_reference_count": sum(value < 0.0 for value in regrets),
            "negative_regret_preserved": any(value < 0.0 for value in regrets),
        }

    return {
        "schema_version": "chemworld-reference-regret-result-0.1",
        "protocol_id": protocol.get("protocol_id"),
        "protocol_sha256": protocol_digest,
        "status": "evaluated",
        "analysis_ready": True,
        "benchmark_claim_allowed": False,
        "reference_is_oracle": False,
        "negative_regret_policy": "preserve_and_report",
        "coverage": {
            "expected_reference_cells": len(expected_cells),
            "observed_reference_cells": len(reference_index),
            "method_ids": sorted(method_ids),
            "observed_method_cells": len(method_index),
            "complete": True,
        },
        "independence": {
            "reference_builder_ids": sorted(builder_ids),
            "evaluated_method_ids": sorted(method_ids),
            "trajectory_digest_sets_disjoint": True,
            "builder_method_ids_disjoint": True,
        },
        "paired_regret": paired,
        "summaries": _plain_dict(summaries),
    }


def audit_reference_regret_protocol(protocol: Mapping[str, Any]) -> dict[str, Any]:
    """Audit the candidate controls without claiming formal reference results."""

    dependencies = _dependency_evidence(protocol)
    checks = _protocol_checks(protocol, dependencies)
    required_probes = tuple(str(value) for value in protocol.get("required_adversarial_probes", ()))
    try:
        references, methods = _synthetic_complete_evidence(protocol)
        control_result = evaluate_reference_regret(protocol, references, methods)
        probes = _adversarial_probes(protocol, references, methods, control_result)
    except (KeyError, TypeError, ValueError) as exc:
        control_result = {"analysis_ready": False, "error": str(exc)}
        probes = dict.fromkeys(required_probes, False)
    checks["required_probes_declared"] = tuple(probes) == required_probes
    controls_ready = all(checks.values()) and all(probes.values())
    return {
        "schema_version": REFERENCE_REGRET_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "protocol_sha256": reference_regret_protocol_sha256(protocol),
        "status": (
            "controls_ready_formal_reference_search_pending"
            if controls_ready
            else "controls_failed"
        ),
        "controls_ready": controls_ready,
        "parent_task_complete": False,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "adversarial_probes": probes,
        "probe_count": len(probes),
        "control_grid": control_result.get("coverage"),
        "reference_semantics": dict(protocol.get("reference_semantics", {})),
        "dependencies": dependencies,
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _validate_protocol_shape(protocol: Mapping[str, Any]) -> None:
    if protocol.get("schema_version") != REFERENCE_REGRET_PROTOCOL_VERSION:
        raise ReferenceRegretError("unsupported reference-regret protocol schema")
    if protocol.get("benchmark_claim_allowed") is not False:
        raise ReferenceRegretError("candidate reference-regret protocol must be non-claiming")
    semantics = protocol.get("reference_semantics")
    if not isinstance(semantics, Mapping) or semantics.get("is_oracle") is not False:
        raise ReferenceRegretError("reference must be explicitly non-oracle")
    if semantics.get("negative_regret_policy") != "preserve_and_report":
        raise ReferenceRegretError("negative regret must be preserved")
    metrics = protocol.get("metrics")
    if not isinstance(metrics, Mapping) or not metrics:
        raise ReferenceRegretError("reference-regret protocol has no metrics")
    for metric_id, spec in metrics.items():
        if not isinstance(spec, Mapping) or spec.get("direction") not in {"maximize", "minimize"}:
            raise ReferenceRegretError(f"metric {metric_id!r} has no valid direction")
    uncertainty = protocol.get("uncertainty_policy")
    if not isinstance(uncertainty, Mapping):
        raise ReferenceRegretError("uncertainty policy is missing")
    confidence = _finite_number(uncertainty.get("confidence_level"), "confidence_level")
    if not 0.0 < confidence < 1.0:
        raise ReferenceRegretError("confidence_level must be in (0, 1)")
    if int(uncertainty.get("bootstrap_samples", 0)) <= 0:
        raise ReferenceRegretError("bootstrap_samples must be positive")


def _expected_cells(protocol: Mapping[str, Any]) -> set[tuple[str, int, str]]:
    tasks = tuple(str(value) for value in protocol.get("formal_task_ids", ()))
    seeds = tuple(int(value) for value in protocol.get("seed_ids", ()))
    metrics = tuple(str(value) for value in protocol.get("metrics", {}))
    if not tasks or not seeds or not metrics:
        raise ReferenceRegretError("formal task, seed, and metric grids must be non-empty")
    if len(tasks) != len(set(tasks)) or len(seeds) != len(set(seeds)):
        raise ReferenceRegretError("formal task and seed grids must be unique")
    return {
        (task_id, seed, metric_id)
        for task_id in tasks
        for seed in seeds
        for metric_id in metrics
    }


def _index_references(
    protocol: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    *,
    protocol_digest: str,
    expected_cells: set[tuple[str, int, str]],
) -> tuple[dict[tuple[str, int, str], Mapping[str, Any]], set[str], set[str]]:
    index: dict[tuple[str, int, str], Mapping[str, Any]] = {}
    digests: set[str] = set()
    builder_ids: set[str] = set()
    policy = protocol["independence_policy"]
    minimum_sources = int(protocol["coverage_policy"]["minimum_reference_source_count_per_cell"])
    expected_confidence = float(protocol["uncertainty_policy"]["confidence_level"])
    for record in records:
        if record.get("schema_version") != REFERENCE_ESTIMATE_VERSION:
            raise ReferenceRegretError("unsupported reference estimate schema")
        cell = _cell(record)
        if cell not in expected_cells:
            raise ReferenceRegretError(f"unexpected reference cell: {cell!r}")
        if cell in index:
            raise ReferenceRegretError(f"duplicate reference cell: {cell!r}")
        if record.get("protocol_sha256") != protocol_digest:
            raise ReferenceRegretError("reference protocol digest mismatch")
        if record.get("is_oracle") is not False:
            raise ReferenceRegretError("reference estimate must not be labeled as an oracle")
        if record.get("source_split") != policy["reference_source_split"]:
            raise ReferenceRegretError("reference estimate uses the wrong source split")
        if record.get("frozen_before_method_scoring") is not True:
            raise ReferenceRegretError("reference estimate was not frozen before method scoring")
        _validate_replay_binding(protocol, record, role="reference")
        estimate = _finite_number(record.get("estimate"), "reference estimate")
        lower = _finite_number(record.get("interval_lower"), "reference interval lower")
        upper = _finite_number(record.get("interval_upper"), "reference interval upper")
        if not lower <= estimate <= upper:
            raise ReferenceRegretError("reference interval does not contain its estimate")
        confidence = _finite_number(record.get("confidence_level"), "reference confidence")
        if not math.isclose(confidence, expected_confidence, rel_tol=0.0, abs_tol=1.0e-12):
            raise ReferenceRegretError("reference confidence level does not match protocol")
        source_count = int(record.get("source_count", 0))
        if source_count < minimum_sources:
            raise ReferenceRegretError("reference source count is below the protocol minimum")
        source_digests = record.get("trajectory_digests")
        if not isinstance(source_digests, list) or len(source_digests) != source_count:
            raise ReferenceRegretError("reference trajectory digest count is inconsistent")
        checked = {
            _validate_sha256(value, "reference trajectory digest")
            for value in source_digests
        }
        if len(checked) != len(source_digests):
            raise ReferenceRegretError("reference trajectory digests must be unique per cell")
        builder_id = str(record.get("builder_id") or "")
        if not builder_id:
            raise ReferenceRegretError("reference builder_id is missing")
        index[cell] = record
        digests.update(checked)
        builder_ids.add(builder_id)
    return index, digests, builder_ids


def _index_methods(
    protocol: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    *,
    protocol_digest: str,
    expected_cells: set[tuple[str, int, str]],
) -> tuple[dict[tuple[str, str, int, str], Mapping[str, Any]], set[str], set[str]]:
    index: dict[tuple[str, str, int, str], Mapping[str, Any]] = {}
    digests: set[str] = set()
    method_ids: set[str] = set()
    for record in records:
        if record.get("schema_version") != METHOD_SCORE_OBSERVATION_VERSION:
            raise ReferenceRegretError("unsupported method score observation schema")
        cell = _cell(record)
        if cell not in expected_cells:
            raise ReferenceRegretError(f"unexpected method cell: {cell!r}")
        method_id = str(record.get("method_id") or "")
        if not method_id:
            raise ReferenceRegretError("method_id is missing")
        key = (method_id, *cell)
        if key in index:
            raise ReferenceRegretError(f"duplicate method cell: {key!r}")
        if record.get("protocol_sha256") != protocol_digest:
            raise ReferenceRegretError("method protocol digest mismatch")
        _validate_replay_binding(protocol, record, role="method")
        _finite_number(record.get("value"), "method value")
        digest = _validate_sha256(record.get("trajectory_sha256"), "method trajectory digest")
        index[key] = record
        digests.add(digest)
        method_ids.add(method_id)
    return index, digests, method_ids


def _validate_replay_binding(
    protocol: Mapping[str, Any],
    record: Mapping[str, Any],
    *,
    role: str,
) -> None:
    if record.get("result_schema_version") != protocol.get("result_schema_version"):
        raise ReferenceRegretError(f"{role} result schema mismatch")
    if record.get("score_replay_binding_version") != protocol.get(
        "score_replay_binding_version"
    ):
        raise ReferenceRegretError(f"{role} score/replay binding mismatch")
    if record.get("replay_verified") is not True:
        raise ReferenceRegretError(f"{role} evidence is not replay verified")


def _cell(record: Mapping[str, Any]) -> tuple[str, int, str]:
    try:
        return str(record["task_id"]), int(record["seed"]), str(record["metric_id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ReferenceRegretError("evidence record has an invalid task/seed/metric cell") from exc


def _paired_bootstrap_interval(
    values: Sequence[float],
    *,
    confidence_level: float,
    samples: int,
    seed: int,
) -> list[float]:
    if not values:
        raise ReferenceRegretError("cannot bootstrap an empty regret vector")
    rng = random.Random(seed)
    count = len(values)
    means = sorted(
        fmean(values[rng.randrange(count)] for _ in range(count))
        for _ in range(samples)
    )
    tail = (1.0 - confidence_level) / 2.0
    return [_quantile(means, tail), _quantile(means, 1.0 - tail)]


def _quantile(values: Sequence[float], probability: float) -> float:
    position = probability * (len(values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(values[lower])
    weight = position - lower
    return float(values[lower] * (1.0 - weight) + values[upper] * weight)


def _group_seed(base: int, *parts: str) -> int:
    digest = hashlib.sha256("\0".join(parts).encode("utf-8")).digest()
    return base ^ int.from_bytes(digest[:8], "big")


def _finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise ReferenceRegretError(f"{field} must be a finite number")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ReferenceRegretError(f"{field} must be a finite number") from exc
    if not math.isfinite(number):
        raise ReferenceRegretError(f"{field} must be finite")
    return number


def _validate_sha256(value: Any, field: str) -> str:
    text = str(value or "")
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise ReferenceRegretError(f"{field} must be a lowercase SHA-256 digest")
    return text


def _protocol_checks(
    protocol: Mapping[str, Any],
    dependencies: Mapping[str, Mapping[str, Any]],
) -> dict[str, bool]:
    try:
        _validate_protocol_shape(protocol)
        expected_cells = _expected_cells(protocol)
        shape_valid = True
    except (KeyError, TypeError, ValueError):
        expected_cells = set()
        shape_valid = False
    semantics = protocol.get("reference_semantics", {})
    independence = protocol.get("independence_policy", {})
    uncertainty = protocol.get("uncertainty_policy", {})
    return {
        "protocol_shape": shape_valid,
        "candidate_is_non_claiming": protocol.get("benchmark_claim_allowed") is False,
        "formal_results_absent": protocol.get("formal_results_present") is False,
        "result_schema_bound": protocol.get("result_schema_version")
        == EVALUATION_RESULT_SCHEMA_VERSION,
        "score_replay_schema_bound": protocol.get("score_replay_binding_version")
        == SCORE_REPLAY_BINDING_VERSION,
        "reference_is_not_oracle": semantics.get("is_oracle") is False,
        "future_method_may_exceed_reference": semantics.get(
            "may_be_exceeded_by_evaluated_methods"
        )
        is True,
        "negative_regret_preserved": semantics.get("negative_regret_policy")
        == "preserve_and_report",
        "random_sample_maximum_excluded": semantics.get(
            "random_sample_maximum_allowed_as_reference"
        )
        is False,
        "reference_and_method_sources_disjoint": independence.get(
            "trajectory_digest_disjoint"
        )
        is True,
        "reference_frozen_before_scoring": independence.get(
            "reference_frozen_before_method_scoring"
        )
        is True,
        "paired_uncertainty_declared": uncertainty.get("aggregate_method")
        == "paired_seed_bootstrap",
        "formal_grid_nonempty": bool(expected_cells),
        "dependencies_ready": bool(dependencies)
        and all(item.get("ready") is True for item in dependencies.values()),
    }


def _dependency_evidence(
    protocol: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    evidence: dict[str, dict[str, Any]] = {}
    for evidence_id, relative in protocol.get("dependencies", {}).items():
        path = ROOT / str(relative)
        ready = path.is_file()
        if ready and path.suffix == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            if "controls_ready" in payload:
                ready = payload.get("controls_ready") is True
            if "status" in payload and "completion_summary" in payload:
                ready = payload.get("status") == "completed"
        evidence[str(evidence_id)] = {
            "path": str(relative),
            "exists": path.is_file(),
            "ready": ready,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        }
    return evidence


def _synthetic_complete_evidence(
    protocol: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    protocol_digest = reference_regret_protocol_sha256(protocol)
    references: list[dict[str, Any]] = []
    methods: list[dict[str, Any]] = []
    for task_index, task_id in enumerate(protocol.get("formal_task_ids", ())):
        for seed_index, seed in enumerate(protocol.get("seed_ids", ())):
            for metric_index, metric_id in enumerate(protocol.get("metrics", {})):
                estimate = 0.55 + task_index * 0.03 + seed_index * 0.001 + metric_index * 0.01
                reference_digest = _synthetic_digest("reference", task_id, seed, metric_id)
                references.append(
                    {
                        "schema_version": REFERENCE_ESTIMATE_VERSION,
                        "protocol_sha256": protocol_digest,
                        "task_id": task_id,
                        "seed": seed,
                        "metric_id": metric_id,
                        "estimate": estimate,
                        "interval_lower": estimate - 0.02,
                        "interval_upper": estimate + 0.02,
                        "confidence_level": protocol["uncertainty_policy"]["confidence_level"],
                        "is_oracle": False,
                        "builder_id": "independent_reference_portfolio",
                        "source_split": protocol["independence_policy"]["reference_source_split"],
                        "frozen_before_method_scoring": True,
                        "source_count": 1,
                        "trajectory_digests": [reference_digest],
                        "result_schema_version": protocol["result_schema_version"],
                        "score_replay_binding_version": protocol[
                            "score_replay_binding_version"
                        ],
                        "replay_verified": True,
                    }
                )
                for method_id, offset in (("control_below", -0.04), ("control_above", 0.01)):
                    methods.append(
                        {
                            "schema_version": METHOD_SCORE_OBSERVATION_VERSION,
                            "protocol_sha256": protocol_digest,
                            "task_id": task_id,
                            "seed": seed,
                            "metric_id": metric_id,
                            "method_id": method_id,
                            "value": estimate + offset,
                            "trajectory_sha256": _synthetic_digest(
                                "method", method_id, task_id, seed, metric_id
                            ),
                            "result_schema_version": protocol["result_schema_version"],
                            "score_replay_binding_version": protocol[
                                "score_replay_binding_version"
                            ],
                            "replay_verified": True,
                        }
                    )
    return references, methods


def _adversarial_probes(
    protocol: Mapping[str, Any],
    references: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    control_result: Mapping[str, Any],
) -> dict[str, bool]:
    def rejected(
        changed_references: list[dict[str, Any]],
        changed_methods: list[dict[str, Any]],
        message: str,
    ) -> bool:
        try:
            evaluate_reference_regret(protocol, changed_references, changed_methods)
        except ReferenceRegretError as exc:
            return message in str(exc)
        return False

    oracle = copy.deepcopy(references)
    oracle[0]["is_oracle"] = True
    duplicate_reference = copy.deepcopy(references)
    duplicate_reference.append(copy.deepcopy(duplicate_reference[0]))
    nonfinite = copy.deepcopy(references)
    nonfinite[0]["estimate"] = math.nan
    invalid_interval = copy.deepcopy(references)
    invalid_interval[0]["interval_lower"] = float(invalid_interval[0]["estimate"]) + 0.1
    overlap_methods = copy.deepcopy(methods)
    overlap_methods[0]["trajectory_sha256"] = references[0]["trajectory_digests"][0]
    builder_overlap = copy.deepcopy(references)
    builder_overlap[0]["builder_id"] = methods[0]["method_id"]
    replay_mismatch = copy.deepcopy(methods)
    replay_mismatch[0]["score_replay_binding_version"] = "tampered"
    duplicate_method = copy.deepcopy(methods)
    duplicate_method.append(copy.deepcopy(duplicate_method[0]))
    negative_values = [
        float(item["signed_regret"])
        for item in control_result.get("paired_regret", ())
        if item.get("method_id") == "control_above"
    ]
    return {
        "oracle_label_rejected": rejected(oracle, methods, "must not be labeled as an oracle"),
        "missing_reference_cell_rejected": rejected(
            references[:-1], methods, "reference coverage incomplete"
        ),
        "duplicate_reference_cell_rejected": rejected(
            duplicate_reference, methods, "duplicate reference cell"
        ),
        "nonfinite_reference_rejected": rejected(nonfinite, methods, "must be finite"),
        "invalid_interval_rejected": rejected(
            invalid_interval, methods, "does not contain its estimate"
        ),
        "trajectory_overlap_rejected": rejected(
            references, overlap_methods, "trajectories overlap"
        ),
        "builder_method_overlap_rejected": rejected(
            builder_overlap, methods, "builder identity overlaps"
        ),
        "replay_binding_mismatch_rejected": rejected(
            references, replay_mismatch, "score/replay binding mismatch"
        ),
        "duplicate_method_cell_rejected": rejected(
            references, duplicate_method, "duplicate method cell"
        ),
        "incomplete_method_grid_rejected": rejected(
            references, methods[:-1], "method coverage incomplete"
        ),
        "negative_regret_preserved": bool(negative_values)
        and all(value < 0.0 for value in negative_values),
    }


def _synthetic_digest(*parts: Any) -> str:
    return hashlib.sha256("\0".join(str(part) for part in parts).encode("utf-8")).hexdigest()


def _plain_dict(value: Any) -> Any:
    if isinstance(value, defaultdict):
        value = dict(value)
    if isinstance(value, dict):
        return {key: _plain_dict(item) for key, item in value.items()}
    return value


__all__ = [
    "DEFAULT_REFERENCE_REGRET_PROTOCOL_PATH",
    "METHOD_SCORE_OBSERVATION_VERSION",
    "REFERENCE_ESTIMATE_VERSION",
    "REFERENCE_REGRET_AUDIT_VERSION",
    "REFERENCE_REGRET_PROTOCOL_VERSION",
    "ReferenceRegretError",
    "audit_reference_regret_protocol",
    "evaluate_reference_regret",
    "load_reference_regret_protocol",
    "reference_regret_protocol_sha256",
]
