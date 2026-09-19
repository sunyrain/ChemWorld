# RX P/S five-world dual-goal block — W01/W02 interim complete reports

Date: 2026-09-19. Status: development evidence; W01 and W02 are complete, while the
full 60-task block remains incomplete and truth-embargoed.

This directory contains the readable pre-truth reports for the first two RX worlds:

- 24/24 task combinations in W01/W02;
- 288/288 source experiments in W01/W02 (12 per task);
- 72/72 sealed posttests in W01/W02 (K1, Q, and K2 per task);
- P and S loci;
- mechanism-discovery and safety-constrained-optimization goals;
- Opaque, Aligned, and MisIndexed arms.

Each task report contains the complete twelve-experiment campaign, all submitted
actions and observed metrics, the sealed recommendation, the full K1 report, all
twelve Q predictions with 80% intervals, the full seven-part K2 retrospective, and
posttest validation metadata.

Raw provider streams, credentials, thread identifiers, token accounting, ignored run
directories, and machine payload JSON are intentionally excluded from Git. They remain
preserved in the write-once server run and in the separately delivered local report
package. Reference truth, prediction scores, and recommendation retests are not present:
the runner may generate them only after all 60 effective K2 chains are sealed.

Start with [W01](RX-W01/WORLD_INDEX.md) or [W02](RX-W02/WORLD_INDEX.md).
