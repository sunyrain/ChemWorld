# Final English manuscript figures

2026-09-23 Figure 3 redesign (Chinese Figure 2): both NCS manuscripts bind the
four-panel [vector figure](../venue-results/figure03-operation-prediction.pdf).
Five-world retest means and prediction errors establish the electrochemical
contrast; all four joint outcomes retain the reaction-processing boundary;
world-specific counts show the distribution of discordant electrochemical pairs.
The plot preserves all 120 campaigns / 60 pairs and distinguishes world means
from individual pair counts. Captions and Results follow a-d. The older scatter
slide in the combined PPT is superseded for manuscript placement and has not
been regenerated. [Data, scope and rebuild](../../../output/figures/operation-prediction-story/README.md).

2026-09-23 approved Figure 6 replacement: both NCS manuscripts now bind the
four-panel [vector figure](../venue-results/figure06-crystal-generalization.pdf).
It connects purity levels, all-four-response baseline wins, arm/budget-specific
recovery and purity errors, and purity interval coverage. The associated Results
paragraphs and captions follow a-d; Supplementary Tables E1/E2 retain baseline
error magnitudes, nearest-neighbour comparisons and interval widths.
Rebuild this figure with `uv run --no-sync python paper/tools/render_crystal_story_preview.py --publish`.
[SVG](../venue-results/figure06-crystal-generalization.svg) and
[PNG](../venue-results/figure06-crystal-generalization.png) are exported alongside
the PDF. The combined PowerPoint deck's old Figure 6 is superseded for manuscript
placement; it has not been regenerated. The earlier jitter/delta panel is not
the current publication figure. [Data and design notes](../../../output/figures/crystal-story-preview/README.md).

2026-09-23 Figure 2 typography update: main Figure 2 (Chinese Figure 4) now uses
`figure02-research-paths-typography.png` from the separate editable
[`chemworld-figure2-typography.pptx`](../../../output/pptx/chemworld-figure2-typography.pptx).
Large headings and values use regular weight. Panel letters follow the supplied
Figure 1's Arial bold style and relative size. Chart keys, quench semantics and
case limitations live in the manuscript caption, with no slide footer.
All original charts, values, process icons and later K1 accounts are retained.
Rebuild this single figure with `build_final_figure_deck.mjs --case-only`, then
run `paper/tools/export_case_typography.ps1` from the repository root.
The combined deck's earlier slide remains available for comparison.

2026-09-23 Figure 1 override: both NCS manuscripts now use slide 1 of the
user-supplied `FIgure1_2.pptx`, exported separately as
[`figure01-user-ppt.pdf`](../venue-results/figure01-user-ppt.pdf).
The deck's earlier framework slide remains available, but is no longer the
manuscript's Figure 1. [Source and export notes](../venue-results/figure01-user-ppt.README.md).

2026-09-23 reader revision: the approved crystallization research path is now main Fig. 2. EQ uses the approved five-world bar comparison with editable chart data; regime statistics are native manuscript Table 1, and all original intervals remain in Supplementary Table F1. Fig. 6 uses the four-panel replacement described above.

The [final English PDF](../../../output/pdf/chemworld-ncs-en-final.pdf) uses this directory's exports from the [PowerPoint master](../../../output/pptx/chemworld-figures-final.pptx), with the Figure 1, 2, 3 and 6 replacements specified above. The user-designated preserved PDF and v16 case PPT remain unchanged. The separate replacement concept set is not used.

## Placement

| Figure | Purpose | Location |
|---|---|---|
| 1 | Experimental instrument and original-session assessment | Main Results, instrument |
| 2 | Recorded 12/24-batch crystallization paths, operations and retests | Main Results, instrument |
| 3 | Retest gains, prediction errors, joint outcomes and five-world discordance | Main Results, commission comparison |
| 4 | Four paired outcomes under larger research envelopes | Main Results, budget comparison |
| 5 | Five-world withheld EQ reference versus original predictions | Main Results, prior comparison |
| 6 | Purity departure, response-specific value, information conditions and interval coverage | Main Results, generalization |
| Table 1 | EQ regime MAE and interval coverage | Main Results, prior comparison |
| S1 | Full prior overview | Appendix A.6 |
| S2 | Reaction prior benefits and full EQ regime comparisons | Appendix A.7 |
| S3 | Complete six-outcome budget comparison | Appendix A.8 |
| S4 | Selected-pair sealed predictions and subsequent reflection | Appendix D.2 |
| S5 | Purification delivery and crystallization size/fines references | Appendix E.1 |
| Tables E1/E2 | Full crystallization baseline errors and purity interval widths | Appendix E.3 |
| Table F1 | All fifteen original EQ intervals and campaign source ranges | Appendix F.1 |

Full response tables, the study matrix, retained failures and the all-fifteen equilibrium account table remain in Appendices A-C. Main-text captions describe the quantities and comparisons; overall titles are not repeated inside the figures.

## Artwork and data

The deck contains eleven slides and 31 native charts with embedded data workbooks. Statistical charts, labels and numerical panels are editable. Approved illustrations retain raster artwork with editable text overlays; they are not fully editable vector drawings. The original framework, case operation icons and reflection illustration are preserved. The selected case's native progress plots are compacted to two recovery plots with feasibility strips; all 36 observations remain, including failures and the undefined feasible-best value before first success.

Fig. 2 uses the retained v16 batch data and approved v15 artwork that underlies v16. Immediate thoughts are not reconstructed. Its K1 summaries are explicitly later public accounts. S4 keeps Q sealed during K2 and labels the proposed experiment as unexecuted. The reference in S4d belongs to the reheating question, not to the proposed cooling substitution.

Quantitative inputs remain in [retained-figure-data.json](../academic-ppt/retained-figure-data.json) and [the selected-case data](../../../output/figures/research-case-v16/data.json). They derive from existing campaign metrics, baseline reanalysis and the complete retained equilibrium process review. No model, simulator or judge calls are made. Chart workbooks use twelve significant digits; retained inputs keep the original precision.

Arial, black/dark-grey anchoring text, slate/teal/ochre arm colours and blue/teal budget colours are maintained. [style-and-export.json](style-and-export.json) records sizes, colours and crop bounds. Publication PNGs are 4,320 pixels wide. Cropping trims unused canvas only; images are scaled uniformly.

## Rebuild

From the repository root in PowerShell, using the installed presentation runtime and Microsoft PowerPoint:

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-uv-cache'
$env:PYTHONIOENCODING = 'utf-8'
uv run --no-sync 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' paper/tools/build_final_figure_deck.mjs
& paper/tools/export_final_figure_deck.ps1
uv run --no-sync python paper/tools/render_crystal_story_preview.py --publish
uv run --no-sync python paper/tools/render_operation_prediction_story.py
uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs --output output/pdf/chemworld-ncs-en-final.pdf
```

The builder finalizes and checks the PPT package. Native PowerPoint then saves the deck, with unsmoothed charts; the export helper restores outlined failure crosses and left/bottom axis placement. The final PPT is reopened in PowerPoint before all slide PNGs are exported and cropped. EQ value labels use the common font and the observed-range band is aligned to the native chart axes. All error differences and means are calculated from retained observations; no new results are fitted. The manuscript reads those final exports. Temporary builds and review images stay in the system temporary directory.

Final checks cover package readability, native series preservation within 1e-9, Methods preservation, all eleven figure captions, sixteen response-table sections and visual review of every PDF page. Focused Python/JavaScript checks and the PDF citation/glyph/overflow checks pass. This editorial integration does not promote development evidence to formal validation.
