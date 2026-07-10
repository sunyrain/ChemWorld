"""Repository applications built on the public ChemWorld package.

The repository uses a ``src`` layout. When a user launches an application with
the system Python from the repository root, transparently re-execute it with the
existing project virtual environment. Library imports and installed-package use
remain unaffected.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _task_lab_module_from_command() -> str | None:
    arguments = list(getattr(sys, "orig_argv", ()))
    try:
        module_index = arguments.index("-m") + 1
    except (ValueError, IndexError):
        return None
    return arguments[module_index] if module_index < len(arguments) else None


def _relaunch_with_repository_venv() -> None:
    module = _task_lab_module_from_command()
    if module is None or not module.startswith("apps.task_lab"):
        return
    root = Path(__file__).resolve().parents[1]
    executable = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not executable.is_file() or Path(sys.executable).resolve() == executable.resolve():
        return
    original = list(getattr(sys, "orig_argv", ()))
    arguments = [str(executable), *original[1:]]
    if os.name == "nt":
        try:
            exit_code = os.spawnv(os.P_WAIT, str(executable), arguments)
        except KeyboardInterrupt:
            exit_code = 130
        raise SystemExit(exit_code)
    os.execv(str(executable), arguments)


_relaunch_with_repository_venv()

_source_root = Path(__file__).resolve().parents[1] / "src"
if _source_root.is_dir() and str(_source_root) not in sys.path:
    sys.path.insert(0, str(_source_root))
