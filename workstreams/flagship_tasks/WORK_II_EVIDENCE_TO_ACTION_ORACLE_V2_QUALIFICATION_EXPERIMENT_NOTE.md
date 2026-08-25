# Work II evidence-to-action oracle v0.2 qualification

Status: frozen development qualification; provider participant execution is not authorized.

## Question and coverage

Can an outcome-blind, candidate-location-calibrated oracle retain the existing typed-law interface
while meeting the frozen `rho >= 0.80` candidate-order gate on genuinely new worlds? Construction may
use all previously exposed W2-51 development and formal-preparation worlds, including the retained
`rho=0.738095` failure, but none of those worlds may enter qualification or any future participant
denominator.

Qualification covers the same three tasks and the deterministic fresh world seeds
`762707071, 712842817, 645405595, 416643243, 577005727`: `15` independent task-world clusters. The
future participant worlds `646446568, 184379333, 376407511, 300512245, 721425518` are reserved and
must not be evaluated during this block.

## Fixed oracle construction

Each cluster executes the same registered `16` candidate/checkpoint queries and the same `96`-query
oracle grid (`32` global Halton plus `64` public-candidate-neighborhood queries), with exact replay.
The oracle may read the 96 grid outcomes and the eight public candidate feature locations. It may
not read candidate outcomes, ranks, checkpoint outcomes, prior arms or provider output.

For each metric, the v0.2 oracle obtains an outcome-blind local prediction at every candidate
location from the four nearest grid rows. Numeric coordinates are standardized on the grid,
categorical mismatches use deterministic one-hot Euclidean distance, and neighbors use inverse-
distance weights with stable query-order tie breaking. Those eight local predictions are added as
pseudo-observations with fixed weight `16` to the 96 real grid observations, then distilled into the
existing conditional-cubic ridge typed-law basis. The ridge penalty is selected only from the 96
real grid observations. The output schema, feature/metric scope and candidate-outcome prohibition
remain unchanged.

## Measurements and pass/failure rules

Report exact registered/grid truth and replay denominators, provider calls, candidate opportunity
gate, fit/candidate identifier and feature-row overlap, oracle Spearman rho, Top-1 agreement and all
failures for every scheduled cluster. The block passes only if all `15/15` clusters pass the existing
candidate opportunity gate and oracle `rho >= 0.80`, with zero candidate outcomes read by fitting,
zero fit/candidate overlap, complete exact replay and zero provider calls. Top-1 remains descriptive.

Any platform defect restarts the affected qualification block from its first cluster after repair.
Any scientific gate failure is retained and closes this oracle version without seed replacement,
threshold relaxation or selective task removal. Passing this development block qualifies the
oracle method only; it does not revive the terminal W2-51 result and does not authorize participant
execution on the reserved worlds.

## Expected outputs

One machine-readable qualification summary, one readable summary, retained per-cluster truth and
replay records, candidate-outcome-read count, overlap counts and construction metadata. Raw run data
remain outside Git.
