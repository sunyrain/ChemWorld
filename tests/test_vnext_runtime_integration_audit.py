from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "audit_vnext_runtime_integration.py"
REPORT = ROOT / "workstreams/world_foundation/reports/wf-110-runtime-integration.json"
CANDIDATE = ROOT / "benchmark/releases/chemworld-serious-vnext"


def _load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("audit_vnext_runtime_integration", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_vnext_runtime_integration_executes_only_declared_providers() -> None:
    report = _load_script().build_audit(ROOT)

    assert report["passed"] is True
    checks = {item["check_id"]: item for item in report["checks"]}
    assert checks["retired_routes_absent"]["evidence"] == []
    assert checks["no_runtime_fallback_provider"]["evidence"] == []
    assert checks["task_route_declarations_aligned"]["evidence"]["gap_count"] == 0
    execution = checks["providers_execute_in_transactions"]["evidence"]
    assert execution["passed"] is True
    assert {
        "spent_sorbent",
        "concentrate_condensate",
        "concentrate_vent",
        "transfer_source_heel",
        "transfer_line_holdup",
    } <= set(execution["typed_inventory_phases"])


def test_committed_vnext_integration_report_is_green() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["schema_version"] == "chemworld-vnext-runtime-integration-audit-0.1"
    assert report["world_law_id"] == "chemworld-physical-chemistry-v0.4"
    assert report["passed"] is True
    assert all(check["passed"] for check in report["checks"])


def test_backend_candidate_is_hash_bound_and_cannot_claim_benchmark_readiness() -> None:
    manifest = json.loads((CANDIDATE / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["release_status"] == "candidate_backend_only"
    assert manifest["benchmark_claim_allowed"] is False
    assert manifest["baseline_results_included"] is False
    assert manifest["frozen_v1_rewritten"] is False
    for filename, expected in manifest["artifact_sha256"].items():
        assert hashlib.sha256((CANDIDATE / filename).read_bytes()).hexdigest() == expected
