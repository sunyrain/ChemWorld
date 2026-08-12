"""Prevent new upward imports across the portable ChemWorld package layers."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Final

BASELINE_PATH: Final = Path("workstreams/repository_quality/package_import_boundary_baseline.json")
FORBIDDEN_TARGETS: Final[dict[str, frozenset[str]]] = {
    "foundation": frozenset(
        {"physchem", "world", "runtime", "envs", "data", "agents", "providers", "eval", "rl"}
    ),
    "physchem": frozenset(
        {"world", "runtime", "envs", "data", "agents", "providers", "eval", "rl"}
    ),
    "world": frozenset({"runtime", "envs", "data", "agents", "providers", "eval", "rl"}),
    "runtime": frozenset({"envs", "data", "agents", "providers", "eval", "rl"}),
    "envs": frozenset({"data", "agents", "providers", "eval", "rl"}),
    "data": frozenset({"envs", "agents", "providers", "eval", "rl"}),
}


def _chemworld_target(module: str | None) -> str | None:
    if not module or not module.startswith("chemworld."):
        return None
    parts = module.split(".")
    return parts[1] if len(parts) > 1 else None


def scan(root: Path) -> dict[str, list[str]]:
    """Return reviewed upward dependency edges as source-path to target-package mappings."""

    findings: dict[str, set[str]] = {}
    package_root = root / "src" / "chemworld"
    for source_package, forbidden_targets in FORBIDDEN_TARGETS.items():
        source_root = package_root / source_package
        if not source_root.is_dir():
            continue
        for path in sorted(source_root.rglob("*.py")):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (OSError, UnicodeError, SyntaxError) as error:
                raise RuntimeError(f"unable to parse package module: {path}") from error
            targets: set[str] = set()
            for node in ast.walk(tree):
                modules: list[str | None]
                if isinstance(node, ast.ImportFrom):
                    modules = [node.module]
                elif isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                else:
                    continue
                for module in modules:
                    target = _chemworld_target(module)
                    if target in forbidden_targets:
                        targets.add(target)
            if targets:
                findings[path.relative_to(root).as_posix()] = targets
    return {path: sorted(targets) for path, targets in sorted(findings.items())}


def _load_baseline(root: Path) -> dict[str, list[str]]:
    path = root / BASELINE_PATH
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"unable to load import-boundary baseline: {path}") from error
    if not isinstance(value, dict) or not all(
        isinstance(key, str)
        and isinstance(targets, list)
        and all(isinstance(target, str) for target in targets)
        for key, targets in value.items()
    ):
        raise RuntimeError(f"invalid import-boundary baseline: {path}")
    return {key: sorted(targets) for key, targets in sorted(value.items())}


def audit(root: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    current = scan(root)
    baseline = _load_baseline(root)
    regressions = [
        f"{path}: chemworld.{target}"
        for path, targets in current.items()
        for target in targets
        if target not in baseline.get(path, [])
    ]
    resolved = [
        f"{path}: chemworld.{target}"
        for path, targets in baseline.items()
        for target in targets
        if target not in current.get(path, [])
    ]
    return regressions, resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    try:
        regressions, resolved = audit(arguments.root)
    except RuntimeError as error:
        print(f"package import-boundary guard could not run: {error}")
        return 2
    if regressions:
        print("package import-boundary guard failed; new upward imports:")
        for regression in regressions:
            print(f"- {regression}")
        return 1
    print("package import-boundary guard passed")
    if resolved:
        print(f"baseline entries eligible for removal: {len(resolved)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
