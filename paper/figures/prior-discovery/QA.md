# Prior-discovery figure and draft QA

Date: 2026-08-10. Status: development/design draft updated through the DeepSeek five-task closeout;
not a formal result.

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
- Figure 3 uses all retained paired development rows for the three five-seed task matrices: 58 paired
  endpoint rows, 18 warning-rate rows and 6 execution-denominator rows. The two additional DeepSeek
  seed-0 gate pilots are bound in the figure manifest and reported in the manuscript closeout table,
  but are not treated as paired scientific contrasts.
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

- PDF: 10 pages, Letter size.
- References: no undefined citations.
- LaTeX errors: none.
- Overfull boxes: 0; underfull boxes: 1 non-blocking paragraph warning.
- The five-task closeout table is a full-width display on page 7; all columns, labels and denominators
  were inspected from a 180 dpi page rendering with no clipping or overlap.
- The persistent-session accounting, harness discussion and Codex/MCP Methods additions were inspected
  on pages 7--9 at 150 dpi; headings, columns and page transitions have no clipping or overlap.
- The evaluator-owned final law-summary contract and Methods description were inspected on pages 4
  and 9 at 150 dpi; the added text preserves column balance and introduces no float or heading drift.
- The PDF is explicitly a development/design draft. Public formal participant results, private
  confirmation and transfer results remain uncollected and are not substituted by development data.

## Visual inspection

Rendered page previews were inspected at reduced page size and the original-resolution PNGs were
inspected for all three figures. No clipping, text overlap, panel-label collision, or provider-ranking
ambiguity remains. Figure 2 and Figure 3 are forced to appear before their corresponding manuscript
sections using explicit float barriers.
