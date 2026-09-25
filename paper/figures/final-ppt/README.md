# Final English manuscript figures

2026-09-25 Figure 4 replacement: the main English manuscript now uses the
user-selected six-panel 2×3 layout. The [editable PowerPoint master](../../../output/pptx/chemworld-figures-final.pptx)
contains native text, lines and point marks calculated from
`retained-figure-data.json`; the [publication PNG](figure04-research-envelope.png)
is its export. Generated concept-art dot positions are not used. Panels a-f show electrochemical
discovery and optimization score MAE, partitioning organic-fraction MAE,
crystallization recovery MAE, fines-interval coverage and independent retest
recovery. Each panel pairs 12/24 campaign means with all fifteen true signed
world-arm differences. Vertical offsets only separate the dots; the diamond is
the paired median. The C-W02/Opaque source-assay shortfall stays visible as a
cross. Supplementary S3 retains the detailed world-arm matrix of all six
outcomes. The reference layout is [A2](../../../output/imagegen/figure4-layout-concepts-20260925/A2-six-readouts-2x3-mean-and-swarm.png).

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

2026-09-25 Figure 2 replacement: the main English manuscript binds
[`figure02-research-paths-typography.png`](figure02-research-paths-typography.png),
exported from the mixed-media, source-checked
[`chemworld-figure2-typography.pptx`](../../../output/pptx/chemworld-figure2-typography.pptx).
It follows all twelve formal W04/MisIndexed source batches, every operation call
in selected batch 8, its independent retest, and three evidence-to-next-test
sequences. The reviewed concept's continuous pictorial process and four-column
Agent-question panel use transparent ImageGen illustrations for the ten physical
stages and the writing/thinking Agent. The two source assets are
[`figure02-b-instruments-imagegen.png`](assets/figure02-b-instruments-imagegen.png)
and [`figure02-c-agent-thought-imagegen.png`](assets/figure02-c-agent-thought-imagegen.png).
The generated entities are cropped and uniformly scaled for placement; labels,
arrows, data marks and panel rules remain editable PowerPoint elements. Source assays
and operations are read and checked against the formal summary by
`w04_crystal_case_panel.mjs`; the intermediate 26.6% fines reading is checked
against the local formal trajectory when available. The Agent questions are
author reconstructions, not contemporaneous model quotations. Rebuild with
`node paper/tools/build_final_figure_deck.mjs --case-only`, then run
`paper/tools/export_case_typography.ps1`. Supplementary S4 retains the distinct
W05/Aligned 12/24 pair and its sealed thermal forecasts.

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
| 2 | One complete W04 twelve-batch crystallization history, B8 procedure and subsequent tests | Main Results, instrument |
| 3 | Retest gains, prediction errors, joint outcomes and five-world discordance | Main Results, commission comparison |
| 4 | Six paired outcomes under larger research envelopes | Main Results, budget comparison |
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

The combined deck contains eleven slides and 31 native charts with embedded data workbooks. Statistical charts, labels and numerical panels are editable. Figure 4's fifteen points per panel are native PowerPoint shapes at source-derived horizontal positions. Approved illustrations retain raster artwork with editable text overlays; they are not fully editable vector drawings. Main Figure 2 is exported from its separate PPT. Its instruments and Agent are embedded ImageGen raster assets; charts, labels, arrows and numerical annotations remain editable.

Fig. 2 uses the formally retained W04 summary and a layout adapted from the reviewed ImageGen concept. The old W05 single-case source module remains available for comparison. S4 keeps Q sealed during K2 and labels the proposed experiment as unexecuted. The reference in S4d belongs to the reheating question, not to the proposed cooling substitution.

Other quantitative inputs remain in [retained-figure-data.json](../academic-ppt/retained-figure-data.json) and [the W05 supplementary-case data](../../../output/figures/research-case-v16/data.json). They derive from existing campaign metrics, baseline reanalysis and the complete retained equilibrium process review. No model, simulator or judge calls are made. Chart workbooks use twelve significant digits; retained inputs keep the original precision.

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
