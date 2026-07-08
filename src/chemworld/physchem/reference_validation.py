"""Optional reference-backend validation helpers.

The helpers in this module deliberately keep external scientific packages out
of ChemWorld's runtime dependency graph. They provide a small, auditable way to
discover local reference repositories, temporarily import reference packages
when a developer opts in, and record scalar comparison results with explicit
tolerances.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from collections.abc import Iterable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType


@dataclass(frozen=True)
class ReferenceBackendSpec:
    """A lightweight description of an optional external reference backend."""

    backend_id: str
    package_name: str
    local_repo_names: tuple[str, ...]
    comparison_scope: tuple[str, ...]
    model_limit_notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "backend_id": self.backend_id,
            "package_name": self.package_name,
            "local_repo_names": list(self.local_repo_names),
            "comparison_scope": list(self.comparison_scope),
            "model_limit_notes": list(self.model_limit_notes),
        }


@dataclass(frozen=True)
class ReferenceBackendStatus:
    """JSON-friendly availability report for a reference backend."""

    backend_id: str
    package_name: str
    installed_available: bool
    local_repo_available: bool
    import_probe_attempted: bool
    import_available: bool | None
    source: str | None = None
    import_error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "backend_id": self.backend_id,
            "package_name": self.package_name,
            "installed_available": self.installed_available,
            "local_repo_available": self.local_repo_available,
            "import_probe_attempted": self.import_probe_attempted,
            "import_available": self.import_available,
            "source": self.source,
            "import_error": self.import_error,
        }


@dataclass(frozen=True)
class ReferenceComparison:
    """A scalar comparison between ChemWorld and an optional reference backend."""

    check_id: str
    backend_id: str
    quantity: str
    chemworld_value: float
    reference_value: float
    unit: str
    rtol: float
    atol: float
    abs_error: float
    rel_error: float | None
    passed: bool
    note: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "check_id": self.check_id,
            "backend_id": self.backend_id,
            "quantity": self.quantity,
            "chemworld_value": self.chemworld_value,
            "reference_value": self.reference_value,
            "unit": self.unit,
            "rtol": self.rtol,
            "atol": self.atol,
            "abs_error": self.abs_error,
            "rel_error": self.rel_error,
            "passed": self.passed,
            "note": self.note,
        }


_REFERENCE_BACKENDS: tuple[ReferenceBackendSpec, ...] = (
    ReferenceBackendSpec(
        backend_id="chemicals",
        package_name="chemicals",
        local_repo_names=("fluids", "chemicals"),
        comparison_scope=(
            "formula-level property correlations",
            "ideal-gas molar volume",
            "Rachford-Rice flash inner loop",
        ),
        model_limit_notes=(
            "ChemWorld keeps a compact benchmark subset rather than the full "
            "chemicals property database.",
        ),
    ),
    ReferenceBackendSpec(
        backend_id="fluids",
        package_name="fluids",
        local_repo_names=("fluids",),
        comparison_scope=("dimensionless numbers", "pressure-drop utilities"),
    ),
    ReferenceBackendSpec(
        backend_id="thermo",
        package_name="thermo",
        local_repo_names=("fluids", "chemicals", "thermo"),
        comparison_scope=("property-package organization", "EOS and flash workflows"),
    ),
    ReferenceBackendSpec(
        backend_id="coolprop",
        package_name="CoolProp",
        local_repo_names=("coolprop",),
        comparison_scope=("high-accuracy pure-fluid property points",),
        model_limit_notes=(
            "A source checkout may not expose an importable Python package until "
            "its compiled extension is built.",
        ),
    ),
    ReferenceBackendSpec(
        backend_id="cantera",
        package_name="cantera",
        local_repo_names=("cantera",),
        comparison_scope=("simple reaction ODE and mechanism loading checks",),
        model_limit_notes=("Cantera normally requires compiled extensions.",),
    ),
    ReferenceBackendSpec(
        backend_id="phasepy",
        package_name="phasepy",
        local_repo_names=("phasepy",),
        comparison_scope=("VLE/LLE activity-model workflows",),
        model_limit_notes=("Local source imports may require compiled activity-model modules.",),
    ),
    ReferenceBackendSpec(
        backend_id="reaktoro",
        package_name="reaktoro",
        local_repo_names=("reaktoro",),
        comparison_scope=("equilibrium toy problems",),
        model_limit_notes=("Reaktoro is a compiled backend and may be unavailable locally.",),
    ),
    ReferenceBackendSpec(
        backend_id="pycalphad",
        package_name="pycalphad",
        local_repo_names=("pycalphad",),
        comparison_scope=("solid-phase and Gibbs-energy toy cases",),
        model_limit_notes=("pycalphad source imports require optional symbolic dependencies.",),
    ),
)


def reference_backend_specs() -> tuple[ReferenceBackendSpec, ...]:
    """Return the optional reference backends tracked by ChemWorld."""

    return _REFERENCE_BACKENDS


def repository_root() -> Path:
    """Return the repository root from this source file location."""

    return Path(__file__).resolve().parents[3]


def reference_repos_root(reference_root: str | Path | None = None) -> Path:
    """Return the expected local reference repository directory."""

    if reference_root is not None:
        return Path(reference_root)
    return repository_root() / "reference_repos"


def reference_repo_paths(
    repo_names: Iterable[str] | None = None,
    *,
    reference_root: str | Path | None = None,
) -> tuple[Path, ...]:
    """Return existing local source paths for reference repositories."""

    root = reference_repos_root(reference_root)
    names = tuple(repo_names) if repo_names is not None else _all_local_repo_names()
    paths: list[Path] = []
    for name in names:
        paths.extend(_python_path_candidates(root, name))
    deduped: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path.resolve())
        if key not in seen:
            deduped.append(path)
            seen.add(key)
    return tuple(deduped)


@contextmanager
def reference_backend_context(
    repo_names: Iterable[str] | None = None,
    *,
    reference_root: str | Path | None = None,
) -> Iterator[tuple[Path, ...]]:
    """Temporarily add local reference repositories to `sys.path`."""

    paths = reference_repo_paths(repo_names, reference_root=reference_root)
    original = list(sys.path)
    try:
        for path in reversed(paths):
            path_string = str(path)
            if path_string not in sys.path:
                sys.path.insert(0, path_string)
        yield paths
    finally:
        sys.path[:] = original


def import_reference_module(
    module_name: str,
    *,
    repo_names: Iterable[str] | None = None,
    reference_root: str | Path | None = None,
) -> ModuleType:
    """Import an optional reference module from installed or local sources."""

    with reference_backend_context(repo_names, reference_root=reference_root):
        return importlib.import_module(module_name)


def reference_backend_status(
    *,
    reference_root: str | Path | None = None,
    probe_import: bool = False,
) -> tuple[ReferenceBackendStatus, ...]:
    """Return availability reports for all tracked reference backends.

    `probe_import=False` keeps this function side-effect-light: it only checks
    whether a module spec exists. Set `probe_import=True` in manual validation
    runs to record actual import errors.
    """

    statuses: list[ReferenceBackendStatus] = []
    for spec in _REFERENCE_BACKENDS:
        installed_available = importlib.util.find_spec(spec.package_name) is not None
        local_repo_available = bool(
            reference_repo_paths(spec.local_repo_names, reference_root=reference_root)
        )
        import_available: bool | None = None
        source: str | None = None
        import_error: str | None = None
        if probe_import:
            try:
                module = import_reference_module(
                    spec.package_name,
                    repo_names=spec.local_repo_names,
                    reference_root=reference_root,
                )
                import_available = True
                module_file = getattr(module, "__file__", None)
                source = str(module_file) if module_file is not None else None
            except Exception as exc:  # pragma: no cover - depends on local extras
                import_available = False
                import_error = f"{type(exc).__name__}: {exc}"
        elif installed_available or local_repo_available:
            with reference_backend_context(spec.local_repo_names, reference_root=reference_root):
                found = importlib.util.find_spec(spec.package_name)
            source = found.origin if found is not None else None
        statuses.append(
            ReferenceBackendStatus(
                backend_id=spec.backend_id,
                package_name=spec.package_name,
                installed_available=installed_available,
                local_repo_available=local_repo_available,
                import_probe_attempted=probe_import,
                import_available=import_available,
                source=source,
                import_error=import_error,
            )
        )
    return tuple(statuses)


def compare_scalar(
    *,
    check_id: str,
    backend_id: str,
    quantity: str,
    chemworld_value: float,
    reference_value: float,
    unit: str,
    rtol: float,
    atol: float = 0.0,
    note: str = "",
) -> ReferenceComparison:
    """Compare one scalar with NumPy-style absolute-plus-relative tolerance."""

    if rtol < 0 or atol < 0:
        raise ValueError("rtol and atol must be nonnegative")
    abs_error = abs(chemworld_value - reference_value)
    rel_error = None if reference_value == 0 else abs_error / abs(reference_value)
    passed = abs_error <= (atol + rtol * abs(reference_value))
    return ReferenceComparison(
        check_id=check_id,
        backend_id=backend_id,
        quantity=quantity,
        chemworld_value=chemworld_value,
        reference_value=reference_value,
        unit=unit,
        rtol=rtol,
        atol=atol,
        abs_error=abs_error,
        rel_error=rel_error,
        passed=passed,
        note=note,
    )


def summarize_reference_comparisons(
    comparisons: Sequence[ReferenceComparison],
) -> dict[str, object]:
    """Summarize a set of optional reference comparisons."""

    total = len(comparisons)
    passed = sum(1 for comparison in comparisons if comparison.passed)
    failed = total - passed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "all_passed": failed == 0,
        "checks": [comparison.to_dict() for comparison in comparisons],
    }


def _all_local_repo_names() -> tuple[str, ...]:
    names: list[str] = []
    for spec in _REFERENCE_BACKENDS:
        names.extend(spec.local_repo_names)
    return tuple(names)


def _python_path_candidates(root: Path, repo_name: str) -> tuple[Path, ...]:
    repo = root / repo_name
    candidates = (
        repo,
        repo / "src",
        repo / "wrappers" / "Python",
        repo / "interfaces" / "python",
        repo / "Python",
    )
    return tuple(path for path in candidates if path.exists())


__all__ = [
    "ReferenceBackendSpec",
    "ReferenceBackendStatus",
    "ReferenceComparison",
    "compare_scalar",
    "import_reference_module",
    "reference_backend_context",
    "reference_backend_specs",
    "reference_backend_status",
    "reference_repo_paths",
    "reference_repos_root",
    "repository_root",
    "summarize_reference_comparisons",
]
