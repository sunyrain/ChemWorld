# Final English manuscript figures

## Current editable figure collection

The [editable PowerPoint](../../../output/pptx/chemworld-current-figures-editable.pptx)
now retains the user's seven-slide selection: Figures 1–6 and S4. The user
edited fonts and grouping after the original 17-slide collection was delivered;
those changes are preserved. Do not overwrite this file with the collection
builder, which produces the original 17-slide selection.

Quantitative plots contain editable text, curves, bars and individual markers.
The converted vector plots support editing their graphic objects; they do not
automatically recalculate from an Excel sheet. Reused slides are grouped and
can be ungrouped or edited through PowerPoint's Selection Pane.
Figures 1 and 2 retain original raster artwork. S4 now preserves its selected
four-section layout with 189 native editable objects for text, timelines,
temperature profiles, table cells and numerical marks. Only six small original
illustrations remain cropped images; there is no full-slide background image.
Figure 3 uses consistent quadrant descriptions relative to Optimization versus
Discovery, separates the information-arm legend, and identifies the circled
example in panels c–d. Its data and all retained objects are unchanged.
These notes describe the collection's preparation before the user's final edits.

2026-09-26 manuscript integration: the user's latest saved seven-slide PPT is
the current source for Figures 1–6 and S4. Native PDF exports are in
[`../current-editable/`](../current-editable/) and are bound directly by both
manuscript sources (S4 appears in the full English supplement). Only external
slide whitespace is cropped; internal layout, fonts, colours, values and
illustrations are preserved. The PPT itself is not changed by export. The older
image/vector files described below are provenance, not the current bindings
for these seven figures.

The [supplementary editable PowerPoint](../../../output/pptx/chemworld-supplementary-figures-editable.pptx)
contains nine pages: S1 (four pages), S2 (two pages), S3, S5 and S6. S4 stays
in the user's seven-slide collection. All current manuscript figures now bind
the native PDFs in `current-editable`; S5 retains its three native charts and
their original embedded workbooks.

Current typography follows the user's 2026-09-26 specification: Times New Roman,
ordinary editable text rounded upward to the next even point, panel letters
20 pt and panel headings 18 pt. Existing raster illustrations are preserved.
Text frames and label spacing were adjusted for fit; numerical data, chart
marks and original illustrations were checked against the source. These are
PPT source sizes; manuscript placement scales each figure proportionally.
Manuscript table text already uses Times New Roman at 10 pt.

Re-export after saving changes in the current PPT:

```powershell
./paper/tools/export_current_figure_ppt.ps1
uv run --no-sync python paper/tools/crop_current_figure_exports.py
./paper/tools/export_current_figure_ppt.ps1 -Kind supplementary
uv run --no-sync python paper/tools/crop_current_figure_exports.py --kind supplementary
uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs
uv run --no-sync python paper/tools/build_ncs_chinese_main.py
```

The crop helper uses Pillow and pypdf. If pypdf is supplied by the bundled
document runtime, pass its `Lib/site-packages` directory with
`--dependency-path`; continue running through the repository's locked Python.
The native export requires a registered presentation application on Windows.
Do not rerun the older figure generators or the 17-slide builder over this
user-edited source.

Earlier 2026-09-26 typography follow-up (superseded by the even-point rule above):
all fractional font sizes in the seven-slide
collection were rounded upward to whole points. Adjusted 50 text boxes,
including S4 heading gaps, cell wrapping and Figure 6 label-to-axis spacing.
The installed presentation application reports integer font sizes for all 631
text objects. All scientific text and values are retained, with only whitespace
reflow; non-text geometry and embedded images are unchanged.

To reproduce the earlier 17-slide collection in a separate output, use
`collect_current_figure_vectors.py --build
"$env:TEMP/chemworld-current-figure-collection"`, then
`build_current_figure_collection.mjs`, `package_current_figure_collection.py
--build "$env:TEMP/chemworld-current-figure-collection"`, and
`finalize_current_figure_collection.mjs`, all under `paper/tools`.
That historical finalizer writes `output/pptx/chemworld-figure-collection-17.pptx`;
it no longer overwrites the user-curated seven-slide file.
Use the locked `uv run --no-sync` environment and the bundled Node executable.
The original collection's S5 preserves three embedded workbooks. The current
seven-slide file was validated and rendered in the installed presentation
application, with both changed pages visually checked and the other slides
verified unchanged.

## Manuscript figure history and bindings

2026-09-26 editorial integration: Figure 6 retains the remote black typography,
clean axes and vector/600-dpi exports. Panel b now explicitly labels the count
as forecasts with lower MAE than the source-mean baseline. Numerical data,
information-arm colours and the other five main figure assets are unchanged.
The current English reading export is `output/pdf/chemworld-ncs-en-final.pdf`;
its Results/Discussion revision is also reflected in the Chinese reading text.

2026-09-25 semantic colour alignment: current quantitative main Figures 3, 5
and 6 and Supplementary S1/S2 use the same information-arm colours:
Opaque `#637482`, Aligned `#277F8A`, and MisIndexed `#BC7850`.
Their Python renderers read these values from the existing `palette` in
`style-and-export.json` through `paper/tools/ncs_figure_style.py`.
Goal, budget, feasibility and reference encodings retain their own panel legends.
This colour-only update preserves figure geometry, typography and all values.

2026-09-25 Supplementary S3/S4 fidelity correction: slides 9 and 10 now follow
the actual user-selected references in
`output/imagegen/s3-s4-layout-concepts-20260925/selected/`.
S3 matches the reference coordinates, full arm labels, compact header and
six-panel point layout using native editable shapes. Its 90 paired point
estimates and six means come from retained data; the concept's fictional
geographic labels, numbers and unsupported error bars are not publication data.
S4 preserves the original reference art, gradients, thinking agents, locked
documents and table geometry as a raster graphical layer, with editable
scientific text and numerical corrections. It is not fully vector-editable.
The W05/Aligned histories, sealed forecasts, K2 answers and unexecuted cooling
proposal remain distinct; its evaluator reference belongs only to thermal Q.
Rebuild the two slides with
`uv run --no-sync python paper/tools/rebuild_selected_supplement_figures.py
--output output/pptx/chemworld-figures-s3s4-candidate.pptx`, using the bundled
`python-pptx` package on `PYTHONPATH`; export slides 9/10 from PowerPoint at
4320×5700 and crop to the bounds in `style-and-export.json`, or export individual
slide copies at heights 960 and 1460 design units. Keep width 1440 and scale
uniformly; publication PNGs are 4320×2880 (S3) and 4320×4380 (S4).
For direct PNG exports, set density metadata to 288 dpi without resampling:
PowerPoint can otherwise emit a spurious 3.048-dpi tag that exceeds TeX bounds.

2026-09-25 applicability closeout: the current English and Chinese manuscripts
bind Figure 5 to [the vector PDF](../venue-results/figure05-eq-coverage-reversal.pdf),
with [SVG](../venue-results/figure05-eq-coverage-reversal.svg) and
[PNG](../venue-results/figure05-eq-coverage-reversal.png) alongside it. Panel a
shows all 180 source assays and 60 withheld reference means; panel b connects
the same three-response regime means as Table 1 to all five-world points;
panel c preserves the original most-dilute five-world forecast comparison.
The old single-panel Figure 5 and its PPT slide remain historical assets.
Other main figure bindings are unchanged. Rebuild with
`uv run --no-sync python paper/tools/render_eq_closeout.py`.
[Scope, data and model sources](../../../output/figures/applicability-closeout/README.md).

2026-09-25 approved narrative reconstruction: the English article retains all six
main figure assets and captions, with Figures 1-2 in the open-experimentation
section, Figures 3-4 in the objectives/resources section, Figure 5 and Table 1 in
the cross-regime prior-reversal section, and Figure 6 in the complementary
generalization section. Main Figure 3 uses
[`figure03-goals-paths-forecasts.pdf`](../venue-results/figure03-goals-paths-forecasts.pdf),
the four-panel paired-outcome, original-path and sealed-forecast version. This
binding supersedes the earlier Figure 3 entry below for the current English
article; archived manuscript bindings are unchanged. No artwork or plotted
data were regenerated for this prose reconstruction.

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

2026-09-25 remote figure assets integrated: the retained three-panel EQ
alternative combines regime MAE, interval coverage and the five-world Q08
comparison. Its PDF/SVG/TIFF/PNG and source data remain under
`paper/figures/venue-results/figure05-regime-bars-reference-style.*`, generated by
`uv run --no-sync python paper/tools/render_figure05_regime_bars.py`.
The remote paired-box Figure 4 alternative is also retained as
`figure04-research-envelope-paired-box-compact.*` with its rendering tool.
The current article and released PDF keep the explicit Figure 4/5 bindings
listed above; importing these alternative assets does not change those bindings.

The [current English PDF](../../../output/pdf/chemworld-ncs-en-final.pdf) uses this directory's exports from the [PowerPoint master](../../../output/pptx/chemworld-figures-final.pptx), with the Figure 1, 2, 3, 5 and 6 replacements specified above. The user-designated preserved PDF and v16 case PPT remain unchanged. The separate replacement concept set is not used.

## Placement

| Figure | Purpose | Location |
|---|---|---|
| 1 | Experimental freedom, controlled worlds and original-session assessment | Main Results, open experimentation |
| 2 | One complete W04 twelve-batch crystallization history, B8 procedure and subsequent tests | Main Results, open experimentation |
| 3 | All goal pairs, original research paths, retests and sealed forecasts | Main Results, objectives and resources |
| 4 | Six paired outcomes under larger research envelopes | Main Results, objectives and resources |
| 5 | Source evidence coverage, three-response regime reversal and five-world EQ forecasts | Main Results, cross-regime prior reversal |
| 6 | Purity departure, response-specific value, information conditions and interval coverage | Main Results, preserving and revising relationships |
| Table 1 | EQ regime MAE and interval coverage | Main Results, cross-regime prior reversal |
| S1 | Full prior overview | Appendix A.6 |
| S2 | Reaction prior benefits and full EQ regime comparisons | Appendix A.7 |
| S3 | Complete six-outcome budget comparison | Appendix A.8 |
| S4 | Selected-pair sealed predictions and subsequent reflection | Appendix D.2 |
| S5 | Purification delivery and crystallization size/fines references | Appendix E.1 |
| Tables E1/E2 | Full crystallization baseline errors and purity interval widths | Appendix E.3 |
| Table F1 | All fifteen original EQ intervals and campaign source ranges | Appendix F.1 |

Appendix A.6 now uses four vector pages of source-derived graphical tables,
[`figureS1-prior-graphical-table-1.pdf`](../venue-results/figureS1-prior-graphical-table-1.pdf)
through `-4.pdf`. Each page retains four strata, five worlds per arm, displayed
MAE values and arm means. Appendix A.7 uses the paired-difference figure
[`figureS2-prior-difference-reaction.pdf`](../venue-results/figureS2-prior-difference-reaction.pdf)
and its [equilibrium continuation](../venue-results/figureS2-prior-difference-equilibrium.pdf).
Opaque absolute values are printed beside world labels; only Aligned-Opaque and
MisIndexed-Opaque differences appear on the signed axes. The other-nine and
dilute-three regimes have separate scales. Rebuild these six vector pages with
`uv run --no-sync python paper/tools/render_ncs_prior_graphical.py` before
building the NCS manuscript. The combined PowerPoint deck's older S1/S2 slides
remain historical exports and are not bound into the current NCS PDF.

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
