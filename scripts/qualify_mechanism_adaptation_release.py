"""Run the targeted RC27 release qualification without consuming formal cohorts."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from chemworld.agents.prompt_context import build_decision_prompt  # noqa: E402
from chemworld.eval.mechanism_adaptation_execution import (  # noqa: E402
    DEFAULT_GATE_A_PLAN_PATH,
    DEFAULT_PROTOCOL_PATH,
    PublicCampaignObservationSession,
    build_action_library,
    load_json_object,
    load_protocol_object,
    validate_precomputed_design_audit,
)
from chemworld.eval.mechanism_relation_graph import (  # noqa: E402
    validate_diagnostic_relation_graph,
)
from chemworld.eval.provenance import (  # noqa: E402
    canonical_json_sha256,
    write_json_atomic,
)
from chemworld.eval.trial_store import (  # noqa: E402
    ConfirmatoryTrialKey,
    ConfirmatoryTrialStore,
    execute_jobs_resumable,
)

DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "mechanism-adaptation-release-qualification-v0.1-rc27.json"
)
TARGETED_TESTS = (
    "tests/test_prompt_context.py",
    "tests/test_trial_store.py",
    "tests/test_keyed_observation_noise.py",
    "tests/test_mechanism_release.py",
    "tests/test_live_llm_agent.py",
    "tests/test_agent_interaction_contract.py",
    "tests/test_agent_interaction.py",
    "tests/test_flagship_mechanism_diagnostics.py",
    "tests/test_mechanism_adaptation.py",
    "tests/test_mechanism_adaptation_execution.py",
    "tests/test_mechanism_preregistration.py",
)
RUFF_TARGETS = (
    "scripts/run_mechanism_adaptation.py",
    "scripts/qualify_mechanism_adaptation_release.py",
    "src/chemworld/agents/prompt_context.py",
    "src/chemworld/agents/live_llm.py",
    "src/chemworld/agents/diagnostic_live_llm.py",
    "src/chemworld/agents/mechanism_adaptation_live_llm.py",
    "src/chemworld/agents/interaction.py",
    "src/chemworld/envs/observation_noise.py",
    "src/chemworld/envs/chemworld_env.py",
    "src/chemworld/envs/reports.py",
    "src/chemworld/eval/trial_store.py",
    "src/chemworld/eval/mechanism_release.py",
    "src/chemworld/eval/mechanism_adaptation_execution.py",
    "src/chemworld/eval/mechanism_preregistration.py",
)


def _source_binding_command(source_commit: str) -> list[str]:
    return [
        "git",
        "diff",
        "--exit-code",
        source_commit,
        "--",
        "src/chemworld",
        "scripts",
        "configs/benchmark/mechanism_adaptation_v0.3.0_rc27.json",
        "configs/benchmark/"
        "mechanism_adaptation_gate_a_v0.3.0_rc27.json",
        "configs/benchmark/"
        "mechanism_adaptation_participant_preregistration_rc27.json",
        "configs/methods/llm_v0.4/llm_methods_rc25.json",
        "configs/methods/llm_v0.4/llm_methods.json",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-diagnostic-relation-graph-v0.3.0-rc27.json",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-design-audit-freeze-rc27.json",
        "workstreams/flagship_tasks/reports/"
        "mechanism-adaptation-sample-size-audit-v0.3.0-rc27.json",
        "workstreams/flagship_tasks/reports/"
        "confirmatory-task-semantics-audit-rc27.json",
        *TARGETED_TESTS,
    ]


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _run(command: list[str]) -> dict[str, Any]:
    started = time.monotonic()
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "command": command,
        "exit_code": result.returncode,
        "wall_time_s": round(time.monotonic() - started, 3),
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
        "passed": result.returncode == 0,
    }


def _qualification_job(job: dict[str, Any]) -> dict[str, int]:
    value = int(job["value"])
    return {"value": value, "square": value * value}


def _development_sentinel(
    protocol: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    seed = int(
        plan["release_qualification"]["development_seed_namespace_start"]
    )
    task_id = "electrochemical-conversion"
    library = build_action_library(task_id, action_count=3, seed=41102)
    action_id = next(iter(library))
    selected = {action_id: library[action_id]}
    noise_keys: list[str] = []
    traces: list[list[float]] = []
    for interventions in (
        (),
        tuple(
            protocol["task_mechanism_contracts"][task_id]["interventions"][
                "constitutive_law_family"
            ]
        ),
    ):
        with PublicCampaignObservationSession(
            task_id=task_id,
            seed=seed,
            interventions=interventions,
            action_library=selected,
            experiment_horizon=1,
            observation_seed=seed + 1,
            observation_noise_namespace="rc27-release-qualification",
        ) as session:
            traces.append(session.observe(action_id))
            operation_noise = session.observation_noise_audit[0][
                "operation_noise"
            ]
            noise_keys.append(
                canonical_json_sha256(
                    [
                        item.get("noise_key_sha256")
                        for item in operation_noise
                    ]
                )
            )
    curve = [index / 100 for index in range(241)]
    prompt = build_decision_prompt(
        task_contract={
            "task_id": task_id,
            "task_goal": "Diagnose and recover from a hidden relation change.",
        },
        decision_context={
            "step": 1,
            "campaign_state": {"remaining_budget": 8},
            "latest_spectra": {
                "has_spectral_packet": True,
                "raw_signal": {
                    "kind": "uvvis_spectrum",
                    "wavelength": curve,
                    "intensity": curve,
                    "peaks": [{"wavelength": 0.4, "assignment": "target"}],
                },
            },
        },
        tool_json={
            "available_actions": [{"operation": "measure"}],
        },
        experiment_memory=[],
        recent_decisions=[],
    )
    with tempfile.TemporaryDirectory(prefix="chemworld-rc27-qualification-") as raw:
        store = ConfirmatoryTrialStore(Path(raw) / "trial-store")
        jobs = [{"value": 1}, {"value": 2}]
        keys = [
            ConfirmatoryTrialKey(
                task_id="qualification",
                truth_family="synthetic",
                world_cluster=str(index),
                changepoint="not_applicable",
                arm="resume",
            )
            for index in (1, 2)
        ]
        execute_jobs_resumable(
            _qualification_job,
            jobs,
            keys,
            workers=1,
            store=store,
            resume=False,
        )
        results, manifest = execute_jobs_resumable(
            _qualification_job,
            jobs,
            keys,
            workers=1,
            store=store,
            resume=True,
        )
    return {
        "formal_result": False,
        "seed_namespace_start": seed,
        "formal_a2_or_a3_seed_consumed": False,
        "task_id": task_id,
        "paired_noise_key_bundle_match": noise_keys[0] == noise_keys[1],
        "paired_trace_lengths": [len(item) for item in traces],
        "prompt_estimated_tokens": prompt.estimated_tokens,
        "prompt_cap": prompt.max_estimated_tokens,
        "raw_arrays_in_prompt": (
            '"intensity":[' in prompt.text
            or '"wavelength":[' in prompt.text
        ),
        "resume_results": results,
        "trial_manifest": manifest,
        "passed": (
            noise_keys[0] == noise_keys[1]
            and prompt.estimated_tokens <= prompt.max_estimated_tokens
            and '"intensity":[' not in prompt.text
            and manifest["complete"] is True
            and manifest["completed_count"] == 2
        ),
    }


def build_qualification(
    *,
    protocol_path: Path,
    plan_path: Path,
    source_commit: str,
    run_tests: bool,
) -> dict[str, Any]:
    protocol = load_protocol_object(protocol_path)
    plan = load_json_object(plan_path)
    relation_graph = load_json_object(
        ROOT / plan["diagnostic_relation_graph"]["report"]
    )
    design_audit = load_json_object(
        ROOT / plan["design_validity_precondition"]["report"]
    )
    sample_size = load_json_object(ROOT / plan["sample_size_audit"]["report"])
    semantics = load_json_object(
        ROOT
        / "workstreams/flagship_tasks/reports/"
        "confirmatory-task-semantics-audit-rc27.json"
    )
    source_binding = _run(_source_binding_command(source_commit))
    static_errors = validate_diagnostic_relation_graph(
        protocol,
        plan,
        relation_graph,
    )
    try:
        validate_precomputed_design_audit(protocol, plan, design_audit)
    except ValueError as error:
        static_errors.append(str(error))
    artifact_checks = {
        "diagnostic_relation_graph": not static_errors,
        "design_audit": design_audit.get("pass") is True,
        "sample_size_audit": sample_size.get("pass") is True,
        "semantic_protocol_audit": semantics.get("pass") is True,
    }
    ruff = _run(
        [sys.executable, "-m", "ruff", "check", *RUFF_TARGETS]
    )
    tests = (
        _run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-o",
                "addopts=",
                "-q",
                *TARGETED_TESTS,
                "--tb=short",
            ]
        )
        if run_tests
        else {
            "command": [],
            "exit_code": None,
            "passed": False,
            "status": "not_run",
        }
    )
    sentinel = _development_sentinel(protocol, plan)
    qualified = (
        source_binding["passed"]
        and not static_errors
        and all(artifact_checks.values())
        and ruff["passed"]
        and tests["passed"]
        and sentinel["passed"]
    )
    payload = {
        "schema_version": "chemworld-mechanism-release-qualification-0.1",
        "release_candidate": "rc27",
        "status": "passed" if qualified else "failed",
        "qualified": qualified,
        "formal_result": False,
        "source_commit": source_commit,
        "head_at_qualification": _git("rev-parse", "HEAD"),
        "protocol_sha256": canonical_json_sha256(protocol),
        "gate_a_plan_sha256": canonical_json_sha256(plan),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "source_binding": source_binding,
        "artifact_checks": artifact_checks,
        "static_errors": static_errors,
        "ruff": ruff,
        "targeted_tests": tests,
        "development_end_to_end_sentinel": sentinel,
        "full_repository_test_run": False,
        "formal_cohorts_consumed": False,
    }
    payload["qualification_sha256"] = canonical_json_sha256(payload)
    return payload


def validate_recorded_qualification(
    report: dict[str, Any],
    *,
    protocol_path: Path,
    plan_path: Path,
    expected_source_commit: str | None,
) -> list[str]:
    """Validate immutable receipts without rerunning nondeterministic commands."""

    errors: list[str] = []
    protocol = load_protocol_object(protocol_path)
    plan = load_json_object(plan_path)
    recorded_hash = report.get("qualification_sha256")
    unsigned = dict(report)
    unsigned.pop("qualification_sha256", None)
    if recorded_hash != canonical_json_sha256(unsigned):
        errors.append("qualification_sha256 does not match the recorded payload")
    if report.get("schema_version") != (
        "chemworld-mechanism-release-qualification-0.1"
    ):
        errors.append("unexpected release qualification schema")
    if report.get("release_candidate") != "rc27":
        errors.append("release candidate is not rc27")
    if report.get("status") != "passed" or report.get("qualified") is not True:
        errors.append("release qualification did not pass")
    for field in (
        "formal_result",
        "full_repository_test_run",
        "formal_cohorts_consumed",
    ):
        if report.get(field) is not False:
            errors.append(f"{field} must remain false")
    if report.get("protocol_sha256") != canonical_json_sha256(protocol):
        errors.append("protocol hash drift")
    if report.get("gate_a_plan_sha256") != canonical_json_sha256(plan):
        errors.append("Gate A plan hash drift")
    source_commit = report.get("source_commit")
    if not isinstance(source_commit, str) or not source_commit:
        errors.append("missing source_commit")
    else:
        if (
            expected_source_commit is not None
            and expected_source_commit != source_commit
        ):
            errors.append("requested source commit differs from recorded receipt")
        source_binding = _run(_source_binding_command(source_commit))
        if not source_binding["passed"]:
            errors.append("qualified source paths drifted from source_commit")
        ancestor = _run(
            ["git", "merge-base", "--is-ancestor", source_commit, "HEAD"]
        )
        if not ancestor["passed"]:
            errors.append("source_commit is not an ancestor of HEAD")
    for field in ("source_binding", "ruff", "targeted_tests"):
        if report.get(field, {}).get("passed") is not True:
            errors.append(f"recorded {field} receipt did not pass")
    sentinel = report.get("development_end_to_end_sentinel", {})
    if sentinel.get("passed") is not True:
        errors.append("recorded development sentinel did not pass")
    if sentinel.get("formal_result") is not False:
        errors.append("development sentinel is incorrectly marked formal")
    if sentinel.get("formal_a2_or_a3_seed_consumed") is not False:
        errors.append("development sentinel consumed a formal seed")
    artifact_checks = report.get("artifact_checks", {})
    if not artifact_checks or not all(artifact_checks.values()):
        errors.append("one or more recorded static artifact checks failed")
    relation_graph = load_json_object(
        ROOT / plan["diagnostic_relation_graph"]["report"]
    )
    current_static_errors = validate_diagnostic_relation_graph(
        protocol,
        plan,
        relation_graph,
    )
    design_audit = load_json_object(
        ROOT / plan["design_validity_precondition"]["report"]
    )
    try:
        validate_precomputed_design_audit(protocol, plan, design_audit)
    except ValueError as error:
        current_static_errors.append(str(error))
    sample_size = load_json_object(ROOT / plan["sample_size_audit"]["report"])
    semantics = load_json_object(
        ROOT
        / "workstreams/flagship_tasks/reports/"
        "confirmatory-task-semantics-audit-rc27.json"
    )
    if sample_size.get("pass") is not True:
        current_static_errors.append("current sample-size audit did not pass")
    if semantics.get("pass") is not True:
        current_static_errors.append("current semantic audit did not pass")
    errors.extend(current_static_errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL_PATH)
    parser.add_argument("--plan", type=Path, default=DEFAULT_GATE_A_PLAN_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--source-commit")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"missing release qualification: {args.output}")
        report = json.loads(args.output.read_text(encoding="utf-8"))
        errors = validate_recorded_qualification(
            report,
            protocol_path=args.protocol,
            plan_path=args.plan,
            expected_source_commit=args.source_commit,
        )
        if errors:
            raise SystemExit(
                "release qualification is invalid:\n- " + "\n- ".join(errors)
            )
    else:
        source_commit = args.source_commit or _git("rev-parse", "HEAD")
        report = build_qualification(
            protocol_path=args.protocol,
            plan_path=args.plan,
            source_commit=source_commit,
            run_tests=not args.skip_tests,
        )
        if args.output.exists():
            raise SystemExit(
                "release qualification is immutable; select a new output"
            )
        write_json_atomic(args.output, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "qualified": report["qualified"],
                "source_commit": report["source_commit"],
                "output": str(args.output.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["qualified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
