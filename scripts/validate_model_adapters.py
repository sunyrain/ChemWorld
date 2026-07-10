"""Validate World Foundation adapter proposals before shared-file integration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chemworld.runtime.model_adapter_intake import (
    INTEGRATION_TARGET_WORLD_LAW,
    validate_adapter_manifests,
)


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
        help="Repository-relative directory whose JSON proposals are discovered.",
    )
    parser.add_argument(
        "--target-world-law",
        default=INTEGRATION_TARGET_WORLD_LAW,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/world_foundation/model_adapter_intake.json"),
    )
    parser.add_argument(
        "--require-manifests",
        action="store_true",
        help="Fail when no adapter proposal is present.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    manifest_dir = args.manifest_dir
    if not manifest_dir.is_absolute():
        manifest_dir = root / manifest_dir
    discovered = sorted(manifest_dir.glob("*.json")) if manifest_dir.is_dir() else []
    explicit = [
        path if path.is_absolute() else root / path
        for path in args.manifests
    ]
    paths = sorted({path.resolve() for path in (*discovered, *explicit)}, key=str)
    report = validate_adapter_manifests(
        paths,
        repository_root=root,
        target_world_law=args.target_world_law,
    )
    if args.require_manifests and not paths:
        report["passed"] = False
        report["empty_manifest_error"] = "no adapter proposals were discovered"
    output = args.output
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({**report, "output": str(output)}, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
