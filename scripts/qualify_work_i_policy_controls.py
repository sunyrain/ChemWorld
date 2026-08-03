"""Qualify the V05/V06 policy-control chain and freeze the W1-V07 receipt."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from chemworld.eval.policy_validity_qualification import (
    PolicyQualificationError,
    assert_qualification_outputs_absent,
    build_qualification,
    build_qualification_delivery_manifest,
    load_qualification_protocol,
)
from chemworld.eval.provenance import write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/benchmark/work_i_policy_control_qualification_v0.1.json"


def _json_text(payload: dict[str, object]) -> str:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def _directory_bytes(root: Path) -> dict[str, bytes]:
    if not root.is_dir():
        raise PolicyQualificationError(f"missing qualification artifact directory: {root}")
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file())
    }


def _write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run outcome-free synthetic and fixed-nonformal qualification. This command "
            "never invokes the W1-V08 formal executor."
        )
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Rebuild in a temporary directory and compare every frozen byte.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    protocol = load_qualification_protocol(config_path)
    paths = protocol["output_paths"]
    committed_artifact_root = ROOT / str(paths["artifact_root"])
    report_path = ROOT / str(paths["report"])
    markdown_path = ROOT / str(paths["markdown"])
    receipt_path = ROOT / str(paths["receipt"])
    delivery_manifest_path = ROOT / str(paths["delivery_manifest"])
    try:
        delivery_manifest_relative = delivery_manifest_path.relative_to(
            committed_artifact_root
        )
    except ValueError as exc:
        raise PolicyQualificationError(
            "delivery manifest must be inside the qualification artifact root"
        ) from exc

    if args.check:
        with tempfile.TemporaryDirectory(prefix="chemworld-v07-check-") as temporary:
            temporary_root = Path(temporary) / "artifacts"
            report, receipt, markdown = build_qualification(
                root=ROOT,
                protocol_path=config_path,
                artifact_root=temporary_root,
            )
            delivery_manifest = build_qualification_delivery_manifest(
                qualification_protocol=protocol,
                artifact_root=temporary_root,
                report=report,
                receipt=receipt,
                markdown=markdown,
            )
            write_json_atomic(
                temporary_root / delivery_manifest_relative,
                delivery_manifest,
            )
            if _directory_bytes(temporary_root) != _directory_bytes(
                committed_artifact_root
            ):
                raise PolicyQualificationError(
                    "committed qualification artifact directory differs from rebuild"
                )
            if report_path.read_text(encoding="utf-8") != _json_text(report):
                raise PolicyQualificationError(
                    "committed qualification report differs from rebuild"
                )
            if receipt_path.read_text(encoding="utf-8") != _json_text(receipt):
                raise PolicyQualificationError(
                    "committed qualification receipt differs from rebuild"
                )
            if markdown_path.read_text(encoding="utf-8") != markdown:
                raise PolicyQualificationError(
                    "committed qualification markdown differs from rebuild"
                )
            if delivery_manifest_path.read_text(encoding="utf-8") != _json_text(
                delivery_manifest
            ):
                raise PolicyQualificationError(
                    "committed qualification delivery manifest differs from rebuild"
                )
    else:
        assert_qualification_outputs_absent(ROOT, protocol)
        report, receipt, markdown = build_qualification(
            root=ROOT,
            protocol_path=config_path,
            artifact_root=committed_artifact_root,
        )
        delivery_manifest = build_qualification_delivery_manifest(
            qualification_protocol=protocol,
            artifact_root=committed_artifact_root,
            report=report,
            receipt=receipt,
            markdown=markdown,
        )
        write_json_atomic(report_path, report)
        write_json_atomic(receipt_path, receipt)
        _write_text_atomic(markdown_path, markdown)
        write_json_atomic(delivery_manifest_path, delivery_manifest)

    print(
        json.dumps(
            {
                "check": bool(args.check),
                "formal_environment_execution_count": report[
                    "formal_environment_execution_count"
                ],
                "formal_outcome_read_count": report["formal_outcome_read_count"],
                "qualification_report_sha256": report["report_sha256"],
                "receipt_sha256": receipt["receipt_sha256"],
                "status": report["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
