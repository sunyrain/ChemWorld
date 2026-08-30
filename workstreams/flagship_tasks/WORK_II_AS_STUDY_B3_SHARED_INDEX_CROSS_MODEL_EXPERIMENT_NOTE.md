# Work II A-S Study B3 shared-index cross-model replication

Status: terminal canary rejection before formal. DeepSeek completed 2/3 sessions and retained one
participant-schema failure; the ordered stop rule kept the GPT canary and both formal blocks
unstarted.

## Question and coverage

Under an identical B3 science surface and a shared integer action-selection contract, do DeepSeek
`deepseek-v4-flash` (high reasoning) and OpenAI `gpt-5.6-sol` (medium reasoning) show the same
separation between structural-law recovery and unseen action choice? Each provider uses the same
five public worlds, three prior arms, two fresh sessions per arm/world, and two turns per session:
30 formal sessions per provider, 60 total. Each provider first has a disjoint three-session canary
using replicate 1 of the first world. Participant physical experiments are zero.

## Measurements

Pre/post prediction error, mechanism family, exponent error, typed-law consistency, selected action
rank, Top-1, regret, and availability-aware gain are reported per provider and arm. The scoring
roster remains eight fixed unseen queries; each query exposes a zero-based `action_index`, and the
post response selects one `selected_action_index` in 0--7. Provider attempts, completed turns,
same-thread continuity, tool events, elapsed time, usage, and every invalid structured payload are
retained separately from scientific outcomes.

## Pass, failure, and stop rules

Provider-free truth, roster, seeds, arms, replicates, thresholds, and denominators match B3 v0.2.
Because this truth is deterministic and provider-invisible, the GPT preparation reuses the completed
DeepSeek provider-free artifact root only after exact science-contract equality and source-manifest
digest validation; it builds a separate GPT manifest and never reuses participant output.
DeepSeek canary runs first; GPT canary runs only if DeepSeek qualifies. Formal execution starts only
if both canaries complete all three arms with two same-thread turns, valid typed outputs, exactly
eight scoring queries, and a valid novel action index. The two 30-session formal blocks then run
sequentially under the unchanged shared contract. Participant/schema/scientific failures are
retained without replacement; only classified infrastructure failures receive at most two retries.
Any shared schema or runner-semantic change after formal unit 1 ends this protocol version; outcomes
never select worlds, arms, sessions, or replacements. Cross-model contrasts require complete,
separately reported provider denominators and remain clustered by the five worlds.

## Expected outputs

Two versioned prepared roots with provider-free truth, input manifests, static harness checks,
three-session canary records, and, only after both canaries qualify, 30 immutable formal cells per
provider plus machine summaries and a cross-model analysis table.

## Outcome

DeepSeek produced six completed provider turns across three fresh sessions with zero retries, zero
tools, and zero infrastructure failures. Aligned and misindexed sessions completed; opaque retained
a valid action index but returned `pre_submission_complete` on the post turn, so the frozen explicit
stage-status contract rejected the canary as 2/3 completed plus one participant-schema failure.
GPT canary sessions were 0/3 and both formal blocks were 0/30 by the ordered stop rule. No result was
replaced. See `reports/WORK_II_AS_STUDY_B3_SHARED_INDEX_DEEPSEEK_CANARY_CLOSEOUT_ZH.md`.
