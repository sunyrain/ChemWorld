from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.audit_public_harness import build_public_harness_report

from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.public_harness import (
    HarnessPolicy,
    PublicHarnessError,
    StudentProtocolError,
    audit_public_message_contract,
    public_task_info,
    validate_public_payload,
    validate_student_response,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs" / "benchmark" / "public_harness_vnext.json"
REPORT_PATH = ROOT / "workstreams" / "benchmark_v1" / "reports" / "public-harness-controls.json"


def _protocol() -> dict[str, object]:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


def test_public_message_contract_covers_all_serious_tasks() -> None:
    report = audit_public_message_contract(_protocol())

    assert report["message_controls_ready"] is True
    assert report["sandbox_ready"] is False
    assert len(report["tasks"]) == 6
    assert all(task["passed"] for task in report["tasks"].values())
    assert report["checks"]["hidden_state_fail_closed"] is True
    assert report["checks"]["private_task_text_fail_closed"] is True
    assert report["checks"]["traceback_fail_closed"] is True
    assert report["checks"]["absolute_path_fail_closed"] is True
    assert report["checks"]["agent_seed_is_decoupled"] is True


def test_public_task_info_does_not_expose_world_seed() -> None:
    env = ChemWorldEnv(task_id="partition-discovery", seed=17)
    try:
        _observation, task_info = env.reset(seed=17)
        hidden_species = set(env.scenario_instance.compiled_mechanism.species_index)
        public = public_task_info(
            task_info,
            hidden_species_ids=hidden_species,
            policy=HarnessPolicy(),
        )
    finally:
        env.close()

    assert task_info["seed"] == 17
    assert "seed" not in public


@pytest.mark.parametrize(
    ("payload", "reason"),
    (
        ({"debug_mechanism": {"theta": [1.0]}}, "sensitive_key"),
        ({"private_prompt": "answer"}, "private_task_text_key"),
        ({"error": 'Traceback: File "C:\\private\\agent.py"'}, "traceback_text"),
        ({"error": "/home/teacher/private.json"}, "absolute_path"),
    ),
)
def test_public_payload_rejects_hidden_debug_text_paths_and_tracebacks(
    payload: dict[str, object],
    reason: str,
) -> None:
    with pytest.raises(PublicHarnessError, match=reason):
        validate_public_payload(payload, max_bytes=10_000)


def test_public_payload_and_student_response_limits_fail_closed() -> None:
    with pytest.raises(PublicHarnessError, match="byte limit"):
        validate_public_payload({"value": "x" * 100}, max_bytes=10)
    policy = HarnessPolicy(message_limit_bytes=1_000, response_limit_bytes=20)
    with pytest.raises(StudentProtocolError, match="response_too_large"):
        validate_student_response(
            {"ok": True, "action": {"operation": "x" * 100}},
            request_type="act",
            policy=policy,
        )


def test_student_error_is_not_reflected_and_extra_fields_are_rejected() -> None:
    policy = HarnessPolicy()
    secret = "C:\\teacher_private\\config.json"
    with pytest.raises(StudentProtocolError) as captured:
        validate_student_response(
            {"ok": False, "error": f"Traceback: File {secret}"},
            request_type="act",
            policy=policy,
        )
    assert secret not in str(captured.value)
    with pytest.raises(StudentProtocolError, match="response_schema"):
        validate_student_response(
            {"ok": True, "action": {"operation": "terminate"}, "debug": "extra"},
            request_type="act",
            policy=policy,
        )


def test_public_harness_report_runs_real_subprocess_without_sandbox_claim() -> None:
    report = build_public_harness_report(_protocol())

    assert report["controls_ready"] is True
    assert report["subprocess_probe"]["separate_process"] is True
    assert report["subprocess_probe"]["passed"] is True
    assert report["security_boundary"] == "trusted-local-subprocess-not-a-sandbox"
    assert report["sandbox_ready"] is False
    assert report["benchmark_claim_allowed"] is False
    assert report["publication_ready"] is False


def test_committed_public_harness_report_matches_runtime_audit() -> None:
    committed = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    assert committed == build_public_harness_report(_protocol())
