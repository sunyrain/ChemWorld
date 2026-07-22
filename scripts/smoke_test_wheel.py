"""Build and exercise ChemWorld from a non-editable wheel installation."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def _validate_readiness_payload(
    payload: dict[str, object],
    *,
    require_validated_benchmark: bool,
) -> None:
    task_count = int(payload["serious_task_count"])
    contract_ready_count = int(payload["contract_ready_count"])
    benchmark_ready_count = int(payload["benchmark_ready_count"])
    suite_status = str(payload["serious_suite_status"])

    if task_count <= 0 or contract_ready_count != task_count:
        raise RuntimeError(f"Wheel task contracts are incomplete: {payload}")
    if suite_status == "candidate":
        if benchmark_ready_count != 0:
            raise RuntimeError(f"Candidate wheel carries inconsistent readiness: {payload}")
    elif suite_status == "validated":
        if benchmark_ready_count != task_count:
            raise RuntimeError(f"Validated wheel benchmark evidence is incomplete: {payload}")
    else:
        raise RuntimeError(f"Wheel carries an unknown suite status: {payload}")
    if require_validated_benchmark and suite_status != "validated":
        raise RuntimeError(f"Wheel does not carry validated benchmark evidence: {payload}")


def _validate_current_registry_payload(payload: dict[str, object]) -> None:
    expected = {
        "current_registry_schema": "chemworld-current-surface-registry-0.4",
        "project_role": "agent_capability_evaluation_and_training_environment",
        "environment_updates_agent_weights": False,
        "formal_results_present": False,
        "publication_ready": False,
    }
    mismatches = {
        key: {"expected": expected_value, "observed": payload.get(key)}
        for key, expected_value in expected.items()
        if payload.get(key) != expected_value
    }
    if mismatches:
        raise RuntimeError(
            f"Wheel current registry has inconsistent claim boundaries: {mismatches}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-validated-benchmark",
        action="store_true",
        help="Reject an installable candidate wheel that does not carry frozen empirical evidence.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="chemworld-wheel-smoke-") as temporary:
        workspace = Path(temporary)
        wheel_dir = workspace / "wheel"
        install_dir = workspace / "install"
        wheel_dir.mkdir()
        install_dir.mkdir()

        _run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                str(repository_root),
                "--no-deps",
                "--wheel-dir",
                str(wheel_dir),
            ],
            cwd=workspace,
        )
        wheels = sorted(wheel_dir.glob("chemworld_bench-*.whl"))
        if len(wheels) != 1:
            raise RuntimeError(f"Expected exactly one ChemWorld wheel, found {wheels}")
        _run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--target",
                str(install_dir),
                str(wheels[0]),
            ],
            cwd=workspace,
        )

        smoke = (
            "import json, pathlib, chemworld, gymnasium as gym; "
            "from chemworld.task_design import serious_task_readiness_manifest; "
            "from chemworld.eval.mechanism_adaptation_execution import ("
            "DEFAULT_GATE_A_PLAN_PATH, DEFAULT_PROTOCOL_PATH as mechanism_protocol); "
            "from chemworld.physchem.mechanism_library import configuration_root; "
            "env=gym.make('ChemWorld', task_id='reaction-to-assay', seed=0); "
            "obs,info=env.reset(seed=0); "
            "readiness=serious_task_readiness_manifest(); "
            "current_path=configuration_root() / 'current.json'; "
            "current=json.loads(current_path.read_text(encoding='utf-8')); "
            "print(json.dumps({'package': chemworld.__file__, "
            "'task_id': info['task_id'], 'observation_keys': sorted(obs), "
            "'serious_suite_status': readiness['suite_status'], "
            "'serious_task_count': len(readiness['task_ids']), "
            "'contract_ready_count': readiness['contract_ready_count'], "
            "'benchmark_ready_count': readiness['benchmark_ready_count'], "
            "'current_registry_schema': current['schema_version'], "
            "'current_registry_path': str(current_path), "
            "'project_role': current['project']['role'], "
            "'environment_updates_agent_weights': "
            "current['project']['environment_updates_agent_weights'], "
            "'formal_results_present': current['formal_evaluation']['formal_results_present'], "
            "'publication_ready': current['publication']['publication_ready'], "
            "'package_config_paths': [str(path) for path in ("
            "DEFAULT_GATE_A_PLAN_PATH, mechanism_protocol)]})); "
            "env.close()"
        )
        env = os.environ.copy()
        env["PYTHONPATH"] = str(install_dir)
        completed = subprocess.run(
            [sys.executable, "-c", smoke],
            cwd=workspace,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout.strip().splitlines()[-1])
        imported_path = Path(str(payload["package"])).resolve()
        if not imported_path.is_relative_to(install_dir.resolve()):
            raise RuntimeError(f"Smoke imported editable source instead of wheel: {imported_path}")
        if payload["task_id"] != "reaction-to-assay":
            raise RuntimeError(f"Unexpected wheel smoke task payload: {payload}")
        _validate_current_registry_payload(payload)
        _validate_readiness_payload(
            payload,
            require_validated_benchmark=args.require_validated_benchmark,
        )
        current_registry_path = Path(str(payload["current_registry_path"])).resolve()
        if not current_registry_path.is_relative_to(install_dir.resolve()):
            raise RuntimeError(
                f"Wheel used current registry outside installed resources: {payload}"
            )
        for raw_path in payload["package_config_paths"]:
            config_path = Path(str(raw_path)).resolve()
            if not config_path.is_relative_to(install_dir.resolve()) or not config_path.is_file():
                raise RuntimeError(
                    f"Wheel evaluation surface used a non-packaged config path: {payload}"
                )
        print(json.dumps({"wheel_smoke": "passed", **payload}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
