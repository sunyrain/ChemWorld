# Prior-discovery figure and draft QA

Date: 2026-08-10. Status: development/design draft; not a formal result.

## Figure contract

- Backend: Python/matplotlib only.
- Output size: 182.9 mm wide; schematic-led Figures 1–2 and quantitative-grid Figure 3.
- Editable text: SVG `svg.fonttype=none`; PDF `pdf.fonttype=42`.
- Raster output: 600 dpi PNG and LZW-compressed TIFF.
- Figure 1 claim: a useful endpoint is not sufficient evidence of law discovery.
- Figure 2 claim: matched prior interventions preserve the world-level denominator.
- Figure 3 claim: explicit priors reshape development behavior, but warnings are not selective.

## Data and source binding

- Figure 1 and Figure 2 are frozen design displays; they do not contain participant outcomes.
- Figure 3 uses all retained development rows: 58 paired endpoint rows, 18 warning-rate rows and
  6 execution-denominator rows.
- WellAU/Codex and DeepSeek recovery are provider-isolated; no scientific cross-provider contrast
  is calculated.
- Development source hashes, output hashes and interpretation limits are recorded in
  `figure_manifest.json`.

## Automated QA

- Nature Figure static preflight: 14 PASS, 0 WARN, 0 FAIL.
- Python syntax compilation: passed.
- SVG text-node audit: Figure 1 = 53, Figure 2 = 66, Figure 3 = 118 `<text>` nodes.
- Two consecutive figure-generation passes produced identical hashes for all 12 figure outputs,
  source CSVs and the figure manifest.
- Two consecutive manuscript-build passes produced identical hashes for the PDF, generated TeX and
  build manifest.

## Manuscript-build QA

- PDF: 9 pages, Letter size.
- References: no undefined citations.
- LaTeX errors: none.
- Overfull/underfull boxes: 0/0.
- The PDF is explicitly a development/design draft. Public formal participant results, private
  confirmation and transfer results remain uncollected and are not substituted by development data.

## Visual inspection

Rendered page previews were inspected at reduced page size and the original-resolution PNGs were
inspected for all three figures. No clipping, text overlap, panel-label collision, or provider-ranking
ambiguity remains. Figure 2 and Figure 3 are forced to appear before their corresponding manuscript
sections using explicit float barriers.
