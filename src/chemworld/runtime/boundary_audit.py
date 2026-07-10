"""Static boundary checks for the ChemWorld transactional runtime."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from chemworld.world.operations import OPERATION_TYPES

REMOVED_CORE_MODULE = "chemworld" + ".core"


@dataclass(frozen=True)
class RuntimeBoundaryFinding:
    check_id: str
    path: str
    lineno: int
    message: str
    severity: str = "error"

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "path": self.path,
            "lineno": self.lineno,
            "message": self.message,
            "severity": self.severity,
        }


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def python_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.py")
        if "__pycache__" not in path.parts
    )


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def parse_python(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def imports_legacy_core(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(
            alias.name == REMOVED_CORE_MODULE
            or alias.name.startswith(f"{REMOVED_CORE_MODULE}.")
            for alias in node.names
        )
    if isinstance(node, ast.ImportFrom):
        module = node.module or ""
        return module == REMOVED_CORE_MODULE or module.startswith(f"{REMOVED_CORE_MODULE}.")
    return False


def scan_legacy_core_imports(root: Path) -> list[RuntimeBoundaryFinding]:
    src_root = root / "src" / "chemworld"
    findings: list[RuntimeBoundaryFinding] = []
    for path in python_files(src_root):
        if "core" in path.relative_to(src_root).parts[:1]:
            continue
        tree = parse_python(path)
        for node in ast.walk(tree):
            if imports_legacy_core(node):
                findings.append(
                    RuntimeBoundaryFinding(
                        "legacy_core_import",
                        relative(path, root),
                        getattr(node, "lineno", 0),
                        "Runtime-facing source must not import the legacy core package.",
                    )
                )
    return findings


def scan_core_package_removed(root: Path) -> list[RuntimeBoundaryFinding]:
    core_root = root / "src" / "chemworld" / "core"
    core_sources = [
        path
        for path in core_root.glob("*.py")
        if path.name != "__init__.py"
    ]
    return [
        RuntimeBoundaryFinding(
            "legacy_core_source_present",
            relative(path, root),
            1,
            "The legacy core package must not contain runtime source files.",
        )
        for path in core_sources
    ]


def node_contains_operation_accessor(node: ast.AST) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.Attribute) and child.attr == "operation_type":
            return True
        if (
            isinstance(child, ast.Subscript)
            and isinstance(child.value, ast.Name)
            and child.value.id == "action"
            and isinstance(child.slice, ast.Constant)
            and child.slice.value == "operation"
        ):
            return True
    return False


def node_contains_operation_literal(node: ast.AST) -> bool:
    operation_names = set(OPERATION_TYPES)
    return any(
        isinstance(child, ast.Constant)
        and isinstance(child.value, str)
        and child.value in operation_names
        for child in ast.walk(node)
    )


def find_step_method(tree: ast.Module) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name != "ChemWorldEnv":
            continue
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == "step":
                return child
    return None


def scan_env_operation_dispatch(root: Path) -> list[RuntimeBoundaryFinding]:
    env_path = root / "src" / "chemworld" / "envs" / "chemworld_env.py"
    tree = parse_python(env_path)
    step = find_step_method(tree)
    if step is None:
        return [
            RuntimeBoundaryFinding(
                "env_step_missing",
                relative(env_path, root),
                1,
                "ChemWorldEnv.step() was not found.",
            )
        ]

    findings: list[RuntimeBoundaryFinding] = []
    for node in ast.walk(step):
        if isinstance(node, ast.If):
            if node_contains_operation_accessor(node.test) and node_contains_operation_literal(
                node.test
            ):
                findings.append(
                    RuntimeBoundaryFinding(
                        "env_operation_branch",
                        relative(env_path, root),
                        node.lineno,
                        "ChemWorldEnv.step() must not branch on specific operation names.",
                    )
                )
        elif isinstance(node, ast.Match):
            if node_contains_operation_accessor(node.subject):
                findings.append(
                    RuntimeBoundaryFinding(
                        "env_operation_match",
                        relative(env_path, root),
                        node.lineno,
                        "ChemWorldEnv.step() must not match-dispatch on operation type.",
                    )
                )
        elif isinstance(node, ast.Attribute) and node.attr == "domain_services":
            findings.append(
                RuntimeBoundaryFinding(
                    "env_runtime_internal_access",
                    relative(env_path, root),
                    node.lineno,
                    "ChemWorldEnv.step() must not access runtime.domain_services directly.",
                )
            )

    source = env_path.read_text(encoding="utf-8")
    if "runtime.apply_transaction" not in source:
        findings.append(
            RuntimeBoundaryFinding(
                "env_runtime_transaction_missing",
                relative(env_path, root),
                1,
                "ChemWorldEnv must delegate valid actions to runtime.apply_transaction().",
            )
        )
    if "runtime.apply_invalid_transaction" not in source:
        findings.append(
            RuntimeBoundaryFinding(
                "env_runtime_invalid_transaction_missing",
                relative(env_path, root),
                1,
                "ChemWorldEnv must delegate invalid actions to "
                "runtime.apply_invalid_transaction().",
            )
        )
    return findings


def audit_runtime_boundaries(project_root: Path | None = None) -> dict[str, Any]:
    root = repository_root() if project_root is None else project_root
    checks = {
        "legacy_core_imports": scan_legacy_core_imports(root),
        "legacy_core_package": scan_core_package_removed(root),
        "env_operation_dispatch": scan_env_operation_dispatch(root),
    }
    findings = [
        finding
        for group in checks.values()
        for finding in group
    ]
    return {
        "schema_version": "chemworld-runtime-boundary-audit-0.1",
        "passed": not findings,
        "finding_count": len(findings),
        "checks": {
            check_id: {
                "passed": not group,
                "finding_count": len(group),
                "findings": [finding.to_dict() for finding in group],
            }
            for check_id, group in checks.items()
        },
        "findings": [finding.to_dict() for finding in findings],
    }


__all__ = [
    "RuntimeBoundaryFinding",
    "audit_runtime_boundaries",
    "scan_core_package_removed",
    "scan_env_operation_dispatch",
    "scan_legacy_core_imports",
]
