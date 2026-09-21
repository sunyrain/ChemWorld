"""Build independent ICLR/NCS drafts from shared retained evidence, without experiments."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
VENUES = PAPER / "venues"
OUT = ROOT / "output/pdf"
BUILD = Path(tempfile.gettempdir()) / "chemworld-venue-manuscripts"
BIB = PAPER / "chemworld_integrated_references.bib"
SOURCES = {"iclr2027": "manuscript.md", "ncs": "article.md"}


def run(command: list[str], cwd: Path):
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stdout[-9000:] + result.stderr[-3000:])
    return result


def load_markdown(path: Path):
    _, metadata, body = path.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(metadata), body.strip()


def word_count(text: str):
    text = re.sub(r"!\[.*?\]\([^\n]+\)(?:\{[^}]+\})?", "", text, flags=re.S)
    text = re.sub(r"\[@[^]]+\]", "", text)
    text = re.sub(r"\$[^$]*\$", " MATH ", text)
    return len(re.findall(r"\b[\w]+(?:[-'.][\w]+)*\b", text))


def assets(text: str):
    text = re.sub(r"\]\((?:\.\./){1,2}(figures/[^)]+)\)", r"](\1)", text)
    for asset in re.findall(r"\]\((figures/[^)]+)\)", text):
        assert (PAPER / asset).is_file(), asset
    return text


def author_block():
    meta, _ = load_markdown(PAPER / "chemworld_integrated_manuscript.md")
    names = []
    for a in meta["author"]:
        marks = "1" + (",*" if a.get("equal_contribution") else "")
        marks += r",\dagger" if a.get("corresponding") else ""
        names.append(a["name"] + "$^{" + marks + "}$")
    text = (
        r"{\normalsize "
        + ", ".join(names[:3])
        + r"\\[4pt]"
        + "\n"
        + ", ".join(names[3:])
        + r"\par}"
        + "\n"
        + r"\vspace{.6em}{\small $^1$"
        + meta["affiliation"][0]["name"]
        + r"\par}"
        + "\n"
        + r"\vspace{.4em}{\small $^*$"
        + meta["equal_contribution_note"]
        + r"\\"
        + "\n"
        + r"$^\dagger$Correspondence: \texttt{"
        + meta["correspondence"]
        + r"}\par}"
    )
    return text, ", ".join(a["name"] for a in meta["author"])


def appendix(venue: str):
    protocol = (VENUES / "shared_protocol.md").read_text(encoding="utf-8")
    # One full-width prior overview per page; keep it apart from protocol text.
    protocol = protocol.replace("## A.6", "\\clearpage\n\n## A.6")
    if venue == "iclr2027":
        protocol += (
            "\n\\clearpage\n\n## A.7 Budget response overview\n\n"
            "![Matched budget effects across responses. Each larger-budget source is a new "
            "session with a larger research envelope. World-level pairs and response-specific "
            "scales are retained.](figures/integrated-results/budgets.pdf){width=100%}\n"
        )
    blocks = [
        protocol,
        (PAPER / "chemworld_integrated_results_appendix.md").read_text(encoding="utf-8"),
        (VENUES / "shared_exploratory_analysis.md").read_text(encoding="utf-8"),
    ]
    text = "\n\\clearpage\n\n".join(blocks)
    text = re.sub(r"^# Appendix [A-C]\. ", "# ", text, flags=re.M)
    text = re.sub(r"^## [A-C]\.\d+ ", "## ", text, flags=re.M)
    # Metric tables are compact units; avoid stranded subsection headings.
    text = re.sub(r"^(## .+)$", r"\\needspace{9\\baselineskip}\n\n\1", text, flags=re.M)
    return assets(text)


def tidy_tex(path: Path, venue: str):
    text = path.read_text(encoding="utf-8")
    placement = "H" if venue == "ncs" else "htbp"
    text = text.replace(r"\begin{figure}", r"\begin{figure}[" + placement + "]")
    # Keep each short appendix table and its manually numbered caption together.
    text = text.replace(
        r"\begin{longtable}[]{", "\\begin{table}[H]\\centering\\small\n\\begin{tabular}{"
    )
    text = re.sub(r"\\endhead\s*\\bottomrule\\noalign\{\}\s*\\endlastfoot", "", text)
    text = text.replace(r"\end{longtable}", "\\bottomrule\n\\end{tabular}\n\\end{table}")
    text = re.sub(
        r"(\\end\{tabular\})\n\\end\{table\}\n\}\s*\n(Table [A-C]\d+\. .*?)\n\n",
        lambda m: m[1] + "\n\\caption*{" + m[2] + "}\n\\end{table}\n}\n\n",
        text,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8")


def build(venue: str):
    meta, body = load_markdown(VENUES / venue / SOURCES[venue])
    abstract_words = word_count(meta["abstract"])
    main_text = body.split("# Methods", 1)[0] if venue == "ncs" else body
    main_words = word_count(main_text)
    displays = len(re.findall(r"^!\[", main_text, flags=re.M))
    assert not re.search(r"^\|", main_text, flags=re.M), "Count main tables before adding them"
    if venue == "ncs":
        assert abstract_words <= 150 and main_words <= 3500 and displays <= 6
        assert not body.startswith("# Introduction")
        discussion = body.split("# Discussion", 1)[1].split("# Methods", 1)[0]
        assert "## " not in discussion
        body = body.replace("# Methods", "\\FloatBarrier\n\\clearpage\n\n# Methods")
        body = re.sub(r"^(#{1,2} .+)$", r"\1 {-}", body, flags=re.M)
        meta["authorblock"] = "CHEMWORLDAUTHORBLOCK"
        meta["pdfauthors"] = author_block()[1]
    body = assets(body)
    keys = set(re.findall(r"@\w+\{([^,]+),", BIB.read_text(encoding="utf-8")))
    assert set(re.findall(r"@([a-zA-Z][\w-]+)", body)) <= keys
    build_dir = BUILD / venue
    build_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BIB, build_dir / "references.bib")
    for folder in ("integrated-results", "venue-results"):
        target = build_dir / "figures" / folder
        target.mkdir(parents=True, exist_ok=True)
        for src in (PAPER / "figures" / folder).glob("*.pdf"):
            shutil.copy2(src, target / src.name)
    if venue == "iclr2027":
        for filename in ("iclr2027_conference.sty", "iclr2027_conference.bst", "math_commands.tex"):
            shutil.copy2(PAPER / "iclr2027" / filename, build_dir / filename)
    pandoc, bibtex = shutil.which("pandoc"), shutil.which("bibtex")
    latex = shutil.which("pdflatex" if venue == "iclr2027" else "xelatex")
    assert pandoc and bibtex and latex
    md = build_dir / "main.md"
    md.write_text(
        "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n" + body,
        encoding="utf-8",
    )
    app = build_dir / "appendix.md"
    app.write_text(appendix(venue), encoding="utf-8")
    common = [
        pandoc,
        "--from=markdown+raw_tex+tex_math_dollars",
        "--to=latex",
        "--natbib",
        "--top-level-division=section",
    ]
    print(
        f"venue={venue} stage=pandoc completed=0/4 "
        f"abstract_words={abstract_words} main_words={main_words}",
        flush=True,
    )
    run([*common, str(app), "-o", "appendix.tex"], build_dir)
    run(
        [
            *common,
            str(md),
            "--standalone",
            "--template=" + str(VENUES / venue / "template.tex"),
            "-o",
            "main.tex",
        ],
        build_dir,
    )
    if venue == "ncs":
        tex = build_dir / "main.tex"
        tex.write_text(
            tex.read_text(encoding="utf-8").replace("CHEMWORLDAUTHORBLOCK", author_block()[0]),
            encoding="utf-8",
        )
    for name in ("main.tex", "appendix.tex"):
        tidy_tex(build_dir / name, venue)
    command = [latex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    print(f"venue={venue} stage=latex completed=1/4", flush=True)
    run(command, build_dir)
    run([bibtex, "main"], build_dir)
    for iteration in range(3):
        print(f"venue={venue} stage=references completed={iteration + 2}/4", flush=True)
        run(command, build_dir)
        log = (build_dir / "main.log").read_text(encoding="utf-8", errors="replace")
        if not re.search(r"Rerun to get cross-references right|undefined citations", log):
            break
    assert not re.search(
        r"Citation .* undefined|There were undefined|LaTeX Error|Missing character", log
    )
    warnings = [line for line in log.splitlines() if "Overfull" in line]
    pdfinfo, pdftotext = shutil.which("pdfinfo"), shutil.which("pdftotext")
    assert pdfinfo and pdftotext
    info = run([pdfinfo, "main.pdf"], build_dir).stdout
    pages = int(re.search(r"Pages:\s*(\d+)", info)[1])
    run([pdftotext, "-layout", "main.pdf", "main.txt"], build_dir)
    extracted = (build_dir / "main.txt").read_text(encoding="utf-8")
    main_pages = None
    if venue == "iclr2027":
        aux = (build_dir / "main.aux").read_text(encoding="utf-8")
        match = re.search(r"\\newlabel\{main-text-end\}\{\{[^}]*\}\{(\d+)\}", aux)
        assert match
        main_pages = int(match[1])
        combined = extracted + info
        for identifying in (
            "Jiangjie",
            "Yijun",
            "Yaotian",
            "Honghao",
            "Wentao",
            "Xiaonan",
            "Tsinghua",
            "wangxiaonan",
            "sunyrain",
            "D:\\Projects",
            "C:\\Users",
        ):
            assert identifying not in combined, identifying
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / (
        "chemworld-iclr2027.pdf" if venue == "iclr2027" else "chemworld-ncs-article.pdf"
    )
    shutil.copy2(build_dir / "main.pdf", output)
    result = {
        "venue": venue,
        "source": (VENUES / venue / SOURCES[venue]).relative_to(ROOT).as_posix(),
        "pdf": output.relative_to(ROOT).as_posix(),
        "abstract_words": abstract_words,
        "main_words_excluding_captions": main_words,
        "main_display_items": displays,
        "main_pages": main_pages,
        "total_pages": pages,
        "layout_warnings": warnings,
        "main_page_limit": 9 if venue == "iclr2027" else None,
        "within_main_page_limit": main_pages is None or main_pages <= 9,
        "undefined_citations": False,
        "new_experiments": False,
        "evidence_promoted": False,
    }
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--venue", choices=["all", *SOURCES], default="all")
    args = parser.parse_args()
    results = [build(v) for v in SOURCES if args.venue in ("all", v)]
    record = VENUES / "BUILD_SUMMARY.json"
    if args.venue != "all" and record.exists():
        previous = json.loads(record.read_text(encoding="utf-8"))
        results += [r for r in previous if r["venue"] != args.venue]
    record.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Build and QA directory: {BUILD}", flush=True)


if __name__ == "__main__":
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1789948800")
    main()
