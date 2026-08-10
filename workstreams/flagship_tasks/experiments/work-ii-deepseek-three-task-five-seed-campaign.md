# Work II DeepSeek three-task, five-seed campaign

Date: 2026-08-10. Status: development execution; not formal evidence.

Question: Can one persistent DeepSeek `deepseek-v4-flash` Codex session use the host-owned
ChemWorld MCP to perform operation-level discovery under opaque, aligned-nominal and
misindexed-nominal prior conditions across electrochemical conversion, reaction-to-crystallization
and reaction-to-distillation?

Coverage: three tasks x three prior arms x world seeds 0--4. Each cell contains four
resource-shared complete experiments, four typed belief checkpoints, one persistent Codex session,
and exact replay verification. The three arms of one seed run concurrently; a failed cell is
retained and the affected seed triplet is terminal before later seeds advance.

Measurements: operation attempts and committed operations; complete lifecycles; final metrics;
belief snapshots; campaign stock, process-time, instrument, sample, cost and risk ledgers; provider
usage; session/MCP receipts; failures; and exact replay. Task-specific process caps and repeat,
quench and transfer allowances remain those in the source task cards. The replacement DeepSeek
method envelopes are task-pattern specific: electrochemical 4.0M cumulative input / 400k uncached /
80k output tokens / 7,200 s session wall; crystallization and distillation 5.5M cumulative input /
800k uncached / 80k output / 7,200 s session wall. Physical task-card process-time caps remain
unchanged.

Pass/failure: a pilot or five-seed block passes only when every scheduled cell completes four
experiments and four checkpoints, retains one campaign session, stays within its task envelope,
has no resource rejection, and passes exact replay. Platform repairs require the affected task
block to restart from seed 0 without changing coverage or thresholds. If DeepSeek repeatedly fails
the frozen provider/session contract after bounded diagnosis, the pre-authorized fallback is the
already qualified WellAU task configuration; no mixed-provider scientific denominator is silently
combined.

Platform closeout amendment before replacement execution: the participant must commit its one
final experiment selection through the host-owned `commit_final_recommendation` MCP tool in the
same persistent session, after campaign terminal and the final typed checkpoint. The tool writes an
atomic, idempotent, hash-bound session record and rejects a differing duplicate. Terminal free text
now carries only `status` and `summary`; a legacy nested recommendation is readable for historical
artifacts but does not qualify a new cell. This changes only the unreliable transport of the
participant-owned decision, not the coverage, scientific denominator, selection authority, resource
budgets or pass/failure thresholds.

Closeout completion rule after live validation: for the new host-commit receipt, a normally exited
Codex turn (`status=completed`, `return_code=0`) plus the hash-bound host MCP recommendation is the
authoritative session closeout. The trailing `status`/`summary` message is retained as best-effort
descriptive metadata but is not a scientific datum and is not required when DeepSeek omits it after
the tool commitment. Historical receipts without the host commit continue to require a valid legacy
final payload. The first five-seed attempt exposing this case is retained; the electrochemical task
block restarts from seed 0 after this platform amendment.

Validation-feedback amendment after the replacement block: seed-1 aligned completed all physical
work but made 55 schema-invalid `step` calls, mostly without `expected_step`. MCP 0.6 returned only
the class name `ValueError`, so DeepSeek could not identify the repair and accumulated 8.60M input
and 117,849 output tokens before the otherwise successful closeout. MCP 0.7 returns the existing
bounded validation detail for `step` errors (for example, `expected_step must be an integer`) while
preserving fail-closed CAS and decision-audit requirements; it does not auto-fill or repair an
action. A seed-1 aligned single-cell diagnostic must verify that invalid retries and provider usage
return inside the unchanged frozen envelope before the electrochemical task block restarts from
seed 0.

The required diagnostic passed on 2026-08-10: seed-1 aligned completed 4/4 experiments with 26
operation attempts, 32 MCP calls, zero failed `step` calls, exact replay and host-MCP recommendation
commitment. Usage was 2,216,172 cumulative input (76,396 uncached) and 38,150 output tokens, all
inside the unchanged electrochemical envelope. The replacement five-seed electrochemical block is
therefore authorized to restart from seed 0 under MCP 0.7.

The first MCP-0.7 replacement attempt retained zero failed tool calls but exposed a genuine
task-pattern envelope tail: seed-1 aligned completed 27 valid operations and all closeout checks at
2,966,829 cumulative input and 59,384 output tokens, exceeding only the previous 2.75M input cap.
Before another replacement run, the electrochemical method envelope was revised to 4.0M cumulative
input, 400k uncached input, 80k output and 7,200 s session wall. This amendment does not change the
28-attempt physical budget, four-experiment denominator, repeat allowance, process-time card,
coverage, seeds or scientific pass/failure criteria; the affected task block restarts from seed 0.

The final MCP-0.7 electrochemical replacement block reached a protocol-valid terminal result at
11/15 qualified cells. Seed-3 misindexed completed all four experiments, checkpoints, host-MCP
recommendation and exact replay, but its attempt to add 0.06 L of solvent exceeded the remaining
campaign stock and produced one `campaign_resource_rejected` event; the frozen
`no_resource_rejection` check therefore failed and seed 4 was not started. This is retained as agent
resource-allocation behavior, not repaired or replaced as a platform failure.

Post-run audit amendment before the next crystallization replacement: the crystallization
`floatfix-v3` block reached 11/15 cells before `seed-3 / opaque` was rejected by the independent
resource replay audit. The participant trajectory itself completed four experiments, four typed
checkpoints, final recommendation commitment and physical exact replay with no resource rejection.
The retained action used the public/runtime alias `amount_mol` for `add_catalyst`; the live action
codec canonicalized it to `catalyst_amount_mol` before updating the authoritative campaign ledger,
whereas the replay auditor reconstructed the event from the raw alias. This created a replay-only
resource hash/state mismatch from step 3 onward. The replay path now applies the same action codec
before resource reconstruction and has a focused regression test for this alias. Because the
resource audit is part of the frozen qualification gate, the affected crystallization block is
restarted from seed 0 without changing coverage, budgets, estimands or pass/failure rules. The
retained `floatfix-v3` artifacts remain historical development evidence and are not silently
reclassified as a passed block.

The first post-readiness seed-0 pilot was infrastructure-right-censored before any complete
experiment. It was launched under a short outer command timeout; when that launcher closed stdout,
the parent and child progress `print` calls raised Windows `OSError 22`, interrupting two cells after
three recorded operations and preventing the third summary from closing. The partial trajectories,
receipts and incomplete usage accounting are retained and excluded from scientific denominators.
Progress JSONL is now authoritative and console output best-effort at both runner levels; parent
exceptions also terminate and explicitly reap every active child. Subsequent provider runs must be
started as detached background processes with stdout/stderr redirected outside the repository and
monitored only through the independent progress JSONL. The affected pilot requires a fresh clean-
commit readiness receipt before another seed-0 triplet may start.

The first DeepSeek crystallization pilot exposed the analogous task-pattern tail: seed-0
misindexed completed all physical and closeout checks with no resource rejection, but reached
5,599,410 cumulative input tokens against the previous 5.5M cap. Before replacement execution,
crystallization and distillation envelopes were revised to 7.0M cumulative input, 1.0M uncached
input, 100k output and 9,000 s session wall. This is an operational envelope amendment only; the
physical budgets, repeat/quench/transfer allowances, coverage, seeds and scientific qualification
rules remain frozen. The crystallization pilot restarts from seed 0.

The replacement crystallization seed-0 pilot passed 3/3 cells and 12/12 experiments with zero
resource rejections, exact replay and one host-MCP recommendation per cell. Maximum observed usage
was 5,605,523 cumulative input, 142,227 uncached input and 45,356 output tokens, inside the revised
7.0M / 1.0M / 100k envelope. The crystallization five-seed block is therefore authorized to start
from seed 0.

The first crystallization five-seed block reached 14/15 cells before seed-4 aligned exposed a
platform floating-point boundary defect: a 14,400 s cooling operation was reported as
14,400.000000000004 s and rejected against an exact 14,400.0 s reservation. The resource ledger now
uses a fixed 1e-9 absolute tolerance for stock/process-time machine tails while retaining failure
for a 2e-6 true overage. The retained failed block is not reinterpreted; crystallization restarts
from seed 0 after this repair.

Expected outputs: one machine-readable report per task, external heartbeat JSONL, concise combined
summary, and retained per-cell trajectories under `runs/development/`. Credentials, raw provider
payloads and private reasoning are not committed.

Provider qualification basis: the retained DeepSeek qualification-v2 seed-0 opaque
electrochemical cell completed four experiments, four typed checkpoints and exact replay in one
session with zero provider errors. The production catalog must keep `supports_search_tool=false`
so the domain MCP is exposed deterministically.
