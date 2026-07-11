# ruff: noqa: E402, I001
"""Audit the candidate public JSONL subprocess harness."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.eval.public_harness import (
    SECURITY_BOUNDARY,
    act_request,
    audit_public_message_contract,
    policy_from_protocol,
    public_task_info,
    reset_request,
)
from local_eval_server.teacher_side.eval_machine import (
    DEMO_SUBMISSION,
    StudentProcess,
    validate_submission,
)

DEFAULT_PROTOCOL = ROOT / "configs" / "benchmark" / "public_harness_vnext.json"
DEFAULT_OUTPUT = ROOT / "workstreams" / "benchmark_v1" / "reports" / "public-harness-controls.json"


def _read_protocol(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("public harness protocol must be a JSON object")
    return payload


def _protocol_sha256(protocol: dict[str, Any]) -> str:
    encoded = json.dumps(
        protocol,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _independent_subprocess_probe(protocol: dict[str, Any]) -> dict[str, Any]:
    policy = policy_from_protocol(protocol)
    env = ChemWorldEnv(task_id="reaction-to-assay", seed=0)
    try:
        _observation, task_info = env.reset(seed=0)
        hidden_species = set(env.scenario_instance.compiled_mechanism.species_index)
        safe_task = public_task_info(
            task_info,
            hidden_species_ids=hidden_species,
            policy=policy,
        )
        submission = validate_submission(DEMO_SUBMISSION)
        with tempfile.TemporaryDirectory(prefix="chemworld-public-harness-") as temporary:
            stderr_path = Path(temporary) / "student.stderr.log"
            with StudentProcess(
                submission,
                timeout_s=10.0,
                runtime_python=None,
                stderr_path=stderr_path,
                policy=policy,
            ) as student:
                separate_process = student.pid is not None and student.pid != os.getpid()
                reset_response = student.request(
                    reset_request(
                        safe_task,
                        0,
                        hidden_species_ids=hidden_species,
                        policy=policy,
                    )
                )
                action_response = student.request(
                    act_request(
                        [],
                        hidden_species_ids=hidden_species,
                        policy=policy,
                    )
                )
        return {
            "separate_process": separate_process,
            "reset_acknowledged": reset_response.get("ok") is True,
            "action_is_object": isinstance(action_response.get("action"), dict),
            "stderr_is_teacher_private": stderr_path.name == "student.stderr.log",
            "passed": separate_process
            and reset_response.get("ok") is True
            and isinstance(action_response.get("action"), dict),
        }
    finally:
        env.close()


def build_public_harness_report(protocol: dict[str, Any]) -> dict[str, Any]:
    message_report = audit_public_message_contract(protocol)
    subprocess_error: str | None = None
    subprocess_report: dict[str, Any]
    try:
        subprocess_report = _independent_subprocess_probe(protocol)
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        subprocess_error = type(error).__name__
        subprocess_report = {
            "separate_process": False,
            "reset_acknowledged": False,
            "action_is_object": False,
            "stderr_is_teacher_private": False,
            "passed": False,
        }
    checks = dict(message_report["checks"])
    checks["independent_jsonl_subprocess"] = subprocess_report["passed"]
    controls_ready = (
        message_report["message_controls_ready"]
        and subprocess_report["passed"]
        and subprocess_error is None
    )
    return {
        "schema_version": "chemworld-public-harness-audit-0.1",
        "protocol_id": protocol.get("protocol_id"),
        "protocol_sha256": _protocol_sha256(protocol),
        "status": (
            "public_message_controls_ready" if controls_ready else "public_message_controls_blocked"
        ),
        "controls_ready": controls_ready,
        "benchmark_claim_allowed": False,
        "publication_ready": False,
        "sandbox_ready": False,
        "execution_mode": message_report["execution_mode"],
        "security_boundary": SECURITY_BOUNDARY,
        "checks": checks,
        "configuration_error": message_report["configuration_error"],
        "subprocess_error": subprocess_error,
        "subprocess_probe": subprocess_report,
        "max_teacher_message_bytes": message_report["max_teacher_message_bytes"],
        "tasks": message_report["tasks"],
        "limitations": [
            (
                "The bundled evaluator isolates the JSONL protocol in a separate process "
                "but is not an operating-system sandbox."
            ),
            (
                "Untrusted submissions still require an external no-network, read-only, "
                "low-privilege container with CPU, memory, PID, and wall-time limits."
            ),
            (
                "The audit proves teacher-to-student message minimization; it does not "
                "prevent trusted local student code from reading host files."
            ),
            (
                "The student RNG seed is a fixed public zero and is deliberately "
                "decoupled from hidden world/evaluation seeds."
            ),
            "Formal private evaluation, exploit controls, and publication claims remain disabled.",
        ],
        "remaining_release_gates": [
            "run the same protocol inside an externally enforced untrusted-code sandbox",
            "complete the expanded exploit and resource-exhaustion matrix",
            "bind private evaluation summaries to frozen harness and method protocol hashes",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = build_public_harness_report(_read_protocol(args.protocol))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
