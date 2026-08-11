# Work II structural initial-world-model pilot

Date: 2026-08-11
Status: environment screen completed; intervention not admitted to provider execution

## Question and tested units

Can one persistent WellAU `gpt-5.6-sol` medium campaign identify whether a reaction-to-distillation
world is locally reaction-limited or separation-limited, and reject an equally plausible but wrong
dominant-module prior?

- Task: `reaction-to-distillation`.
- Development world: `public-test`, `world_seed=0`; excluded from formal denominators.
- Participant cells: `opaque`, `aligned_structural`, `misspecified_structural`.
- Each cell: one Codex process/session, four complete experiments, one shared within-cell campaign
  ledger and checkpoints before evidence and after experiments 1, 2 and 4.
- All three cells receive `opaque_codes`; only the agent-facing dominant-module hypothesis changes.

## Frozen diagnostic and intervention rule

An evaluator-only provider-free 2 × 2 factorial uses catalyst `0`, solvent `0`, reagent `0.01 mol`
and the existing frozen unregistered controls. Reaction settings are:

- `R_low`: `340 K`, `1800 s`;
- `R_high`: `410 K`, `6000 s`.

Distillation settings are:

- `S_low`: `355 K`, `1200 s`, reflux ratio `0.8`;
- `S_high`: `390 K`, `3300 s`, reflux ratio `4.5`.

Reaction influence is the mean absolute score change from switching `R_low ↔ R_high` at fixed
separation. Separation influence is the corresponding mean absolute change from switching
`S_low ↔ S_high` at fixed reaction. The aligned prior names the larger influence as the dominant
module; the misspecified prior names the other module. Both supplied arms use identical wording,
fields, confidence and scope limits and state that experimental evidence is authoritative.

The intervention qualifies only if all four recipes execute and replay exactly and the two influence
values differ by at least `0.10`. Failure ends this block without changing settings or threshold.

## Measurements and failure rules

Measure initial experiment allocation between reaction and separation controls, evidence acquisition,
checkpoint reliability, held-out prediction error, executable-law error, law/action consistency,
blind recommendation outcome and complete operational denominators. Operational pass requires three
retained terminal cells, four complete experiments and four valid checkpoints per cell, one provider
session per cell, exact replay and no arm/evaluator-truth leakage. Scientific direction is never a
pass criterion. Persisted trajectories are not replaced; only a missing-infrastructure-only failure
before a persisted operation may use the existing single-resume rule.

## Expected outputs

- one four-recipe diagnostic summary with exact denominators and all failures;
- one matched three-arm structural pilot config;
- one terminal summary and trajectory per participant cell plus a combined pilot analysis;
- a go/no-go decision for a five-seed structural extension.

## Environment-screen result

All **4/4** frozen factorial recipes completed and replayed exactly. Reaction influence was
`0.0768558`, separation influence was `0.0465084`, and the absolute influence gap was
`0.0303474 < 0.10`. The intervention therefore failed its prespecified identifiability gate. No
provider call is authorized, and this distillation construction remains a retained negative design
result rather than an agent-capability outcome.
