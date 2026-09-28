# Papers and current deliverables

Start with the [current bilingual manuscript](venues/ncs/README.md): it identifies
the synchronized English/Chinese sources, complete and main-only PDFs, Word files,
and approved editable figure collection. The `authors` files are the current
reading copies. Earlier `final`, `revised` and `main` filenames are not version selectors.

| Paper | Canonical sources | Current deliverables |
| --- | --- | --- |
| Work I: programmable chemical worlds | [Manuscript](experimental_intelligence_v1_manuscript.md), [display plan](experimental_intelligence_v1_display_items.md) | [arXiv PDF](exports/experimental-intelligence-v1-arxiv/chemworld-experimental-agency-arxiv.pdf) and source bundles in the same directory |
| Work II: experimental knowledge and decisions | [Long manuscript](prior_discovery_manuscript.md); separately maintained [anonymous submission](iclr2027/submission.md) and [appendix](iclr2027/appendix.md) | [Long PDF](exports/prior-discovery-draft/prior-discovery-draft.pdf), [anonymous PDF](exports/prior-discovery-iclr2027/prior-discovery-iclr2027-anonymous.pdf), [anonymous supplement](exports/prior-discovery-iclr2027/prior-discovery-iclr2027-supplement.zip) |
| Integrated autonomous-study Article — current bilingual edition | [English](venues/ncs/article.md), [中文](venues/ncs/article_zh.md), paired supplements and [build guide](venues/ncs/README.md) | [English complete PDF](../output/pdf/chemworld-ncs-en-authors.pdf), [中文完整 PDF](../output/pdf/chemworld-ncs-zh-authors.pdf), [editable figures](../output/pptx/chemworld-ncs-final-figures.pptx) |
| Integrated-study ICLR edition — retained separate layout | [ICLR manuscript](venues/iclr2027/manuscript.md) and [venue guide](venues/README.md) | [ICLR reading PDF](../output/pdf/chemworld-iclr2027.pdf) |

For the retained earlier Work II evidence track, read the [complete story](prior_discovery_story_zh.md), then the
[experiment matrix](../workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md).
The [evidence map](prior_discovery_evidence_map.md) maps claims to bound results; the
[display plan](prior_discovery_display_items.md) owns figure roles. Execution status belongs in
the workstream TODO, and publication checks in the [submission checklist](ICLR_2027_SUBMISSION_CHECKLIST.md).

Both drafts and the anonymous package now include the observation-mapping intervention: 120 original
sessions, 112 valid completions and eight retained failures or interruptions. Eight additional
selected-failure retries are reported separately as a descriptive sensitivity analysis. The four
conversion questions connect conditional structural recovery to its action limits and the observed
M1/M3 successes and boundaries; the historical interface/tool diagnostic remains in the appendix.
Current page counts and completed verification are recorded in the
[submission checklist](ICLR_2027_SUBMISSION_CHECKLIST.md). Experiments and manuscript integration are
complete; the remaining submission steps are author review and OpenReview preparation.

## Build from sources

For the current integrated-study edition, follow the
[bilingual Word/PDF build](venues/ncs/README.md#rebuild-and-export) and
[current figure tools](tools/README.md). The commands below rebuild the separately
retained Work I and earlier Work II releases.

From the repository root, use the locked environment:

```powershell
# Work I
uv run --no-sync python paper/tools/build_arxiv_release.py

# Work II: refresh figures only when their sources or design change
uv run --no-sync python paper/figures/prior-discovery/render_prior_discovery_figures.py
uv run --no-sync python paper/tools/build_prior_discovery_draft.py
uv run --no-sync python paper/tools/build_prior_discovery_iclr.py
```

Edit manuscript Markdown and plot code, then build. Generated TeX, PDFs and source bundles are
outputs; do not edit them to bypass their canonical sources. Review changed figures at manuscript
width and inspect rendered PDFs after layout changes. Builds do not create experimental evidence.

Current Work I figures live in `figures/first-paper-world-instrument-v1/`; Work II figures in
`figures/prior-discovery/`. Retained older figure/proof packages are historical artifacts bound to
their original evidence. They are not alternative current manuscripts or mandatory build steps.
Superseded editorial tools, candidates and document exports are packaged in the
[workspace archive](../archive/README.md), with an original-path recovery index.
Frozen releases and their bound inputs remain at their original paths. Git retains
all prior versions; no history has been rewritten.
