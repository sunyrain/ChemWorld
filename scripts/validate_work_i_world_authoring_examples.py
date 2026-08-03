"""Validate the frozen Work I world-authoring examples and emit a receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any, Literal, cast

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from chemworld.foundation.world_fork_manifest import (  # type: ignore[import-untyped]  # noqa: E402
    WorldComponentInventory,
    audit_world_component_inventory,
    load_world_component_inventory,
)
from chemworld.foundation.world_fork_spec import (  # type: ignore[import-untyped]  # noqa: E402
    WorldForkSpec,
    audit_world_fork_spec,
    build_world_fork_spec,
)

INVENTORY_PATH = Path("configs/benchmark/work_i_world_fork_component_inventory_v0.1.json")
DOC_PATH = Path("docs/world-authoring-contract.md")
EXAMPLE_PATHS = (
    Path("examples/world-authoring/mechanism-fork-v0.1.json"),
    Path("examples/world-authoring/material-law-fork-v0.1.json"),
)
REPORT_PATH = Path("workstreams/arxiv_v1/reports/work-i-world-authoring-examples-v0.1.json")

EXAMPLE_SCHEMA_VERSION = "chemworld-world-authoring-example-0.1"
EXAMPLE_KEYS = frozenset(
    {
        "schema_version",
        "example_id",
        "purpose",
        "world_seed",
        "intervention_class",
        "target_component_id",
        "intervention_payload",
        "claim_boundary",
    }
)
CLAIM_BOUNDARY = {
    "agent_performance_claim": False,
    "divergence_claim": False,
    "execution_claim": False,
}
InterventionClass = Literal[
    "mechanism_or_constitutive_law",
    "material_law_counterfactual",
]


class WorldAuthoringExampleError(RuntimeError):
    """Raised when an example wrapper or receipt fails closed."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorldAuthoringExampleError(f"cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise WorldAuthoringExampleError(f"JSON root must be an object: {path}")
    return payload


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise WorldAuthoringExampleError(f"cannot read bound file: {path}") from exc
    return digest.hexdigest()


def _canonical_sha256(payload: Any, hash_field: str | None = None) -> str:
    unhashed = deepcopy(payload)
    if hash_field is not None:
        if not isinstance(unhashed, dict):
            raise WorldAuthoringExampleError("self-hashed payload must be an object")
        unhashed.pop(hash_field, None)
    return hashlib.sha256(
        json.dumps(
            unhashed,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def receipt_sha256(payload: Mapping[str, Any]) -> str:
    """Return the receipt digest excluding its embedded self-hash."""

    return _canonical_sha256(payload, "receipt_sha256")


def _synthetic_component_digests(
    inventory: WorldComponentInventory, example_id: str, target_component_id: str
) -> tuple[dict[str, str], dict[str, str]]:
    component_ids = sorted(
        component.component_id
        for component in inventory.components
        if component.layer != "identity"
    )
    parent = {
        component_id: hashlib.sha256(f"{example_id}:parent:{component_id}".encode()).hexdigest()
        for component_id in component_ids
    }
    child = dict(parent)
    child[target_component_id] = hashlib.sha256(
        f"{example_id}:child:{target_component_id}".encode()
    ).hexdigest()
    return parent, child


def validate_example_payload(
    payload: Mapping[str, Any], inventory: WorldComponentInventory
) -> tuple[WorldForkSpec, dict[str, Any]]:
    """Validate one authoring request by building the frozen WorldForkSpec surface."""

    actual_keys = set(payload)
    if actual_keys != EXAMPLE_KEYS:
        raise WorldAuthoringExampleError(
            "example fields do not match schema: "
            f"missing={sorted(EXAMPLE_KEYS - actual_keys)}, "
            f"unknown={sorted(actual_keys - EXAMPLE_KEYS)}"
        )
    if payload.get("schema_version") != EXAMPLE_SCHEMA_VERSION:
        raise WorldAuthoringExampleError("unsupported authoring example schema")
    example_id = payload.get("example_id")
    purpose = payload.get("purpose")
    world_seed = payload.get("world_seed")
    intervention_class = payload.get("intervention_class")
    target_component_id = payload.get("target_component_id")
    intervention_payload = payload.get("intervention_payload")
    if not isinstance(example_id, str) or not example_id:
        raise WorldAuthoringExampleError("example_id must be a non-empty string")
    if not isinstance(purpose, str) or not purpose:
        raise WorldAuthoringExampleError("purpose must be a non-empty string")
    if isinstance(world_seed, bool) or not isinstance(world_seed, int) or world_seed < 0:
        raise WorldAuthoringExampleError("world_seed must be a non-negative integer")
    if intervention_class not in (
        "mechanism_or_constitutive_law",
        "material_law_counterfactual",
    ):
        raise WorldAuthoringExampleError("unsupported intervention_class")
    if not isinstance(target_component_id, str) or not target_component_id:
        raise WorldAuthoringExampleError("target_component_id must be a non-empty string")
    if not isinstance(intervention_payload, Mapping) or not intervention_payload:
        raise WorldAuthoringExampleError("intervention_payload must be a non-empty object")
    if payload.get("claim_boundary") != CLAIM_BOUNDARY:
        raise WorldAuthoringExampleError("authoring examples cannot claim execution or outcomes")

    parent, child = _synthetic_component_digests(inventory, example_id, target_component_id)
    spec = build_world_fork_spec(
        inventory=inventory,
        world_seed=world_seed,
        intervention_class=cast(InterventionClass, intervention_class),
        target_component_id=target_component_id,
        intervention_payload=intervention_payload,
        parent_component_sha256=parent,
        child_component_sha256=child,
    )
    audit = audit_world_fork_spec(spec, inventory=inventory)
    if (
        audit.get("passed") is not True
        or audit.get("public_contract_invariant") is not True
        or audit.get("public_contract_component_count") != 9
        or audit.get("component_diff", {}).get("changed_component_ids") != [target_component_id]
        or audit.get("claim_boundary")
        != {
            "agent_performance_claim": False,
            "divergence_claim": False,
            "execution_claim": False,
            "single_private_physics_target": True,
        }
    ):
        raise WorldAuthoringExampleError("built WorldForkSpec audit failed")
    return spec, audit


def build_validation_receipt(root: Path = ROOT) -> dict[str, Any]:
    """Build a self-hashed receipt for the two frozen authoring examples."""

    resolved = root.resolve()
    inventory = load_world_component_inventory(resolved / INVENTORY_PATH)
    inventory_audit = audit_world_component_inventory(inventory, repository_root=resolved)
    if (
        inventory_audit.get("passed") is not True
        or inventory_audit.get("inventory_sha256")
        != "654b710fcfb0a66232e4a3c6e14f1abb1dd6c24357e7eac995d23d11f64ee6da"
        or inventory_audit.get("summary", {}).get("component_count") != 17
    ):
        raise WorldAuthoringExampleError("frozen F01 inventory binding changed")

    example_rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in EXAMPLE_PATHS:
        payload = _read_json(resolved / path)
        spec, audit = validate_example_payload(payload, inventory)
        example_id = str(payload["example_id"])
        if example_id in seen_ids:
            raise WorldAuthoringExampleError(f"duplicate example_id: {example_id}")
        seen_ids.add(example_id)
        example_rows.append(
            {
                "example_id": example_id,
                "file_sha256": _file_sha256(resolved / path),
                "fork_id": spec.fork_id,
                "fork_spec_sha256": spec.content_sha256,
                "intervention_class": spec.intervention_class,
                "invariant_component_count": len(spec.component_diff.invariant_component_ids),
                "path": path.as_posix(),
                "public_contract_component_count": audit["public_contract_component_count"],
                "public_contract_invariant": True,
                "target_component_id": spec.target_component_id,
                "world_seed": spec.world_seed,
            }
        )

    source_paths = (
        INVENTORY_PATH,
        Path("src/chemworld/foundation/world_fork_manifest.py"),
        Path("src/chemworld/foundation/world_fork_spec.py"),
        DOC_PATH,
    )
    receipt: dict[str, Any] = {
        "schema_id": "chemworld.work_i_world_authoring_examples_receipt",
        "schema_version": "0.1.0",
        "receipt_id": "work-i-w1-f08-world-authoring-examples-v0.1",
        "owner_task": "W1-F08",
        "status": "passed",
        "inventory": {
            "component_count": 17,
            "derived_identity_component_count": 2,
            "intervention_target_count": 3,
            "inventory_id": inventory.inventory_id,
            "inventory_sha256": inventory.content_sha256,
            "non_identity_component_count": 15,
            "public_contract_component_count": 9,
        },
        "examples": example_rows,
        "source_bindings": [
            {
                "bytes": (resolved / path).stat().st_size,
                "path": path.as_posix(),
                "sha256": _file_sha256(resolved / path),
            }
            for path in source_paths
        ],
        "validator_contract": {
            "content_addressed_parent_and_child": True,
            "derived_identity_fields_recomputed": True,
            "examples_validated": 2,
            "single_declared_private_target": True,
            "unknown_fields_fail_closed": True,
        },
        "claim_boundary": {
            "agent_performance_claim": False,
            "divergence_claim": False,
            "execution_claim": False,
            "provider_calls_required": False,
            "qualification_certificate_replaced": False,
        },
    }
    receipt["receipt_sha256"] = receipt_sha256(receipt)
    return receipt


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt = build_validation_receipt(ROOT)
    if args.check:
        committed = _read_json(ROOT / REPORT_PATH)
        if committed.get("receipt_sha256") != receipt_sha256(committed):
            raise SystemExit("committed world-authoring receipt self-hash mismatch")
        if committed != receipt:
            raise SystemExit("committed world-authoring receipt differs from deterministic rebuild")
    else:
        (ROOT / REPORT_PATH).write_text(_json_text(receipt), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "check": bool(args.check),
                "examples_validated": len(receipt["examples"]),
                "inventory_sha256": receipt["inventory"]["inventory_sha256"],
                "receipt_sha256": receipt["receipt_sha256"],
                "status": receipt["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
