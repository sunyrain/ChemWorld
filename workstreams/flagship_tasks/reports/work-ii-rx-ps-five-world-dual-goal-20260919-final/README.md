# RX P/S five-world dual-goal block — final 60-cell reports

Date: 2026-09-19. Status: complete development evidence.

This write-once package contains the complete sanitized result surface for the frozen RX P/S block:

- 60/60 task cells across five worlds, P/S loci, two goals, and three prior arms;
- 720/720 source experiments (12 per cell);
- 180/180 valid sealed posttests (K1, Q, K2);
- 600/600 provider-free reference executions (five repeats for each of 12 queries in each world/locus);
- 60/60 independent recommendation retests;
- complete experiment actions and observations, recommendations, K1 reports, Q predictions and rationales, K2 retrospectives, prediction evaluations, released reference truth, and retest comparisons.

Each cell contains a readable `EXPERIMENT_REPORT.md` and an explicitly whitelisted `RESULT.json`. Raw provider streams, credentials, provider stderr, thread identifiers, token accounting, and ignored run directories are excluded.

The original transport failures and all recovery evidence remain preserved in the server run; effective results are selected without overwriting the retained failures. See the [v11 recovery record](../../WORK_II_RX_PS_FIVE_WORLD_DUAL_GOAL_RECOVERY_V11.md).

World indices: [RX-W01](RX-W01/WORLD_INDEX.md), [RX-W02](RX-W02/WORLD_INDEX.md), [RX-W03](RX-W03/WORLD_INDEX.md), [RX-W04](RX-W04/WORLD_INDEX.md), [RX-W05](RX-W05/WORLD_INDEX.md).

Aggregate interpretation: [REPORT.md](REPORT.md). Machine-readable aggregate: [SUMMARY.json](SUMMARY.json).
