# Work II evidence-to-action oracle v0.3 qualification

Status: frozen development qualification; provider participant execution is not authorized.

## Question and coverage

Can an outcome-blind local oracle be represented in the shared typed-law schema without the
candidate-order distortion that scientifically rejected v0.2? All 24 completed worlds exposed by
the original W2-51 construction/preparation and v0.2 diagnosis are construction-only. The partial
v0.2 `seed712842817` unit is retained but is neither construction evidence nor reusable truth.

Qualification covers three tasks and five deterministic new seeds
`468887863, 536231621, 739019988, 874364593, 666796452`: `15` independent task-world clusters.
The seeds are the first five values from
`100000000 + uint64_be(sha256("work-ii-evidence-to-action-oracle-v0.3-qualification-{i}")[0:8])
mod 900000000`, for `i=1..5`. Future participant/formal seeds
`784028559, 535572815, 825628705, 803013343, 439555627` use the identical derivation with
`formal-{i}` and must not be evaluated in this block.

## Fixed oracle construction

Each cluster executes the same registered `16` candidate/checkpoint queries and the same `96`-query
oracle grid (`32` global Halton plus `64` public-candidate-neighborhood queries), with exact replay.
The oracle may read the 96 grid outcomes and the eight public candidate feature locations. It may
not read candidate outcomes, ranks, checkpoint outcomes, prior arms or provider output.

For each metric, the oracle predicts the eight candidate locations from the four nearest grid rows
using standardized numeric coordinates, deterministic one-hot categorical distance and inverse-
distance weights. It then projects those eight outcome-blind predictions into the existing
conditional-cubic typed-law basis by standardized minimum-norm least squares. The candidate design
must have rank `8`, and the typed law must reconstruct every local prediction with maximum absolute
error `<=1e-9`. This replaces v0.2's weighted mixture of 96 grid rows and eight pseudo-observations;
the output schema, feature/metric scope and candidate-outcome prohibition do not change.

## Measurements and pass/failure rules

Report exact registered/grid truth and replay denominators, provider calls, candidate opportunity
gate, fit/candidate identifier and feature-row overlap, candidate-design rank, distillation error,
oracle Spearman rho, Top-1 agreement and all failures for every executed cluster. The block passes
only if all `15/15` clusters pass the existing candidate opportunity gate and oracle `rho >= 0.80`,
with rank `8`, distillation error `<=1e-9`, zero candidate outcomes read by fitting, zero
fit/candidate overlap, complete exact replay and zero provider calls. Top-1 remains descriptive.

Any platform defect restarts the affected qualification block from its first cluster after repair.
The first scientific gate failure closes v0.3 immediately; all later clusters remain not started,
without seed replacement, threshold relaxation or selective task removal. Passing this development
block qualifies the oracle method only. It does not revive terminal W2-51 and does not authorize
participant execution on the reserved worlds.

## Expected outputs

One machine-readable qualification summary, one readable summary, retained per-cluster truth and
replay records, candidate-outcome-read count, overlap counts and distillation metadata. Raw run data
remain outside Git.
