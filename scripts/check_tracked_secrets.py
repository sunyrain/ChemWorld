"""Fail closed when Git-managed content contains forbidden paths or credential fingerprints."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path, PurePosixPath
from typing import Final

FORBIDDEN_BASENAMES: Final = frozenset({"api.md", "key2.md"})
FORBIDDEN_DIRECTORY_NAMES: Final = frozenset(
    {
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "raw_provider_payloads",
        "runs",
        "site",
    }
)
SAFE_ENV_TEMPLATE_NAMES: Final = frozenset({".env.example", ".env.sample", ".env.template"})
CREDENTIAL_PATTERNS: Final[dict[str, str]] = {
    "private-key block": r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "AWS access-key identifier": r"(^|[^A-Z0-9])(AKIA|ASIA)[A-Z0-9]{16}([^A-Z0-9]|$)",
    "GitHub token": r"(^|[^[:alnum:]_])gh[pousr]_[[:alnum:]]{36,}([^[:alnum:]_]|$)",
    "Google API key": r"(^|[^[:alnum:]_])AIza[[:alnum:]_-]{35}([^[:alnum:]_]|$)",
    "OpenAI project/service key": (
        r"(^|[^[:alnum:]_])sk-(proj|svcacct)-[[:alnum:]_-]{32,}([^[:alnum:]_]|$)"
    ),
    "Anthropic API key": r"(^|[^[:alnum:]_])sk-ant-[[:alnum:]_-]{30,}([^[:alnum:]_]|$)",
    "Slack token": r"(^|[^[:alnum:]_])xox[baprs]-[[:alnum:]-]{20,}([^[:alnum:]_]|$)",
}


def _git(root: Path, *arguments: str, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *arguments],
        cwd=root,
        capture_output=True,
        check=False,
        text=text,
    )


def _managed_paths(root: Path) -> list[str]:
    completed = _git(root, "ls-files", "--cached", "-z")
    if completed.returncode != 0:
        raise RuntimeError("unable to enumerate Git-managed paths")
    return sorted(
        item.decode("utf-8", errors="surrogateescape")
        for item in completed.stdout.split(b"\0")
        if item
    )


def _forbidden_path_reason(path: str) -> str | None:
    parts = tuple(part.casefold() for part in PurePosixPath(path).parts)
    if not parts:
        return None
    basename = parts[-1]
    if basename in FORBIDDEN_BASENAMES:
        return "credential-bearing filename"
    if basename == ".env" or (
        basename.startswith(".env.") and basename not in SAFE_ENV_TEMPLATE_NAMES
    ):
        return "environment credential file"
    blocked_directory = next(
        (part for part in parts[:-1] if part in FORBIDDEN_DIRECTORY_NAMES), None
    )
    if blocked_directory is not None:
        return f"forbidden generated/private directory: {blocked_directory}"
    return None


def _credential_matches(root: Path, *, cached: bool) -> dict[str, set[str]]:
    matches: dict[str, set[str]] = {}
    for label, pattern in CREDENTIAL_PATTERNS.items():
        arguments = ["grep"]
        if cached:
            arguments.append("--cached")
        arguments.extend(["-I", "-l", "-E", "-e", pattern, "--"])
        completed = _git(root, *arguments, text=True)
        if completed.returncode not in {0, 1}:
            raise RuntimeError(f"unable to scan Git-managed content for {label}")
        for path in completed.stdout.splitlines():
            matches.setdefault(path, set()).add(label)
    return matches


def audit(root: Path) -> list[str]:
    """Return path-only findings without reading untracked or ignored files."""

    root = root.resolve()
    findings = [
        f"{path}: {reason}"
        for path in _managed_paths(root)
        if (reason := _forbidden_path_reason(path)) is not None
    ]
    credential_matches = _credential_matches(root, cached=True)
    worktree_matches = _credential_matches(root, cached=False)
    for path, labels in worktree_matches.items():
        credential_matches.setdefault(path, set()).update(labels)
    findings.extend(
        f"{path}: credential fingerprint ({', '.join(sorted(labels))})"
        for path, labels in sorted(credential_matches.items())
    )
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    try:
        findings = audit(arguments.root)
    except RuntimeError as error:
        print(f"tracked-secret guard could not run: {error}")
        return 2
    if findings:
        print("tracked-secret guard failed; findings are path-only:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("tracked-secret guard passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
