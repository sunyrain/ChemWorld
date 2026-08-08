# Work II electrochemical five-seed campaign

Date: 2026-08-08. Status: development five-seed execution; not formal evidence.

Question: Across five fixed electrochemical worlds, do opaque, aligned-nominal and blinded
misindexed-nominal priors produce reproducible differences in experiment selection, prior
revision, law summaries, endpoint outcomes and operational cost when one persistent Codex session
controls a four-experiment campaign?

Coverage: `electrochemical-conversion × 3 prior arms × world_seed={0,1,2,3,4}`. There are 15
independent world-level cells, one WellAU `gpt-5.6-sol` medium session per cell, four complete
experiments and four typed checkpoints per session. Noise identity is paired across the three arms
within each world seed. The participant owns every physical operation. Execution uses exactly three
concurrent OS-isolated cells: the opaque, aligned-nominal and misindexed-nominal arms for one world
seed run together, while world seeds remain sequential. Each cell remains internally sequential;
the three in-flight cells have independent workspaces, sessions, worlds and campaign ledgers. If any
cell fails, the in-flight seed triplet is retained to terminal state and no later world seed starts.

Resources per cell: 28 operation attempts, four vessel starts, four final assays, no non-final
instrument uses, 0.08 mol reagent and 0.16 L solvent. Process time is capped at 72,000 s:
57,600 s for four required maximum-duration electrolysis stages plus one explicitly allowed
14,400 s repeated electrolysis; `electrolyze` is limited to five committed uses. There is no
quench/transfer reserve for this task pattern. Provider caps are one session, 5,400 s wall time,
2.4M cumulative input tokens, 320k uncached input tokens and 24k output tokens.

Measurements: exact operations and transaction status; lifecycle completion/censoring; all public
final-assay metrics; belief reliability, suspected misindexed fields, uncertainty, evidence IDs,
law summary and next intent; campaign physical ledgers; provider tokens/cache/wall time; exact
replay. Every participant operation also carries a bounded public decision audit containing its
expected effect, diagnostic target, expected information gain, supported/not-supported belief
updates, uncertainty and adaptation source. MCP receipts retain tool order, status, start time,
duration, error class and argument/result hashes, but not raw private reasoning or provider payloads.
Arm contrasts remain descriptive until all five paired worlds finish.

Pass/failure: pass only if all 15 cells reach terminal state with four complete experiments, four
valid checkpoints, one session identity, reconciled hard resources and exact replay. Any provider,
checkpoint, process-time, token, ledger or lifecycle failure is retained, stops the remaining
matrix, and is not replaced or rerun for a more favorable result. Coverage and thresholds do not
change after launch.

Expected outputs: redacted trajectories and per-cell/per-seed reports under ignored `runs/`, a
matrix report with exact denominators and failures, and an external 30 s progress/heartbeat JSONL.
Raw provider payloads and credentials are not retained. Evaluator-owned held-out and blind
validation are a subsequent sealed block and do not feed back into participant sessions.
