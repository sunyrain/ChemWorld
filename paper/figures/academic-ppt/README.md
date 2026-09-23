# English manuscript figures

Superseded for manuscript use by the [preserved-artwork correction](../preserved-ppt/README.md). The user rejected the visual redesign of the three generated illustrations. This directory retains the previous reconstruction for comparison.

The editing master is [chemworld-academic-figures.pptx](../../../output/pptx/chemworld-academic-figures.pptx). It contains seven main figures and two supplementary figures, in manuscript order. Text, diagrams and data marks are native editable PowerPoint objects; 31 charts also contain editable data workbooks. The aligned budget comparison uses native lines, points and text so every world/arm row can be edited independently.

The full English article is [chemworld-ncs-en-full.pdf](../../../output/pdf/chemworld-ncs-en-full.pdf), built from [article.md](../../venues/ncs/article.md). Figures are exported **after reopening the finalized PPTX**, then inserted into the article. Publication PNGs are 4,320 pixels wide (about 670 dpi at the manuscript's 164 mm figure width). They are raster exports; the editable master is the PPTX.

## Consistent styling

- White canvas; no overall title inside a figure. Panel letters, conditions, variable names and axis labels remain; full explanations are in manuscript captions.
- Arial throughout: 23 px primary labels, 20 px ticks and secondary labels, 29 px panel letters on a 1,440 px-wide master.
- Opaque: slate `#637482`; Aligned: teal `#277F8A`; MisIndexed: muted ochre `#BC7850`.
- Budget 12: blue `#416B92`; budget 24: teal `#277F8A`. In the budget-change panel, teal and brown instead encode favorable and unfavorable changes, as explicitly keyed there.
- Thin rules and restrained color; no generated crystal artwork, instrument renderings or decorative backgrounds.

## Evidence and interpretation

The figures reuse retained results; no new scientific experiment is run. The numerical inputs preserve all 240 campaigns, all 15 EQ parameter-prior sessions and all 30 crystallization campaigns. Supplementary Figure S2 shows sixteen selected response panels; complete response tables remain in the PDF.

Embedded chart workbooks use twelve significant digits, comfortably beyond the plotted and reported precision. The retained source JSON preserves the full original precision. Workbooks are new chart-data snapshots, not live links to external evidence files.

Sources are the integrated `campaign_metrics.csv` and `analysis.json`, `STORY_WORLD_ANALYSIS.json`, `EQ_AUTONOMOUS_PROCESS.json`, and the retained crystallization `BASELINE_REANALYSIS.json`. The data exporter names the exact local source paths. Figures 4 and 7 use the original `C-W05-B12-E-Aligned.md` and `C-W05-B24-E-Aligned.md` traces under `work-ii-c-formal-20260920-v3-auto`.

Figure 4 distinguishes recorded operations and outcomes from illustrative decision considerations. Figure 7 uses condensed public retrospective answers, distinguishes Q from later K2, and marks the proposed cooling experiment as unexecuted. Its evaluator reference applies to the reheating question, not to the proposed experiment. The case pair is selected retrospectively and does not estimate a population budget effect.

## Rebuild

From the repository root in PowerShell:

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-uv-cache'
$env:PYTHONIOENCODING = 'utf-8'
uv run --no-sync python paper/tools/prepare_academic_figure_data.py
uv run --no-sync 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' paper/tools/build_academic_figure_deck.mjs
uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs --output output/pdf/chemworld-ncs-en-full.pdf
```

The PPT builder uses the installed presentation runtime and finalizer, repairs native chart marker fills before validation, and renders every finalized slide. `CODEX_NODE_MODULES` can override the bundled module directory. Temporary renders and validation receipts stay outside the repository. `style-and-export.json` records the figure crop heights and export scale. The fixed-width slides share one editing canvas; publication exports trim only the unused bottom area.

Validation covers package structure, Arial typography, geometry, chart/workbook value agreement, reopening the final PPTX and visual review of all rendered figures. Native Microsoft PowerPoint is unavailable on this host, so an interactive PowerPoint edit/save/reopen test was not performed.
