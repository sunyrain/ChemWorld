"""Build and inspect the complete illustrated Chinese manuscript from Markdown."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from build_venue_manuscripts import appendix, tidy_tex
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
SOURCE = PAPER / "venues/ncs/archive/ChemWorld_NCS_中文正文_v1.md"
BUILD = Path(tempfile.gettempdir()) / "chemworld-ncs-chinese-full"
OUTPUT = ROOT / "output/pdf/archive/ncs/chemworld-ncs-zh-full.pdf"


def run(command, stage):
    print(f"pdf stage={stage} command={Path(command[0]).name}", flush=True)
    started = time.monotonic()
    with (BUILD / f"{stage}.stdout.log").open("w", encoding="utf-8") as stdout:
        process = subprocess.Popen(command, cwd=BUILD, stdout=stdout, stderr=subprocess.STDOUT)
        while True:
            try:
                code = process.wait(timeout=45)
                break
            except subprocess.TimeoutExpired:
                print(
                    f"pdf stage={stage} alive elapsed_s={time.monotonic() - started:.0f}",
                    flush=True,
                )
    log = (BUILD / f"{stage}.stdout.log").read_text(encoding="utf-8", errors="replace")
    if code:
        raise RuntimeError(f"{stage} failed ({code})\n{log[-7000:]}")
    return log


def bound_figures(path):
    tex = path.read_text(encoding="utf-8")
    tex = re.sub(
        r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
        r"\\includegraphics[width=\\linewidth,height=.74\\textheight,keepaspectratio]{\1}",
        tex,
    )
    tex = tex.replace(r"\begin{figure}[H]", r"\begin{figure}[htbp]")
    path.write_text(tex, encoding="utf-8")


def render_pages(pages):
    qa = BUILD / "pages"
    qa.mkdir(exist_ok=True)
    for old in [*qa.glob("page-*.png"), *BUILD.glob("contact-*.png")]:
        old.unlink()
    poppler = shutil.which("pdftoppm")
    assert poppler
    # Each bounded chunk provides an explicit denominator and avoids a long silent render.
    for first in range(1, pages + 1, 4):
        last = min(first + 3, pages)
        run(
            [
                poppler,
                "-f",
                str(first),
                "-l",
                str(last),
                "-r",
                "80",
                "-png",
                str(OUTPUT),
                str(qa / "page"),
            ],
            f"render-{first:02d}-{last:02d}",
        )
        print(f"pdf stage=visual-QA-render completed={last}/{pages}", flush=True)
    paths = sorted(qa.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    assert len(paths) == pages
    for offset in range(0, pages, 6):
        subset = paths[offset : offset + 6]
        sheet = Image.new("RGB", (3 * 360, 2 * 535), "#dde2e5")
        draw = ImageDraw.Draw(sheet)
        for i, path in enumerate(subset):
            with Image.open(path) as raw:
                im = raw.convert("RGB")
                im.thumbnail((344, 497))
                x, y = (i % 3) * 360 + (360 - im.width) // 2, (i // 3) * 535 + 25
                sheet.paste(im, (x, y))
                draw.text(((i % 3) * 360 + 12, (i // 3) * 535 + 7), path.stem, fill="black")
        sheet.save(BUILD / f"contact-{offset + 1:02d}-{min(offset + 6, pages):02d}.png")


def main():
    global OUTPUT
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    OUTPUT = parser.parse_args().output.resolve()
    BUILD.mkdir(parents=True, exist_ok=True)
    source = SOURCE.read_text(encoding="utf-8")
    assert source.count("{#fig:") == 8
    assert "[Figure " not in source and "about here" not in source
    assert "# 图件建议" not in source
    body = source.replace("](../../../figures/", "](figures/")
    # Section headings provide the visual hierarchy; manuscript draft rules are redundant.
    body = body.replace("\n\n---\n\n", "\n\n")
    results_start, results_end = body.index("# 结果"), body.index("# 讨论")
    results = body[results_start:results_end]
    results = re.sub(r"^## ", r"\\FloatBarrier\n\n## ", results, flags=re.M)
    body = body[:results_start] + results + body[results_end:]
    body = body.replace("# 讨论", "\\FloatBarrier\n\n# 讨论")
    # Keep the closing Results paragraph after its deferred full-page case figure.
    body = body.replace("这一系列结果最终把问题", "\\FloatBarrier\n\n这一系列结果最终把问题")
    body = body.replace("# 方法", "\\FloatBarrier\n\n# 方法")
    body = body.replace("# 扩展图", "\\clearpage\n\n# 扩展图")
    body = re.sub(r"^(#{1,2} .+)$", r"\\needspace{5\\baselineskip}\n\n\1", body, flags=re.M)
    (BUILD / "main.md").write_text(body, encoding="utf-8")
    for folder in ("ncs-full", "integrated-results", "venue-results", "final-ppt"):
        target = BUILD / "figures" / folder
        target.mkdir(parents=True, exist_ok=True)
        for src in (PAPER / "figures" / folder).iterdir():
            if src.suffix.lower() in (".png", ".pdf"):
                shutil.copy2(src, target / src.name)
    shutil.copy2(PAPER / "chemworld_integrated_references.bib", BUILD / "references.bib")
    appendix_text = appendix("ncs")
    # Chinese extended Fig. S1 precedes the five shared English supplement figures.
    # Adjust prose references only; the asset filenames retain their English numbering.
    appendix_text = re.sub(
        r"\b(Figure|Fig\.) S(\d+)",
        lambda match: f"{match[1]} S{int(match[2]) + 1}",
        appendix_text,
    )
    # The selected research path is main Fig. 4 in this Chinese edition.
    appendix_text = re.sub(r"\b(Figure|Fig\.) 2\b", r"\1 4", appendix_text)
    (BUILD / "appendix.md").write_text(appendix_text, encoding="utf-8")
    pandoc, latex, bibtex = (shutil.which(t) for t in ("pandoc", "xelatex", "bibtex"))
    assert pandoc and latex and bibtex
    common = [
        pandoc,
        "--from=markdown+raw_tex+tex_math_dollars+tex_math_single_backslash",
        "--to=latex",
        "--natbib",
        "--top-level-division=section",
    ]
    run(
        [
            *common,
            "main.md",
            "--standalone",
            "--template=" + str(PAPER / "venues/ncs/archive/template_zh.tex"),
            "-o",
            "main.tex",
        ],
        "pandoc-main",
    )
    run([*common, "appendix.md", "-o", "appendix.tex"], "pandoc-appendix")
    for name in ("main.tex", "appendix.tex"):
        tidy_tex(BUILD / name, "ncs")
        bound_figures(BUILD / name)
    command = [latex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    run(command, "latex-1")
    run([bibtex, "main"], "bibtex")
    for i in (2, 3):
        run(command, f"latex-{i}")
    log = (BUILD / "main.log").read_text(encoding="utf-8", errors="replace")
    bad = re.findall(
        r"^.*(?:Missing character|undefined citations|Citation .*undefined|LaTeX Error).*$",
        log,
        re.M,
    )
    assert not bad, bad
    warnings = [s for s in log.splitlines() if "Overfull" in s]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BUILD / "main.pdf", OUTPUT)
    info = run([shutil.which("pdfinfo"), str(OUTPUT)], "pdfinfo")
    pages = int(re.search(r"Pages:\s*(\d+)", info)[1])
    run([shutil.which("pdftotext"), "-layout", str(OUTPUT), str(BUILD / "main.txt")], "text-QA")
    text = (BUILD / "main.txt").read_text(encoding="utf-8")
    assert all(term in text for term in ("参考文献", "补充材料", "封存", "240", "335/360"))
    assert "about here" not in text
    render_pages(pages)
    report = {
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "output": OUTPUT.relative_to(ROOT).as_posix(),
        "main_figures": 7,
        "main_tables": len(re.findall(r"^\|[ \t:|\-]+\|[ \t]*$", results, flags=re.M)),
        "extended_figures": 1,
        "supplementary_figures": len(re.findall(r"^!\[", appendix_text, flags=re.M)),
        "includes_methods_references_supplement": True,
        "pages": pages,
        "layout_warnings": warnings,
        "missing_glyphs_or_citations": bad,
        "new_experiments": 0,
        "qa_directory": str(BUILD),
    }
    (PAPER / "venues/ncs/archive/CHINESE_BUILD_SUMMARY.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1790078400")
    main()
