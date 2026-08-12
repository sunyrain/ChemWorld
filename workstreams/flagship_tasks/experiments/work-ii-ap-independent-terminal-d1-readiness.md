# Work II independent A-P terminal D1 readiness

Status: provider-free design gate; provider execution is not authorized.

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
