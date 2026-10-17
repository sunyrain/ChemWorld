"""Build the independent Nature-style preview from retained manuscript sources."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
VENUE = ROOT / "paper/venues/nature"
OUT = ROOT / "output/pdf"
TEX = VENUE / "tex"
BUILD = ROOT.parent / "ChemWorld-local-research/manuscript-nature-20261016/build"


def run(args: list[str], cwd: Path, label: str) -> str:
    start = time.monotonic()
    process = subprocess.Popen(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    while True:
        try:
            output, _ = process.communicate(timeout=30)
            break
        except subprocess.TimeoutExpired:
            print(f"{label}: alive, {time.monotonic() - start:.0f}s elapsed", flush=True)
    if process.returncode:
        raise RuntimeError(f"{label} failed:\n{output[-14000:]}")
    if "WARNING" in output:
        print("\n".join(line for line in output.splitlines() if "WARNING" in line), flush=True)
    return output


def read(name: str) -> str:
    return (VENUE / name).read_text(encoding="utf-8")


def strip_frontmatter(text: str) -> tuple[dict, str]:
    parts = text.split("---", 2)
    return (yaml.safe_load(parts[1]), parts[2].strip()) if len(parts) == 3 else ({}, text)


def render_template(values: dict) -> str:
    template = read("template.tex")
    pattern = re.compile(r"\$if\((\w+)\)\$(.*?)\$endif\$", re.S)

    def choose(match: re.Match) -> str:
        parts = match[2].split("$else$")
        return parts[0] if values.get(match[1]) else (parts[1] if len(parts) > 1 else "")

    template = pattern.sub(choose, template)
    return re.sub(r"\$(\w+)\$", lambda m: str(values.get(m[1], "")), template)


def authors() -> tuple[str, str]:
    text = (ROOT / "paper/venues/ncs/article.md").read_text(encoding="utf-8")
    meta, _ = strip_frontmatter(text)
    names = []
    for author in meta["author"]:
        marks = "1" + (",*" if author.get("equal_contribution") else "")
        marks += ",\\textdagger" if author.get("corresponding") else ""
        names.append(author["name"] + r"\textsuperscript{" + marks + "}")
    block = r"{\normalsize " + ", ".join(names) + r"\par}" + "\n"
    block += (
        r"{\footnotesize\textsuperscript{1}" + meta["affiliation"][0]["name"] + r".\par}" + "\n"
    )
    block += r"{\footnotesize * " + meta["equal_contribution_note"] + r"\par}" + "\n"
    block += (
        r"{\footnotesize $\dagger$ Correspondence: \href{mailto:"
        + meta["correspondence"]
        + "}{"
        + meta["correspondence"]
        + r"}.\par}"
    )
    return block, meta["pdf_author"]


def build(language: str, review: bool = False, supplement: bool = False) -> dict:
    chinese = language == "zh"
    stem = "chemworld-nature-" + ("supplement" if supplement else language)
    if review:
        stem += "-review"
    suffix = "_zh" if chinese else ""
    meta, article = strip_frontmatter(read("article" + suffix + ".md"))
    if supplement:
        text = read("supplementary.md")
        title = "Supplementary Information: " + meta["title"]
    else:
        title = meta["title"]
        opening, body = article.split("\n\n", 1)
        methods = read("methods" + suffix + ".md")
        extended = read("extended_data" + suffix + ".md")
        funding_heading = "\n## " + ("资助" if chinese else "Funding") + "\n"
        if funding_heading in methods:
            methods, funding = methods.split(funding_heading, 1)
            # Keep the short Chinese funding note with back matter so it does not
            # occupy an otherwise empty page after the two-column discussion.
            if chinese:
                methods += "\n" + funding_heading + funding
            else:
                body += "\n" + funding_heading + funding
        refs = "参考文献" if chinese else "References"
        text = opening + "\n\n\\MainStart\n\n" + body
        text += "\n\n\\clearpage\n\\onecolumn\n\n# " + refs + "\n\n::: {#refs}\n:::\n\n"
        text += "\\clearpage\n\n" + methods + "\n\n\\Needspace{.70\\textheight}\n\n" + extended
    source = BUILD / (stem + ".md")
    source.write_text(text, encoding="utf-8")
    body_path = BUILD / (stem + "-body.tex")
    args = [
        "pandoc",
        str(source),
        "--from=markdown+raw_tex",
        "--to=latex",
        "--top-level-division=section",
        "--wrap=none",
        "--citeproc",
        "--bibliography=" + str(ROOT / "paper/chemworld_integrated_references.bib"),
        "--csl=" + str(VENUE / "numeric-references.csl"),
        "-o",
        str(body_path),
    ]
    run(args, VENUE, stem + " citation conversion")
    latex = body_path.read_text(encoding="utf-8")
    latex = re.sub(r"\\bibitem\[\\citeproctext\]\{([^}]+)\}", r"\\hypertarget{\1}{}", latex)
    if supplement:
        opening_tex = ""
    else:
        opening_tex, latex = latex.split(r"\MainStart", 1)
    latex = re.sub(
        # Pandoc's alt text can itself contain brackets (e.g. prediction intervals).
        r"\\includegraphics(?:\[[^\n]*?\])?\{(figures/[^}]+)\}",
        r"\\includegraphics[width=\\linewidth,height=.68\\textheight,keepaspectratio]{../\1}",
        latex,
    )
    twocolumn = not review and not supplement
    if twocolumn:
        main, rest = latex.split(r"\onecolumn", 1)
        main = main.replace(r"\begin{figure}", r"\begin{figure*}[t]")
        main = main.replace(r"\end{figure}", r"\end{figure*}")
        latex = main + r"\onecolumn" + rest
    # Prevent main figures drifting beyond the scientific argument into Discussion.
    discussion_marker = r"\subsection{" + ("讨论" if chinese else "Discussion") + "}"
    latex = latex.replace(discussion_marker, r"\FloatBarrier" + "\n" + discussion_marker)
    latex = latex.replace(r"\begin{figure}", r"\begin{figure}[htbp]")
    # Keep each Extended Data figure and its own caption on one page.
    ed_marker = "扩展数据" if chinese else "Extended Data"
    marker = r"\section{" + ed_marker + "}"
    if marker in latex:
        before, after = latex.split(marker, 1)
        after = after.replace(r"\begin{figure}[htbp]", r"\clearpage\begin{figure}[H]")
        after = after.replace(r"\clearpage\begin{figure}[H]", r"\begin{figure}[H]", 1)
        latex = before + marker + after
    if supplement:
        latex = latex.replace(r"\def\LTcaptype{none}", r"\def\LTcaptype{table}")
        latex = latex.replace(r"\subsubsection{", r"\Needspace{9\baselineskip}\subsubsection{")
        latex = latex.replace(r"\real{0.1429}", r"\real{0.14285}")
        latex = latex.replace(r"\begin{longtable}", r"\small\begin{longtable}")
        latex = latex.replace(r"\end{longtable}", r"\end{longtable}\normalsize")
    authorblock, pdfauthors = authors()
    notice = (
        "全部插图为ImageGen预览，点位与几何仅作示意；精确数值见补充材料。"  # noqa: RUF001 - Chinese prose punctuation
        if chinese
        else "All figures are ImageGen previews with illustrative geometry; "
        "exact numerical evidence is retained separately."
    )
    if supplement:
        notice = (
            "Retained numerical evidence. "
            "Research cohorts and all failure dispositions remain separate."
        )
    rendered = render_template(
        {
            "title": title,
            "opening": opening_tex,
            "body": latex,
            "review": review,
            "chinese": chinese,
            "twocolumn": twocolumn,
            "authorblock": authorblock,
            "pdfauthors": pdfauthors,
            "previewnotice": notice,
            "runninglabel": "Supplementary evidence" if supplement else "Integrated research draft",
        }
    )
    tex_path = TEX / (stem + ".tex")
    tex_path.write_text(rendered, encoding="utf-8")
    for pass_index in range(2):
        run(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                "-output-directory=" + str(BUILD),
                tex_path.name,
            ],
            TEX,
            f"{stem} typesetting pass {pass_index + 1}/2",
        )
    shutil.copy2(BUILD / (stem + ".pdf"), OUT / (stem + ".pdf"))
    info = run(["pdfinfo", str(OUT / (stem + ".pdf"))], VENUE, "PDF metadata")
    pages = int(re.search(r"Pages:\s+(\d+)", info)[1])
    print(f"Built {stem}: {pages} pages", flush=True)
    return {
        "file": stem + ".pdf",
        "pages": pages,
        "contains_imagegen_data_previews": not supplement,
        "contains_imagegen_concept": not supplement,
        "native_quantitative_main_figures": [],
        "imagegen_preview_figures": 0
        if supplement
        else len(re.findall(r"^!\[.*\]\(figures/imagegen-", text, re.M)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=["en", "review", "zh", "supplement"])
    args = parser.parse_args()
    for directory in (OUT, TEX, BUILD):
        directory.mkdir(parents=True, exist_ok=True)
    tasks = [("en", False, False), ("en", True, False), ("zh", False, False), ("en", False, True)]
    labels = ["en", "review", "zh", "supplement"]
    tasks = [
        t for t, label in zip(tasks, labels, strict=True) if not args.only or label == args.only
    ]
    results = []
    started = time.monotonic()
    for index, task in enumerate(tasks):
        print(f"Manuscript build {index}/{len(tasks)} complete; starting {task}", flush=True)
        results.append(build(*task))
        elapsed = time.monotonic() - started
        eta = elapsed / (index + 1) * (len(tasks) - index - 1)
        print(
            f"Progress {index + 1}/{len(tasks)}; {elapsed / (index + 1):.1f}s/PDF; ETA {eta:.0f}s",
            flush=True,
        )
    (BUILD / "build-summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
