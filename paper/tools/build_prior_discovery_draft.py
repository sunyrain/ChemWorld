#!/usr/bin/env python3
"""Build a reproducible venue-neutral PDF draft of the prior-discovery manuscript."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "paper/prior_discovery_manuscript.md"
BIBLIOGRAPHY = ROOT / "paper/prior_discovery_references.bib"
TEMPLATE = ROOT / "paper/prior_discovery/template.tex"
FIGURE_DIR = ROOT / "paper/figures/prior-discovery"
FIGURE_MANIFEST = FIGURE_DIR / "figure_manifest.json"
PUBLIC_C2_FIGURE = ROOT / (
    "workstreams/flagship_tasks/reports/figures/work-ii-deepseek-c2-public/"
    "current/deepseek_c2_prediction_law_action.pdf"
)
PUBLIC_C2_FIGURE_BUILD_NAME = "figure-5-capability-chain.pdf"
EXPORT_DIR = ROOT / "paper/exports/prior-discovery-draft"
OUTPUT_PDF = EXPORT_DIR / "prior-discovery-draft.pdf"
OUTPUT_TEX = EXPORT_DIR / "prior-discovery-draft.tex"
BUILD_MANIFEST = EXPORT_DIR / "build-manifest.json"
SOURCE_DATE_EPOCH = 1_786_406_400  # 2026-08-11 00:00:00 UTC
EXPECTED_FIGURE_IDS = ("figure_1", "figure_2", "figure_3", "figure_4", "figure_6")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def optional_tool(name: str, fallback: Path | None = None) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    if fallback is not None and fallback.is_file():
        return str(fallback)
    return None


def required_tool(name: str, fallback: Path | None = None) -> str:
    found = optional_tool(name, fallback)
    if found is None:
        raise RuntimeError(f"required build tool is unavailable: {name}")
    return found


def run(command: list[str], *, cwd: Path) -> str:
    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = str(SOURCE_DATE_EPOCH)
    environment["FORCE_SOURCE_DATE"] = "1"
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode != 0:
        tail = "\n".join(completed.stdout.splitlines()[-80:])
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{tail}")
    return completed.stdout


def load_figure_pdfs() -> list[Path]:
    manifest = json.loads(FIGURE_MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise RuntimeError("figure manifest must be an object")
    declared = manifest.pop("manifest_sha256", None)
    if declared != canonical_sha(manifest):
        raise RuntimeError("figure manifest self-hash mismatch")
    figures = manifest.get("figures")
    if not isinstance(figures, dict) or set(figures) != set(EXPECTED_FIGURE_IDS):
        raise RuntimeError("draft requires exactly generated Figures 1--4 and 6")
    pdfs: list[Path] = []
    for figure_id in EXPECTED_FIGURE_IDS:
        outputs = figures[figure_id]
        matches = [row for row in outputs if str(row.get("path", "")).endswith(".pdf")]
        if len(matches) != 1:
            raise RuntimeError(f"{figure_id} must bind exactly one PDF")
        row = matches[0]
        path = ROOT / row["path"]
        if (
            not path.is_file()
            or path.stat().st_size != row["bytes"]
            or sha256_file(path) != row["sha256"]
        ):
            raise RuntimeError(f"stale figure binding: {figure_id}")
        pdfs.append(path)
    return pdfs


def build() -> dict[str, Any]:
    figure_pdfs = load_figure_pdfs()
    pandoc = required_tool("pandoc", Path.home() / "AppData/Local/Pandoc/pandoc.exe")
    miktex = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"
    pdflatex = optional_tool("pdflatex", miktex / "pdflatex.exe")
    bibtex = optional_tool("bibtex", miktex / "bibtex.exe")
    tectonic = None if pdflatex and bibtex else required_tool("tectonic")
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="chemworld-prior-discovery-") as temp_name:
        build_dir = Path(temp_name)
        figure_build_dir = build_dir / "figures/prior-discovery"
        figure_build_dir.mkdir(parents=True)
        shutil.copy2(BIBLIOGRAPHY, build_dir / "references.bib")
        for source in figure_pdfs:
            shutil.copy2(source, figure_build_dir / source.name)
        if not PUBLIC_C2_FIGURE.is_file():
            raise RuntimeError("current public C2 evaluator figure is unavailable")
        shutil.copy2(
            PUBLIC_C2_FIGURE,
            figure_build_dir / PUBLIC_C2_FIGURE_BUILD_NAME,
        )
        main_tex = build_dir / "main.tex"
        run(
            [
                pandoc,
                str(MANUSCRIPT),
                "--from=markdown+raw_tex+tex_math_dollars",
                "--to=latex",
                "--standalone",
                "--natbib",
                f"--template={TEMPLATE}",
                f"--resource-path={ROOT / 'paper'};{ROOT}",
                "--output",
                str(main_tex),
            ],
            cwd=ROOT,
        )
        main_tex.write_text(main_tex.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        if tectonic is not None:
            run([tectonic, "-k", "--keep-logs", "main.tex"], cwd=build_dir)
        else:
            assert pdflatex is not None and bibtex is not None
            latex = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
            run(latex, cwd=build_dir)
            run([bibtex, "main"], cwd=build_dir)
            run(latex, cwd=build_dir)
            run(latex, cwd=build_dir)

        log = (build_dir / "main.log").read_text(encoding="utf-8", errors="replace")
        if re.search(r"Citation .* undefined|There were undefined citations", log):
            raise RuntimeError("compiled draft contains undefined citations")
        if "LaTeX Error" in log:
            raise RuntimeError("compiled draft contains a LaTeX error")
        overfull_widths = [
            float(value)
            for value in re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", log)
        ]
        underfull_hbox_count = len(re.findall(r"Underfull \\hbox", log))
        overfull_vbox_count = len(re.findall(r"Overfull \\vbox", log))
        page_match = re.search(r"Output written on main\.(?:pdf|xdv) \((\d+) pages?", log)
        if page_match is None:
            raise RuntimeError("could not determine PDF page count")
        page_count = int(page_match.group(1))
        shutil.copy2(build_dir / "main.pdf", OUTPUT_PDF)
        shutil.copy2(main_tex, OUTPUT_TEX)

    source_paths = [
        MANUSCRIPT,
        BIBLIOGRAPHY,
        TEMPLATE,
        FIGURE_MANIFEST,
        ROOT / "paper/prior_discovery_evidence_map.md",
        ROOT / "paper/prior_discovery_display_items.md",
        ROOT
        / (
            "workstreams/flagship_tasks/reports/"
            "WORK_II_OPEN_ACTION_DEVELOPMENT_CLOSEOUT_ZH.md"
        ),
        ROOT
        / (
            "workstreams/flagship_tasks/reports/"
            "work-ii-deepseek-five-task-development-complete-20260810.json"
        ),
        ROOT / (
            "workstreams/flagship_tasks/reports/"
            "work-ii-deepseek-five-task-development-evaluation-20260811.json"
        ),
        ROOT / (
            "workstreams/flagship_tasks/reports/"
            "work-ii-parametric-initial-model-pilot-evaluation-20260811.json"
        ),
        ROOT / (
            "workstreams/flagship_tasks/reports/"
            "work-ii-deepseek-c2-paper-story-analysis-v0.1.json"
        ),
        ROOT / (
            "workstreams/flagship_tasks/reports/"
            "work-ii-deepseek-c2-current-composite-evaluation-v0.2.json"
        ),
        ROOT / (
            "workstreams/flagship_tasks/reports/"
            "work-ii-study-b-matched-evidence-results-v0.1.json"
        ),
        ROOT / (
            "workstreams/flagship_tasks/reports/"
            "work-ii-as-study-b2-phase-process-results-v0.1.json"
        ),
        ROOT
        / (
            "workstreams/flagship_tasks/reports/"
            "WORK_II_MULTI_TASK_OPEN_ACTION_FORMAL_AUDIT_ZH.md"
        ),
        ROOT
        / (
            "runs/formal/"
            "work-ii-deepseek-multi-task-open-action-five-world-v0.1-20260817-formal2/summary.json"
        ),
        ROOT
        / (
            "configs/benchmark/"
            "work_ii_deepseek_five_task_development_complete_analysis_sources_20260810.json"
        ),
        PUBLIC_C2_FIGURE,
        *figure_pdfs,
    ]
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-prior-discovery-draft-build-0.1",
        "status": "compiled_development_draft",
        "formal_result": False,
        "page_count": page_count,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "typesetting_audit": {
            "overfull_hbox_count": len(overfull_widths),
            "maximum_overfull_hbox_pt": max(overfull_widths, default=0.0),
            "underfull_hbox_count": underfull_hbox_count,
            "overfull_vbox_count": overfull_vbox_count,
            "undefined_citations": False,
            "latex_errors": False,
        },
        "sources": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in source_paths
        ],
        "outputs": [
            {
                "path": OUTPUT_PDF.relative_to(ROOT).as_posix(),
                "bytes": OUTPUT_PDF.stat().st_size,
                "sha256": sha256_file(OUTPUT_PDF),
            },
            {
                "path": OUTPUT_TEX.relative_to(ROOT).as_posix(),
                "bytes": OUTPUT_TEX.stat().st_size,
                "sha256": sha256_file(OUTPUT_TEX),
            },
        ],
        "interpretation_limits": [
            "Figures 1 and 2 state the identification problem and executed study architecture.",
            (
                "Figure 3 combines prospective formal locus decisions with retrospective "
                "starting-state and first-recipe manipulation summaries; first-recipe "
                "divergence has no repeated same-arm baseline."
            ),
            (
                "Figure 4 uses only the corrected five-world structural matched-evidence "
                "study; its selective-update contrast and structural recovery rates are "
                "descriptive and non-confirmatory."
            ),
            (
                "Figure 5 reports completed prospective prediction, executable-law and "
                "blind-incumbent evaluation without additional participant calls."
            ),
            (
                "Development matrices motivate the prospective design but remain separate "
                "from its causal denominators and are not used for cross-system ranking."
            ),
            (
                "Public participant, evaluator and matched-evidence results "
                "are collected; "
                "private confirmation remains uncollected."
            ),
            (
                "The five-world unseen-plan matrix has "
                "45 scheduled cells, 42 eligible action readouts and three retained "
                "crystallization failures. It has no no-evidence or pre-exploration "
                "ranking control, so causal action-transfer and arm-level effects are not claimed."
            ),
            (
                "W2-51 and W2-52 are zero-participant qualification results; exposed "
                "construction and fresh qualification remain separate evidence roles."
            ),
            (
                "The W2-53 panel reuses 16 frozen unit versions with no new execution "
                "and changes no historical rank threshold or stop decision."
            ),
        ],
    }
    manifest["manifest_sha256"] = canonical_sha(manifest)
    BUILD_MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return {
        "status": manifest["status"],
        "page_count": page_count,
        "typesetting_audit": manifest["typesetting_audit"],
        "pdf": str(OUTPUT_PDF),
        "tex": str(OUTPUT_TEX),
        "manifest_sha256": manifest["manifest_sha256"],
    }


def main() -> int:
    print(json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
