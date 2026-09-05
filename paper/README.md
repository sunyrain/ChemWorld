# Papers and current deliverables

| Paper | Canonical sources | Current deliverables |
| --- | --- | --- |
| Work I: programmable chemical worlds | [Manuscript](experimental_intelligence_v1_manuscript.md), [display plan](experimental_intelligence_v1_display_items.md) | [arXiv PDF](exports/experimental-intelligence-v1-arxiv/chemworld-experimental-agency-arxiv.pdf) and source bundles in the same directory |
| Work II: experimental knowledge and decisions | [Long manuscript](prior_discovery_manuscript.md); separately maintained [anonymous submission](iclr2027/submission.md) and [appendix](iclr2027/appendix.md) | [Long PDF](exports/prior-discovery-draft/prior-discovery-draft.pdf), [anonymous PDF](exports/prior-discovery-iclr2027/prior-discovery-iclr2027-anonymous.pdf), [anonymous supplement](exports/prior-discovery-iclr2027/prior-discovery-iclr2027-supplement.zip) |

For Work II, read the [complete story](prior_discovery_story_zh.md), then the
[experiment matrix](../workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md).
The [evidence map](prior_discovery_evidence_map.md) maps claims to bound results; the
[display plan](prior_discovery_display_items.md) owns figure roles. Execution status belongs in
the workstream TODO, and publication checks in the [submission checklist](ICLR_2027_SUBMISSION_CHECKLIST.md).

The current closeout plan restores the four conversion-loss questions and keeps one final B3
interface/tool diagnostic before manuscript integration. The story and experiment matrix describe
that plan. The manuscripts, evidence map, display plan and PDFs still describe the last exported
revision; update them together after the final experiment reaches its recorded endpoint.

## Build from sources

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
