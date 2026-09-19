from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "recover_work_ii_rx_ps_five_world_dual_goal",
    ROOT / "scripts" / "recover_work_ii_rx_ps_five_world_dual_goal.py",
)
assert SPEC and SPEC.loader
recovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recovery)


def _report(text: str = "English report") -> dict:
    return {"payload": {"report": text}}


def _predictions() -> dict:
    metrics = {
        metric: {"estimate": 0.5, "lower80": 0.4, "upper80": 0.6}
        for metric in recovery.campaign.METRICS
    }
    return {
        "payload": {
            "predictions": [
                {"query_id": f"Q{index:02d}", "metrics": metrics, "rationale": "English"}
                for index in range(1, 13)
            ],
            "rationale": "English overall rationale",
        }
    }


def test_repair_plan_is_exact() -> None:
    assert set(recovery.POSTTEST_REPAIRS) == {
        "RX-W01--S--mechanism_discovery--Opaque",
        "RX-W01--S--safety_constrained_optimization--MisIndexed",
        "RX-W02--P--mechanism_discovery--MisIndexed",
    }
    assert recovery.SOURCE_RERUN_CELL == "RX-W02--P--safety_constrained_optimization--Opaque"
    assert recovery.NUMERICS_LIMIT == 256
    assert recovery.POSTTEST_TOOL_ATTEMPT_LIMIT == 256


def test_merge_posttest_repair_seals_without_mutating_original() -> None:
    original = {
        "cell_id": "cell",
        "source_status": "completed",
        "failure": None,
        "status": "retained_nonconforming",
        "posttest_chain_sealed": False,
        "posttests": {"K1": _report(), "Q": {"payload": None}, "K2": _report()},
        "posttest_validation": {
            "K1": {"valid": True, "failure": None},
            "Q": {"valid": False, "failure": "missing_payload"},
            "K2": {"valid": True, "failure": None},
        },
    }
    query_rows = [{"query_id": f"Q{index:02d}"} for index in range(1, 13)]
    merged = recovery.merge_posttest_repair(
        original,
        {"Q": _predictions(), "K2": _report("Repaired English report")},
        query_rows,
    )
    assert merged["status"] == "completed"
    assert merged["posttest_chain_sealed"] is True
    assert merged["posttest_validation"]["Q"]["valid"] is True
    assert original["status"] == "retained_nonconforming"
    assert original["posttests"]["Q"]["payload"] is None


def test_high_budget_command_changes_only_numerics_limit(monkeypatch) -> None:
    base = [
        "codex",
        "-c",
        'mcp_servers.public_numerics.args=["server.py", "--limit", "128"]',
        "exec",
    ]
    monkeypatch.setattr(recovery, "_BASE_BUILD_COMMAND", lambda *args, **kwargs: list(base))
    command = recovery.high_budget_build_command({}, Path("schema"), Path("workspace"))
    assert command[:2] == base[:2]
    encoded = next(
        value for value in command if value.startswith("mcp_servers.public_numerics.args=")
    )
    values = json.loads(encoded.split("=", 1)[1])
    assert values[values.index("--limit") + 1] == "256"


def test_recovery_launch_replaces_legacy_eight_call_monitor() -> None:
    assert recovery.POSTTEST_TOOL_ATTEMPT_LIMIT > 8
    assert recovery.POSTTEST_TOOL_ATTEMPT_LIMIT == recovery.NUMERICS_LIMIT
