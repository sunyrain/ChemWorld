# Work II DeepSeek reaction-safety parametric D1

Date: 2026-08-11
Status: frozen before provider execution

## Question and tested units

Can one DeepSeek Codex-compatible campaign session use, test and revise a supplied local
temperature-duration model in the reaction-safety world under the same operation-level MCP,
shared-resource and checkpoint contract as the retained Work II campaigns?

- One development world: `public-test`, `world_seed=0`, excluded from formal denominators.
- Three matched cells: `opaque`, `aligned_nominal` and `misindexed_nominal`.
- One persistent Codex session per cell; four complete experiments share one campaign ledger.
- The aligned reference is `420 K / 7200 s`; the misindexed reference is `340 K / 900 s`, fixed by
  the provider-free 16-recipe screen before this run.

## Measurements

- 3/3 terminal cells, 12/12 experiments, 12/12 typed checkpoints and all operation attempts;
- exact physical/resource replay, validation failures, resource rejections and terminal state;
- input/cached/uncached/output tokens, session time, MCP recoveries and provider errors;
- held-out prediction error, prior reliability and challenged fields, executable-law error, endpoint
  score and paired blind replay.

## Pass and failure rules

- Operational pass requires all three cells to complete four experiments and four checkpoints, pass
  exact replay and the current execution audit, and stay within the frozen task/provider limits.
- No resource rejection is allowed for this task; up to three recovered MCP failures, one consecutive
  MCP failure and one provider-error event per cell remain allowed.
- Scientific direction is not a pass rule. Prior persistence, correction, harmful updating and no
  effect are all retained outcomes.
- A scientific trajectory is never replaced. Only a missing-infrastructure-only failure before the
  first committed operation may use the existing one-resume rule.

## Expected outputs

- one ignored zero-provider readiness receipt and one ignored three-cell participant run;
- one tracked zero-provider evaluator JSON and one concise Markdown analysis;
- a task-specific D1 decision only, with no automatic five-seed expansion.
