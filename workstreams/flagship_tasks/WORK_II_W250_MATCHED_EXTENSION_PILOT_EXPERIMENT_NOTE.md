# Work II W2-50 matched-extension three-session pilot experiment note

Status: development pilot; frozen before provider execution on 2026-08-25.

## Question and fixed coverage

Can the existing W2-50 autonomous record be reused as a read-only donor for the three non-oracle
counterfactual conditions without hidden candidate outcomes, ranks, donor reasoning, or resource
state crossing conditions? The donor is the first cell in the frozen W2-50 input manifest:
`A_S_MULTI_TASK_OAD--electrochemical-conversion--seed0--opaque`. Its existing autonomous session is
not rerun. The pilot adds exactly one fresh DeepSeek V4 Flash session for each of `no_evidence`,
`learned_law_only`, and `yoked_evidence`, in that order. The yoked condition is one persistent
session with five belief-checkpoint turns and one terminal-ranking turn. No new physical or truth
execution is authorized.

## Measurements

Retain provider status, fresh thread identity, tool-event count, usage, all schema-valid belief
snapshots, terminal ranking, selected candidate, Top-1, within-0.01, raw and normalized regret, and
near-tie-aware pairwise ordering. Bind the donor summary and trajectory, the extracted public
action/observation packet, and the final typed-law artifact. Report the existing autonomous result
beside the three new conditions, but do not pool this single stratum into an arm-level claim.

## Failure and stop rules

The donor must remain `completed_uncontaminated` with 12 committed final assays, one committed final
typed law, and a complete eight-candidate terminal ranking. Candidate outcomes and evaluator ranks
must remain absent from all provider contexts. Yoked checkpoints cannot reveal the candidate packet
before the terminal turn; learned-law-only cannot receive donor evidence or reasoning. Any provider,
schema, tool-contamination, or reveal-gate failure is retained and stops later pilot calls. A poor
ranking or unfavorable regret is a valid scientific result and does not stop or authorize a rerun.
Existing or partial records are never overwritten.

## Expected outputs

The ignored development root `runs/development/w2-50-matched-extension-pilot-20260825/` contains the
materialized input bundle, progress JSONL, sanitized provider-turn records, one result per attempted
condition, and a machine-readable summary with exact session, turn, provider-call, and zero-physical
experiment denominators.
