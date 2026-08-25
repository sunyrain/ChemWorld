# Work II evidence-to-action oracle v0.4 qualification

Status: frozen final development qualification; provider participant execution is not authorized.

## Question and coverage

Can one fixed outcome-blind tree ensemble predict candidate order from the disjoint provider-free
grid and remain exactly representable in the shared typed-law schema? All 25 completed worlds
exposed through W2-51, v0.2 and v0.3 are construction-only. No incomplete or failed unit is reused
as qualification evidence.

Qualification covers three tasks and the five deterministic new seeds
`185025137, 506689830, 219953397, 879767494, 241995082`: `15` independent task-world clusters.
They are generated as
`100000000 + uint64_be(sha256("work-ii-evidence-to-action-oracle-v0.4-qualification-{i}")[0:8])
mod 900000000`, for `i=1..5`. Future participant/formal seeds
`441035172, 362834953, 806478787, 463638143, 116946577` use the identical `formal-{i}`
derivation and must not be evaluated here.

## Fixed oracle construction

Each cluster executes the registered `16` candidate/checkpoint queries and the same `96`-query
oracle grid (`32` global Halton plus `64` public-candidate-neighborhood queries), with exact replay.
The predictor may read the 96 grid outcomes and public candidate feature locations, but not candidate
outcomes/ranks, checkpoint outcomes, priors or provider output.

Numeric grid features are standardized; categorical features are deterministically one-hot encoded.
One ExtraTrees regressor with `512` trees, `min_samples_leaf=1`, `max_features=1.0`, no bootstrap,
`random_state=20260824` and single-thread fitting predicts every registered metric independently at the
eight candidate locations. These outcome-blind predictions are projected into the existing
conditional-cubic typed-law basis by standardized minimum-norm least squares. Candidate design rank
must equal `8` and maximum absolute reconstruction error must be `<=1e-9`. The typed-law schema,
feature/metric scope and candidate-outcome prohibition are unchanged.

## Measurements and pass/failure rules

Report exact registered/grid truth and replay denominators, provider calls, candidate opportunity
gate, fit/candidate overlap, predictor metadata, design rank, distillation error, Spearman rho,
Top-1 agreement and every failure. Passing requires all `15/15` clusters to pass the existing
candidate gate and oracle `rho >= 0.80`, with rank `8`, distillation error `<=1e-9`, zero candidate
outcomes read, zero fit/candidate overlap, complete exact replay and zero provider calls. Top-1 is
descriptive.

A platform defect restarts the affected block from its first cluster after repair. The first
scientific failure closes v0.4 immediately with all later clusters not started; no seed replacement,
threshold relaxation or selective task removal is allowed. This is the final oracle-development
iteration for the current 96-grid design. Passing qualifies only the oracle method and does not
revive terminal W2-51 or authorize participant/formal execution.

## Expected outputs

One machine-readable summary, one readable summary, retained truth/replay records and complete
predictor/distillation metadata. Raw run data remain outside Git.
