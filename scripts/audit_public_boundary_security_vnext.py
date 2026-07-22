# ruff: noqa: E402, I001
"""Build the executable vNext public-boundary security gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
WHEEL_PROBE_PROCESS = os.environ.get("CHEMWORLD_BOUNDARY_WHEEL_PROBE") == "1"
if not WHEEL_PROBE_PROCESS and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import chemworld
import numpy as np

from chemworld.agents.task_recipes import task_recipe_dimension, task_recipe_from_unit_vector
from chemworld.data.logging import load_jsonl, observation_to_json
from chemworld.eval.exploit_matrix import (
    REQUIRED_PUBLIC_HARNESS_PROBES,
    REQUIRED_TASK_PROBES,
    audit_public_boundary_exploits,
    load_exploit_matrix_protocol,
)
from chemworld.eval.public_harness import (
    MESSAGE_SCHEMA_VERSION,
    STEP_INFO_ALLOWLIST,
    TASK_INFO_ALLOWLIST,
    HarnessPolicy,
    PublicHarnessError,
    StudentProtocolError,
    act_request,
    audit_public_message_contract,
    public_step_info,
    public_task_info,
    reset_request,
    update_request,
    validate_public_payload,
    validate_student_response,
)
from chemworld.eval.runner import make_agent, run_agent
from chemworld.eval.score_replay_audit import (
    audit_score_replay_protocol,
    load_score_replay_protocol,
)
from chemworld.eval.semantic_invariance import REQUIRED_PROBES, audit_semantic_invariance
from chemworld.eval.verify import verify_records
from chemworld.envs.chemworld_env import ChemWorldEnv
from chemworld.schemas.validation import validate_action_schema
from chemworld.tasks import SERIOUS_TASK_IDS
from chemworld.world.operations import PUBLIC_OBSERVATION_KEYS

PROTOCOL_SCHEMA_VERSION = "chemworld-foundation-public-boundary-security-protocol-0.1"
REPORT_SCHEMA_VERSION = "chemworld-foundation-public-boundary-security-audit-0.1"
DEFAULT_PROTOCOL = ROOT / "configs" / "foundation" / "public_boundary_security_vnext.json"
DEFAULT_OUTPUT = (
    ROOT / "workstreams" / "world_foundation" / "reports" / "public-boundary-security-vnext.json"
)


def load_protocol(path: str | Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("public-boundary protocol must be a JSON object")
    return payload


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _expect_exception(operation: Any, expected: type[BaseException]) -> bool:
    try:
        operation()
    except expected:
        return True
    return False


def _dependency_bindings(protocol: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
    raw = protocol.get("dependency_bindings")
    if not isinstance(raw, Mapping) or not raw:
        return {}, False
    report: dict[str, Any] = {}
    for binding_id, item in sorted(raw.items()):
        path_text = item.get("path") if isinstance(item, Mapping) else None
        relative = Path(str(path_text)) if path_text is not None else Path(".")
        safe = path_text is not None and not relative.is_absolute() and ".." not in relative.parts
        path = ROOT / relative
        payload: Any = None
        if safe and path.is_file():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                payload = None
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if safe and path.is_file() else None
        passed = safe and isinstance(payload, Mapping)
        report[str(binding_id)] = {
            "path": str(path_text),
            "actual_sha256": actual,
            "passed": passed,
        }
    return report, all(item["passed"] for item in report.values())


def _identity_findings(payload: Any, forbidden_keys: frozenset[str]) -> list[str]:
    findings: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                key_text = str(key)
                child_path = f"{path}.{key_text}"
                if key_text.lower() in forbidden_keys:
                    findings.append(child_path)
                visit(child, child_path)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")

    visit(payload, "$")
    return findings


def _message_and_leakage_probes(
    protocol: Mapping[str, Any],
) -> tuple[dict[str, bool], dict[str, bool], dict[str, Any]]:
    limits = protocol["limits"]
    policy = HarnessPolicy(
        message_limit_bytes=int(limits["teacher_message_bytes"]),
        response_limit_bytes=int(limits["student_response_bytes"]),
    )
    forbidden_keys = frozenset(str(key).lower() for key in protocol["forbidden_identity_keys"])
    task_allowlist = frozenset(str(key) for key in protocol["public_task_info_allowlist"])
    step_allowlist = frozenset(str(key) for key in protocol["public_step_info_allowlist"])
    allowlist = {
        "source_allowlists_exact": task_allowlist == TASK_INFO_ALLOWLIST
        and step_allowlist == STEP_INFO_ALLOWLIST,
        "message_schema_exact": True,
        "unknown_teacher_field_stripped": True,
        "unknown_student_field_rejected": _expect_exception(
            lambda: validate_student_response(
                {"ok": True, "action": {"operation": "terminate"}, "unknown": "x"},
                request_type="act",
                policy=policy,
            ),
            StudentProtocolError,
        ),
        "observation_schema_exact": True,
    }
    clean_payloads = True
    task_details: dict[str, Any] = {}
    max_message_bytes = 0
    for task_id in SERIOUS_TASK_IDS:
        env = ChemWorldEnv(task_id=task_id, seed=0)
        try:
            observation, task_info = env.reset(seed=0)
            hidden_species = set(env.scenario_instance.compiled_mechanism.species_index)
            source_with_unknown = {**task_info, "unknown_teacher_internal": "must-not-pass"}
            safe_task = public_task_info(
                source_with_unknown,
                hidden_species_ids=hidden_species,
                policy=policy,
            )
            allowlist["unknown_teacher_field_stripped"] &= (
                "unknown_teacher_internal" not in safe_task
            )
            reset = reset_request(
                safe_task,
                0,
                hidden_species_ids=hidden_species,
                policy=policy,
            )
            dimension = task_recipe_dimension(task_info)
            recipe = task_recipe_from_unit_vector(
                task_info,
                np.full(dimension, 0.5, dtype=float),
            )
            action = recipe["steps"][0]
            observation, reward, _terminated, _truncated, info = env.step(action)
            safe_info = public_step_info(
                {**info, "unknown_teacher_internal": "must-not-pass"},
                hidden_species_ids=hidden_species,
                policy=policy,
            )
            update = update_request(
                action=action,
                observation=observation_to_json(observation),
                reward=float(reward),
                info=safe_info,
                hidden_species_ids=hidden_species,
                policy=policy,
            )
            act = act_request([], hidden_species_ids=hidden_species, policy=policy)
            allowlist["unknown_teacher_field_stripped"] &= (
                "unknown_teacher_internal" not in safe_info
            )
            allowlist["message_schema_exact"] &= (
                set(reset) == {"schema_version", "type", "task_info", "seed"}
                and set(act) == {"schema_version", "type", "history"}
                and set(update)
                == {"schema_version", "type", "action", "observation", "reward", "info"}
                and all(
                    message["schema_version"] == MESSAGE_SCHEMA_VERSION
                    for message in (reset, act, update)
                )
            )
            observation_json = observation_to_json(observation)
            allowlist["observation_schema_exact"] &= set(observation_json) == set(
                PUBLIC_OBSERVATION_KEYS
            ) and all(value is None or math.isfinite(value) for value in observation_json.values())
            payloads = (safe_task, reset, act, safe_info, update, observation_json)
            identity_findings = [
                finding
                for payload in payloads
                for finding in _identity_findings(payload, forbidden_keys)
            ]
            payloads_clean = not identity_findings
            clean_payloads &= payloads_clean
            encoded_sizes = [
                len(
                    json.dumps(
                        payload,
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=False,
                        allow_nan=False,
                    ).encode("utf-8")
                )
                for payload in payloads
            ]
            max_message_bytes = max(max_message_bytes, *encoded_sizes)
            task_details[task_id] = {
                "payloads_scanned": len(payloads),
                "max_payload_bytes": max(encoded_sizes),
                "identity_findings": identity_findings,
                "passed": payloads_clean,
            }
        finally:
            env.close()

    leakage = {
        "all_task_payloads_clean": clean_payloads,
        "hidden_state_rejected": _expect_exception(
            lambda: validate_public_payload(
                {"hidden_parameters": {"theta": [1.0]}}, max_bytes=10_000
            ),
            PublicHarnessError,
        ),
        "private_seed_rejected": _expect_exception(
            lambda: validate_public_payload({"private_seed": 991}, max_bytes=10_000),
            PublicHarnessError,
        ),
        "debug_rejected": _expect_exception(
            lambda: validate_public_payload({"debug_mechanism": {}}, max_bytes=10_000),
            PublicHarnessError,
        ),
        "exception_rejected": _expect_exception(
            lambda: validate_public_payload(
                {"error": 'Traceback (most recent call last): File "agent.py"'},
                max_bytes=10_000,
            ),
            PublicHarnessError,
        ),
        "absolute_path_rejected": _expect_exception(
            lambda: validate_public_payload(
                {"error": "C:\\teacher_private\\model.json"}, max_bytes=10_000
            ),
            PublicHarnessError,
        ),
        "task_text_rejected": _expect_exception(
            lambda: validate_public_payload({"task_text": "secret"}, max_bytes=10_000),
            PublicHarnessError,
        ),
        "provider_parameters_detected": bool(
            _identity_findings({"provider_parameters": {"temperature": 0.1}}, forbidden_keys)
        ),
        "model_identity_detected": bool(
            _identity_findings({"model_id": "private-model"}, forbidden_keys)
        ),
    }
    details = {"tasks": task_details, "max_public_payload_bytes": max_message_bytes}
    return allowlist, leakage, details


def _strict_replay_verified(
    records: list[dict[str, Any]],
    *,
    expected_digest: str,
) -> bool:
    if _canonical_sha256(records) != expected_digest:
        return False
    try:
        replay = verify_records(records)
    except (KeyError, TypeError, ValueError):
        return False
    if not replay.verified or not records:
        return False
    terminal_indices = [
        index
        for index, record in enumerate(records)
        if bool(record.get("terminated")) or bool(record.get("truncated"))
    ]
    if terminal_indices != [len(records) - 1]:
        return False
    last = records[-1]
    if bool(last.get("truncated")) and int(last["step"]) != int(last["budget"]):
        return False
    return all(int(record["step"]) == index for index, record in enumerate(records, start=1))


def _replay_probes(workspace: Path) -> tuple[dict[str, bool], dict[str, Any]]:
    trajectory = workspace / "strict-replay.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("scripted_chemistry"),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=trajectory,
    )
    records = load_jsonl(trajectory)
    digest = _canonical_sha256(records)
    shortened = copy.deepcopy(records[:-1])
    tampered = copy.deepcopy(records)
    tampered[0]["agent_metadata"]["agent_name"] = "tampered"
    score_report = audit_score_replay_protocol(
        load_score_replay_protocol(),
        workspace=workspace / "score-replay",
    )
    probes = {
        "valid_trajectory_verified": _strict_replay_verified(
            records,
            expected_digest=digest,
        ),
        "trajectory_truncation_rejected": not _strict_replay_verified(
            shortened,
            expected_digest=_canonical_sha256(shortened),
        ),
        "trajectory_digest_tamper_rejected": not _strict_replay_verified(
            tampered,
            expected_digest=digest,
        ),
        "score_replay_adversarial_probes": score_report["controls_ready"] is True
        and all(score_report["adversarial_probes"].values()),
    }
    details = {
        "strict_replay_step_count": len(records),
        "terminal_kind": "terminated" if records[-1]["terminated"] else "truncated",
        "score_replay_probes": score_report["adversarial_probes"],
    }
    return probes, details


def _adversarial_probes() -> tuple[dict[str, bool], dict[str, Any]]:
    exploit_protocol = copy.deepcopy(load_exploit_matrix_protocol())
    exploit_report = audit_public_boundary_exploits(exploit_protocol)
    all_task_probes = {
        probe: all(report["probes"][probe] for report in exploit_report["tasks"].values())
        for probe in REQUIRED_TASK_PROBES
    }
    public_probes = exploit_report["public_harness_probes"]
    probes = {
        "nan_rejected": all_task_probes["nonfinite_numeric_variants_no_score"]
        and public_probes["nonfinite_teacher_payload_rejected"],
        "positive_inf_rejected": all_task_probes["nonfinite_numeric_variants_no_score"]
        and public_probes["student_nonfinite_action_rejected"],
        "negative_inf_rejected": all_task_probes["nonfinite_numeric_variants_no_score"],
        "oversized_payload_rejected": public_probes["oversized_teacher_payload_rejected"]
        and public_probes["oversized_student_response_rejected"],
        "illegal_enum_rejected": all_task_probes["unknown_operation_no_score"]
        and not validate_action_schema({"operation": "not-an-operation"}).valid,
        "repeated_assay_blocked": all_task_probes["repeated_final_assay_no_score"],
        "budget_exhaustion_blocked": all_task_probes["budget_exhaustion_blocks_further_steps"],
    }
    details = {
        "exploit_controls_ready": exploit_report["controls_ready"],
        "exploit_probes_revalidated_directly": True,
        "task_count": len(exploit_report["tasks"]),
        "task_probe_count": sum(
            len(report["probes"]) for report in exploit_report["tasks"].values()
        ),
        "public_harness_probe_count": len(public_probes),
        "public_harness_probes": {
            probe: public_probes[probe] for probe in REQUIRED_PUBLIC_HARNESS_PROBES
        },
    }
    return probes, details


def _invariance_probes() -> tuple[dict[str, bool], dict[str, Any]]:
    protocol = json.loads(
        (ROOT / "configs" / "benchmark" / "semantic_invariance_vnext.json").read_text(
            encoding="utf-8"
        )
    )
    report = audit_semantic_invariance(protocol)
    probes = {
        probe: report["controls_ready"] is True
        and all(task["probes"][probe] for task in report["tasks"].values())
        for probe in REQUIRED_PROBES
    }
    return probes, {
        "controls_ready": report["controls_ready"],
        "paired_run_count": report["paired_run_count"],
        "task_count": len(report["tasks"]),
    }


def _child_probe(*, expect_wheel: bool) -> dict[str, Any]:
    bad_payloads: tuple[dict[str, Any], ...] = (
        {"hidden_parameters": {"theta": [1.0]}},
        {"private_seed": 99},
        {"debug_mechanism": {}},
        {"reward": math.nan},
        {"error": 'Traceback (most recent call last): File "private.py"'},
    )
    policy = HarnessPolicy(message_limit_bytes=1_024, response_limit_bytes=1_024)
    probes = {
        "teacher_payloads_fail_closed": all(
            _expect_exception(
                lambda payload=payload: validate_public_payload(payload, max_bytes=1_024),
                PublicHarnessError,
            )
            for payload in bad_payloads
        ),
        "student_schema_fails_closed": _expect_exception(
            lambda: validate_student_response(
                {"ok": True, "action": {"operation": "terminate"}, "debug": "x"},
                request_type="act",
                policy=policy,
            ),
            StudentProtocolError,
        ),
        "illegal_enum_fails_closed": not validate_action_schema(
            {"operation": "not-an-operation"}
        ).valid,
    }
    imported = Path(chemworld.__file__).resolve()
    source_import = imported.is_relative_to(SRC.resolve())
    return {
        "pid": os.getpid(),
        "platform": sys.platform,
        "package_version": chemworld.__version__,
        "wheel_import": expect_wheel and not source_import,
        "source_import": (not expect_wheel) and source_import,
        "probes": probes,
        "passed": all(probes.values()) and ((expect_wheel and not source_import) or source_import),
    }


def _run_child(
    python: Path,
    *,
    pythonpath: Sequence[Path],
    expect_wheel: bool,
) -> dict[str, Any]:
    environment = {
        key: value for key, value in os.environ.items() if key not in {"PYTHONHOME", "PYTHONPATH"}
    }
    environment["PYTHONPATH"] = os.pathsep.join(str(path) for path in pythonpath)
    environment["CHEMWORLD_BOUNDARY_WHEEL_PROBE"] = "1" if expect_wheel else "0"
    command = [
        str(python),
        str(Path(__file__).resolve()),
        "--child-probe",
        "--expect-wheel" if expect_wheel else "--expect-source",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if completed.returncode != 0:
        return {
            "passed": False,
            "returncode": completed.returncode,
            "error": "child_process_failed",
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "returncode": completed.returncode, "error": "invalid_json"}
    if not isinstance(payload, dict):
        return {"passed": False, "returncode": completed.returncode, "error": "non_object"}
    payload["separate_process"] = payload.pop("pid", os.getpid()) != os.getpid()
    return payload


def _execution_probes() -> tuple[dict[str, bool], dict[str, Any]]:
    source_child = _run_child(
        Path(sys.executable),
        pythonpath=(SRC, ROOT),
        expect_wheel=False,
    )
    wheel_child: dict[str, Any]
    with tempfile.TemporaryDirectory(prefix="chemworld-boundary-wheel-") as temporary:
        temporary_path = Path(temporary)
        wheels = temporary_path / "wheels"
        target = temporary_path / "installed"
        wheels.mkdir()
        uv = shutil.which("uv")
        build_command = (
            [uv, "build", "--wheel", "--out-dir", str(wheels), str(ROOT)]
            if uv
            else [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                "--no-build-isolation",
                "--no-deps",
                "--wheel-dir",
                str(wheels),
                str(ROOT),
            ]
        )
        build = subprocess.run(
            build_command,
            cwd=temporary_path,
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
        )
        wheel_files = sorted(wheels.glob("*.whl"))
        install_ok = False
        if build.returncode == 0 and len(wheel_files) == 1:
            install = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "--target",
                    str(target),
                    str(wheel_files[0]),
                ],
                cwd=temporary_path,
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
            )
            install_ok = install.returncode == 0
        if install_ok:
            wheel_child = _run_child(
                Path(sys.executable),
                pythonpath=(target, ROOT),
                expect_wheel=True,
            )
        else:
            wheel_child = {
                "passed": False,
                "error": "wheel_build_or_install_failed",
                "build_returncode": build.returncode,
            }
    probes = {
        "windows_source_process": sys.platform == "win32",
        "independent_process": source_child.get("separate_process") is True,
        "independent_process_fail_closed": source_child.get("passed") is True,
        "clean_wheel_import": wheel_child.get("wheel_import") is True,
        "clean_wheel_fail_closed": wheel_child.get("passed") is True,
    }
    details = {
        "source_child": {
            key: value for key, value in source_child.items() if key != "separate_process"
        },
        "wheel_child": {
            key: value for key, value in wheel_child.items() if key != "separate_process"
        },
        "security_boundary": "trusted-local-subprocess-not-an-os-sandbox",
    }
    return probes, details


def build_report(protocol: Mapping[str, Any]) -> dict[str, Any]:
    dependency_reports, dependencies_ready = _dependency_bindings(protocol)
    declared_groups = protocol.get("required_probe_groups")
    checks = {
        "schema": protocol.get("schema_version") == PROTOCOL_SCHEMA_VERSION,
        "candidate_gate": protocol.get("status") == "candidate_gate",
        "fail_closed_policy": protocol.get("freeze_policy") == "all_declared_checks_must_pass",
        "task_scope": protocol.get("task_ids") == list(SERIOUS_TASK_IDS),
        "probe_groups_declared": isinstance(declared_groups, Mapping),
        "dependency_bindings": dependencies_ready,
    }
    public_harness_protocol = json.loads(
        (ROOT / "configs" / "benchmark" / "public_harness_vnext.json").read_text(encoding="utf-8")
    )
    harness_report = audit_public_message_contract(public_harness_protocol)
    checks["public_harness_runtime"] = harness_report["message_controls_ready"] is True

    details: dict[str, Any] = {}
    allowlist, leakage, message_details = _message_and_leakage_probes(protocol)
    details["public_messages"] = message_details
    adversarial, adversarial_details = _adversarial_probes()
    details["adversarial"] = adversarial_details
    invariance, invariance_details = _invariance_probes()
    details["invariance"] = invariance_details
    with tempfile.TemporaryDirectory(prefix="chemworld-boundary-replay-") as temporary:
        replay, replay_details = _replay_probes(Path(temporary))
    details["replay"] = replay_details
    execution, execution_details = _execution_probes()
    details["execution"] = execution_details
    probe_groups = {
        "allowlist_schema": allowlist,
        "leakage": leakage,
        "adversarial": adversarial,
        "replay": replay,
        "invariance": invariance,
        "execution": execution,
    }
    declared_exact = (
        isinstance(declared_groups, Mapping)
        and all(
            set(probes) == set(declared_groups.get(group, ()))
            for group, probes in probe_groups.items()
        )
        and set(declared_groups) == set(probe_groups)
    )
    checks["probe_scope_exact"] = declared_exact
    all_probes_pass = all(all(probes.values()) for probes in probe_groups.values())
    controls_ready = all(checks.values()) and all_probes_pass
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "protocol_id": protocol.get("protocol_id"),
        "protocol_sha256": _canonical_sha256(protocol),
        "status": "controls_ready" if controls_ready else "controls_blocked",
        "controls_ready": controls_ready,
        "backend_freeze_allowed": controls_ready,
        "checks": checks,
        "probe_groups": probe_groups,
        "probe_count": sum(len(probes) for probes in probe_groups.values()),
        "dependency_bindings": dependency_reports,
        "details": details,
        "limitations": [
            (
                "This gate secures the public message and replay boundary; it is not a "
                "chemistry safety certification."
            ),
            (
                "The independent student process is a trusted local subprocess, not an "
                "operating-system sandbox."
            ),
            (
                "Untrusted submissions still require an external no-network, read-only, "
                "resource-limited container."
            ),
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--child-probe", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--expect-wheel", action="store_true")
    mode.add_argument("--expect-source", action="store_true")
    args = parser.parse_args()
    if args.child_probe:
        result = _child_probe(expect_wheel=bool(args.expect_wheel))
        print(json.dumps(result, sort_keys=True))
        return 0 if result["passed"] else 1
    report = build_report(load_protocol(args.protocol))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["controls_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
