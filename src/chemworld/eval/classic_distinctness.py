"""Fail-closed implementation distinctness audit for classic baselines."""

from __future__ import annotations

import copy
import hashlib
import inspect
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.agents.bo import (
    StructuredGaussianProcessBOAgent,
    StructuredGaussianProcessPIAgent,
    StructuredGaussianProcessUCBAgent,
    StructuredRandomForestEIAgent,
    StructuredSafetyConstrainedBOAgent,
)
from chemworld.agents.greedy import GreedyLocalAgent
from chemworld.agents.lhs import LatinHypercubeAgent
from chemworld.agents.random import RandomAgent
from chemworld.physchem.mechanism_library import configuration_root

CLASSIC_DISTINCTNESS_PROTOCOL_VERSION = "chemworld-classic-distinctness-protocol-0.1"
CLASSIC_DISTINCTNESS_AUDIT_VERSION = "chemworld-classic-distinctness-audit-0.1"
DEFAULT_CLASSIC_DISTINCTNESS_PROTOCOL_PATH = (
    configuration_root() / "benchmark" / "classic_distinctness_vnext.json"
)
ROOT = Path(__file__).resolve().parents[3]

_IMPLEMENTATIONS: dict[str, type[Any]] = {
    "random": RandomAgent,
    "lhs": LatinHypercubeAgent,
    "greedy": GreedyLocalAgent,
    "structured_gp_bo": StructuredGaussianProcessBOAgent,
    "structured_gp_pi": StructuredGaussianProcessPIAgent,
    "structured_gp_ucb": StructuredGaussianProcessUCBAgent,
    "structured_rf_ei": StructuredRandomForestEIAgent,
    "structured_safe_gp_bo": StructuredSafetyConstrainedBOAgent,
}


def load_classic_distinctness_protocol(
    path: str | Path = DEFAULT_CLASSIC_DISTINCTNESS_PROTOCOL_PATH,
) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("classic distinctness protocol must be a JSON object")
    return payload


def audit_classic_distinctness(protocol: Mapping[str, Any]) -> dict[str, Any]:
    """Verify classic roles against their real classes, manifests, and policy code."""

    cards, method_checks = _method_cards(protocol)
    dependencies = _dependency_evidence(protocol)
    policies = protocol.get("policies", {})
    class_ids = [card["class_id"] for card in cards.values()]
    act_digests = [card["act_sha256"] for card in cards.values()]
    semantic_digests = [card["semantic_fingerprint_sha256"] for card in cards.values()]
    surrogate_cards = [card for card in cards.values() if card["surrogate"] is not None]
    safe = cards.get("structured_safe_gp_ei", {})
    checks = {
        "schema": protocol.get("schema_version") == CLASSIC_DISTINCTNESS_PROTOCOL_VERSION,
        "candidate_is_nonclaiming": protocol.get("benchmark_claim_allowed") is False,
        "formal_results_absent": protocol.get("formal_results_present") is False,
        "required_method_count": len(cards) == 8,
        "all_method_contracts_match": bool(method_checks) and all(method_checks.values()),
        "classes_unique": len(class_ids) == len(set(class_ids)) == len(cards),
        "act_implementations_unique": len(act_digests) == len(set(act_digests)) == len(cards),
        "semantic_fingerprints_unique": len(semantic_digests)
        == len(set(semantic_digests))
        == len(cards),
        "surrogates_use_typed_encoding": bool(surrogate_cards)
        and all(
            card["recipe_encoding"] == "continuous_plus_material_one_hot"
            for card in surrogate_cards
        ),
        "ordinal_encoding_forbidden": policies.get("ordinal_material_encoding_allowed")
        is False,
        "safe_method_has_distinct_constraint": safe.get("constraint")
        == "upper_confidence_risk_mask_with_minimum_risk_fallback",
        "greedy_is_task_aware": cards.get("greedy_local", {}).get("search_policy")
        == "task_recipe_local_perturbation",
        "dependencies_ready": bool(dependencies)
        and all(item["ready"] for item in dependencies.values()),
    }
    probes = _adversarial_probes(protocol)
    required = tuple(str(value) for value in protocol.get("required_adversarial_probes", ()))
    checks["required_probes_declared"] = tuple(probes) == required
    controls_ready = all(checks.values()) and all(probes.values())
    return {
        "schema_version": CLASSIC_DISTINCTNESS_AUDIT_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "status": "controls_ready_formal_matrix_pending" if controls_ready else "controls_failed",
        "controls_ready": controls_ready,
        "parent_task_complete": False,
        "formal_results_present": False,
        "formal_classic_matrix_ready": False,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "checks": checks,
        "method_checks": method_checks,
        "methods": cards,
        "adversarial_probes": probes,
        "probe_count": len(probes),
        "dependencies": dependencies,
        "remaining_release_gates": list(protocol.get("remaining_release_gates", ())),
    }


def _method_cards(
    protocol: Mapping[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, bool]]:
    cards: dict[str, dict[str, Any]] = {}
    checks: dict[str, bool] = {}
    methods = protocol.get("required_methods", {})
    if not isinstance(methods, Mapping):
        return cards, {"required_methods_object": False}
    for role, raw_spec in methods.items():
        if not isinstance(raw_spec, Mapping):
            checks[str(role)] = False
            continue
        spec = dict(raw_spec)
        implementation = str(spec.get("implementation", ""))
        constructor = _IMPLEMENTATIONS.get(implementation)
        if constructor is None:
            checks[str(role)] = False
            continue
        agent = constructor()
        manifest = agent.manifest()
        act_function = agent.__class__.act
        act_source = inspect.getsource(act_function)
        class_id = f"{agent.__class__.__module__}.{agent.__class__.__qualname__}"
        act_owner = f"{act_function.__module__}.{act_function.__qualname__}"
        expected_manifest = spec.get("manifest", {})
        manifest_matches = isinstance(expected_manifest, Mapping) and all(
            manifest.get(key) == value for key, value in expected_manifest.items()
        )
        tokens = tuple(str(value) for value in spec.get("source_tokens", ()))
        tokens_match = bool(tokens) and all(token in act_source for token in tokens)
        card = {
            "role": str(role),
            "implementation": implementation,
            "class_id": class_id,
            "class_name": agent.__class__.__name__,
            "agent_name": agent.name,
            "act_owner": act_owner,
            "act_sha256": hashlib.sha256(act_source.encode("utf-8")).hexdigest(),
            "policy_family": spec.get("policy_family"),
            "recipe_encoding": manifest.get("recipe_encoding"),
            "search_policy": manifest.get("search_policy"),
            "surrogate": manifest.get("surrogate_family"),
            "acquisition": spec.get("acquisition"),
            "constraint": spec.get("constraint"),
            "source_tokens": list(tokens),
            "source_tokens_match": tokens_match,
            "manifest_contract_matches": manifest_matches,
        }
        semantic = {
            key: card[key]
            for key in (
                "class_id",
                "act_owner",
                "policy_family",
                "recipe_encoding",
                "search_policy",
                "surrogate",
                "acquisition",
                "constraint",
            )
        }
        card["semantic_fingerprint_sha256"] = hashlib.sha256(
            json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        card["contract_matches"] = (
            agent.__class__.__name__ == spec.get("class_name")
            and agent.name == spec.get("agent_name")
            and manifest_matches
            and tokens_match
        )
        cards[str(role)] = card
        checks[str(role)] = bool(card["contract_matches"])
    return cards, checks


def _adversarial_probes(protocol: Mapping[str, Any]) -> dict[str, bool]:
    def failed(changed: dict[str, Any], check: str) -> bool:
        cards, method_checks = _method_cards(changed)
        if check == "classes_unique":
            values = [card["class_id"] for card in cards.values()]
            return len(values) != len(set(values))
        if check == "typed_encoding":
            return not all(
                card["recipe_encoding"] == "continuous_plus_material_one_hot"
                for card in cards.values()
                if card["surrogate"] is not None
            )
        if check == "contracts":
            return not method_checks or not all(method_checks.values())
        if check == "safe_constraint":
            return cards.get("structured_safe_gp_ei", {}).get("constraint") is None
        if check == "method_count":
            return len(cards) != 8
        raise AssertionError(check)

    alias: dict[str, Any] = copy.deepcopy(dict(protocol))
    alias["required_methods"]["lhs"].update(
        {
            "implementation": "random",
            "class_name": "RandomAgent",
            "agent_name": "random",
            "source_tokens": ["sample_task_recipe"],
        }
    )
    ordinal: dict[str, Any] = copy.deepcopy(dict(protocol))
    ordinal["required_methods"]["structured_gp_ei"]["manifest"][
        "recipe_encoding"
    ] = "ordinal_material_coordinate"
    collapsed: dict[str, Any] = copy.deepcopy(dict(protocol))
    collapsed["required_methods"]["structured_gp_pi"]["source_tokens"] = [
        "gp_expected_improvement"
    ]
    unconstrained: dict[str, Any] = copy.deepcopy(dict(protocol))
    unconstrained["required_methods"]["structured_safe_gp_ei"]["constraint"] = None
    missing: dict[str, Any] = copy.deepcopy(dict(protocol))
    del missing["required_methods"]["lhs"]
    return {
        "implementation_alias_rejected": failed(alias, "classes_unique"),
        "ordinal_encoding_rejected": failed(ordinal, "contracts"),
        "acquisition_collapse_rejected": failed(collapsed, "contracts"),
        "unconstrained_safe_method_rejected": failed(unconstrained, "safe_constraint"),
        "missing_method_rejected": failed(missing, "method_count"),
    }


def _dependency_evidence(protocol: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    evidence = {}
    for evidence_id, relative in protocol.get("dependencies", {}).items():
        path = ROOT / str(relative)
        ready = path.is_file()
        if ready:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if "controls_ready" in payload:
                ready = payload.get("controls_ready") is True
            elif "completion_summary" in payload:
                ready = payload.get("status") == "completed"
        evidence[str(evidence_id)] = {
            "path": str(relative),
            "exists": path.is_file(),
            "ready": ready,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        }
    return evidence


__all__ = [
    "CLASSIC_DISTINCTNESS_AUDIT_VERSION",
    "CLASSIC_DISTINCTNESS_PROTOCOL_VERSION",
    "DEFAULT_CLASSIC_DISTINCTNESS_PROTOCOL_PATH",
    "audit_classic_distinctness",
    "load_classic_distinctness_protocol",
]
