"""Build a read-only World Law vNext staging plan from adapter proposals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.runtime.model_adapter_intake import INTEGRATION_TARGET_WORLD_LAW
from chemworld.runtime.vnext_staging import build_vnext_integration_plan


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="*", type=Path)
    parser.add_argument("--root", type=Path, default=repository_root())
    parser.add_argument(
        "--manifest-dir",
        type=Path,
        default=Path("workstreams/world_foundation/adapters"),
    )
    parser.add_argument("--target-world-law", default=INTEGRATION_TARGET_WORLD_LAW)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/world_foundation/vnext_integration_plan.json"),
    )
    parser.add_argument(
        "--require-integration-ready",
        action="store_true",
        help="Fail unless at least one completed, accepted proposal is ready for review.",
    )
    parser.add_argument(
        "--require-runtime-replacement",
        action="store_true",
        help="Fail unless at least one runtime replacement proposal is staged.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    manifest_dir = args.manifest_dir
    if not manifest_dir.is_absolute():
        manifest_dir = root / manifest_dir
    discovered = sorted(manifest_dir.glob("*.json")) if manifest_dir.is_dir() else []
    explicit = [path if path.is_absolute() else root / path for path in args.manifests]
    paths = sorted({path.resolve() for path in (*discovered, *explicit)}, key=str)
    report = build_vnext_integration_plan(
        paths,
        repository_root=root,
        target_world_law=args.target_world_law,
    )
    requirement_errors: list[str] = []
    if args.require_integration_ready and report["integration_ready_count"] == 0:
        requirement_errors.append("no completed adapter proposal is integration-ready")
    if args.require_runtime_replacement and report["runtime_replacement_count"] == 0:
        requirement_errors.append("no runtime replacement proposal is staged")
    if requirement_errors:
        report["passed"] = False
        report["requirement_errors"] = requirement_errors
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({**report, "output": str(output)}, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
