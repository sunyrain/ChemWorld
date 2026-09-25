# NCS Article — current reading entry

The current English manuscript is [article.md](article.md). Read its complete
[PDF](../../../output/pdf/chemworld-ncs-en-final.pdf), which includes Methods,
references and supplementary information. Figure sources and rebuild instructions
are in the [figure guide](../../figures/final-ppt/README.md).

The article uses the shared [protocol](../shared_protocol.md),
[exploratory analysis](../shared_exploratory_analysis.md) and
[metric appendix](../../chemworld_integrated_results_appendix.md), with the
case and prediction details in this directory. The current build has six main
figures and one main table. It is a complete reading draft, not a submitted
journal package; the public archive and author declarations remain pending.

Rebuild the current PDF from the repository root with
`uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs`.
The default NCS output is the PDF linked above.

Earlier NCS manuscript versions, the Chinese draft and the superseded story
guide are indexed in [the archive](archive/README.md). They are provenance,
not alternative current manuscript sources.
