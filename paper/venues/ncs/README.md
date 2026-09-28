# ChemWorld — current bilingual manuscript

## Current reading and editing files

The English and Chinese manuscripts are synchronized as of **28 September 2026**.
This closeout incorporates the latest Chinese author Word revisions into both
languages, completes the reference list and Appendices A–H, and preserves the
approved six-main-figure narrative. Both languages contain the same evidence,
tables and scientific figures.

Both versions now include the identified ICLR author order: Jiangjie Qiu,
Yijun Li, Yaotian Yang, Honghao Chen, Wentao Li and Xiaonan Wang. The first
three authors share equal contribution; Xiaonan Wang is the corresponding
author. The affiliation and correspondence address follow the ICLR author
records. The user-supplied funding acknowledgement is reproduced verbatim
in English in both complete manuscripts.

The latest editorial revision presents differences in evidence acquisition and
extrapolation across models as findings in their own right. The abstract,
Introduction, Results transitions and Discussion connect predictive outcomes to
distinct research paths. Figure 4/5 captions now concentrate on reading the
panels; subgroup construction, world reuse and limits of trajectory interpretation
are consolidated in Methods and the closing Discussion. The English abstract
remains 212 words, and main-text length is slightly reduced.

The final prose polish keeps the title and abstract unchanged. The Figure 2
transition now explains how successive interventions shape the researcher's
evidence; the repeated equilibrium introduction is removed. Discussion ends
its first paragraph with the concrete generalization question, states the
experiment-selection design implication directly, and condenses the closing
scope statement while locating the single-campaign unit in the cross-model
equilibrium comparison. Authors, funding, artwork and numerical results are
unchanged.

| Version | Complete PDF | Editable Word | Main-text-only PDF |
| --- | --- | --- | --- |
| English | [51 pages](../../../output/pdf/chemworld-ncs-en-authors.pdf) | [English Word](../../../output/docx/chemworld-ncs-en-authors.docx) | [11 pages](../../../output/pdf/chemworld-ncs-en-authors-main.pdf) |
| 中文 | [52 页完整版](../../../output/pdf/chemworld-ncs-zh-authors.pdf) | [中文 Word](../../../output/docx/chemworld-ncs-zh-authors.docx) | [11 页仅正文](../../../output/pdf/chemworld-ncs-zh-authors-main.pdf) |

In both complete PDFs, pages 1–11 contain the abstract, Introduction, Results and
Discussion; pages 12–16 contain Methods, availability text and acknowledgements;
pages 17–18 contain 30 references. Complete supplementary information starts on
page 19. Different supplementary page counts reflect language-dependent layout.
The main-text-only PDFs include the author block but omit Methods,
acknowledgements, references and supplementary information.
The current files use the `authors` suffix because the preceding Chinese Word
and complete PDF were occupied during publication. Earlier `final`, `revised`
and `main` paths are retained and are not the current editing or reading entry
points; use the files in the table above. Superseded Word/PDF copies are now in
the [workspace archive](../../../archive/README.md), with original-path recovery.
The retained English `final.pdf` also remains a legacy build-summary dependency.

The current editable text sources are:

- [English main text and Methods](article.md) and [中文正文及方法](article_zh.md).
- [English supplementary information](supplementary_en.md) and [中文补充材料](supplementary_zh.md), including all Appendices A–H and 34 native tables.
- [Shared bibliography](../../chemworld_integrated_references.bib) and [numeric citation style](numeric-references.csl).

[article_zh_main.md](article_zh_main.md) and [article_zh_methods.md](article_zh_methods.md)
are synchronized section derivatives. Subsequent edits should update the paired
full sources and regenerate Word/PDF files together. If an author edits Word
directly, reconcile those changes into the paired sources before rebuilding.
The prior Chinese Word supplied content for this closeout; the build now uses
Word only as a style reference.

## Retained scientific story

**From experimental autonomy to scientific understanding in programmable chemical worlds**
opens with the opportunities and practical constraints of real self-driving
laboratories. ChemWorld combines flexible experimentation on persistent samples
with independent evaluator control over compatible process laws and supplied
information. Four Results sections connect:

1. The experimental platform to a complete autonomous crystallization history.
2. Research objectives and resources to operational and predictive gains that need not coincide.
3. Shared chemical worlds to distinct evidence-acquisition and extrapolation paths, including prior reversal and two observed routes to accurate prediction.
4. Nearly stable crystal purity to systematic underprediction despite useful recovery forecasts.

The Discussion develops applicability-aware experimental planning as a future
direction. It distinguishes observed predictions and public scientific accounts
from causal explanations that remain to be tested.

The evidence comprises 240 Sol-medium campaigns across six system families and
60 targeted equilibrium campaigns from Luna, Terra, GPT-5.5 and Astra at medium.
Including Sol, the five-model equilibrium comparison contains 75 campaigns.
The targeted comparison retains its exploratory development status. No new
experiments or promotion of evidence status occurred during this editorial closeout.

## Current figure allocation

The [nine-slide editable collection](../../../output/pptx/chemworld-ncs-final-figures.pptx)
and [native exports and source notes](../../figures/narrative-final/README.md)
retain the accepted artwork. Quantitative replacement panels are editable
PowerPoint objects; accepted raster illustrations remain raster objects.

| Figure | Role |
| --- | --- |
| 1 | Experimental freedom, independent evaluator control and study scope |
| 2 | Complete autonomous crystallization history and experimental procedure |
| 3 | Operational outcomes and withheld predictions under different objectives |
| 4 | Sol prior reversal and all five models' condition-specific errors |
| 5 | Actually acquired evidence, the full Astra example and Sol/Opaque extrapolation |
| 6 | Stable purity underprediction and useful recovery forecasts |
| S1 | Complete graphical overview of prior conditions, across four figure pages |
| S2 | Paired prior effects in reaction and equilibrium, across two figure pages |
| S3 | Detailed world–arm budget comparisons |
| S4 | Preserved six-outcome budget summary |
| S5 | Separate crystallization histories, subsequent questions and unperformed thermal test |
| S6 | Supporting outcomes and response-specific baselines |
| S7 | World-level objective comparisons |
| S8 | Preserved detailed Sol source coverage and original forecasts |

Figures 4 and 5 occupy pages 8 and 9 in both languages. Figure 4b/c use bars;
Figure 5a uses three information-arm-colored boxplots per model, each containing
five world-specific campaign minima. Both figures use the approved display order:
GPT-5.5, GPT-5.6 Luna, GPT-5.6 Terra, GPT-5.6 Sol, GPT-6 Astra. This is not an
empirically measured intelligence ranking. Figure 5d has no batch callout lines.

All inserted figures use a common physical scale, **0.4564026975** of the native
PDF/PPT dimensions. Equal source font sizes therefore remain equal in the paper;
figures are not independently stretched to page width. Scientific artwork is
identical in both language versions; prose and captions are translated.

Appendix C.4 covers retrospective equilibrium trace-loading proposals. Figure S5
instead covers a crystallization thermal proposal. Neither proposed experiment
was executed; they are distinct examples.

Supplementary figures are numbered by their appearance in the supplement.
The final numbering changes the former S7/S4/S5/S6 to S4/S5/S6/S7, respectively.
Artwork and asset filenames retain their source identities; all reader-facing
captions and cross-references use the current numbering. The manuscript describes
the targeted comparison through its fixed design, pilots and exploratory analyses;
the execution records retain the original development provenance.

## Evidence and code for collaborator review

The manuscript and supplementary tables are accompanied by these repository
records. These are project-repository entry points, not a claim of public archival
availability or reviewer access.

| Scope | Evidence | Code |
| --- | --- | --- |
| Cross-system study and Sol equilibrium histories | [Integrated evidence](../../../workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921/) and [current artifact bindings](../../../configs/current.json) | [Experiment and analysis scripts](../../../scripts/) |
| Luna, Terra and GPT-5.5 equilibrium matrix | [45-campaign report and linked machine summaries](../../../workstreams/flagship_tasks/reports/eq-three-model-matrix-20260927/REPORT_ZH.md) | [Runner](../../../scripts/run_work_ii_eq_three_model_matrix.py), [analysis](../../../scripts/analyze_work_ii_eq_three_model_matrix.py) |
| Astra equilibrium matrix and joint comparison | [15-campaign report and joint 60-campaign summaries](../../../workstreams/flagship_tasks/reports/eq-astra-medium-20260927/REPORT_ZH.md) | [Runner](../../../scripts/run_work_ii_eq_astra_matrix.py), [analysis](../../../scripts/analyze_work_ii_eq_astra_matrix.py) |
| Retained initial six-session block | [Pilot report](../../../workstreams/flagship_tasks/reports/eq-six-model-comparison-20260927/REPORT_ZH.md) | [Runner](../../../scripts/run_work_ii_eq_six_model_comparison.py), [analysis](../../../scripts/analyze_work_ii_eq_six_model_comparison.py) |
| Current quantitative figures | [Figure source data](../../figures/narrative-final/source-data.json) and [figure notes](../../figures/narrative-final/README.md) | [Figure renderer](../../tools/render_ncs_selected_concepts.py) |

Reports include per-batch exported observations, sealed predictions, public
scientific accounts, reference observations and retained failures. Original
provider payloads, credentials and local run directories are excluded from Git.
Analysis scripts that read those local run directories require the retained
execution files; the exported CSV/JSON and public accounts support inspection
without rerunning a model. Before submission, arrange reviewer access to the
needed execution records and verify the privacy-reviewed archival package.
Keep the manuscript availability statement aligned with that actual access status.

## Rebuild and export

From the repository root, resolve the bundled Python dependency directory using
the desktop workspace dependency tool, then build into a private staging directory:

```powershell
$env:UV_CACHE_DIR = Join-Path $env:TEMP 'chemworld-uv-cache'
$env:PYTHONUTF8 = '1'
$buildDirectory = Join-Path $env:TEMP 'chemworld-bilingual-closeout'
$dependencyPath = 'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages'
uv run --no-sync python paper/tools/build_ncs_bilingual.py --build $buildDirectory --reference output/docx/chemworld-ncs-zh-authors.docx --dependency-path $dependencyPath
& paper/tools/export_ncs_bilingual.ps1 -InputDirectory $buildDirectory -OutputDirectory $buildDirectory
```

The build uses Pandoc and native editable Word tables/equations; PDF export uses
installed Microsoft Word. Inspect rendered pages and verify bilingual values,
citations and figure references before copying checked artifacts into `output`.
Extract main-only PDFs from the actual main-text page span of that build; the
current span is pages 1–11. Do not hard-code that span for future revisions.

The earlier `build_venue_manuscripts.py --venue ncs` is a historical TeX export.
The old Chinese export scripts are packaged with the retired editorial tools in
the [archive](../../../archive/README.md). Those routes do not reproduce the
current bilingual narrative, figure allocation and complete supplement, and must
not overwrite these current artifacts.
The older TeX template and archived reading variants likewise remain provenance,
not competing manuscript sources.

The reading manuscripts are complete; public archiving and final author
declarations remain pending before submission. [Archived versions](archive/README.md)
are retained as provenance.
