# NCS Article — current reading entry

The current English manuscript is [article.md](article.md). Read its complete
[PDF](../../../output/pdf/chemworld-ncs-en-final.pdf), which includes Methods,
references and supplementary information. Figure sources and rebuild instructions
are in the [figure guide](../../figures/final-ppt/README.md).

Current title: **From experimental autonomy to scientific understanding in
programmable chemical worlds**. The main text follows the approved four-part
Results outline: open experimentation; objectives and resource gains;
cross-regime reversal of correct-prior benefits; and complementary failures to
revise or preserve experimental relationships. The Discussion develops the
prospective connection between experiment choice, competing explanations and
applicability. The 2026-09-26 integration retains the remote four-section Results
and three-paragraph Discussion, with selected effect magnitudes and scope
qualifiers restored after reviewing the compression. The Chinese reading text
follows the same revision.

The related-work update cites 30 works, verified against publisher records and
official proceedings, covering autonomous laboratories, scientific-agent
environments, experimental design and predictive evaluation. The Introduction
explicitly positions ChemWorld alongside PhysGym, BoxingGym and other close
environments. The main text is 2,498 words; the Discussion remains three
paragraphs (281 words). Results, Methods, evidence and figure assets are unchanged.

The bounded closeout sharpens the abstract's within-regime 8.7-fold comparator
and connects Figure 5's source coverage, regime reversal and five-world forecasts.
[Appendix G](applicability_diagnostics.md) decomposes all retained equilibrium
responses and crystallization purity errors; [Appendix H](process_model_details.md)
documents the executed process models and a concrete three-arm input example.
These analyses add no experiments and preserve all campaigns and failures.

The [Chinese main-text translation](article_zh_main.md) is a reading derivative
of this English source, rendered as [a main-text-only PDF](../../../output/pdf/chemworld-ncs-zh-main.pdf).
It translates the title, abstract, Introduction, Results, Discussion, captions
and table, retains the original figure artwork, and omits Methods, the reference
list and supplementary material. Rebuild it with
`uv run --no-sync python paper/tools/build_ncs_chinese_main.py`.
The current reference-expanded export has 11 pages and uses the standard
filename above; the temporary `-references.pdf` export has been retired.

The article uses the shared [protocol](../shared_protocol.md),
[exploratory analysis](../shared_exploratory_analysis.md) and
[metric appendix](../../chemworld_integrated_results_appendix.md), with the
case and prediction details in this directory. The current build has six main
figures and one main table. It is a complete reading draft, not a submitted
journal package; the public archive and author declarations remain pending.

Rebuild the current PDF from the repository root with
`uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs`.
Figures 1–6 and S4 now use native PDF exports of the user's final edited
[seven-slide PPT](../../../output/pptx/chemworld-current-figures-editable.pptx).
The [figure guide](../../figures/final-ppt/README.md) explains how to re-export
that source after further edits. S1–S3, S5 and S6 use the separate
[nine-page supplementary PPT](../../../output/pptx/chemworld-supplementary-figures-editable.pptx).
All editable figure text now follows the Times New Roman/even-point rule, with
20 pt panel letters and 18 pt panel headings; the original artwork and data
are preserved. All figures bind native vector PDF exports. No figure
regeneration is needed for a manuscript PDF build.
Figure 5 now follows the selected remote three-panel bar-chart layout, with
larger Times New Roman text, the established arm colours, actual source
concentration coverage and explicit five-world/SD information. Its editable
source and both reading PDFs are synchronized. Figure 4 retains the current
unconnected difference plots; the user rejected the connected-pair candidates.
The default output is the current PDF linked above. It includes the unified
information-arm colours and the revised prose. The earlier
`chemworld-ncs-en-palette.pdf` contains the preceding prose and is superseded.

Earlier NCS manuscript versions, the Chinese draft and the superseded story
guide are indexed in [the archive](archive/README.md). They are provenance,
not alternative current manuscript sources.
