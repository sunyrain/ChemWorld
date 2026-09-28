# Paper tools

The [bilingual manuscript guide](../venues/ncs/README.md) owns the current reading
and editing paths. Build into a private temporary directory and inspect the result
before replacing a delivered document or user-edited deck.

| Purpose | Entry points |
| --- | --- |
| Current bilingual manuscript | `build_ncs_bilingual.py`, `export_ncs_bilingual.ps1` |
| Current Figures 4/5 | `render_ncs_selected_concepts.py`, `build_ncs_narrative_figures.mjs`, `package_ncs_selected_concepts.py`, `finalize_ncs_narrative_figures.mjs` |
| Export accepted PPT artwork | `export_current_figure_ppt.ps1`, `crop_current_figure_exports.py` |
| Retained figure reconstruction | `render_goal_prediction_panels.py`, `render_ncs_prior_graphical.py`, `render_figure05_readable.py`, `rebuild_selected_supplement_figures.py`, current-collection helpers |
| Work I release | `build_arxiv_release.py`, `finalize_arxiv_release.py` |
| Earlier Work II releases | `build_prior_discovery_draft.py`, `build_prior_discovery_iclr.py`, `build_prior_discovery_supplement.py` |
| Retained integrated ICLR layout | `build_venue_manuscripts.py --venue iclr2027` |

Some retained modules have historical names: `render_figure05_bar_b_overlay_candidate.py`
supplies data to the current renderer, and `render_ncs_narrative_closeout.py` supplies
shared drawing/data helpers. They are dependencies, not redundant alternatives.
`ncs_figure_style.py` reads the retained palette in
`paper/figures/final-ppt/style-and-export.json`.

Superseded Chinese exporters, one-off typography patches and discarded preview
builders are packaged in [the archive](../../archive/README.md). Restore an old
tool together with its original inputs only when reconstructing that historical
version. The historical `build_venue_manuscripts.py --venue ncs` route remains for
its separate TeX layout and must not be used to rebuild the current bilingual edition.
