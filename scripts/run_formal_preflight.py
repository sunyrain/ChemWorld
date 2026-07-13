"""Audit and issue a ChemWorld formal run manifest without a force bypass."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import uuid
from pathlib import Path
from typing import Any

from chemworld.eval.formal_preflight import run_formal_preflight


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object required: {path}")
    return payload


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex[:12]}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--private-assignments", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    parser.add_argument("--private-runtime-output-dir", type=Path, required=True)
    parser.add_argument("--report-output", type=Path, required=True)
    args = parser.parse_args()

    try:
        request = _read_object(args.request.resolve(strict=True))
        private = _read_object(args.private_assignments.resolve(strict=True))
        manifest_output = args.manifest_output.resolve()
        report_output = args.report_output.resolve()
        private_output = args.private_runtime_output_dir.resolve()
        if manifest_output.exists() or report_output.exists() or private_output.exists():
            parser.error("preflight outputs must not already exist")
        outcome = run_formal_preflight(
            request,
            private,
            repository_root=args.repo_root.resolve(strict=True),
        )
        print(json.dumps(outcome.report, indent=2, sort_keys=True), flush=True)
        if not outcome.passed:
            _atomic_json(report_output, outcome.report)
            return 1
        assert outcome.run_manifest is not None and outcome.private_runtimes is not None
        staging = private_output.with_name(
            f".{private_output.name}.staging-{uuid.uuid4().hex[:12]}"
        )
        staging.mkdir(parents=True, exist_ok=False)
        try:
            for cell_id, runtime in outcome.private_runtimes.items():
                runtime_path = staging / f"{cell_id}.json"
                runtime_path.write_text(
                    json.dumps(runtime, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                runtime_path.chmod(0o600)
            os.replace(staging, private_output)
        except BaseException:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        _atomic_json(report_output, outcome.report)
        # The manifest is the issuance authority and is therefore published last.
        _atomic_json(manifest_output, outcome.run_manifest)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        parser.exit(2, f"formal preflight error: {type(exc).__name__}: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
