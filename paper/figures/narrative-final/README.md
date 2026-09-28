# Figures for the final bilingual manuscript

These native PowerPoint PDF/PNG exports match the synchronized
[English Word](../../../output/docx/chemworld-ncs-en-authors.docx) and
[Chinese Word](../../../output/docx/chemworld-ncs-zh-authors.docx), with complete
[51-page English](../../../output/pdf/chemworld-ncs-en-authors.pdf) and
[52-page Chinese](../../../output/pdf/chemworld-ncs-zh-authors.pdf) reading PDFs.
The [editable collection](../../../output/pptx/chemworld-ncs-final-figures.pptx)
contains nine slides, ordered 1–6, S5, S4 and S8. Both manuscripts contain all
six main figures and the complete supplement, including S5, S4 and S8.
The [bilingual manuscript entry](../../venues/ncs/README.md) identifies all
current sources, complete files and main-text-only PDFs.

Supplementary numbering follows appearance in the current manuscript. The
budget summary is S4 (asset `figureS7`), the crystallization case is S5 (asset
`figureS4`), supporting outcomes are S6 (source asset `figureS5`), and the
world-level objective comparison is S7 (source asset `figureS6`). Source asset
names and the retained slide order remain stable; current captions and manuscript
cross-references carry the updated numbering.

The source user-edited seven-slide collection is preserved. Its slides 2–7
retain their original XML and artwork. Figure 1 changes only the scope label
to distinguish 240 Sol campaigns across six families and 60 targeted equilibrium
campaigns. The original budget and detailed Sol figures become S4 and S8.
Two quantitative slides replace their main-text positions. The current versions
faithfully reconstruct the user-selected F4-C and F5-B layouts, with the requested
bar-chart substitutions in Figure 4b/c and retained numerical evidence throughout.
The subsequent clarity revision uses three arm-colored boxplots per model in
Figure 5a and removes the batch callouts in 5d.

## Meaning of the new panels

Figure 4a shows the 180 Sol source assays and 12 withheld query means with
world-level sample SD. Figure 4b shows Sol's prior-benefit reversal as bars of
five-world mean MAE, with a logarithmic baseline of 0.001. Figure 4c contains
five horizontal model panels, each showing grouped horizontal bars for both
condition groups and all three arms on the same logarithmic axis, starting at
0.001. The group labels emphasize the lowest concentrations (n=3) and remaining
conditions (n=9), rather than treating three questions as a scientific category.
This retained posthoc partition includes all twelve query conditions and reveals
opposite directions of prior benefit that a single pooled error can obscure.
All 150 world/group values remain
in source-data.json and the supplementary tables. The other nine queries are
not all in-distribution. Panel a error bars are descriptive sample SD, not
confidence intervals.

Figure 5a summarizes all 75 campaigns' minimum positively loaded, actually assayed
nominal concentration in three arm-colored boxplots per model. Each box contains
the five world-specific campaign minima for one information condition. Boxes show
Q1–Q3, middle lines show medians, and whiskers span the minimum and maximum.
Quartiles are calculated on the original concentration scale before display on
the logarithmic axis. Coincident quartiles produce a horizontal line, not an
artificially enlarged box. A dashed line and pooled count row mark 1 mM; there
is no dilute-query shading. All 75 underlying values remain in source-data.json.
Figure 5b shows the actual
12 Sol World 1/Opaque source assays. Figure 5c shows the five Sol/Opaque
most-dilute predictions with their original 80% intervals. Figure 5d connects
all 12 Astra W03/MisIndexed batch observations, the post-experiment K1 account
and the original sealed prediction interval in one right-hand column. Batch
callout text and leader lines are removed; a legend identifies the two physical
traces, and the main text describes the relevant operations. The synchronized
captions explain the panels concisely; Methods retain the statistical and
trajectory-interpretation details.
The Astra case's return to high loading after batch 5 remains visible. Its K1
wording is condensed, not a quotation of contemporaneous internal reasoning.
The source minimum does not imply continuous coverage; 1 mM is a descriptive
threshold rather than a physical boundary. The two successful examples do not
identify the causal effect or necessity of dilute sampling.

Both figures use the user-approved display order: GPT-5.5, GPT-5.6 Luna,
GPT-5.6 Terra, GPT-5.6 Sol, GPT-6 Astra. This is a display order, not a measured
intelligence ranking.

[source-data.json](source-data.json) preserves the plotted cross-model errors,
source minima, Astra batches and original Q08 interval. Exact Sol observations,
query reference means, five-world original intervals and regime errors remain in:

- [EQ_AUTONOMOUS_PROCESS.json](../../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/EQ_AUTONOMOUS_PROCESS.json)
- [STORY_WORLD_ANALYSIS.json](../../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/STORY_WORLD_ANALYSIS.json)
- [joint_cell_metrics.csv](../../../workstreams/flagship_tasks/reports/eq-astra-medium-20260927/joint_cell_metrics.csv)
- [Astra source batches](../../../workstreams/flagship_tasks/reports/eq-astra-medium-20260927/source_batches.csv) and [summary](../../../workstreams/flagship_tasks/reports/eq-astra-medium-20260927/summary.json)
- [Luna, Terra and GPT-5.5 source batches](../../../workstreams/flagship_tasks/reports/eq-three-model-matrix-20260927/source_batches.csv)

This is an editorial use of retained evidence; no agent, simulator or judge was
called. The targeted model comparison remains exploratory development evidence.

## Typography and editability

Text, marks, bars, axes and lines in the two new figures are native editable
PowerPoint objects. They do not recalculate from an embedded Excel workbook.
Only the small researcher/screen illustration in Figure 5d remains a separate
cropped raster object from the selected concept, preserved at its original aspect
ratio. Neither scientific figure is flattened into a bitmap slide.
All figures retain Times New Roman and the common slate/teal/ochre arm palette.
Native text uses 16/18 pt, panel letters 20 pt and panel headings 18 pt.
The Word scales native PDF/PPT dimensions by 0.4564026975, uniformly for all
figures; Figure 2 is 16.6 cm wide and Figure 5 is approximately 16.75 cm wide.
[sizes.json](sizes.json)
records cropped native PDF dimensions in points. Cropping removes external
whitespace only, without stretching or rearranging figure elements.

## Rebuild and export

To rebuild the new figures and merge a candidate collection, choose an absolute
private build directory, copy the current nine-slide collection into it as
`source.pptx`, and run these tools from the repository root, in order:

1. `uv run --no-sync python paper/tools/render_ncs_selected_concepts.py --build <private-build>`
2. `uv run --no-sync <bundled-node> paper/tools/build_ncs_narrative_figures.mjs <private-build>`
3. `uv run --no-sync python paper/tools/package_ncs_selected_concepts.py --build <private-build>`
4. `uv run --no-sync <bundled-node> paper/tools/finalize_ncs_narrative_figures.mjs <private-build>`

Use the bundled Node executable resolved through workspace dependencies. The
package step replaces only the two selected slides and retains the seven other
slide XML parts byte for byte. Pass `--figures figure05` to that step when only
Figure 5 should change, preserving the eight other slide XML parts. The checked nine-slide deck path is
written to `checked-path.txt`; review its native exports before replacing the
delivered collection. Do not overwrite later author edits by rebuilding.

For exports after editing the delivered deck, run
`paper/tools/export_current_figure_ppt.ps1 -Kind narrative`, then
`uv run --no-sync python paper/tools/crop_current_figure_exports.py --kind narrative --output paper/figures/narrative-final`.
The latter accepts `--dependency-path <bundled-python-site-packages>` when
needed for pypdf. It writes the native PDFs to the requested output and leaves
cropped PNGs in the private export directory. The delivered PNGs are the same
native crops, copied here for Word placement. Preserve the common physical
scale when updating Word; its latest prose must not be regenerated from older
Markdown.
