from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from chemworld.eval.formal_llm import load_live_llm_method_freeze
from chemworld.eval.method_freeze_v0_4 import (
    METHOD_FREEZE_REPORT_VERSION,
    MethodFreezeAuditError,
    _audit_llm,
    artifact_file_sha256,
    audit_method_freeze,
    load_method_freeze_plan,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/audit_method_freeze_v0.4.py"
SPEC = importlib.util.spec_from_file_location("audit_method_freeze_v0_4_script", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
SCRIPT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCRIPT)


def _audit(plan: dict[str, object]) -> dict[str, Any]:
    return audit_method_freeze(
        plan,
        root=ROOT,
        source_probe={"commit": "a" * 40, "clean": True},
    )


def test_current_method_freeze_scaffold_reports_exact_gaps_without_bench_access() -> None:
    report = _audit(load_method_freeze_plan())
    assert report["schema_version"] == METHOD_FREEZE_REPORT_VERSION
    assert report["status"] == "method_freeze_preflight_blocked"
    assert report["method_freeze_ready"] is False
    assert report["preflight_issuance_allowed"] is False
    assert report["bench_unlock_allowed"] is False
    assert report["bench_manifest_issued"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["private_bench_manifest_opened"] is False
    assert report["force_override_available"] is False

    families = report["method_families"]
    assert families["classic"]["controls_ready"] is True
    assert families["classic"]["development_ready"] is False
    assert families["classic"]["cell_count"] == 768
    assert families["operation_baselines"]["pending_adapter_method_ids"] == []
    assert families["operation_baselines"]["development_ready"] is False
    assert families["rl"]["ppo"]["selected_checkpoint_count"] == 0
    assert families["rl"]["ppo"]["missing_task_ids"] == [
        "flow-reaction-optimization",
        "partition-discovery",
        "reaction-to-crystallization",
        "reaction-to-distillation",
    ]
    assert families["rl"]["sac"]["development_ready"] is False
    assert families["llm"]["controls_ready"] is True
    assert families["llm"]["development_ready"] is False
    assert report["reference_independence"]["builder_implementation_ready"] is True
    assert report["reference_independence"]["ready"] is True

    blockers = set(report["blockers"])
    assert {
        "rl:ppo:expected_4_selected_checkpoints_found_0",
        "rl:ppo:missing_task:partition-discovery",
        "rl:ppo:missing_task:reaction-to-crystallization",
        "rl:ppo:missing_task:reaction-to-distillation",
        "rl:ppo:missing_task:flow-reaction-optimization",
        "rl:sac:development_evidence_missing",
        "llm:development_matrix:report_missing",
        "selection:dev_family_champions_missing",
        "formal_budget:freeze_missing",
        "classic:development_contract_failed",
        "operation_baseline:development_contract_failed",
        "method_freeze:development_incomplete",
    }.issubset(blockers)
    encoded = json.dumps(report)
    assert ".git/chemworld-private" not in encoded
    assert "bench-manifest.json" not in encoded


def test_bound_artifact_tampering_fails_closed() -> None:
    plan = copy.deepcopy(load_method_freeze_plan())
    plan["artifact_bindings"]["formal_protocol"]["sha256"] = "0" * 64
    report = _audit(plan)
    assert report["method_freeze_ready"] is False
    assert "artifact:formal_protocol:sha256_mismatch" in report["blockers"]
    assert report["checks"]["formal_core_tasks_exact"] is False
    assert report["bench_unlock_allowed"] is False


def test_llm_plan_rejects_stale_schema_or_broader_candidate_scope() -> None:
    method_freeze_plan = load_method_freeze_plan()
    contract = method_freeze_plan["llm_evidence_contract"]
    development_plan = json.loads(
        (ROOT / "configs/methods/llm_v0.4/llm_development_plan.json").read_text(encoding="utf-8")
    )

    blockers: list[str] = []
    summary = _audit_llm(
        freeze=load_live_llm_method_freeze(),
        development_plan=development_plan,
        development=None,
        contract=contract,
        observed={},
        blockers=blockers,
    )
    assert summary["controls_ready"] is True
    assert summary["development_plan_ready"] is True

    for mutation in ("schema", "task_scope"):
        stale = copy.deepcopy(development_plan)
        if mutation == "schema":
            stale["schema_version"] = "chemworld-live-llm-development-plan-0.4.3"
        else:
            stale["stages"]["candidate_screen"]["tasks"].append("partition-discovery")
        stale_blockers: list[str] = []
        stale_summary = _audit_llm(
            freeze=load_live_llm_method_freeze(),
            development_plan=stale,
            development=None,
            contract=contract,
            observed={},
            blockers=stale_blockers,
        )
        assert stale_summary["development_plan_ready"] is False
        assert "llm:development_plan_invalid" in stale_blockers


@pytest.mark.parametrize(
    ("field", "blocker"),
    [
        ("benchmark_claim_allowed", "control:benchmark_claim_denied"),
        ("bench_access_allowed", "control:bench_access_denied"),
        (
            "bench_manifest_issuance_allowed",
            "control:bench_manifest_issuance_denied",
        ),
    ],
)
def test_plan_cannot_request_claim_or_bench_issuance(field: str, blocker: str) -> None:
    plan = copy.deepcopy(load_method_freeze_plan())
    plan[field] = True
    report = _audit(plan)
    assert blocker in report["blockers"]
    assert report["method_freeze_ready"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["bench_unlock_allowed"] is False
    assert report["bench_manifest_issued"] is False


def test_outside_repository_binding_is_rejected_without_reading_it() -> None:
    plan = copy.deepcopy(load_method_freeze_plan())
    plan["artifact_bindings"]["formal_protocol"] = {
        "path": "../outside.json",
        "sha256": "0" * 64,
    }
    report = _audit(plan)
    assert "artifact:formal_protocol:path_unsafe" in report["blockers"]
    assert report["method_freeze_ready"] is False


def test_loader_rejects_unsupported_schema(tmp_path: Path) -> None:
    path = tmp_path / "plan.json"
    path.write_text('{"schema_version":"wrong"}\n', encoding="utf-8")
    with pytest.raises(MethodFreezeAuditError, match="unsupported"):
        load_method_freeze_plan(path)


def test_committed_json_binding_is_crlf_lf_transport_stable(tmp_path: Path) -> None:
    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    binary_lf = tmp_path / "lf.bin"
    binary_crlf = tmp_path / "crlf.bin"
    lf.write_bytes(b'{\n  "status": "ready"\n}\n')
    crlf.write_bytes(b'{\r\n  "status": "ready"\r\n}\r\n')
    binary_lf.write_bytes(lf.read_bytes())
    binary_crlf.write_bytes(crlf.read_bytes())

    assert artifact_file_sha256(lf) == artifact_file_sha256(crlf)
    assert artifact_file_sha256(binary_lf) != artifact_file_sha256(binary_crlf)


def test_cli_writes_blocked_report_and_exposes_no_force(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output = tmp_path / "method-freeze.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "audit_method_freeze_v0.4.py",
            "--repo-root",
            str(ROOT),
            "--output",
            str(output),
        ],
    )
    assert SCRIPT.main() == 1
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["method_freeze_ready"] is False
    assert report["bench_unlock_allowed"] is False
    summary = json.loads(capsys.readouterr().out)
    assert summary["blocker_count"] > 0

    monkeypatch.setattr(sys, "argv", ["audit_method_freeze_v0.4.py", "--force"])
    with pytest.raises(SystemExit) as exc:
        SCRIPT.main()
    assert exc.value.code == 2
    assert "--force" in capsys.readouterr().err
