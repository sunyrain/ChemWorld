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
            "from chemworld.eval.benchmark_validation import official_validation_path; "
            "env=gym.make('ChemWorld', task_id='reaction-to-assay', seed=0); "
            "obs,info=env.reset(seed=0); "
            "readiness=serious_task_readiness_manifest(); "
            "print(json.dumps({'package': chemworld.__file__, "
            "'task_id': info['task_id'], 'observation_keys': sorted(obs), "
            "'serious_suite_status': readiness['suite_status'], "
            "'serious_task_count': len(readiness['task_ids']), "
            "'contract_ready_count': readiness['contract_ready_count'], "
            "'benchmark_ready_count': readiness['benchmark_ready_count'], "
            "'official_validation_path': str(official_validation_path())})); "
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
        _validate_readiness_payload(
            payload,
            require_validated_benchmark=args.require_validated_benchmark,
        )
        validation_path = Path(str(payload["official_validation_path"])).resolve()
        if not validation_path.is_relative_to(install_dir.resolve()):
            raise RuntimeError(f"Wheel used validation outside installed resources: {payload}")
        print(json.dumps({"wheel_smoke": "passed", **payload}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
