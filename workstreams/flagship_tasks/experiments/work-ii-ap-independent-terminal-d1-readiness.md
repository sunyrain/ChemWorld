# Work II independent A-P terminal D1 readiness

Status: development provider execution authorized; formal/R5 execution remains unauthorized.

## Question and coverage

Can a new A-P terminal D1 triplet be configured from a five-world Q2 pass without selecting on
participant outcomes or replacing any historical failed/confounded D1? For each task, the frozen
deterministic rule selects the numerically smallest Q2-passed world seed absent from the semantic scan
of tracked participant reports. Exposure means matching task ID, integer world seed and a positive
participant-provider-session denominator; schema versions, hashes, participant results and Q2 effect
sizes are ignored.

Each eligible block has one previously unexposed world, three frozen arms, ten autonomous complete
experiments per arm and checkpoints at `0/2/4/7/10`. It receives a new pilot ID and observation-noise
namespace. This is C2 terminal-admission preparation, not a W2-26 prerequisite.

## Measurements and rules

- Verify that every selectable world is a unique passing row in the task's provider-free Q2 package.
- Discover historical participant exposure directly from tracked reports and expose every matched path,
  seed and provider-session denominator in the readable output.
- Form the eligible set as `Q2-passed seeds - participant-exposed seeds`; select its minimum, or fail
  closed without a config when that set is empty.
- Preserve all historical results; scientific effect direction and magnitude are not readiness or
  later operational-admission rules.
- Generated configs must retain three arms, ten experiments, five checkpoints and remain explicitly
  provider/R5 blocked.

## Expected outputs

One machine-readable readiness summary and static configs only for eligible tasks. A blocked task has
no generated config. No provider call, participant outcome or terminal admission is produced here.

## Development execution handoff

The two ready seed-2 rows deterministically generate separate development execution configs. This
handoff only fills the runner's resource, recovery and write-once lifecycle fields; it does not
change the selected worlds, priors, measurements, rounds or scientific pass rules. It does unify
runtime failure retention and lifecycle semantics. A synthetic zero-provider three-cell/ten-round
evaluator shakedown must pass for both tasks before provider authorization.

Provider execution then requires one explicit user authorization naming the exact two task blocks,
their output roots, six initial provider sessions, 60 complete experiments, explicit credential-use
authorization and either a positive USD ceiling or explicit unlimited-spend authorization. Development execution remains non-formal and cannot be
used for R5 or C2 admission without its terminal reports and the later common release freeze.

On 2026-08-13 the user authorized unlimited provider spend and fixed the development execution
order to DeepSeek `deepseek-v4-flash` first, followed only after terminal retention by WellAU
`gpt-5.6-sol`. Each provider block independently contains the same two seed-2 tasks, three prior
arms, ten complete experiments and five belief checkpoints. The hard two-attempt-per-cell
infrastructure rule remains in force despite unlimited spend; scientific failures are retained and
never retried for a more favorable outcome. Existing provider credentials were explicitly
authorized for use; no credential material or raw provider response enters Git.
