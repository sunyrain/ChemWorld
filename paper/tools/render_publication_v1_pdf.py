"""Assemble the arXiv-v1 manuscript and render publication and concept-atlas PDFs."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import tempfile
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import markdown

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANUSCRIPT = Path("paper/experimental_intelligence_v1_manuscript.md")
DEFAULT_DISPLAY = Path("paper/experimental_intelligence_v1_display_items.md")
DEFAULT_BIBLIOGRAPHY = Path("paper/experimental_intelligence_v1_references.bib")
DEFAULT_DATA = Path("benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json")
DEFAULT_RELEASE_MANIFEST = Path("benchmark/releases/chemworld-serious-v1/manifest.json")
DEFAULT_FIGURES = Path("paper/arxiv/figures")
DEFAULT_CONCEPTS = Path("paper/figures/experimental-intelligence-v1/concept-placeholders")
DEFAULT_OUTPUT = Path("paper/exports/experimental-intelligence-v1")

FIGURE_STEMS = {
    1: "figure-1-controlled-apparatus.svg",
    2: "figure-2-compiled-controls.svg",
    3: "figure-3-autonomous-lifecycle.svg",
    4: "figure-4-trajectory-dynamics.svg",
    5: "figure-5-within-world-replication.svg",
    6: "figure-6-experimental-agency-profile.svg",
}

FIGURE_COPY = {
    1: (
        "ChemWorld is a controlled apparatus for measuring experimental agency",
        "Typed state transitions couple public observations to resource receipts, "
        "immutable traces and exact physical replay while experimental contrasts remain explicit.",
    ),
    2: (
        "Compiled controls distinguish task outcome, information response and epistemic readouts",
        "Paired worlds, a misindexed-prior manipulation and separate outcome and "
        "epistemic measures establish the low-authority calibration layer.",
    ),
    3: (
        "Primitive-control agents close complete experimental lifecycles",
        "The agent selects operations, observes intermediate evidence, decides when to stop and "
        "requests final assay under a reconstructable campaign ledger.",
    ),
    4: (
        "Similar endpoints can arise from different experimental trajectories",
        "Development worlds expose early discovery, loss, gradual improvement, retention and "
        "terminal divergence that an endpoint alone cannot resolve.",
    ),
    5: (
        "Fresh trajectories separate endpoint direction from lifecycle repeatability",
        "Matched-world session pairs keep right-censored cells visible and show mixed lifecycle "
        "directions under every possible sign of the missing differences.",
    ),
    6: (
        "Experimental agency is resolved as a profile of separate readouts",
        "Outcome, prediction, calibration, claim reliability, completion, retention, recovery and "
        "terminal behavior remain separate rather than being collapsed into a composite score.",
    ),
}

CONCEPT_STEMS = {
    1: "concept-figure-1-controlled-apparatus-v1.png",
    2: "concept-figure-2-autonomous-experiment-v1.png",
    3: "concept-figure-3-trajectory-phenotypes-v1.png",
    4: "concept-figure-4-prior-intervention-v1.png",
    5: "concept-figure-5-within-world-replication-v1.png",
    6: "concept-figure-6-intelligence-profile-v1.png",
}


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_sha(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _md(value: str) -> str:
    return markdown.markdown(
        value,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )


def _sections(markdown_text: str) -> tuple[str, str, list[tuple[str, str]]]:
    front_match = re.match(r"\A---\s*\n(?P<front>.*?)\n---\s*\n", markdown_text, re.DOTALL)
    if front_match is None:
        raise ValueError("manuscript YAML metadata is missing")
    front = front_match.group("front")
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front, re.MULTILINE)
    if title_match is None:
        raise ValueError("manuscript title is missing")
    lines = front.splitlines()
    try:
        abstract_index = next(
            index for index, line in enumerate(lines) if line.strip() == "abstract: |"
        )
    except StopIteration as exc:
        raise ValueError("manuscript abstract is missing") from exc
    abstract_lines: list[str] = []
    for line in lines[abstract_index + 1 :]:
        if line and not line.startswith("  "):
            break
        abstract_lines.append(line[2:] if line.startswith("  ") else "")
    abstract = "\n".join(abstract_lines).strip()
    body = markdown_text[front_match.end() :]
    matches = list(re.finditer(r"^#(?!#)\s+(.+)$", body, flags=re.MULTILINE))
    values: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        section = body[match.end() : end].strip()
        section = re.sub(r"```\{=latex\}.*?```", "", section, flags=re.DOTALL)
        values.append((match.group(1).strip(), section.strip()))
    return title_match.group(1).strip(), abstract, values


def _extract_table(display: str, number: int) -> tuple[str, str]:
    pattern = re.compile(
        rf"^### Table {number} \| (?P<title>.+?)\n\n"
        r"(?P<body>.*?)(?=\n### Table |\n## Figure legends)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(display)
    if match is None:
        raise ValueError(f"Table {number} is missing from display items")
    body = match.group("body").strip().replace("螖", "Δ")
    return match.group("title").strip(), body


def _extract_legend(display: str, number: int) -> tuple[str, str]:
    pattern = re.compile(
        rf"^\*\*Figure {number} \| (?P<title>.+?)\.\*\*\s*(?P<body>.*?)(?=\n\*\*Figure |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(display)
    if match is None:
        raise ValueError(f"Figure {number} legend is missing from display items")
    return match.group("title").strip(), match.group("body").strip()


def _latex_clean(value: str) -> str:
    replacements = {
        '{\\"a}': "ä",
        '{\\"o}': "ö",
        '{\\"u}': "ü",
        '{\\"i}': "ï",
        "{\\'a}": "á",
        "{\\'e}": "é",
        "{\\'i}": "í",
        "{\\'n}": "ń",
        "{\\'o}": "ó",
        "{\\c{c}}": "ç",
        "\\&": "&",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    value = value.replace("--", "\N{EN DASH}")
    value = value.replace("{", "").replace("}", "")
    value = value.replace("\\", "")
    return " ".join(value.split())


def _bib_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    cursor = 0
    while True:
        start = text.find("@", cursor)
        if start < 0:
            break
        open_brace = text.find("{", start)
        if open_brace < 0:
            break
        depth = 1
        index = open_brace + 1
        while index < len(text) and depth:
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
            index += 1
        if depth:
            raise ValueError("unbalanced BibTeX entry")
        block = text[open_brace + 1 : index - 1]
        comma = block.find(",")
        if comma < 0:
            cursor = index
            continue
        entry: dict[str, str] = {"key": block[:comma].strip()}
        fields = block[comma + 1 :]
        pos = 0
        while pos < len(fields):
            field_match = re.search(r"([A-Za-z][A-Za-z0-9]*)\s*=\s*\{", fields[pos:])
            if field_match is None:
                break
            name = field_match.group(1).lower()
            value_start = pos + field_match.end()
            field_depth = 1
            value_end = value_start
            while value_end < len(fields) and field_depth:
                if fields[value_end] == "{":
                    field_depth += 1
                elif fields[value_end] == "}":
                    field_depth -= 1
                value_end += 1
            entry[name] = _latex_clean(fields[value_start : value_end - 1])
            pos = value_end
        entries.append(entry)
        cursor = index
    return entries


def _author_label(raw: str) -> str:
    names = [name.strip() for name in raw.split(" and ")]
    if not names:
        return ""
    if "others" in names:
        names = names[: names.index("others")]
        has_et_al = True
    else:
        has_et_al = len(names) > 6
    shown = names[:3] if has_et_al else names
    formatted: list[str] = []
    for name in shown:
        if "," not in name:
            formatted.append(name)
            continue
        family, given = [part.strip() for part in name.split(",", 1)]
        initials = "".join(f"{token[0]}." for token in re.findall(r"[A-Za-zÀ-ž]+", given))
        formatted.append(f"{family}, {initials}")
    suffix = " et al." if has_et_al else ""
    return "; ".join(formatted) + suffix


def _references_html(bib_path: Path) -> str:
    entries = _bib_entries(bib_path.read_text(encoding="utf-8"))
    rows: list[str] = []
    for number, entry in enumerate(entries, start=1):
        authors = html.escape(_author_label(entry.get("author", "")))
        title = html.escape(entry.get("title", ""))
        journal = html.escape(entry.get("journal", entry.get("archiveprefix", "Preprint")))
        volume = html.escape(entry.get("volume", ""))
        pages = html.escape(entry.get("pages", entry.get("eprint", "")))
        year = html.escape(entry.get("year", ""))
        container = journal
        if volume:
            container += f" <strong>{volume}</strong>"
        if pages:
            container += f", {pages}"
        if year:
            container += f" ({year})"
        doi = entry.get("doi")
        link = f' <a href="https://doi.org/{html.escape(doi)}">doi</a>' if doi else ""
        note = f" {html.escape(entry['note'])}." if entry.get("note") else ""
        rows.append(
            f'<li id="ref-{number}"><span class="ref-authors">{authors}</span> '
            f'<span class="ref-title">{title}.</span> <em>{container}</em>.{note}{link}</li>'
        )
    return '<ol class="references-list">' + "".join(rows) + "</ol>"


def _relative_uri(target: Path, html_path: Path) -> str:
    return (
        Path(target).resolve().relative_to(ROOT).as_posix()
        if html_path.parent == ROOT
        else _relative_path(target, html_path.parent)
    )


def _relative_path(target: Path, base: Path) -> str:
    import os

    return Path(os.path.relpath(target.resolve(), base.resolve())).as_posix()


def _figure_html(number: int, display: str, figures: Path, html_path: Path) -> str:
    del display
    title, legend = FIGURE_COPY[number]
    image = figures / FIGURE_STEMS[number]
    if not image.is_file():
        raise FileNotFoundError(image)
    src = html.escape(_relative_path(image, html_path.parent))
    legend_html = _md(legend)
    return (
        f'<figure class="result-figure figure-{number}">'
        f'<img src="{src}" alt="Figure {number}: {html.escape(title)}">'
        f"<figcaption><strong>Figure {number} | {html.escape(title)}.</strong> "
        f"{legend_html}</figcaption></figure>"
    )


def _table_html(number: int, display: str) -> str:
    title, body = _extract_table(display, number)
    return (
        f'<section class="table-block table-{number}"><h3>Table {number} | '
        f"{html.escape(title)}</h3>{_md(body)}</section>"
    )


PUBLICATION_CSS = r"""
:root { --ink:#17222e; --muted:#66727e; --rule:#cfd7dd; --wash:#f4f7f8;
        --navy:#26577c; --coral:#d95f52; --teal:#3d9487; }
@page { size: A4; margin: 15mm 16mm 17mm 16mm; }
* { box-sizing: border-box; }
html { color: var(--ink); background: #fff; font-family: Arial, "Helvetica Neue", sans-serif; }
body { margin: 0; font-size: 8.2pt; line-height: 1.38; text-rendering: optimizeLegibility; }
a { color: var(--navy); text-decoration: none; }
.cover { display: flex; flex-direction: column; page-break-after: always; break-inside:avoid-page; }
.kicker { margin-top: 4mm; color: var(--coral); font-size: 7.5pt; font-weight: 700;
          text-transform: uppercase; letter-spacing: .12em; }
h1 { font-family: Georgia, "Times New Roman", serif; font-size: 27pt; line-height: 1.03;
     letter-spacing: -.025em; max-width: 165mm; margin: 5mm 0 3mm; font-weight: 600; }
.deck { font-family: Georgia, "Times New Roman", serif; font-size: 11.2pt; line-height: 1.28;
        color: #394550; max-width: 155mm; margin: 0 0 5mm; }
.proof-meta { color: var(--muted); border-top: 1px solid var(--rule); padding-top: 3mm; }
.scope-ribbon { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2mm; margin: 6mm 0 5mm; }
.scope-ribbon div { border-top: 2px solid var(--navy); padding-top: 2.5mm; }
.scope-ribbon strong { display:block; font-size: 15pt; line-height:1; }
.scope-ribbon span { color:var(--muted); font-size:7pt; }
.abstract { border-top: 2px solid var(--ink); padding-top: 3.5mm; }
.abstract h2 { margin:0 0 3mm; font-size:10pt; text-transform:uppercase; letter-spacing:.08em; }
.abstract p { font-family: Georgia, "Times New Roman", serif; font-size: 8.7pt; line-height:1.37;
              margin: 0 0 2.1mm; }
.scope-note { color:var(--muted); font-size:6.5pt; margin-top:3mm; }
.article { column-count: 2; column-gap: 7mm; }
.article > section.prose { break-inside: auto; }
h2 { column-span: none; font-family: Georgia, "Times New Roman", serif; font-size: 13pt;
     line-height:1.15; margin: 5mm 0 2.2mm; break-after: avoid; }
h3 { font-size: 8.3pt; line-height:1.2; margin:3.4mm 0 1.6mm; break-after:avoid; }
p { margin:0 0 2.6mm; text-align: justify; hyphens:auto; orphans:3; widows:3; }
code { font-family: "Cascadia Mono", Consolas, monospace; font-size:.86em; overflow-wrap:anywhere; }
.result-figure, .table-block, .references { column-span: all; break-inside: avoid-page;
                  background:#fff; margin: 7mm 0 5mm; }
.result-figure { break-before: auto; }
.result-figure img { width:100%; max-height: 200mm; object-fit:contain; display:block; }
figcaption { border-top:.55px solid var(--rule); margin-top:2.2mm; padding-top:2mm;
             font-size:6.6pt; line-height:1.35; color:#34404b; }
figcaption p { display:inline; text-align:left; margin:0; }
.table-block { break-before: auto; }
.table-block h3 { font-size:9pt; border-top:2px solid var(--ink); padding-top:2.2mm; }
table { border-collapse: collapse; width:100%; margin:2mm 0; font-size:6.15pt; line-height:1.22; }
th { border-top:1.2px solid var(--ink); border-bottom:.8px solid var(--ink); text-align:left;
     padding:1.2mm 1mm; vertical-align:bottom; }
td { border-bottom:.35px solid var(--rule); padding:1.05mm 1mm; vertical-align:top; }
.table-3 table, .table-4 table { font-size:5.4pt; }
.table-block > p { font-size:6.3pt; text-align:left; color:#43505b; }
.references { break-before: page; column-count:2; column-gap:7mm; }
.references h2 { column-span:all; border-top:2px solid var(--ink); padding-top:3mm; }
.references-list { margin:0; padding-left:4.5mm; font-size:6.2pt; line-height:1.28; }
.references-list li { margin:0 0 1.5mm; padding-left:.6mm; break-inside:avoid; }
.end-note { column-span:all; margin-top:6mm; padding:3mm; background:var(--wash);
            color:var(--muted); font-size:6.2pt; }
"""


CONCEPT_CSS = r"""
@page { size: A4 landscape; margin: 10mm 12mm 10mm 12mm; }
* { box-sizing:border-box; }
html, body { margin:0; color:#17222e; font-family:Arial, "Helvetica Neue", sans-serif; }
.cover { height:185mm; display:flex; flex-direction:column; justify-content:center;
         page-break-after:always; }
.kicker { color:#d95f52; font-size:9pt; font-weight:700; text-transform:uppercase;
          letter-spacing:.12em; }
h1 { font-family:Georgia, "Times New Roman", serif; font-size:31pt; margin:5mm 0; }
.cover p { max-width:190mm; font-size:12pt; line-height:1.45; color:#4a5661; }
.plate { height:185mm; page-break-after:always; display:grid; grid-template-rows:auto 1fr auto; }
.plate:last-child { page-break-after:auto; }
.plate h2 { font-size:13pt; margin:0 0 2mm; }
.plate img { width:100%; height:160mm; object-fit:contain; }
.plate p { margin:1mm 0 0; font-size:7pt; line-height:1.3; color:#65717c;
           border-top:.5px solid #d5dce1; padding-top:1.5mm; }
"""


def _publication_html(
    manuscript_path: Path,
    display_path: Path,
    bib_path: Path,
    data_path: Path,
    release_manifest_path: Path,
    figures: Path,
    html_path: Path,
) -> str:
    manuscript = manuscript_path.read_text(encoding="utf-8")
    display = display_path.read_text(encoding="utf-8")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    release_manifest = json.loads(release_manifest_path.read_text(encoding="utf-8"))
    title, abstract, sections = _sections(manuscript)
    body_sections = [
        (heading, body) for heading, body in sections if not heading.startswith("Appendix")
    ]
    executed = release_manifest["experiment_accounting"]["final_executed_physical_experiment_total"]
    q = data["environment_qualification"]
    derived_sha = data["derived_data_sha256"]
    inserts: dict[str, list[str]] = {
        "3.": [_figure_html(1, display, figures, html_path), _table_html(1, display)],
        "4.": [_figure_html(2, display, figures, html_path), _table_html(2, display)],
        "5.": [_figure_html(3, display, figures, html_path), _table_html(3, display)],
        "6.": [_figure_html(4, display, figures, html_path)],
        "7.": [_figure_html(5, display, figures, html_path), _table_html(4, display)],
        "8.": [_figure_html(6, display, figures, html_path)],
    }
    article_parts: list[str] = []
    for heading, body in body_sections:
        article_parts.append(
            f'<section class="prose"><h2>{html.escape(heading)}</h2>{_md(body)}</section>'
        )
        prefix = heading.split(maxsplit=1)[0]
        article_parts.extend(inserts.get(prefix, []))
    references = _references_html(bib_path)
    abstract_html = _md(abstract)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | publication proof</title><style>{PUBLICATION_CSS}</style></head>
<body>
<header class="cover">
  <div class="kicker">ChemWorld | arXiv v1 publication proof</div>
  <h1>{html.escape(title)}</h1>
  <p class="deck">An executable, chemistry-native apparatus that separates experimental
  success from reproducible experimental behavior.</p>
  <p class="proof-meta">P0 release proof | 2 August 2026 | Frozen evidence and claim audit</p>
  <div class="scope-ribbon">
    <div><strong>{executed:,}</strong><span>executed physical experiments</span></div>
    <div><strong>{q["registered_tasks"]}</strong><span>registered task designs</span></div>
    <div><strong>{q["registered_operations"]}</strong><span>typed operation types</span></div>
    <div><strong>{q["registered_instruments"]}</strong><span>instrument types</span></div>
  </div>
  <section class="abstract"><h2>Abstract</h2>{abstract_html}
    <p class="scope-note">Environment counts qualify the release surface; formal agent
    evidence covers the tasks stated in the manuscript.</p>
  </section>
</header>
<main class="article">{"".join(article_parts)}
  <section class="references"><h2>References</h2>{references}</section>
  <aside class="end-note">This PDF is generated from the frozen paper-data object
  <code>{derived_sha}</code>. Result figures are deterministic SVGs. Image-generated concept
  art is kept in a separate visual-development atlas and is not evidence.</aside>
</main></body></html>"""


def _concept_html(display_path: Path, concepts: Path, html_path: Path) -> str:
    display = display_path.read_text(encoding="utf-8")
    plates: list[str] = []
    for number in range(1, 7):
        title, _legend = _extract_legend(display, number)
        asset = concepts / CONCEPT_STEMS[number]
        if not asset.is_file():
            raise FileNotFoundError(asset)
        src = html.escape(_relative_path(asset, html_path.parent))
        plates.append(
            f'<section class="plate"><h2>Concept {number} | {html.escape(title)}</h2>'
            f'<img src="{src}" alt="Image-generated concept placeholder {number}">'
            "<p>Image-generated composition reference only. Not experimental evidence; "
            "objects and labels are symbolic and require deterministic editorial redraw."
            "</p></section>"
        )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>ChemWorld concept atlas</title><style>{CONCEPT_CSS}</style></head><body>
<header class="cover"><div class="kicker">ChemWorld | visual development</div>
<h1>Concept atlas</h1><p>Six GPT Image 2 concept plates corresponding to the manuscript
display items. These images establish composition and visual language only. The publication
proof uses separately generated, data-bound SVG figures for every scientific result.</p>
<p>Exact prompts and editorial caveats are recorded in
<code>concept-placeholders/README.md</code>.</p></header>{"".join(plates)}</body></html>"""


def _find_chrome(explicit: Path | None) -> Path:
    candidates = [
        explicit,
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate is not None and candidate.is_file():
            return candidate
    raise FileNotFoundError("Chrome or Edge was not found; pass --chrome")


def _print_pdf(chrome: Path, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chemworld-pdf-") as profile:
        command = [
            str(chrome),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--allow-file-access-from-files",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={pdf_path.resolve()}",
            html_path.resolve().as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=180, check=False)
        if result.returncode != 0:
            raise RuntimeError(f"browser PDF export failed: {result.stderr.strip()}")
    for _ in range(50):
        if pdf_path.is_file() and pdf_path.stat().st_size > 0:
            return
        time.sleep(0.1)
    raise FileNotFoundError(pdf_path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path, default=DEFAULT_MANUSCRIPT)
    parser.add_argument("--display-items", type=Path, default=DEFAULT_DISPLAY)
    parser.add_argument("--bibliography", type=Path, default=DEFAULT_BIBLIOGRAPHY)
    parser.add_argument("--derived-data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--release-manifest", type=Path, default=DEFAULT_RELEASE_MANIFEST)
    parser.add_argument("--figures", type=Path, default=DEFAULT_FIGURES)
    parser.add_argument("--concepts", type=Path, default=DEFAULT_CONCEPTS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chrome", type=Path)
    parser.add_argument("--html-only", action="store_true")
    parser.add_argument(
        "--refresh-concept-pdf",
        action="store_true",
        help="re-render the static image-generated concept atlas PDF",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    manuscript = _resolve(args.manuscript)
    display = _resolve(args.display_items)
    bibliography = _resolve(args.bibliography)
    data = _resolve(args.derived_data)
    release_manifest = _resolve(args.release_manifest)
    figures = _resolve(args.figures)
    concepts = _resolve(args.concepts)
    output = _resolve(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    publication_html = output / "experimental-intelligence-v1-publication-proof.html"
    concept_html = output / "experimental-intelligence-v1-concept-atlas.html"
    publication_html.write_text(
        _publication_html(
            manuscript,
            display,
            bibliography,
            data,
            release_manifest,
            figures,
            publication_html,
        ),
        encoding="utf-8",
        newline="\n",
    )
    concept_html.write_text(
        _concept_html(display, concepts, concept_html), encoding="utf-8", newline="\n"
    )
    outputs: list[Path] = [publication_html, concept_html]
    if not args.html_only:
        chrome = _find_chrome(args.chrome)
        publication_pdf = output / "experimental-intelligence-v1-publication-proof.pdf"
        concept_pdf = output / "experimental-intelligence-v1-concept-atlas.pdf"
        _print_pdf(chrome, publication_html, publication_pdf)
        if args.refresh_concept_pdf or not concept_pdf.is_file():
            _print_pdf(chrome, concept_html, concept_pdf)
        outputs.extend([publication_pdf, concept_pdf])
    source_paths = [
        Path(__file__).resolve(),
        ROOT / "paper/tools/render_arxiv_release_figures.py",
        manuscript,
        display,
        bibliography,
        data,
        release_manifest,
        figures.parent / "figure-manifest.json",
        concepts / "README.md",
        *[concepts / CONCEPT_STEMS[number] for number in range(1, 7)],
    ]
    release_payload = json.loads(release_manifest.read_text(encoding="utf-8"))
    publication_ready = release_payload.get("publication_ready") is True
    manifest: dict[str, Any] = {
        "schema_version": "chemworld-publication-proof-manifest-0.1",
        "status": "publication_ready" if publication_ready else "working_proof",
        "publication_ready": publication_ready,
        "sources": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha(path),
            }
            for path in source_paths
        ],
        "outputs": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha(path),
            }
            for path in outputs
        ],
    }
    manifest["manifest_sha256"] = _canonical_sha(manifest)
    manifest_path = output / "publication-proof-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    outputs.append(manifest_path)
    print(
        json.dumps(
            {
                "outputs": [
                    {
                        "path": path.relative_to(ROOT).as_posix(),
                        "bytes": path.stat().st_size,
                        "sha256": _sha(path),
                    }
                    for path in outputs
                ]
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
