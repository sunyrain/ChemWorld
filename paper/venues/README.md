# Current integrated-study manuscripts

| Track | Current source | Reading PDF |
| --- | --- | --- |
| NCS Article | [English article](ncs/article.md) | [Complete NCS draft](../../output/pdf/chemworld-ncs-en-final.pdf) |
| ICLR 2027 | [Anonymous manuscript](iclr2027/manuscript.md) | [Complete ICLR draft](../../output/pdf/chemworld-iclr2027.pdf) |

These are separate versions of the same retained autonomous-study evidence.
The [NCS guide](ncs/README.md) identifies its current figures and supplements;
the shared [protocol](shared_protocol.md) and
[exploratory analysis](shared_exploratory_analysis.md) serve both builds.
Build summaries are in [BUILD_SUMMARY.json](BUILD_SUMMARY.json).

The older NCS and Chinese exports are in the
[PDF archive](../../output/pdf/archive/README.md). The earlier venue status
overview is [archived](archive/README-20260923.md). Historical reports and
editorial notes may still cite their original paths; the archive index maps
them to the relocated files. Neither draft has been submitted.

Use `uv run --no-sync python paper/tools/build_venue_manuscripts.py --venue ncs`
or `--venue iclr2027` from the repository root. These builds read retained
evidence and do not run new agent or simulator experiments.
