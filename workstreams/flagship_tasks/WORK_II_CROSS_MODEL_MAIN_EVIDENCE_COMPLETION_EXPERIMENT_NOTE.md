# Work II W2-59 cross-model main-evidence completion

Status: frozen design; participant execution authorized by the user on 2026-08-31. Provider
canaries must qualify before each corresponding formal block scales.

## Question and fixed coverage

Do the participant-bearing results that support the current Paper 2 capability chain persist when
the same public worlds, prior arms, evidence packets, measurements and evaluator semantics are run
with both DeepSeek `deepseek-v4-flash`/high and OpenAI `gpt-5.6-sol`/medium?

The missing participant denominators are fixed as follows.

- Public C2 OpenAI replication: 45 task--world clusters, three prior arms, 135 persistent sessions
  and 1,260 complete physical experiments. The first A-E electrochemical world triplet is an
  in-denominator operational canary.
- Matched evidence OpenAI replication: A-P electrochemical 5 worlds x 3 arms = 15 formal two-turn
  sessions, and A-S B2 phase-process 5 worlds x 3 arms = 15 formal two-turn sessions. Each block
  has a separate three-session canary excluded from its formal denominator and no participant
  physical experiments.
- W2-50 OpenAI replication: 3 tasks x 5 worlds x 3 arms = 45 persistent sessions and 540 complete
  physical experiments. The first electrochemical world triplet is an in-denominator operational
  canary.
- B3 paired successor: 5 worlds x 3 arms x 2 fresh sessions for each provider, giving 30 DeepSeek
  and 30 OpenAI formal two-turn sessions. Each provider has an excluded three-session canary; both
  canaries must qualify before either formal provider block scales. There are no participant
  physical experiments.

Provider-free W2-51/W2-52/W2-53 controls are model-independent and are not duplicated. W2-55 is
recomputed on the new C2/W2-50 outputs without new provider calls. The earlier 60-cell static
material-information study already contains OpenAI/Codex evidence and remains an exploratory
predecessor rather than a missing OpenAI denominator.

## Measurements

Each successor retains its source block's registered measurements and denominators. C2 retains
search trajectories, physical-resource accounting, belief checkpoints, prediction error, typed-law
fidelity, blind action and all failures. Matched evidence retains pre/post prediction error, update
gain, structural recovery, same-thread continuity and exact query/metric counts. W2-50 retains
complete ActionPlan binding, Top-1, rank, regret, law error, truth and exact replay. B3 retains
family/exponent recovery, typed-law predictions, selected unseen action, regret, action opportunity,
same-thread continuity and provider usage.

Cross-provider reporting is block-specific. It reports provider-stratified estimates and matched
differences on the same registered task--world units; it does not pool heterogeneous blocks into a
single model leaderboard.

## Qualification, failure and stop rules

- Deterministic configuration materialization, the production runner, real task/world compiler,
  raw writer and production validator must pass provider-free checks before a provider canary.
- A canary checks interface, persistence, tool/action execution, schema, resource/replay and public
  packet identity only. Canary scientific outcomes never change coverage, thresholds or prompts.
- C2 and W2-50 canary triplets remain in their formal denominators. Matched-evidence and B3 canaries
  are excluded and use separate fresh sessions.
- Participant/schema/scientific failures and valid resource exhaustion are retained without
  replacement. Only a classified zero-action infrastructure failure may use the source block's
  bounded retry/resume rule.
- A participant-visible runner, schema, task, physics, resource, prompt or hidden-information defect
  after a formal block starts requires that affected formal block to restart from its first unit;
  downstream-only analysis defects are recomputed without provider calls.
- No old W2-56/W2-57/W2-58 or DeepSeek C2/W2-50 result is overwritten or spliced into a successor
  denominator. A provider block that fails its canary is retained and stops before formal scaling.

## Expected outputs

Ignored run roots contain the exact generated runtime configs, input manifests, raw/sanitized cell
records, provider receipts, progress, truth/replay, resource ledgers and readable machine summaries
with exact denominators and all failures. Tracked reports contain only bounded aggregate results and
paper-facing analyses; raw provider payloads and credentials remain outside Git.
