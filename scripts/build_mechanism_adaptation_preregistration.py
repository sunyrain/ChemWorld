"""Build or verify the immutable mechanism-adaptation preregistration."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from chemworld.eval.mechanism_adaptation import (  # noqa: E402
    load_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_preregistration import (  # noqa: E402
    build_mechanism_preregistration,
    validate_mechanism_preregistration,
)
from chemworld.eval.provenance import write_json_atomic  # noqa: E402

DEFAULT_PROTOCOL = (
    ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0.json"
)
DEFAULT_PLAN = (
    ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "configs/benchmark/"
    "mechanism-adaptation-preregistration-v0.3.0-rc24.json"
)


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _source_commit_binding_errors(
    source_commit: str,
    *,
    protocol_path: Path,
    plan_path: Path,
    plan: dict[str, object],
) -> list[str]:
    """Verify that the lock commit exists and contains the executable inputs."""

    commit_check = subprocess.run(
        ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if commit_check.returncode != 0:
        return ["preregistration source_commit is not a Git commit"]
    ancestor_check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if ancestor_check.returncode != 0:
        return ["preregistration source_commit is not an ancestor of HEAD"]
    bound_paths = [
        "src/chemworld",
        "scripts/run_mechanism_adaptation.py",
        "scripts/audit_mechanism_adaptation_design.py",
        "scripts/audit_mechanism_adaptation_sample_size.py",
        "scripts/build_mechanism_diagnostic_relation_graph.py",
        protocol_path.resolve().relative_to(ROOT).as_posix(),
        plan_path.resolve().relative_to(ROOT).as_posix(),
        str(plan["diagnostic_relation_graph"]["report"]),  # type: ignore[index]
        str(plan["sample_size_audit"]["report"]),  # type: ignore[index]
        str(plan["design_validity_precondition"]["report"]),  # type: ignore[index]
    ]
    source_diff = subprocess.run(
        ["git", "diff", "--quiet", source_commit, "--", *bound_paths],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if source_diff.returncode == 1:
        return [
            "current mechanism execution inputs differ from preregistration source_commit"
        ]
    if source_diff.returncode != 0:
        return ["could not verify preregistration source_commit path binding"]
    return []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--source-commit",
        help=(
            "Full implementation commit SHA. Required for first generation; "
            "a check reuses the locked manifest value."
        ),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    protocol = load_mechanism_adaptation_protocol(args.protocol)
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    graph = json.loads(
        (ROOT / plan["diagnostic_relation_graph"]["report"]).read_text(
            encoding="utf-8"
        )
    )
    sample_size = json.loads(
        (ROOT / plan["sample_size_audit"]["report"]).read_text(
            encoding="utf-8"
        )
    )
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"missing preregistration: {args.output}")
        manifest = json.loads(args.output.read_text(encoding="utf-8"))
        source_errors = _source_commit_binding_errors(
            str(manifest.get("source_commit", "")),
            protocol_path=args.protocol,
            plan_path=args.plan,
            plan=plan,
        )
        errors = validate_mechanism_preregistration(
            manifest,
            repository_root=ROOT,
            protocol=protocol,
            plan=plan,
            relation_graph=graph,
            sample_size_audit=sample_size,
        )
        if source_errors or errors:
            raise SystemExit("; ".join([*source_errors, *errors]))
    else:
        if args.output.exists():
            raise SystemExit(
                "preregistration is immutable; use --check or select a new RC path"
            )
        source_commit = args.source_commit or _git_head()
        source_errors = _source_commit_binding_errors(
            source_commit,
            protocol_path=args.protocol,
            plan_path=args.plan,
            plan=plan,
        )
        if source_errors:
            raise SystemExit("; ".join(source_errors))
        manifest = build_mechanism_preregistration(
            repository_root=ROOT,
            protocol=protocol,
            plan=plan,
            relation_graph=graph,
            sample_size_audit=sample_size,
            source_commit=source_commit,
        )
        write_json_atomic(args.output, manifest)
    print(
        json.dumps(
            {
                "status": "passed",
                "manifest_sha256": manifest["manifest_sha256"],
                "source_commit": manifest["source_commit"],
                "output": str(args.output.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
