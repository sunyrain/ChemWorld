# Work II DeepSeek resource-calibration cohort v0.1 — experiment note

Status: design frozen before provider execution; development qualification evidence only.

## Question and coverage

Can DeepSeek `deepseek-v4-flash`, using the current production Codex/MCP path already
requalified by W2-39, complete the unchanged W2-26 task-specific resource calibration? Coverage
remains exactly nine task triplets, 27 cells, 252 complete experiments and 135 typed checkpoints:
five A-E tasks at eight experiments, two A-P tasks at ten, and two A-S tasks at twelve. Every
triplet contains `opaque`, `aligned_nominal` and `misindexed_nominal` at world seed 0. No task,
arm, seed, round count, checkpoint plan, measurement or stop rule changes with the provider cohort.

## Measurements and rules

Retain all complete experiments, recipes and exact repeats, attempted and committed operations,
typed checkpoints, final recommendations, lifecycle closeout, exact replay, process time, tokens,
provider time, provider processes and sessions, resource ledgers, and every typed failure. The
existing W2-26 v0.2 pass, failure, missing-infrastructure resume and affected-triplet restart rules
apply unchanged. DeepSeek planning token ceilings scale the retained ten-experiment production
envelope to 28.8M/36M/43.2M input, 480k/600k/720k uncached input, and 128k/160k/192k output for
8/10/12 experiments. These are permissive calibration ceilings, not observed results or formal
resource cards.

## Expected outputs and claim boundary

Produce one isolated DeepSeek execution manifest and authorization, nine DeepSeek runtime configs,
one readable terminal summary with exact denominators and all failures, and nine task-owned resource
cards if all resource-calibration cells complete. Do not mix this cohort with WellAU results. It is
not formal evidence and supports no H1-H4, law-discovery, transfer or model-ranking conclusion.
