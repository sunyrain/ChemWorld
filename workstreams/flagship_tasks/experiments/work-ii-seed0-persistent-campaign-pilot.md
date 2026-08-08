# Work II seed-0 persistent campaign pilot

Date: 2026-08-08. Status: development pilot; not formal evidence.

Question: Can one WellAU `gpt-5.6-sol` medium Codex process control a complete four-experiment
ChemWorld campaign at operation level, retain scientific context across fresh batches, share one
resource ledger, and commit belief checkpoints under opaque, aligned-nominal and
misindexed-nominal priors?

Coverage: `electrochemical-conversion`, `world_seed=0`, three prior arms, one participant session
per arm, four complete experiments per session. Checkpoints occur before evidence and after 1, 2
and 4 completed experiments. All physical experiment selection belongs to the participant.

Measurements: operation attempts and transaction status; completed/right-censored lifecycles;
campaign-resource state; final-assay metrics and score; provider sessions, tokens, cache and wall
time; structured prior reliability, suspected misindexing, law summary and held-out predictions;
exact replay.

Pass/failure: pass only if all three cells use one session each, complete four lifecycles, commit
all four valid checkpoints, preserve one campaign ledger, and replay exactly. Provider failure,
missing checkpoint, ledger mismatch, unclosed batch or resource-limit termination is retained as a
pilot failure; no arm is replaced or rerun for a more favorable result.

Expected outputs: one redacted trajectory and machine-readable summary per arm, one combined pilot
report, and an external progress JSONL. Raw provider payloads and credentials are not retained.
