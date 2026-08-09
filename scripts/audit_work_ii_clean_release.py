#!/usr/bin/env python3
"""Audit Work II from a clean independent clone and emit an outcome-free receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import file_sha256, write_json_atomic
from chemworld.eval.work_ii_release import (
    CLEAN_RELEASE_RECEIPT_VERSION,
    clean_release_receipt_sha256,
    validate_clean_release_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GRAPH = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-prerun-evidence-graph-v0.1.json"
)
DEFAULT_OUTPUT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-clean-release-receipt-v0.1.json"
)
WORK_II_TEST_FILES = (
    "tests/test_work_ii_analysis.py",
    "tests/test_work_ii_analysis_plan_audit.py",
    "tests/test_work_ii_blind_evaluator.py",
    "tests/test_work_ii_campaign_runner.py",
    "tests/test_work_ii_formal_design.py",
    "tests/test_work_ii_formal_runner.py",
    "tests/test_work_ii_preregistration.py",
    "tests/test_work_ii_process_profile.py",
    "tests/test_work_ii_qualification.py",
    "tests/test_work_ii_release.py",
    "tests/test_work_ii_report.py",
    "tests/test_work_ii_truth.py",
)
FROZEN_CHECKS = (
    ("formal_preflight", "scripts/run_work_ii_formal_matrix.py", "--preflight", "--check"),
    ("method_qualification", "scripts/run_work_ii_method_qualification.py", "--check"),
    (
        "preregistration_readiness",
        "scripts/build_work_ii_preregistration_readiness.py",
        "--check",
    ),
    (
        "prerun_evidence_graph",
        "scripts/build_work_ii_prerun_evidence_graph.py",
        "--check",
    ),
)


def _text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _run(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout_s: int = 300,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=timeout_s,
    )
    if result.returncode != 0:
        command = " ".join(args[:4])
        detail = (result.stdout + "\n" + result.stderr)[-4000:]
        raise RuntimeError(f"command failed ({command}):\n{detail}")
    return result


def _git_output(*args: str, cwd: Path) -> str:
    return _run(["git", *args], cwd=cwd).stdout.strip()


def _python_environment(checkout: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(checkout / "src")
    env["PYTHONNOUSERSITE"] = "1"
    return env


def _progress(stage: str, completed: int, total: int, started: float) -> None:
    elapsed = max(time.monotonic() - started, 0.001)
    rate = completed / elapsed
    remaining = max(total - completed, 0)
    eta = remaining / rate if completed else 0.0
    print(
        f"[work-ii-release] stage={stage} completed={completed}/{total} "
        f"throughput={rate:.2f}_stages_per_s eta_s={eta:.1f}",
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--graph", type=Path, default=DEFAULT_GRAPH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    git = shutil.which("git")
    uv = shutil.which("uv")
    if git is None or uv is None:
        raise RuntimeError("git and uv are required for the clean-release audit")
    if _run([git, "diff", "--quiet"], cwd=ROOT).returncode != 0:
        raise RuntimeError("tracked working tree differs from HEAD")
    if _run([git, "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
        raise RuntimeError("index differs from HEAD")
    tested_commit = _git_output("rev-parse", f"{args.commit}^{{commit}}", cwd=ROOT)
    if tested_commit != _git_output("rev-parse", "HEAD", cwd=ROOT):
        raise RuntimeError("clean-release audit must test the current HEAD")

    total_stages = 9
    completed = 0
    started = time.monotonic()
    _progress("source_preflight", completed, total_stages, started)
    with tempfile.TemporaryDirectory(prefix="chemworld-work-ii-release-") as temp_name:
        temp = Path(temp_name).resolve()
        checkout = temp / "checkout"
        dist = temp / "dist"
        wheel_site = temp / "wheel-site"

        _run(
            [git, "clone", "--quiet", "--no-local", "--no-hardlinks", str(ROOT), str(checkout)],
            cwd=temp,
        )
        _run([git, "checkout", "--quiet", "--detach", tested_commit], cwd=checkout)
        if _git_output("status", "--porcelain", "--untracked-files=all", cwd=checkout):
            raise RuntimeError("independent checkout is not initially clean")
        completed += 1
        _progress("independent_clone", completed, total_stages, started)

        source_env = _python_environment(checkout)
        source_probe = _run(
            [
                sys.executable,
                "-c",
                (
                    "from pathlib import Path; import chemworld; "
                    "print(Path(chemworld.__file__).resolve())"
                ),
            ],
            cwd=checkout,
            env=source_env,
        )
        imported_source = Path(source_probe.stdout.strip()).resolve()
        if checkout not in imported_source.parents:
            raise RuntimeError("source probe did not import from the independent checkout")
        completed += 1
        _progress("independent_source_probe", completed, total_stages, started)

        check_records: list[dict[str, Any]] = []
        for check_id, script, *flags in FROZEN_CHECKS:
            result = _run(
                [sys.executable, script, *flags],
                cwd=checkout,
                env=source_env,
            )
            check_records.append(
                {
                    "id": check_id,
                    "status": "passed",
                    "stdout_sha256": _text_sha256(result.stdout),
                    "stderr_sha256": _text_sha256(result.stderr),
                }
            )
        completed += 1
        _progress("frozen_checks", completed, total_stages, started)

        graph_path = checkout / args.graph.resolve().relative_to(ROOT.resolve())
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        graph_summary = graph.get("summary", {})
        graph_record = {
            "status": "passed",
            "path": str(graph_path.relative_to(checkout)).replace("\\", "/"),
            "file_sha256": file_sha256(graph_path),
            "graph_sha256": graph.get("graph_sha256"),
            "node_count": graph_summary.get("node_count"),
            "edge_count": graph_summary.get("edge_count"),
        }
        completed += 1
        _progress("evidence_graph", completed, total_stages, started)

        tests = _run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "-o",
                "addopts=",
                *WORK_II_TEST_FILES,
            ],
            cwd=checkout,
            env=source_env,
        )
        pytest_output = tests.stdout + "\n" + tests.stderr
        match = re.search(r"(\d+) passed(?:, (\d+) skipped)? in ", pytest_output)
        if match is None:
            raise RuntimeError("could not parse the Work II pytest denominator")
        passed = int(match.group(1))
        skipped = int(match.group(2) or 0)
        if passed != 66 or skipped != 0:
            raise RuntimeError(
                f"unexpected Work II pytest result: passed={passed}, skipped={skipped}"
            )
        completed += 1
        _progress("work_ii_tests", completed, total_stages, started)

        build = _run(
            [uv, "build", "--offline", "--wheel", "--out-dir", str(dist), str(checkout)],
            cwd=checkout,
        )
        wheels = list(dist.glob("*.whl"))
        if len(wheels) != 1:
            raise RuntimeError(f"expected one wheel, found {len(wheels)}")
        wheel = wheels[0]
        completed += 1
        _progress("clean_wheel_build", completed, total_stages, started)

        install = _run(
            [
                uv,
                "pip",
                "install",
                "--offline",
                "--no-deps",
                "--target",
                str(wheel_site),
                str(wheel),
            ],
            cwd=temp,
        )
        completed += 1
        _progress("isolated_wheel_install", completed, total_stages, started)

        wheel_env = os.environ.copy()
        wheel_env["PYTHONPATH"] = str(wheel_site)
        wheel_env["PYTHONNOUSERSITE"] = "1"
        smoke = _run(
            [
                sys.executable,
                "-c",
                (
                    "import json; from importlib.resources import files; from pathlib import Path; "
                    "import chemworld; p=Path(chemworld.__file__).resolve(); "
                    "c=files('chemworld').joinpath('resources/configs'); "
                    "print(json.dumps({'module': str(p), 'configs': c.is_dir()}))"
                ),
            ],
            cwd=temp,
            env=wheel_env,
        )
        smoke_payload = json.loads(smoke.stdout.strip())
        installed_module = Path(smoke_payload["module"]).resolve()
        if wheel_site not in installed_module.parents or smoke_payload.get("configs") is not True:
            raise RuntimeError(
                "installed wheel smoke did not use its isolated site-packages/configs"
            )
        completed += 1
        _progress("installed_wheel_smoke", completed, total_stages, started)

        final_status = _git_output("status", "--porcelain", "--untracked-files=all", cwd=checkout)
        if final_status:
            raise RuntimeError("independent checkout changed during the release audit")
        completed += 1
        _progress("clean_after", completed, total_stages, started)

        receipt: dict[str, Any] = {
            "schema_version": CLEAN_RELEASE_RECEIPT_VERSION,
            "status": "passed",
            "formal_result": False,
            "formal_execution_allowed": False,
            "provider_calls_executed": 0,
            "formal_participant_outcome_count": 0,
            "tested_commit": tested_commit,
            "independent_checkout": {
                "mode": "git_clone_no_local",
                "path_recorded": False,
                "clean_before": True,
                "clean_after": True,
                "source_import_from_checkout": True,
                "source_probe_stdout_sha256": _text_sha256(source_probe.stdout),
            },
            "frozen_checks": {
                "status": "passed",
                "passed": len(check_records),
                "failed": 0,
                "checks": check_records,
            },
            "evidence_graph": graph_record,
            "work_ii_tests": {
                "status": "passed",
                "test_file_count": len(WORK_II_TEST_FILES),
                "passed": passed,
                "skipped": skipped,
                "failed": 0,
                "stdout_sha256": _text_sha256(tests.stdout),
                "stderr_sha256": _text_sha256(tests.stderr),
            },
            "wheel": {
                "status": "passed",
                "filename": wheel.name,
                "sha256": file_sha256(wheel),
                "bytes": wheel.stat().st_size,
                "installed_import_smoke": True,
                "bundled_configs_present": True,
                "dependency_source": "auditor_locked_environment",
                "build_stdout_sha256": _text_sha256(build.stdout),
                "build_stderr_sha256": _text_sha256(build.stderr),
                "install_stdout_sha256": _text_sha256(install.stdout),
                "install_stderr_sha256": _text_sha256(install.stderr),
                "smoke_stdout_sha256": _text_sha256(smoke.stdout),
                "smoke_stderr_sha256": _text_sha256(smoke.stderr),
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "uv": _run([uv, "--version"], cwd=temp).stdout.strip(),
            },
            "source_bindings": {
                "audit_script_sha256": file_sha256(
                    checkout / "scripts/audit_work_ii_clean_release.py"
                ),
                "evidence_graph_file_sha256": file_sha256(graph_path),
            },
            "failures": [],
        }
        receipt["receipt_sha256"] = clean_release_receipt_sha256(receipt)
        errors = validate_clean_release_receipt(receipt)
        if errors:
            raise RuntimeError("invalid Work II clean-release receipt: " + "; ".join(errors))
        write_json_atomic(args.output.resolve(), receipt)

    print(
        json.dumps(
            {
                "status": receipt["status"],
                "tested_commit": receipt["tested_commit"],
                "work_ii_tests_passed": receipt["work_ii_tests"]["passed"],
                "wheel_sha256": receipt["wheel"]["sha256"],
                "graph_sha256": receipt["evidence_graph"]["graph_sha256"],
                "provider_calls_executed": receipt["provider_calls_executed"],
                "receipt_sha256": receipt["receipt_sha256"],
                "output": str(args.output.resolve()),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
