"""Validate or execute one preflight-issued ChemWorld formal cell."""

from __future__ import annotations

import argparse
import importlib
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, cast

from chemworld.eval.formal_runner import (
    FormalCellSpec,
    FormalExecutionAdapter,
    PrivateCellRuntime,
    discard_incomplete_staging,
    load_issued_cell,
    run_formal_cell,
)


def _read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object required: {path}")
    return payload


def _load_adapter_factory(reference: str) -> Callable[[FormalCellSpec], FormalExecutionAdapter]:
    module_name, separator, attribute_name = reference.partition(":")
    if not separator or not module_name or not attribute_name:
        raise ValueError("adapter factory must use module.path:callable syntax")
    factory = getattr(importlib.import_module(module_name), attribute_name)
    if not callable(factory):
        raise TypeError("adapter factory reference is not callable")
    return cast(Callable[[FormalCellSpec], FormalExecutionAdapter], factory)


def _summary(payload: Mapping[str, Any]) -> None:
    print(json.dumps(dict(payload), indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--cell-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--private-runtime", type=Path)
    parser.add_argument("--adapter-factory")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate issuance without resolving private runtime values",
    )
    parser.add_argument(
        "--discard-incomplete",
        action="store_true",
        help="explicitly delete unpublished staging attempts before execution",
    )
    args = parser.parse_args()

    try:
        manifest = _read_object(args.manifest)
        issued = load_issued_cell(manifest, cell_identity_sha256=args.cell_id)
        if args.validate_only:
            _summary(
                {
                    "cell_identity_sha256": issued.spec.cell_identity_sha256,
                    "issued": True,
                    "method_id": issued.spec.method.method_id,
                    "method_kind": issued.spec.method.kind,
                    "run_manifest_sha256": issued.run_manifest_sha256,
                    "task_id": issued.spec.task_id,
                }
            )
            return 0
        if args.private_runtime is None or args.adapter_factory is None:
            parser.error("execution requires --private-runtime and --adapter-factory")
        if args.discard_incomplete:
            discarded = discard_incomplete_staging(
                args.output_dir,
                cell_identity_sha256=issued.spec.cell_identity_sha256,
            )
        else:
            discarded = 0
        runtime = PrivateCellRuntime.from_payload(_read_object(args.private_runtime))
        adapter = _load_adapter_factory(args.adapter_factory)(issued.spec)
        outcome = run_formal_cell(
            issued_cell=issued,
            runtime=runtime,
            adapter=adapter,
            output_root=args.output_dir,
        )
    except (OSError, ValueError, TypeError, RuntimeError) as exc:
        parser.exit(2, f"formal cell rejected: {type(exc).__name__}: {exc}\n")

    _summary(
        {
            "cached": outcome.cached,
            "cell_dir": str(outcome.cell_dir),
            "cell_identity_sha256": outcome.cell_identity_sha256,
            "discarded_incomplete_attempts": discarded,
            "failure_class": outcome.failure_class,
            "status": outcome.status,
        }
    )
    return 0 if outcome.status == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
