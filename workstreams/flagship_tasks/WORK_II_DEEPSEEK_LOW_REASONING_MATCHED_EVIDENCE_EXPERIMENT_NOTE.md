# Work II W2-60 DeepSeek low-reasoning matched-evidence replication

Status: frozen design; provider execution authorized by the user on 2026-08-31.

## Question and coverage

Does the matched-evidence acquisition--revision--identification profile persist when only the
DeepSeek Codex reasoning effort changes from `high` to `low`? This is a low-reasoning ablation, not
a provider-level `thinking=off` experiment: the latter requires a different direct-controller
harness and would confound reasoning mode with agent interface.

Coverage is fixed to the existing public matched-evidence coordinates. A-P electrochemical uses
5 worlds x 3 arms = 15 formal two-turn sessions. A-S B2 phase-process uses 5 worlds x 3 arms = 15
formal two-turn sessions. Each block has a separate excluded three-session interface canary. Worlds,
arms, packets, prompts, schemas, scoring queries, truth and evaluators are identical to the existing
DeepSeek-high blocks; new sessions never replace or enter those historical denominators.

## Measurements and rules

Both blocks retain pre/post normalized prediction error, arm update gain, the registered
misindexed-minus-aligned world-level contrast, same-thread continuity, schema validity, provider
usage and all failures. A-P also retains wrong-direction rejection and peak-and-collapse response.
B2 retains public structural-summary audit and exact recovery of the registered 1.75 power law.
Results are configuration-stratified; no pooled model or reasoning-superiority test is performed.

A canary tests only interface, two-turn persistence, packet identity, schema and scoring coverage.
Scientific outcomes cannot alter coverage or prompts. A schema/scientific failure is retained
without replacement and stops that block before formal scaling; only a classified zero-action
infrastructure failure may use the existing bounded retry rule. Once a formal block starts, all
15 sessions must reach terminal records under the frozen rules.

## Expected outputs

Ignored run roots retain manifests, canaries, cell records, receipts, progress and machine summaries.
Tracked reports contain aggregate denominators, all failures, the low-versus-high matched descriptive
comparison and paper-facing figure sources. Raw provider payloads, private reasoning and credentials
remain outside Git.
