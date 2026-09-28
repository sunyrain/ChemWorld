# Current integrated-study manuscripts

| Track | Current source | Reading PDF |
| --- | --- | --- |
| Bilingual Article | [English](ncs/article.md), [中文](ncs/article_zh.md), [current build guide](ncs/README.md) | [English complete](../../output/pdf/chemworld-ncs-en-authors.pdf), [中文完整](../../output/pdf/chemworld-ncs-zh-authors.pdf) |
| ICLR 2027 | [Anonymous manuscript](iclr2027/manuscript.md) | [Complete ICLR draft](../../output/pdf/chemworld-iclr2027.pdf) |

These are separate versions of the same retained autonomous-study evidence.
The [NCS guide](ncs/README.md) identifies its current figures and supplements;
the shared [protocol](shared_protocol.md) and
[exploratory analysis](shared_exploratory_analysis.md) serve both builds.
The retained TeX-build summaries are in [BUILD_SUMMARY.json](BUILD_SUMMARY.json);
their NCS entry describes an earlier build, not the current bilingual Word/PDF edition.

The older exports and venue-status snapshots are packaged in the
[workspace archive](../../archive/README.md). Historical reports may cite their
original paths; the archive index and Git source commit preserve recovery.
Neither draft has been submitted.

Use the [bilingual build](ncs/README.md#rebuild-and-export) for the current Article.
Use `uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue iclr2027`
for the retained ICLR layout. The legacy `--venue ncs` TeX export does not reproduce
the current bilingual edition. Builds do not run agent or simulator experiments.
