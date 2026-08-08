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

Resource-accounting amendment before the completed three-arm block: the first opaque attempt
completed all four physical lifecycles but exposed a cap-definition defect. One persistent MCP
turn reported 1,608,946 cumulative input tokens, of which 1,469,952 were cache hits and 138,994
were uncached. The original 480,000 cap incorrectly used short-call semantics. The rerun freezes
separate limits of 2,400,000 cumulative input tokens and 192,000 uncached input tokens; model-call,
output-token, operation, experiment and physical-resource limits are unchanged. The affected block
must restart from the opaque arm.

Second pre-qualification defect found in that rerun: the public material envelope exposed the
internal mode name `anonymous_misindexed_properties`, the temporary workspace path included the arm
name, and observation-noise namespaces differed by arm. Therefore the resulting belief trajectories
are transport/resource shakedown only and cannot support prior-rejection claims. Before the next
full-block rerun, aligned and misindexed arms receive identical public envelope topology and wording,
workspace paths become arm-neutral, and all three arms share the same keyed-noise namespace. The
misindexed attempt also measured 264,302 uncached input tokens, so the predeclared uncached cap is
raised to 320,000 while the 2,400,000 cumulative cap and all physical limits remain unchanged.

Expected outputs: one redacted trajectory and machine-readable summary per arm, one combined pilot
report, and an external progress JSONL. Raw provider payloads and credentials are not retained.
