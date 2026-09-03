# Work II W2-61 W2-50 action-aligned causal extension experiment note

Status: prospective development experiment; frozen before provider execution on 2026-09-02.

## Question and fixed coverage

Does access to experimental evidence, an agent-compressed executable law, or the full autonomous
exploration loop improve selection among unseen public ActionPlans relative to the same model with no
evidence, and does the result replicate across DeepSeek V4 Flash and Codex `gpt-5.6-sol`/medium? Each
model has the same 45 W2-50 task-world-prior strata and four scheduled conditions:
`no_evidence`, `yoked_evidence`, `autonomous_exploration`, and `learned_law_only`, for 180 condition
slots per model and 360 total. DeepSeek reuses all 45 read-only W2-50 autonomous records: its 42
completed donors admit learned-law and yoked recipients, while no-evidence is run for all 45 strata
(129 new DeepSeek recipient sessions). Codex uses the same provider-free truth, public ActionPlans,
worlds, priors, resources, and evaluator but creates an independent 45-session autonomous donor
cohort; it then runs 45 no-evidence sessions and learned-law/yoked recipients for every completed
donor (at most 135 recipient sessions). Donor failures and their two donor-dependent slots remain in
the scheduled denominator and are never replaced. Historical W2-54 and W2-59 participant outcomes
are excluded. No oracle condition or new candidate-truth execution is authorized; only the new Codex
autonomous cohort performs physical experiments, with 12 planned experiments per donor.

## Measurements and estimands

The primary outcome is failure-aware normalized regret. Secondary outcomes are selected true rank,
Top-1, selection within 0.01 raw score of the optimum, and pairwise ordering after excluding truth
gaps below 0.01. Within each model, the primary paired contrasts are
autonomous-minus-no-evidence, yoked-minus-no-evidence, learned-law-minus-no-evidence, and
autonomous-minus-yoked; negative regret differences favor the first condition. Cross-model
comparisons use only common strata with complete donors in both cohorts and never substitute a
failure from one model with the other model's record. Report model-specific and common-stratum
denominators, task- and prior-stratified summaries, task-world-cluster bootstrap intervals, all
failures, thread identity, tool events, usage, provider calls, and the Codex physical-experiment
ledger. Candidate outcomes and evaluator ranks remain hidden from every participant context.

## Failure and stop rules

Within each model, strata follow the original manifest order. `no_evidence` is attempted once for
every stratum; `learned_law_only` and `yoked_evidence` are attempted once only after that model's
autonomous donor satisfies the frozen W2-50 completion contract. Participant, provider, schema,
session, resource, or process failures are retained and do not authorize replacement; independent
later sessions continue. A result file or attempt marker is never overwritten, and an interrupted
marked attempt is retained rather than relaunched. A candidate reveal before the terminal turn, a
tool event, a reused condition thread, or source-binding drift stops later calls in that model cohort
as contamination without deleting the other model's records. Poor rankings, model differences, and
unfavorable contrasts are valid scientific results and never stop either cohort. A zero-action
platform defect discovered before the first completed participant record requires retention of that
root and a full cohort restart after repair; it cannot be patched in place.

## Expected outputs

Separate ignored DeepSeek-recipient, Codex-donor, and Codex-recipient roots contain bound inputs,
immutable attempt markers, sanitized receipts, progress JSONL, and model-specific summaries. The
combined machine summary contains all 360 scheduled condition slots. A compact generated closeout
under `workstreams/flagship_tasks/reports/` records exact model-specific/common denominators,
failures, contrasts, resource use, and source hashes for paper integration.

## Platform recovery amendment — frozen before recovery calls on 2026-09-02

The completed recipient cohorts exposed a local yoked-snapshot consumption defect: the provider
compatibility client removed `category_value: null` from unconditional law terms and the shared
runtime validator attempted the same removal again, producing `KeyError('category_value')`. This is
an execution-path defect rather than a participant outcome. All original completed and failed
records remain immutable and are not reclassified or overwritten.

The repair removes only the client-side duplicate normalization. The provider-facing schema and
prompt, shared typed-law validator, four scientific conditions, candidates, truths, thresholds,
evaluator and estimands remain unchanged. Recovery reruns the entire admitted `yoked_evidence`
condition for each model, not selected failed slots: `42` DeepSeek sessions followed serially by
`26` Codex sessions. Each recovery session is attempted once in a new root; all new participant,
provider or platform failures are retained without slot-level retries. The prior yoked results are
reported as platform-incident evidence, while the recovery blocks supply the primary yoked rows in
the combined 360-slot analysis. No tools, truth executions or physical experiments are authorized.
The first admitted session in each model is also the operational canary: recurrence of the repaired
`KeyError('category_value')`, zero-action launch failure or contamination halts later calls for that
model, whereas an unfavorable ranking or an ordinary retained participant failure does not.
