"""Build a separate integrated review PDF without changing the frozen Paper 1 export."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
OUT = ROOT / "output/pdf/archive/integrated-review"
SOURCE = PAPER / "chemworld_integrated_manuscript.md"


def run(command, cwd):
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
        raise RuntimeError(result.stdout[-7000:] + result.stderr[-7000:])
    return result


def main():
    text = SOURCE.read_text(encoding="utf-8")
    _, metadata, body = text.split("---", 2)
    meta = yaml.safe_load(metadata)
    appendix = (PAPER / "chemworld_integrated_results_appendix.md").read_text(encoding="utf-8")
    body = body.replace("# Appendix A.", "\\clearpage\n\n# Appendix A.")
    body = body.replace(
        "# References", "\\clearpage\n\n" + appendix + "\n\\clearpage\n\n# References"
    )
    bibliography = PAPER / meta["bibliography"]
    keys = set(re.findall(r"@\w+\{([^,]+),", bibliography.read_text(encoding="utf-8")))
    used = set(re.findall(r"@([a-zA-Z][\w-]+)", body))
    assert used <= keys, used - keys
    assert "Prospective nine-system" not in text
    assert "[TODO" not in text and "[TBD" not in text
    for asset in re.findall(r"\]\((figures/[^)]+)\)", body):
        assert (PAPER / asset).is_file(), asset
        body = body.replace("](" + asset + ")", "](" + (PAPER / asset).as_posix() + ")")
    OUT.mkdir(parents=True, exist_ok=True)
    # Keep transient LaTeX and QA files outside the repository.
    build = Path(tempfile.gettempdir()) / "chemworld-integrated-review-build"
    build.mkdir(exist_ok=True)
    header = build / "header.tex"
    header.write_text(
        r"""
\usepackage{float}
\usepackage{caption}
\captionsetup{font=small,labelfont=bf}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small ChemWorld}
\fancyhead[R]{\small Integrated research manuscript}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{15pt}
\setlength{\emergencystretch}{3em}
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.16}
\AtBeginEnvironment{longtable}{\small}
\floatplacement{figure}{htbp}
\widowpenalty=1000
\clubpenalty=1000
""",
        encoding="utf-8",
    )
    authors = []
    for author in meta["author"]:
        marker = "1" + (",*" if author.get("equal_contribution") else "")
        marker += ",\\dagger" if author.get("corresponding") else ""
        authors.append(author["name"] + "$^{" + marker + "}$")
    title = build / "title.tex"
    title.write_text(
        "\\begin{center}\n{\\LARGE\\bfseries "
        + meta["title"]
        + "\\par}\n\\vspace{1em}\n"
        + "{\\normalsize "
        + ", ".join(authors[:3])
        + "\\\\[4pt]\n"
        + ", ".join(authors[3:])
        + "\\par}\n\\vspace{.8em}\n{\\small $^1$"
        + meta["affiliation"][0]["name"]
        + "\\par}\n\\vspace{.5em}\n"
        + "{\\small $^*$"
        + meta["equal_contribution_note"]
        + "\\\\\n"
        + "$^\\dagger$Correspondence: \\texttt{"
        + meta["correspondence"]
        + "}\\par}\n\\end{center}\n\\vspace{.5em}\n",
        encoding="utf-8",
    )
    manuscript = build / "review.md"
    manuscript.write_text(body, encoding="utf-8")
    tex = build / "chemworld-integrated-review.tex"
    pandoc = shutil.which("pandoc")
    xelatex = shutil.which("xelatex")
    assert pandoc and xelatex, "Pandoc and XeLaTeX are required"
    print("stage=pandoc completed=0/3", flush=True)
    result = run(
        [
            pandoc,
            str(manuscript),
            "--standalone",
            "--citeproc",
            "--from=markdown+tex_math_dollars",
            "--resource-path=" + str(PAPER),
            "--bibliography=" + str(bibliography),
            "--include-in-header=" + str(header),
            "--include-before-body=" + str(title),
            "-V",
            "documentclass=article",
            "-V",
            "fontsize=11pt",
            "-V",
            "papersize=a4",
            "-V",
            "geometry:margin=23mm",
            "-V",
            "mainfont=Times New Roman",
            "-V",
            "sansfont=Arial",
            "-V",
            "monofont=Consolas",
            "-V",
            "colorlinks=true",
            "-V",
            "linkcolor=black",
            "-V",
            "urlcolor=blue",
            "-V",
            "citecolor=black",
            "-M",
            "lang=en-US",
            "-M",
            "link-citations=true",
            "-M",
            "reference-section-title=",
            "-o",
            str(tex),
        ],
        build,
    )
    (build / "pandoc.log").write_text(result.stderr, encoding="utf-8")
    latex = tex.read_text(encoding="utf-8").replace("\\begin{figure}", "\\begin{figure}[H]")
    # These are compact review tables, all shorter than a page. Keep each together.
    latex = latex.replace(
        "\\begin{longtable}[]{", "\\begin{table}[H]\\centering\\small\n\\begin{tabular}{"
    )
    latex = re.sub(r"\\endhead\s*\\bottomrule\\noalign\{\}\s*\\endlastfoot", "", latex)
    latex = latex.replace("\\end{longtable}", "\\bottomrule\n\\end{tabular}\n\\end{table}")
    # Keep the manually numbered Markdown caption with its table, including A1/A2.
    latex = re.sub(
        r"(\\end\{tabular\})\n\\end\{table\}\n\}\s*\n"
        r"(Table (?:A)?\d+\. .*?)\n\n",
        lambda m: m[1] + "\n\\caption*{" + m[2] + "}\n\\end{table}\n}\n\n",
        latex,
        flags=re.DOTALL,
    )
    tex.write_text(latex, encoding="utf-8")
    # Pandoc emits an absolute resource path for figures; compile in this isolated directory.
    for iteration in range(2):
        print(f"stage=xelatex completed={iteration + 1}/3", flush=True)
        run([xelatex, "-interaction=nonstopmode", "-halt-on-error", str(tex)], build)
    pdf = build / "chemworld-integrated-review.pdf"
    target = OUT / pdf.name
    shutil.copyfile(pdf, target)
    log = (build / "chemworld-integrated-review.log").read_text(encoding="utf-8", errors="replace")
    warnings = [
        line
        for line in log.splitlines()
        if any(
            x in line for x in ("Overfull", "Missing character", "undefined references", "Citation")
        )
    ]
    print(f"stage=complete completed=3/3 pdf={target} bytes={target.stat().st_size}", flush=True)
    print("Layout diagnostics:", warnings)
    print("Build diagnostics retained at", build)


if __name__ == "__main__":
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1789948800")
    main()
