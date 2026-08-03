"""Build the sole numeric source and CSV tables for arXiv v1."""

from __future__ import annotations

import argparse
import json
import tempfile
from collections.abc import Sequence
from pathlib import Path

from chemworld.eval.arxiv_v1_derived_data import (
    build_arxiv_v1_derived_data,
    build_derived_data_manifest,
    canonical_sha256,
    file_sha256,
    rebind_figure_manifest,
    write_arxiv_v1_tables,
    write_fvl_derived_report,
    write_json,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_G2_V04 = Path(
    "runs/development/"
    "g2-autonomous-electrochemical-material-5x2-codex-sol-medium-mcp-v2/"
    "autonomous_material_campaign_audit.json"
)
DEFAULT_G2_V05 = Path(
    "runs/development/"
    "g2-autonomous-material-seed1-seed3-r5-codex-sol-medium-v2/"
    "audit.json"
)

FVL_DEFAULTS = {
    "work_i_data_contract": Path("configs/benchmark/work_i_incremental_data_contract_v0.1.json"),
    "fork_qualification": Path(
        "workstreams/arxiv_v1/reports/work-i-world-fork-qualification-v0.1.json"
    ),
    "fork_certificate": Path(
        "workstreams/arxiv_v1/reports/work-i-world-fork-certificate-v0.1.json"
    ),
    "policy_report": Path(
        "workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.json"
    ),
    "policy_audit": Path(
        "workstreams/arxiv_v1/reports/work-i-policy-control-formal-audit-v0.1.json"
    ),
    "policy_delivery_manifest": Path(
        "workstreams/arxiv_v1/reports/work-i-known-policy-validity-report-v0.1.manifest.json"
    ),
    "latent_contract": Path("configs/benchmark/work_i_latent_terminal_contract_v0.1.json"),
    "latent_reconstructability": Path(
        "workstreams/arxiv_v1/reports/work-i-latent-terminal-reconstructability-v0.1.json"
    ),
    "latent_formal": Path(
        "workstreams/arxiv_v1/reports/work-i-latent-terminal-shadow-assays-v0.1.json"
    ),
    "latent_analysis": Path(
        "workstreams/arxiv_v1/reports/work-i-latent-terminal-analysis-v0.1.json"
    ),
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--g0-v1-0",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/reports/static-s0-v1.0-formal-campaign-summary.json"
        ),
    )
    parser.add_argument(
        "--g0-v1-2",
        type=Path,
        default=Path(
            "workstreams/flagship_tasks/reports/"
            "static-s0-v1.2-three-arm-information-campaign-summary.json"
        ),
    )
    parser.add_argument(
        "--task-design",
        type=Path,
        default=Path("workstreams/flagship_tasks/reports/task-design-matrix-v1.json"),
    )
    parser.add_argument(
        "--experiment-ledger",
        type=Path,
        default=Path(
            "workstreams/arxiv_v1/reports/experimental-intelligence-experiment-ledger-v0.1.json"
        ),
    )
    parser.add_argument("--g2-v0-4-audit", type=Path, default=DEFAULT_G2_V04)
    parser.add_argument("--g2-v0-5-audit", type=Path, default=DEFAULT_G2_V05)
    parser.add_argument(
        "--work-i-data-contract",
        type=Path,
        default=FVL_DEFAULTS["work_i_data_contract"],
    )
    parser.add_argument(
        "--fork-qualification",
        type=Path,
        default=FVL_DEFAULTS["fork_qualification"],
    )
    parser.add_argument("--fork-certificate", type=Path, default=FVL_DEFAULTS["fork_certificate"])
    parser.add_argument("--policy-report", type=Path, default=FVL_DEFAULTS["policy_report"])
    parser.add_argument("--policy-audit", type=Path, default=FVL_DEFAULTS["policy_audit"])
    parser.add_argument(
        "--policy-delivery-manifest",
        type=Path,
        default=FVL_DEFAULTS["policy_delivery_manifest"],
    )
    parser.add_argument("--latent-contract", type=Path, default=FVL_DEFAULTS["latent_contract"])
    parser.add_argument(
        "--latent-reconstructability",
        type=Path,
        default=FVL_DEFAULTS["latent_reconstructability"],
    )
    parser.add_argument("--latent-formal", type=Path, default=FVL_DEFAULTS["latent_formal"])
    parser.add_argument("--latent-analysis", type=Path, default=FVL_DEFAULTS["latent_analysis"])
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json"),
    )
    parser.add_argument(
        "--table-output-dir",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/tables"),
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=Path(
            "benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.manifest.json"
        ),
    )
    parser.add_argument(
        "--report-output",
        type=Path,
        default=Path("workstreams/arxiv_v1/reports/work-i-fvl-derived-data-layer-v0.1.md"),
    )
    parser.add_argument(
        "--figure-manifest",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/figure-manifest.json"),
    )
    parser.add_argument("--check", action="store_true")
    return parser


def _resolve(path: Path) -> Path:
    if path.is_absolute():
        return path
    local = REPOSITORY_ROOT / path
    if local.exists() or not path.parts or path.parts[0].lower() != "runs":
        return local
    git_pointer = REPOSITORY_ROOT / ".git"
    if git_pointer.is_file():
        prefix = "gitdir: "
        line = git_pointer.read_text(encoding="utf-8").strip()
        if line.lower().startswith(prefix):
            git_dir = Path(line[len(prefix) :])
            common_root = git_dir.parents[2]
            fallback = common_root / path
            if fallback.exists():
                return fallback
    return local


def _check_outputs(
    *,
    data: dict[str, object],
    json_output: Path,
    table_output_dir: Path,
    manifest_output: Path,
    figure_manifest_path: Path,
) -> list[str]:
    errors: list[str] = []
    if json.loads(json_output.read_text(encoding="utf-8")) != data:
        errors.append("derived-data JSON is stale")
    with tempfile.TemporaryDirectory(prefix="chemworld-d03-check-") as temporary:
        generated = write_arxiv_v1_tables(Path(temporary), data)
        for path in generated:
            committed = table_output_dir / path.name
            if not committed.is_file() or committed.read_bytes() != path.read_bytes():
                errors.append(f"table is stale: {path.name}")
    manifest = json.loads(manifest_output.read_text(encoding="utf-8"))
    declared_manifest_sha = manifest.pop("manifest_sha256", None)
    if declared_manifest_sha != canonical_sha256(manifest):
        errors.append("derived-data manifest self-hash mismatch")
    if manifest.get("derived_data_sha256") != data["derived_data_sha256"]:
        errors.append("derived-data manifest binding is stale")
    for row in manifest.get("files", []):
        path = REPOSITORY_ROOT / row["path"]
        if (
            not path.is_file()
            or path.stat().st_size != row["bytes"]
            or file_sha256(path) != row["sha256"]
        ):
            errors.append(f"manifest file binding is stale: {row['path']}")
    figure = json.loads(figure_manifest_path.read_text(encoding="utf-8"))
    declared_figure_sha = figure.pop("manifest_sha256", None)
    if declared_figure_sha != canonical_sha256(figure):
        errors.append("figure manifest self-hash mismatch")
    if figure.get("derived_data_sha256") != data["derived_data_sha256"]:
        errors.append("figure manifest derived-data binding is stale")
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data = build_arxiv_v1_derived_data(
        g0_v10_path=_resolve(args.g0_v1_0),
        g0_v12_path=_resolve(args.g0_v1_2),
        task_design_path=_resolve(args.task_design),
        experiment_ledger_path=_resolve(args.experiment_ledger),
        g2_v04_audit_path=_resolve(args.g2_v0_4_audit),
        g2_v05_audit_path=(None if args.g2_v0_5_audit is None else _resolve(args.g2_v0_5_audit)),
        work_i_data_contract_path=_resolve(args.work_i_data_contract),
        fork_qualification_path=_resolve(args.fork_qualification),
        fork_certificate_path=_resolve(args.fork_certificate),
        policy_report_path=_resolve(args.policy_report),
        policy_audit_path=_resolve(args.policy_audit),
        policy_delivery_manifest_path=_resolve(args.policy_delivery_manifest),
        latent_contract_path=_resolve(args.latent_contract),
        latent_reconstructability_path=_resolve(args.latent_reconstructability),
        latent_formal_path=_resolve(args.latent_formal),
        latent_analysis_path=_resolve(args.latent_analysis),
    )
    output = _resolve(args.json_output)
    table_dir = _resolve(args.table_output_dir)
    manifest_output = _resolve(args.manifest_output)
    report_output = _resolve(args.report_output)
    figure_manifest_path = _resolve(args.figure_manifest)
    if args.check:
        errors = _check_outputs(
            data=data,
            json_output=output,
            table_output_dir=table_dir,
            manifest_output=manifest_output,
            figure_manifest_path=figure_manifest_path,
        )
        print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}))
        return 0 if not errors else 1
    write_json(output, data)
    tables = write_arxiv_v1_tables(table_dir, data)
    manifest = build_derived_data_manifest(
        root=REPOSITORY_ROOT,
        derived_data_path=output,
        table_paths=tables,
        data=data,
    )
    write_json(manifest_output, manifest)
    write_json(
        figure_manifest_path,
        rebind_figure_manifest(
            figure_manifest_path,
            derived_data_sha256=str(data["derived_data_sha256"]),
        ),
    )
    write_fvl_derived_report(report_output, data, manifest)
    print(
        json.dumps(
            {
                "status": data["status"],
                "derived_data_sha256": data["derived_data_sha256"],
                "json_output": output.as_posix(),
                "table_outputs": [path.as_posix() for path in tables],
                "manifest_output": manifest_output.as_posix(),
                "report_output": report_output.as_posix(),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if data["status"] == "frozen_complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
