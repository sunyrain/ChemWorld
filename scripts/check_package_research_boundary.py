"""Prevent new package modules from depending on repository-only research paths."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Final

FORBIDDEN_PREFIXES: Final = (
    "configs/benchmark/",
    "paper/",
    "scripts/",
    "workstreams/",
)
FORBIDDEN_ROOT_LITERALS: Final = {
    "configs/benchmark": "configs/benchmark/",
    "scripts": "scripts/",
    "workstreams": "workstreams/",
}
BASELINE_PATH: Final = Path(
    "workstreams/repository_quality/package_research_boundary_baseline.json"
)


def _literal_families(value: str) -> set[str]:
    normalized = value.replace("\\", "/").lstrip("./")
    families = {prefix for prefix in FORBIDDEN_PREFIXES if normalized.startswith(prefix)}
    root_family = FORBIDDEN_ROOT_LITERALS.get(normalized.rstrip("/"))
    if root_family is not None:
        families.add(root_family)
    return families


def scan(root: Path) -> dict[str, list[str]]:
    """Return package modules and their repository-only literal families."""

    findings: dict[str, set[str]] = {}
    for path in sorted((root / "src" / "chemworld").rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as error:
            raise RuntimeError(f"unable to parse package module: {path}") from error
        families = {
            family
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            for family in _literal_families(node.value)
        }
        if families:
            relative = path.relative_to(root).as_posix()
            findings[relative] = families
    return {path: sorted(families) for path, families in sorted(findings.items())}


def _load_baseline(root: Path) -> dict[str, list[str]]:
    path = root / BASELINE_PATH
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"unable to load boundary baseline: {path}") from error
    if not isinstance(value, dict) or not all(
        isinstance(key, str)
        and isinstance(families, list)
        and all(isinstance(family, str) for family in families)
        for key, families in value.items()
    ):
        raise RuntimeError(f"invalid boundary baseline: {path}")
    return {key: sorted(families) for key, families in sorted(value.items())}


def audit(root: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    current = scan(root)
    baseline = _load_baseline(root)
    regressions = [
        f"{path}: {family}"
        for path, families in current.items()
        for family in families
        if family not in baseline.get(path, [])
    ]
    resolved = [
        f"{path}: {family}"
        for path, families in baseline.items()
        for family in families
        if family not in current.get(path, [])
    ]
    return regressions, resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    try:
        regressions, resolved = audit(arguments.root)
    except RuntimeError as error:
        print(f"package-boundary guard could not run: {error}")
        return 2
    if regressions:
        print("package-boundary guard failed; new repository-only dependencies:")
        for regression in regressions:
            print(f"- {regression}")
        return 1
    print("package-boundary guard passed")
    if resolved:
        print(f"baseline entries eligible for removal: {len(resolved)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
