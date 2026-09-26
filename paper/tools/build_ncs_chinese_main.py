"""Render the current article's Chinese main text, keeping the approved figures."""

from __future__ import annotations

import os
import re
import shutil
import tempfile
from pathlib import Path

import yaml
from build_venue_manuscripts import assets, load_markdown, run, tidy_tex

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
SOURCE = PAPER / "venues/ncs/article_zh_main.md"
BUILD = Path(tempfile.gettempdir()) / "chemworld-ncs-chinese-main"
OUTPUT = ROOT / "output/pdf/chemworld-ncs-zh-main.pdf"


def citation_numbers(text: str, english: str) -> str:
    """Keep the full English article's citation order without a reference list."""
    order = list(dict.fromkeys(re.findall(r"@([a-zA-Z][\w-]+)", english)))
    numbering = {key: index + 1 for index, key in enumerate(order)}
    assert set(re.findall(r"@([a-zA-Z][\w-]+)", text)) == set(order)

    def replace(match: re.Match) -> str:
        keys = re.findall(r"@([a-zA-Z][\w-]+)", match[0])
        values = sorted(numbering[key] for key in keys)
        if len(values) > 2 and values == list(range(values[0], values[-1] + 1)):
            label = f"{values[0]}--{values[-1]}"
        else:
            label = ",".join(map(str, values))
        return r"\textsuperscript{" + label + "}"

    return re.sub(r"\[@[^\]]+\]", replace, text)


def main() -> None:
    meta, body = load_markdown(SOURCE)
    _, english = load_markdown(PAPER / "venues/ncs/article.md")
    english = english.split("# Methods", 1)[0]
    expected_assets = re.findall(r"!\[[^\n]+\]\(([^)]+)\)", english)
    figure_assets = re.findall(r"!\[[^\n]+\]\(([^)]+)\)", body)
    assert figure_assets == expected_assets and len(figure_assets) == 6
    assert len(re.findall(r"^## ", body, re.M)) == 4
    assert not re.search(r"^# (?:方法|参考文献|补充材料)", body, re.M)
    body = citation_numbers(body, english)
    body = re.sub(r"^(## .+)$", r"\\FloatBarrier\n\n\1", body, flags=re.M)
    body = body.replace("# 讨论", "\\FloatBarrier\n\\clearpage\n\n# 讨论")
    body = body.replace("# 结果", "\\needspace{12\\baselineskip}\n\n# 结果")
    body = re.sub(r"^(#{1,2} .+)$", r"\\needspace{5\\baselineskip}\n\n\1", body, flags=re.M)
    body = assets(body)

    BUILD.mkdir(parents=True, exist_ok=True)
    for asset in figure_assets:
        src = (SOURCE.parent / asset).resolve()
        dst = BUILD / src.relative_to(PAPER)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    (BUILD / "main.md").write_text(
        "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n" + body,
        encoding="utf-8",
    )
    pandoc, latex = shutil.which("pandoc"), shutil.which("xelatex")
    assert pandoc and latex
    print("Chinese main text: stage=typesetting completed=0/3", flush=True)
    run(
        [
            pandoc,
            "main.md",
            "--from=markdown+raw_tex+tex_math_dollars",
            "--to=latex",
            "--standalone",
            "--template=" + str(SOURCE.parent / "template_zh_main.tex"),
            "-o",
            "main.tex",
        ],
        BUILD,
    )
    tex_path = BUILD / "main.tex"
    tidy_tex(tex_path, "ncs")
    tex = tex_path.read_text(encoding="utf-8")
    tex = re.sub(
        r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
        r"\\includegraphics[width=\\linewidth,height=.70\\textheight,keepaspectratio]{\1}",
        tex,
    )
    tex_path.write_text(tex, encoding="utf-8")
    for iteration in (1, 2):
        print(f"Chinese main text: stage=latex completed={iteration}/3", flush=True)
        run([latex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"], BUILD)
    log = (BUILD / "main.log").read_text(encoding="utf-8", errors="replace")
    failures = re.findall(
        r"^.*(?:Missing character|undefined citations|LaTeX Error|Overfull).*$", log, re.M
    )
    assert not failures, failures
    info = run([shutil.which("pdfinfo"), "main.pdf"], BUILD).stdout
    pages = int(re.search(r"Pages:\s*(\d+)", info)[1])
    run([shutil.which("pdftotext"), "-layout", "main.pdf", "main.txt"], BUILD)
    text = (BUILD / "main.txt").read_text(encoding="utf-8")
    assert all(term in text for term in ("摘要", "结果", "讨论", "240", "335", "0.15862"))
    assert not re.search(r"^\s*(?:方法|参考文献|补充材料)\s*$", text, re.M)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BUILD / "main.pdf", OUTPUT)
    print(
        f"Chinese main text: completed=3/3 pages={pages} figures=6 tables=1 "
        f"layout_warnings=0 output={OUTPUT}",
        flush=True,
    )
    print(f"QA directory: {BUILD}", flush=True)


if __name__ == "__main__":
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1790294400")
    main()
