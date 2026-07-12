"""Build the backend-only v0.5 candidate evidence bundle for World Law v0.4."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from chemworld.runtime.model_reachability import default_model_reachability_registry
from chemworld.task_design import serious_task_readiness_manifest
from chemworld.tasks import SERIOUS_TASK_IDS, get_task
from chemworld.world.scenario import get_scenario_card
from chemworld.world.world_law import world_law_spec

SCHEMA_VERSION = "chemworld-backend-candidate-bundle-0.1"


def _write_json(path: Path, payload: Any) -> None:
    canonical = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.write_bytes(canonical.encode("utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_bundle(root: Path, output: Path) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    tasks = [get_task(task_id) for task_id in SERIOUS_TASK_IDS]
    registry = default_model_reachability_registry()
    artifacts: dict[str, Any] = {
        "task_contracts.json": {
            "schema_version": "chemworld-vnext-task-contract-set-0.1",
            "tasks": [task.to_dict() for task in tasks],
        },
        "scenario_cards.json": {
            "schema_version": "chemworld-vnext-scenario-card-set-0.1",
            "scenarios": [
                get_scenario_card(task.scenario_id, split=task.world_split)
                for task in tasks
            ],
        },
        "world_law.json": world_law_spec().to_dict(),
        "runtime_routes.json": {
            "schema_version": "chemworld-vnext-runtime-routes-0.1",
            "providers": registry.providers.to_dict(),
            "routes": [route.to_dict() for route in registry.routes],
        },
        "readiness.json": serious_task_readiness_manifest(),
    }
    for filename, payload in artifacts.items():
        _write_json(output / filename, payload)

    copied_sources = {
        "integration_audit.json": (
            root / "workstreams/world_foundation/reports/wf-110-runtime-integration.json"
        ),
        "backend_freeze.json": (
            root / "workstreams/world_foundation/reports/backend-v0.5.json"
        ),
        "maturity_truth.json": (
            root / "workstreams/world_foundation/reports/maturity-truth-vnext.json"
        ),
        "public_boundary.json": (
            root / "workstreams/world_foundation/reports/public-boundary-security-vnext.json"
        ),
        "core_golden_summaries.json": (
            root / "tests/fixtures/golden/core_scripted_trajectories.json"
        ),
    }
    for filename, source in copied_sources.items():
        _write_json(output / filename, json.loads(source.read_text(encoding="utf-8")))

    artifact_paths = sorted(
        output / filename
        for filename in (*artifacts, *copied_sources, "README.md")
        if (output / filename).is_file()
    )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": "chemworld-physical-chemistry-v0.5-backend-candidate",
        "world_law_id": "chemworld-physical-chemistry-v0.4",
        "task_contract_version": "chemworld-task-contract-0.6",
        "release_status": "candidate_backend_only",
        "benchmark_claim_allowed": False,
        "baseline_results_included": False,
        "frozen_v1_rewritten": False,
        "serious_task_ids": list(SERIOUS_TASK_IDS),
        "task_contract_hashes": {
            task.task_id: task.contract_hash for task in tasks
        },
        "artifact_sha256": {
            path.name: _sha256(path) for path in artifact_paths
        },
        "required_next_gate": (
            "run validity/power, generalization/security, and resource-matched "
            "method experiments before building a frozen benchmark release"
        ),
    }
    _write_json(output / "manifest.json", manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-vnext"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output if args.output.is_absolute() else root / args.output
    manifest = build_bundle(root, output)
    print(json.dumps({"output": str(output), **manifest}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
