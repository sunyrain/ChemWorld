#!/usr/bin/env python3
"""Build and audit the anonymous ICLR 2027 prior-discovery submission."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ICLR_DIR = ROOT / "paper/iclr2027"
MANUSCRIPT = ICLR_DIR / "submission.md"
APPENDIX = ICLR_DIR / "appendix.md"
TEMPLATE = ICLR_DIR / "template.tex"
BIBLIOGRAPHY = ROOT / "paper/prior_discovery_references.bib"
FIGURE_DIR = ROOT / "paper/figures/prior-discovery"
STYLE_HASHES = {
    "iclr2027_conference.sty": (
        "797deef41724e93761426ac0cbcca46279a91cc650dd1f0ce76a4f08d2098ea6"
    ),
    "iclr2027_conference.bst": (
        "2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5"
    ),
    "math_commands.tex": (
        "90473c4d0542070db244cea73ef962d6cddc5b2a746757e6a40ddf5fdfb90ba9"
    ),
}
FIGURES = (
    "figure-1-prior-to-law.pdf",
    "figure-3-prior-uptake-and-correction.pdf",
    "figure-4-matched-evidence-localization.pdf",
    "figure-5-capability-chain.pdf",
    "figure-6-open-action-formal.pdf",
)
EXPORT_DIR = ROOT / "paper/exports/prior-discovery-iclr2027"
OUTPUT_PDF = EXPORT_DIR / "prior-discovery-iclr2027-anonymous.pdf"
OUTPUT_TEX = EXPORT_DIR / "prior-discovery-iclr2027-anonymous.tex"
SUPPLEMENT_ZIP = EXPORT_DIR / "prior-discovery-iclr2027-supplement.zip"
BUILD_MANIFEST = EXPORT_DIR / "build-manifest.json"
SOURCE_DATE_EPOCH = 1_787_616_000  # 2026-08-25 00:00:00 UTC

FORBIDDEN_IDENTITY_STRINGS = (
    "Jiangjie Qiu",
    "Yijun Li",
    "Yaotian Yang",
    "Honghao Chen",
    "Wentao Li",
    "Xiaonan Wang",
    "wangxiaonan@tsinghua.edu.cn",
    "Beijing Key Laboratory of Artificial Intelligence",
    "State Key Laboratory of Chemical Engineering",
    "Department of Chemical Engineering, Tsinghua University",
)
FORBIDDEN_ANONYMOUS_PATTERNS = {
    "absolute_windows_path": re.compile(r"(?i)(?:^|[\s\"'])(?:[A-Z]:[\\/])"),
    "absolute_unix_user_path": re.compile(r"(?i)(?:/home/|/Users/|/root/)[^\s\"']*"),
    "local_run_root": re.compile(r"(?i)(?:^|[\s\"'/])runs[\\/]"),
    "credential_file": re.compile(r"(?i)(?:api\.md|key2\.md|\.env(?:\W|$))"),
    "secret_field": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|bearer[_-]?token)"),
    "provider_identity": re.compile(r"(?i)(?:thread[_-]?id|request[_-]?id|session[_-]?id)"),
    "email_address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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
        tail = "\n".join(completed.stdout.splitlines()[-100:])
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n{tail}"
        )
    return completed.stdout


def assert_official_assets() -> None:
    for name, expected_hash in STYLE_HASHES.items():
        path = ICLR_DIR / name
        if not path.is_file() or sha256_file(path) != expected_hash:
            raise RuntimeError(f"official ICLR asset is missing or modified: {name}")


def parse_page_count(log: str) -> int:
    match = re.search(r"Output written on main\.(?:pdf|xdv) \((\d+) pages?", log)
    if match is None:
        raise RuntimeError("could not determine PDF page count")
    return int(match.group(1))


def parse_main_text_page(aux: str) -> int:
    match = re.search(
        r"\\newlabel\{iclr-main-text-end\}\{\{[^}]*\}\{(\d+)\}", aux
    )
    if match is None:
        raise RuntimeError("could not determine main-text page count")
    return int(match.group(1))


def anonymous_text_hits(text: str) -> list[str]:
    lower = text.lower()
    hits = [
        f"identity:{value}"
        for value in FORBIDDEN_IDENTITY_STRINGS
        if value.lower() in lower
    ]
    hits.extend(
        f"pattern:{name}"
        for name, pattern in FORBIDDEN_ANONYMOUS_PATTERNS.items()
        if pattern.search(text)
    )
    return hits


def assert_anonymous_supplement() -> None:
    if not SUPPLEMENT_ZIP.is_file():
        raise FileNotFoundError(
            "anonymous supplement is missing; run build_prior_discovery_supplement.py"
        )
    with zipfile.ZipFile(SUPPLEMENT_ZIP) as archive:
        names = archive.namelist()
        if "manifest.json" not in names or "verify_supplement.py" not in names:
            raise RuntimeError("anonymous supplement lacks its manifest or verifier")
        leaks: dict[str, list[str]] = {}
        for name in names:
            payload = archive.read(name)
            if b"\x00" in payload:
                continue
            hits = anonymous_text_hits(payload.decode("utf-8"))
            if hits:
                leaks[name] = hits
        if leaks:
            raise RuntimeError(f"anonymous supplement contains identifying data: {leaks}")


def build() -> dict[str, Any]:
    assert_official_assets()
    assert_anonymous_supplement()
    pandoc = required_tool("pandoc", Path.home() / "AppData/Local/Pandoc/pandoc.exe")
    miktex = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"
    pdflatex = required_tool("pdflatex", miktex / "pdflatex.exe")
    bibtex = required_tool("bibtex", miktex / "bibtex.exe")
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="chemworld-iclr2027-") as temp_name:
        build_dir = Path(temp_name)
        build_figure_dir = build_dir / "figures/prior-discovery"
        build_figure_dir.mkdir(parents=True)

        for name in STYLE_HASHES:
            shutil.copy2(ICLR_DIR / name, build_dir / name)
        shutil.copy2(BIBLIOGRAPHY, build_dir / "references.bib")
        for name in FIGURES:
            shutil.copy2(FIGURE_DIR / name, build_figure_dir / name)
        appendix_tex = build_dir / "appendix.tex"
        run(
            [
                pandoc,
                str(APPENDIX),
                "--from=markdown+raw_tex+tex_math_dollars",
                "--to=latex",
                "--natbib",
                "--top-level-division=section",
                "--output",
                str(appendix_tex),
            ],
            cwd=ROOT,
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
                "--top-level-division=section",
                f"--template={TEMPLATE}",
                f"--resource-path={ROOT / 'paper'};{ROOT}",
                "--output",
                str(main_tex),
            ],
            cwd=ROOT,
        )
        generated_tex = main_tex.read_text(encoding="utf-8")
        if "\\iclrfinalcopy" in generated_tex.replace(
            "% Keep review mode anonymous. Do not enable \\iclrfinalcopy here.", ""
        ):
            raise RuntimeError("anonymous build must not enable iclrfinalcopy")
        main_tex.write_text(generated_tex, encoding="utf-8", newline="\n")
        appendix_tex.write_text(
            appendix_tex.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
        )

        latex = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        run(latex, cwd=build_dir)
        run([bibtex, "main"], cwd=build_dir)
        for _ in range(4):
            run(latex, cwd=build_dir)
            pass_log = (build_dir / "main.log").read_text(
                encoding="utf-8", errors="replace"
            )
            if not re.search(r"Rerun to get cross-references right", pass_log):
                break

        log = (build_dir / "main.log").read_text(encoding="utf-8", errors="replace")
        aux = (build_dir / "main.aux").read_text(encoding="utf-8", errors="replace")
        if re.search(r"Citation .* undefined|There were undefined citations", log):
            raise RuntimeError("compiled submission contains undefined citations")
        if "LaTeX Error" in log:
            raise RuntimeError("compiled submission contains a LaTeX error")
        if re.search(r"Rerun to get cross-references right", log):
            raise RuntimeError("compiled submission contains unstable cross-references")

        overfull_widths = [
            float(value)
            for value in re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", log)
        ]
        total_pages = parse_page_count(log)
        main_text_pages = parse_main_text_page(aux)
        shutil.copy2(build_dir / "main.pdf", OUTPUT_PDF)
        shutil.copy2(main_tex, OUTPUT_TEX)

    tex_text = OUTPUT_TEX.read_text(encoding="utf-8", errors="replace")
    leaks = anonymous_text_hits(tex_text)
    if leaks:
        raise RuntimeError(f"anonymous TeX contains identifying strings: {leaks}")

    source_paths = [
        MANUSCRIPT,
        APPENDIX,
        TEMPLATE,
        ICLR_DIR / "SOURCE.md",
        BIBLIOGRAPHY,
        *(ICLR_DIR / name for name in STYLE_HASHES),
        *(FIGURE_DIR / name for name in FIGURES),
    ]
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-prior-discovery-iclr2027-build-0.1",
        "status": (
            "anonymous_review_draft_within_main_text_limit"
            if main_text_pages <= 9
            else "anonymous_review_draft_over_main_text_limit"
        ),
        "formal_result": False,
        "anonymous_review_mode": True,
        "main_text_page_limit": 9,
        "main_text_page_count": main_text_pages,
        "total_page_count": total_pages,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "typesetting_audit": {
            "overfull_hbox_count": len(overfull_widths),
            "maximum_overfull_hbox_pt": max(overfull_widths, default=0.0),
            "underfull_hbox_count": len(re.findall(r"Underfull \\hbox", log)),
            "overfull_vbox_count": len(re.findall(r"Overfull \\vbox", log)),
            "undefined_citations": False,
            "latex_errors": False,
            "unstable_cross_references": False,
            "identifying_string_leaks": [],
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
            {
                "path": SUPPLEMENT_ZIP.relative_to(ROOT).as_posix(),
                "bytes": SUPPLEMENT_ZIP.stat().st_size,
                "sha256": sha256_file(SUPPLEMENT_ZIP),
            },
        ],
        "claim_boundaries": [
            (
                "The longitudinal open-action matrix remains descriptive; the independent "
                "four-condition successor supplies the action baselines."
            ),
            (
                "The five-condition participant cohort was not executed after oracle "
                "qualification failed."
            ),
            (
                "The 320-query result separates exposed construction repair from "
                "fresh-world rejection."
            ),
            (
                "The gate-alignment analysis adds no execution and changes no historical "
                "stop decision."
            ),
            "The reduced-condition pilot is development-only and supports no arm-level conclusion.",
            (
                "C2 and B3 have matched scheduled surfaces for both models, but differential "
                "failure patterns make their contrasts descriptive rather than capability rankings."
            ),
            (
                "The four-condition successor retains unequal donor eligibility and substantial "
                "failure, so autonomous-minus-yoked is not a pure experiment-selection effect."
            ),
            (
                "DeepSeek low is a same-harness reasoning-budget ablation, not provider-level "
                "thinking-off or a configuration-superiority result."
            ),
            (
                "The DeepSeek-low A-P canary produced no qualified terminal denominator; "
                "formal execution remained 0/15 and no parametric low-reasoning effect "
                "is estimated."
            ),
        ],
    }
    BUILD_MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def main() -> int:
    manifest = build()
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
