# Work II reaction-safety matched-prior D1

Date: 2026-08-11
Status: frozen before provider execution

## Question and tested units

In a fixed reaction-safety world, can one persistent Codex session use autonomous experiments to
form a predictive temperature-duration law, preserve a useful aligned prior, or falsify and revise a
matched but directionally wrong prior?

- Development world: `public-test`, `world_seed=0`; excluded from formal/R5 denominators.
- Three matched cells: opaque, aligned and misspecified semantics, represented by the existing
  internal compatibility IDs. The participant never receives those IDs.
- One WellAU `gpt-5.6-sol`, medium-reasoning Codex session per cell; three cells run concurrently.
- Each cell controls 10 complete experiments operation by operation in one context and one shared
  campaign ledger. No protocol-owned diagnostic experiment is inserted.
- Five frozen belief checkpoints occur at 0, 2, 4, 7 and 10 complete experiments. The final
  recommendation must select one of experiments 1--10 before any evaluator-owned replay.

## Measurements

- 3/3 terminal cells; 30/30 complete experiments; five typed snapshots per cell;
- every operation status, dynamic physical failure, resource rejection, complete/discarded batch,
  exact physical/resource replay and campaign terminal state;
- cumulative input, cache-hit input, uncached input, output, session time, MCP recoveries and provider
  errors, reported separately rather than interpreting cache tokens as repeated output;
- pre/checkpoint/final held-out prediction error, calibration, prior reliability, challenged fields,
  executable-law error, temperature-direction recovery, unique intervention coverage, repeats,
  safety outcomes, selected action and endpoint score.

## Frozen resources and failures

- Physical pattern: eight unique recipes plus at most two participant-chosen exact repeats;
  `145,200 s` process time = eight heat maxima + two repeat maxima + ten quench reserves;
  100 operation attempts and 10 vessel/final-assay slots.
- Provider development envelope per cell: one session, `12,000,000` cumulative input tokens,
  `1,200,000` uncached input tokens, `96,000` output tokens, `6,600 s` session time and `7,200 s`
  method wall time. These are calibration envelopes, not formal caps.
- Up to three recovered MCP failures, one consecutive MCP failure, one provider error event and one
  resource-rejected action are retained and reported. Exceeding them fails operational qualification.
- A legal action that dynamically exceeds the temperature bound is a model-selected safety outcome,
  not a platform failure. Contract mismatch, missing outcome, replay failure or provider/harness crash
  is an operational failure.
- Scientific direction is never an operational pass rule. No correction, harmful updating, unsafe
  exploration and prior persistence are retained results and are never replaced.

## D2 and outputs

The cross-world heterogeneity trigger is already hit before participant execution: four Q2 worlds
favor the lower-temperature side and one favors the higher-temperature side. If D1 reaches terminal
records without a systemic pre-operation infrastructure failure, D2 is therefore pre-authorized for
worlds 1 and 4 irrespective of the D1 effect direction; the D1 outcome cannot add, remove or swap
those worlds.

Expected outputs are an ignored readiness receipt, one ignored three-cell participant run with
30-second liveness events, a tracked machine evaluation and concise analysis. This D1 does not
authorize R5.

## Pre-operation launch audit

The first triplet launch ended in `0.1 s` per cell before any provider session, operation, token or
experiment was created. All three cells hit the same configuration error:
`MethodResourceLimits` rejected the descriptive `resource_status` key that had been placed inside
the executable limit payload. The empty run is retained under the ignored run-1 root and is not a
scientific trajectory.

The correction moves descriptive resource provenance outside `method_resources` and makes the
zero-provider readiness gate instantiate the exact `MethodResourceLimits` payload, so unknown fields
now fail before launch. No experiment design, prior, threshold, world, resource ceiling or D2 rule
changed. The complete triplet restarts as run 2 after a fresh clean-commit readiness receipt.
