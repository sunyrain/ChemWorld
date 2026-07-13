"""Formal recipe/operation interaction strata and fairness audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

from chemworld.agents.interaction import INTERACTION_CONTRACT_VERSION
from chemworld.eval.method_protocol import METHOD_RESOURCE_LEDGER_VERSION
from chemworld.physchem.mechanism_library import configuration_root

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROTOCOL_PATH = configuration_root() / "benchmark" / "interaction_strata_v0.4.json"
DEFAULT_REPORT_PATH = (
    ROOT / "workstreams" / "benchmark_v1" / "reports" / "interaction-strata-v0.4.json"
)
PROTOCOL_VERSION = "chemworld-interaction-strata-0.4"
RECIPE_METHODS = (
    "random",
    "lhs",
    "greedy_local",
    "structured_gp_ei",
    "structured_gp_pi",
    "structured_gp_ucb",
    "structured_rf_ei",
    "structured_safe_gp_ei",
)
OPERATION_METHODS = (
    "operation_random",
    "observation_blind",
    "rule_based",
    "ppo",
    "sac",
    "live_llm_a",
    "live_llm_b",
)
RESOURCE_AXES = (
    "complete_experiment_count",
    "operation_count",
    "measurement_count",
    "decision_count",
    "provider_request_count",
    "provider_retry_count",
    "input_token_count",
    "output_token_count",
    "monetary_cost_usd",
    "fit_count",
    "acquisition_optimization_count",
    "training_environment_step_count",
    "cpu_time_s",
    "gpu_time_s",
    "wall_time_s",
)
REQUIRED_DECLARATIONS = (
    "method_id",
    "track",
    "family",
    "decision_scope",
    "public_observation_set",
    "spectrum_capability",
    "spectrum_conditions",
    "adapts_within_experiment",
    "adapts_across_experiments",
    "update_boundary",
    "action_affordance",
    "harness_assistance",
    "resource_profile",
    "implementation_status",
)


class InteractionStrataError(RuntimeError):
    """Raised when a method lacks a valid formal capability declaration."""


@dataclass(frozen=True)
class MethodCapabilityDeclaration:
    """Complete public declaration required before formal method registration."""

    method_id: str
    track: Literal["recipe_level", "operation_level"]
    family: str
    decision_scope: Literal["experiment_recipe", "operation"]
    public_observation_set: str
    spectrum_capability: Literal["none", "current_and_history_on_explicit_request"]
    spectrum_conditions: tuple[str, ...]
    adapts_within_experiment: bool
    adapts_across_experiments: bool
    update_boundary: str
    action_affordance: str
    harness_assistance: tuple[str, ...]
    resource_profile: str
    implementation_status: str

    def __post_init__(self) -> None:
        for field_name in (
            "method_id",
            "family",
            "public_observation_set",
            "update_boundary",
            "action_affordance",
            "resource_profile",
            "implementation_status",
        ):
            if not str(getattr(self, field_name)).strip():
                raise InteractionStrataError(f"empty method declaration: {field_name}")
        if self.track not in {"recipe_level", "operation_level"}:
            raise InteractionStrataError("unsupported interaction track")
        expected_scope = "experiment_recipe" if self.track == "recipe_level" else "operation"
        if self.decision_scope != expected_scope:
            raise InteractionStrataError("decision scope does not match interaction track")
        if self.track == "recipe_level" and self.adapts_within_experiment:
            raise InteractionStrataError("recipe methods cannot adapt within an experiment")
        if self.spectrum_capability == "none":
            if self.spectrum_conditions != ("masked",):
                raise InteractionStrataError(
                    "methods without spectra must declare only the masked condition"
                )
        elif self.spectrum_capability == "current_and_history_on_explicit_request":
            if self.spectrum_conditions != ("assigned", "unassigned", "masked"):
                raise InteractionStrataError(
                    "spectrum-capable methods require assigned/unassigned/masked conditions"
                )
            if self.track != "operation_level":
                raise InteractionStrataError("spectrum use requires operation-level decisions")
        else:
            raise InteractionStrataError("unsupported spectrum capability")
        if not self.harness_assistance or len(set(self.harness_assistance)) != len(
            self.harness_assistance
        ):
            raise InteractionStrataError("harness assistance must be explicit and unique")
        if any(not item.strip() for item in self.harness_assistance):
            raise InteractionStrataError("empty harness assistance declaration")

    @classmethod
    def from_payload(
        cls, method_id: str, payload: Mapping[str, Any]
    ) -> MethodCapabilityDeclaration:
        missing = [
            field
            for field in REQUIRED_DECLARATIONS
            if field != "method_id" and field not in payload
        ]
        if missing:
            raise InteractionStrataError(
                f"method {method_id!r} is missing declarations: {', '.join(missing)}"
            )
        if "method_id" in payload and payload["method_id"] != method_id:
            raise InteractionStrataError("embedded method id does not match registry key")
        spectrum_conditions = payload.get("spectrum_conditions")
        assistance = payload.get("harness_assistance")
        if not isinstance(spectrum_conditions, list | tuple) or not isinstance(
            assistance, list | tuple
        ):
            raise InteractionStrataError("spectrum conditions and harness assistance must be lists")
        return cls(
            method_id=method_id,
            track=str(payload["track"]),  # type: ignore[arg-type]
            family=str(payload["family"]),
            decision_scope=str(payload["decision_scope"]),  # type: ignore[arg-type]
            public_observation_set=str(payload["public_observation_set"]),
            spectrum_capability=str(payload["spectrum_capability"]),  # type: ignore[arg-type]
            spectrum_conditions=tuple(str(item) for item in spectrum_conditions),
            adapts_within_experiment=_required_bool(
                payload, "adapts_within_experiment"
            ),
            adapts_across_experiments=_required_bool(
                payload, "adapts_across_experiments"
            ),
            update_boundary=str(payload["update_boundary"]),
            action_affordance=str(payload["action_affordance"]),
            harness_assistance=tuple(str(item) for item in assistance),
            resource_profile=str(payload["resource_profile"]),
            implementation_status=str(payload["implementation_status"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_interaction_strata_protocol(path: Path | None = None) -> dict[str, Any]:
    resolved = DEFAULT_PROTOCOL_PATH if path is None else path
    payload = _read_object(resolved)
    if payload.get("schema_version") != PROTOCOL_VERSION:
        raise InteractionStrataError("unsupported interaction-strata schema")
    return payload


def validate_method_declaration(
    method_id: str,
    payload: Mapping[str, Any],
    *,
    protocol: Mapping[str, Any],
) -> MethodCapabilityDeclaration:
    """Reject a method before registration if any capability is missing or incoherent."""

    declaration = MethodCapabilityDeclaration.from_payload(method_id, payload)
    observation_sets = protocol.get("public_observation_sets", {})
    resource_profiles = protocol.get("parallel_resource_ledger", {}).get("profiles", {})
    if not isinstance(observation_sets, Mapping) or (
        declaration.public_observation_set not in observation_sets
    ):
        raise InteractionStrataError("method references an unknown public observation set")
    if not isinstance(resource_profiles, Mapping) or declaration.resource_profile not in (
        resource_profiles
    ):
        raise InteractionStrataError("method references an unknown resource profile")
    observations = observation_sets[declaration.public_observation_set]
    if not _is_sequence(observations) or not observations:
        raise InteractionStrataError("public observation set must be a non-empty list")
    normalized = {str(item).lower() for item in observations}
    if any("hidden" in item or "private" in item for item in normalized):
        raise InteractionStrataError("method observation set crosses the public boundary")
    has_spectrum_observation = any("spectr" in item for item in normalized)
    if (declaration.spectrum_capability != "none") != has_spectrum_observation:
        raise InteractionStrataError("spectrum declaration does not match observation access")
    return declaration


def classify_comparison(
    left: MethodCapabilityDeclaration,
    right: MethodCapabilityDeclaration,
    *,
    protocol: Mapping[str, Any],
) -> str:
    """Return the strongest interpretation allowed by the frozen comparison blocks."""

    blocks = protocol.get("comparison_blocks", {})
    if isinstance(blocks, Mapping):
        for block in blocks.values():
            if not isinstance(block, Mapping):
                continue
            methods = {str(item) for item in block.get("methods", ())}
            if {left.method_id, right.method_id}.issubset(methods):
                return str(block.get("interpretation", "system_level_descriptive"))
    if left.track != right.track:
        return "cross_track_system_level_descriptive"
    return "within_track_capability_different_system_level"


def audit_interaction_strata(
    protocol: Mapping[str, Any], *, workspace: Path = ROOT
) -> dict[str, Any]:
    controls: dict[str, bool] = {}
    controls["schema_and_state_are_nonclaiming"] = (
        protocol.get("schema_version") == PROTOCOL_VERSION
        and protocol.get("status") == "preregistered_controls_methods_pending"
        and protocol.get("formal_results_present") is False
        and protocol.get("benchmark_claim_allowed") is False
    )
    controls["parent_formal_protocol_is_exact_and_ready"] = _parent_ready(
        protocol.get("parent_formal_protocol"), workspace
    )
    controls["interaction_contract_version_matches_runtime"] = (
        protocol.get("interaction_contract_version") == INTERACTION_CONTRACT_VERSION
    )

    tracks = protocol.get("tracks", {})
    recipe = tracks.get("recipe_level", {}) if isinstance(tracks, Mapping) else {}
    operation = tracks.get("operation_level", {}) if isinstance(tracks, Mapping) else {}
    controls["recipe_track_scope_is_exact"] = (
        isinstance(recipe, Mapping)
        and tuple(recipe.get("methods", ())) == RECIPE_METHODS
        and recipe.get("algorithmic_comparison_allowed_within_track") is True
    )
    controls["operation_track_scope_is_exact"] = (
        isinstance(operation, Mapping)
        and tuple(operation.get("methods", ())) == OPERATION_METHODS
        and operation.get("algorithmic_comparison_allowed_within_track") is True
    )
    controls["tracks_are_disjoint"] = not set(RECIPE_METHODS).intersection(OPERATION_METHODS)

    comparison = protocol.get("comparison_policy", {})
    controls["cross_track_claims_are_restricted"] = (
        isinstance(comparison, Mapping)
        and comparison.get("cross_track") == "system_level_descriptive_comparison_only"
        and comparison.get("cross_track_algorithm_superiority_claim") == "forbidden"
        and comparison.get("single_combined_ranking") == "forbidden"
        and comparison.get("capability_difference_table_required") is True
        and comparison.get("harness_assistance_difference_table_required") is True
    )

    budget = protocol.get("shared_evaluation_budget", {})
    controls["experiment_budget_and_checkpoints_match_parent"] = (
        isinstance(budget, Mapping)
        and budget.get("complete_experiments_per_cell") == 40
        and tuple(budget.get("checkpoints", ())) == (4, 8, 12, 20, 40)
        and budget.get("same_complete_experiment_budget_for_all_methods") is True
        and budget.get("operation_limit") == "frozen_task_contract"
        and budget.get("measurement_limit") == "frozen_task_contract"
    )
    ledger = protocol.get("parallel_resource_ledger", {})
    controls["parallel_resource_axes_are_complete_and_not_scalarized"] = (
        isinstance(ledger, Mapping)
        and ledger.get("schema_version") == METHOD_RESOURCE_LEDGER_VERSION
        and ledger.get("resource_axes_are_not_scalarized") is True
        and ledger.get("missing_required_axis_policy")
        == "accounting_failure_retained_in_denominator"
        and tuple(ledger.get("axes", ())) == RESOURCE_AXES
        and _resource_profiles_ready(ledger.get("profiles"))
    )

    spectrum = protocol.get("spectrum_policy", {})
    controls["spectrum_access_is_paired_explicit_and_costed"] = (
        isinstance(spectrum, Mapping)
        and tuple(spectrum.get("conditions", ())) == ("assigned", "unassigned", "masked")
        and spectrum.get("historical_packets_are_pushed_automatically") is False
        and spectrum.get("historical_packet_access")
        == "explicit_request_by_public_spectrum_id"
        and spectrum.get("retrieval_cost_and_failure_enter_ledger") is True
        and spectrum.get("non_spectrum_context_is_paired_across_conditions") is True
        and spectrum.get("private_chain_of_thought_required") is False
        and spectrum.get("structured_public_decision_audit_required_for_live_llm") is True
    )
    controls["registration_requirements_are_complete"] = tuple(
        protocol.get("registration_requirements", ())
    ) == REQUIRED_DECLARATIONS

    methods = protocol.get("methods", {})
    declarations: dict[str, MethodCapabilityDeclaration] = {}
    registration_failures: dict[str, str] = {}
    expected_methods = RECIPE_METHODS + OPERATION_METHODS
    if isinstance(methods, Mapping):
        for method_id in expected_methods:
            payload = methods.get(method_id)
            if not isinstance(payload, Mapping):
                registration_failures[method_id] = "missing method declaration"
                continue
            try:
                declarations[method_id] = validate_method_declaration(
                    method_id, payload, protocol=protocol
                )
            except InteractionStrataError as exc:
                registration_failures[method_id] = str(exc)
    controls["every_method_has_a_valid_complete_declaration"] = (
        isinstance(methods, Mapping)
        and tuple(methods) == expected_methods
        and set(declarations) == set(expected_methods)
        and not registration_failures
    )
    controls["declared_tracks_match_track_membership"] = all(
        declaration.track
        == ("recipe_level" if method_id in RECIPE_METHODS else "operation_level")
        for method_id, declaration in declarations.items()
    ) and len(declarations) == len(expected_methods)
    controls["comparison_blocks_cover_each_method_once"] = _comparison_blocks_ready(
        protocol.get("comparison_blocks"), expected_methods
    )
    controls["system_level_differences_are_material_and_visible"] = (
        _material_capability_differences(declarations)
    )
    registration = protocol.get("registration_policy", {})
    controls["registration_fails_closed_on_missing_or_observed_drift"] = (
        isinstance(registration, Mapping)
        and registration.get("missing_or_invalid_declaration") == "reject_registration"
        and registration.get("undeclared_harness_assistance") == "formal_ineligibility"
        and registration.get("observed_capability_exceeds_declaration") == "invalidate_cell"
        and registration.get("observed_capability_below_declaration")
        == "report_noncompliance_and_invalidate_claim"
    )

    controls_ready = all(controls.values())
    commit, dirty = _git_provenance(workspace)
    capability_matrix = {
        method_id: declarations[method_id].to_dict()
        for method_id in expected_methods
        if method_id in declarations
    }
    return {
        "schema_version": "chemworld-interaction-strata-audit-0.4",
        "protocol_id": protocol.get("protocol_id"),
        "status": "interaction_strata_frozen_methods_pending"
        if controls_ready
        else "interaction_strata_controls_failed",
        "controls_ready": controls_ready,
        "formal_results_present": False,
        "benchmark_claim_allowed": False,
        "source_commit": commit,
        "source_tree_dirty": dirty,
        "protocol_sha256": _canonical_sha256(protocol),
        "track_summary": {
            "recipe_level": {
                "method_count": len(RECIPE_METHODS),
                "methods": list(RECIPE_METHODS),
            },
            "operation_level": {
                "method_count": len(OPERATION_METHODS),
                "methods": list(OPERATION_METHODS),
            },
        },
        "capability_matrix": capability_matrix,
        "comparison_blocks": protocol.get("comparison_blocks", {}),
        "registration_failures": registration_failures,
        "resource_axes": list(RESOURCE_AXES),
        "controls": controls,
        "limitations": [
            "This audit freezes fairness controls; it does not assert that pending adapters exist.",
            (
                "Cross-track differences are system-level and cannot support "
                "algorithm-only superiority."
            ),
            "Resource axes remain parallel quantities and are not collapsed into one cost score.",
        ],
        "next_gates": [
            "freeze paired estimands and multiplicity control",
            "implement the formal runner and resource accounting",
            "validate and freeze each method adapter on Train/Dev only",
        ],
    }


def _parent_ready(raw: Any, workspace: Path) -> bool:
    if not isinstance(raw, Mapping):
        return False
    path = _resolve_workspace_path(workspace, raw.get("path"))
    if path is None or not path.is_file() or _file_sha256(path) != raw.get("file_sha256"):
        return False
    parent = _read_object(path)
    return (
        parent.get("protocol_id") == raw.get("protocol_id")
        and _canonical_sha256(parent) == raw.get("protocol_sha256")
        and parent.get("status") == "preregistered_controls_bench_sealed"
        and parent.get("formal_results_present") is False
        and parent.get("benchmark_claim_allowed") is False
    )


def _resource_profiles_ready(raw: Any) -> bool:
    if not isinstance(raw, Mapping) or set(raw) != {
        "classic_recipe",
        "operation_baseline",
        "rl_evaluation",
        "live_llm_evaluation",
    }:
        return False
    classic = raw["classic_recipe"]
    baseline = raw["operation_baseline"]
    rl = raw["rl_evaluation"]
    llm = raw["live_llm_evaluation"]
    return (
        isinstance(classic, Mapping)
        and classic.get("online_provider_requests") == 0
        and classic.get("fit_and_acquisition_usage") == "required_when_applicable"
        and isinstance(baseline, Mapping)
        and baseline.get("online_provider_requests") == 0
        and isinstance(rl, Mapping)
        and rl.get("training_environment_steps_per_task_max") == 1_000_000
        and rl.get("training_resources_reported_separately_from_evaluation") is True
        and isinstance(llm, Mapping)
        and llm.get("provider_request_limit_per_operation") == 6
        and llm.get("failed_requests_count_toward_limit") is True
        and llm.get("input_token_limit_per_cell") == 1_000_000
        and llm.get("output_token_limit_per_cell") == 200_000
        and llm.get("monetary_cost_usd_limit_per_cell") == 50.0
    )


def _comparison_blocks_ready(raw: Any, expected_methods: tuple[str, ...]) -> bool:
    if not isinstance(raw, Mapping) or not raw:
        return False
    observed: list[str] = []
    for block in raw.values():
        if not isinstance(block, Mapping):
            return False
        methods = block.get("methods")
        interpretation = block.get("interpretation")
        if not _is_sequence(methods) or not methods or not isinstance(interpretation, str):
            return False
        observed.extend(str(item) for item in methods)
    return len(observed) == len(set(observed)) and set(observed) == set(expected_methods)


def _material_capability_differences(
    declarations: Mapping[str, MethodCapabilityDeclaration]
) -> bool:
    if len(declarations) != len(RECIPE_METHODS) + len(OPERATION_METHODS):
        return False
    recipe = declarations["random"]
    llm = declarations["live_llm_a"]
    return (
        recipe.decision_scope != llm.decision_scope
        and recipe.public_observation_set != llm.public_observation_set
        and recipe.spectrum_capability != llm.spectrum_capability
        and recipe.harness_assistance != llm.harness_assistance
    )


def _required_bool(payload: Mapping[str, Any], field: str) -> bool:
    value = payload.get(field)
    if not isinstance(value, bool):
        raise InteractionStrataError(f"method declaration {field} must be boolean")
    return value


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _resolve_workspace_path(workspace: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip() or Path(raw).is_absolute():
        return None
    resolved = (workspace / raw).resolve()
    try:
        resolved.relative_to(workspace.resolve())
    except ValueError:
        return None
    return resolved


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise InteractionStrataError("JSON object required")
    return payload


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_provenance(workspace: Path) -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=workspace,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT_PATH)
    args = parser.parse_args()
    report = audit_interaction_strata(load_interaction_strata_protocol(args.protocol))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "controls_ready": report["controls_ready"],
                "recipe_method_count": report["track_summary"]["recipe_level"][
                    "method_count"
                ],
                "operation_method_count": report["track_summary"]["operation_level"][
                    "method_count"
                ],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "InteractionStrataError",
    "MethodCapabilityDeclaration",
    "audit_interaction_strata",
    "classify_comparison",
    "load_interaction_strata_protocol",
    "validate_method_declaration",
]
