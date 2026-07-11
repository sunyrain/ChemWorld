"""Fail-closed validation for the pre-registered publication protocol."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chemworld.eval.benchmark_validation import PRIMARY_METRIC_FIELDS
from chemworld.eval.runner import AGENT_REGISTRY
from chemworld.physchem.mechanism_library import configuration_root
from chemworld.task_design import SERIOUS_TASK_DESIGNS
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.parameters import WORLD_FAMILY_VERSION

PUBLICATION_PROTOCOL_SCHEMA_VERSION = "chemworld-publication-protocol-0.1"
DEFAULT_PUBLICATION_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "publication_protocol_v0.1.json"
)


@dataclass(frozen=True)
class ProtocolCheck:
    check_id: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "passed": self.passed,
            "message": self.message,
        }


def canonical_protocol_sha256(protocol: dict[str, Any]) -> str:
    """Return the stable digest used to bind runs to the frozen protocol."""

    encoded = json.dumps(
        protocol,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_publication_protocol(
    path: str | Path = DEFAULT_PUBLICATION_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("publication protocol must be a JSON object")
    return payload


def validate_publication_protocol(protocol: dict[str, Any]) -> tuple[ProtocolCheck, ...]:
    """Validate scientific scope, resource matching, and statistical commitments."""

    task_entries = protocol.get("tasks", [])
    methods = protocol.get("methods", [])
    contrasts = protocol.get("confirmatory_contrasts", [])
    design = protocol.get("experimental_design", {})
    statistics = protocol.get("statistics", {})
    reporting = protocol.get("reporting", {})
    boundaries = protocol.get("claim_boundaries", {})

    task_ids = [item.get("task_id") for item in task_entries if isinstance(item, dict)]
    method_ids = [item.get("method_id") for item in methods if isinstance(item, dict)]
    scientific_methods = [
        item.get("method_id")
        for item in methods
        if isinstance(item, dict) and item.get("paper_role") != "protocol_only"
    ]
    expected_task_ids = list(SERIOUS_TASK_IDS)
    expected_seeds = list(range(20))

    task_contracts_match = len(task_entries) == len(expected_task_ids)
    for item in task_entries:
        if not isinstance(item, dict) or item.get("task_id") not in SERIOUS_TASK_IDS:
            task_contracts_match = False
            continue
        task_id = str(item["task_id"])
        design_contract = SERIOUS_TASK_DESIGNS[task_id]
        task_contracts_match = task_contracts_match and all(
            (
                item.get("task_contract_hash") == get_task(task_id).contract_hash,
                item.get("primary_metric") == design_contract.primary_metric,
                item.get("primary_result_field") == PRIMARY_METRIC_FIELDS[task_id],
                item.get("capability_claim") == design_contract.capability_claim,
                bool(item.get("non_claims")),
            )
        )

    method_registry_match = (
        bool(method_ids)
        and len(method_ids) == len(set(method_ids))
        and all(method in AGENT_REGISTRY for method in method_ids)
    )
    confirmatory_pair = any(
        isinstance(item, dict)
        and item.get("method") == "structured_gp_bo"
        and item.get("comparator") == "random"
        and item.get("metric") == "total_score"
        for item in contrasts
    )
    forbidden_scientific_stubs = {
        "tool_using_llm_stub",
        "llm_replay",
        "codex_subagent_replay",
    }
    statistics_ready = all(
        (
            statistics.get("unit_of_analysis") == "paired_task_seed",
            statistics.get("alpha") == 0.05,
            statistics.get("confidence_level") == 0.95,
            statistics.get("sesoi_total_score") == 0.05,
            int(statistics.get("bootstrap_samples", 0)) >= 5_000,
            statistics.get("multiple_comparison_policy") == "holm_within_metric_family",
        )
    )
    claim_boundary_ready = all(
        (
            bool(boundaries.get("primary_claim")),
            len(boundaries.get("supported_claims", [])) >= 2,
            len(boundaries.get("prohibited_claims", [])) >= 3,
        )
    )
    checks = (
        ProtocolCheck(
            "schema",
            protocol.get("schema_version") == PUBLICATION_PROTOCOL_SCHEMA_VERSION,
            "protocol schema must be explicitly versioned",
        ),
        ProtocolCheck(
            "world_law",
            protocol.get("world_law_id") == WORLD_FAMILY_VERSION,
            "protocol must bind the current frozen world law",
        ),
        ProtocolCheck(
            "serious_task_scope",
            task_ids == expected_task_ids,
            "publication scope must list the six serious tasks in canonical order",
        ),
        ProtocolCheck(
            "task_contracts",
            task_contracts_match,
            "claims and primary metrics must match executable task contracts",
        ),
        ProtocolCheck(
            "paired_seed_depth",
            design.get("seeds") == expected_seeds,
            "formal evaluation requires the pre-registered 20 paired seeds",
        ),
        ProtocolCheck(
            "learning_horizon",
            design.get("complete_experiments_per_task_seed") == 40,
            "each method receives exactly 40 complete experiments per task-seed",
        ),
        ProtocolCheck(
            "public_split",
            design.get("world_split") == "public-test",
            "candidate publication results use the reproducible public-test split",
        ),
        ProtocolCheck(
            "clean_provenance",
            design.get("require_clean_tracked_tree") is True
            and design.get("require_trajectory_replay") is True,
            "formal runs require clean source provenance and replay verification",
        ),
        ProtocolCheck(
            "method_registry",
            method_registry_match,
            "every pre-registered method must resolve to an executable agent",
        ),
        ProtocolCheck(
            "stub_exclusion",
            not (forbidden_scientific_stubs & set(scientific_methods)),
            "stubs and replay traces cannot be reported as scientific baselines",
        ),
        ProtocolCheck(
            "confirmatory_contrast",
            confirmatory_pair,
            "structured GP-EI versus random is the pre-registered primary contrast",
        ),
        ProtocolCheck(
            "statistics",
            statistics_ready,
            "paired uncertainty, SESOI, and multiplicity control must be frozen",
        ),
        ProtocolCheck(
            "task_level_reporting",
            reporting.get("primary_reporting") == "per_task"
            and reporting.get("cross_task_aggregate_score") is None,
            "heterogeneous tasks are reported separately without an invented total score",
        ),
        ProtocolCheck(
            "claim_boundaries",
            claim_boundary_ready,
            "supported and prohibited scientific claims must be explicit",
        ),
    )
    return checks


def publication_protocol_manifest(protocol: dict[str, Any]) -> dict[str, Any]:
    checks = validate_publication_protocol(protocol)
    valid = all(check.passed for check in checks)
    return {
        "schema_version": PUBLICATION_PROTOCOL_SCHEMA_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "protocol_sha256": canonical_protocol_sha256(protocol),
        "valid": valid,
        "checks": [check.to_dict() for check in checks],
    }


def assert_valid_publication_protocol(protocol: dict[str, Any]) -> None:
    manifest = publication_protocol_manifest(protocol)
    if manifest["valid"]:
        return
    failures = [
        item["check_id"] for item in manifest["checks"] if not bool(item["passed"])
    ]
    raise ValueError(f"Invalid publication protocol: {', '.join(failures)}")


__all__ = [
    "DEFAULT_PUBLICATION_PROTOCOL_PATH",
    "PUBLICATION_PROTOCOL_SCHEMA_VERSION",
    "ProtocolCheck",
    "assert_valid_publication_protocol",
    "canonical_protocol_sha256",
    "load_publication_protocol",
    "publication_protocol_manifest",
    "validate_publication_protocol",
]
