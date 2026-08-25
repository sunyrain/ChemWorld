# Work II evidence-to-action large-grid oracle v1.0 prospective qualification

Status: frozen prospective development qualification; provider participant execution is not
authorized.

## Question and coverage

Does the fixed large-grid oracle that passed the exposed construction screen generalize to all three
tasks on new worlds? All previous W2-51, v0.2-v0.4, defective-partial, and large-grid construction
worlds are exposed and excluded from qualification evidence.

Qualification covers three tasks and the five deterministic new seeds
`799649867, 203573908, 796425860, 539943079, 967945108`: `15` independent task-world clusters.
They were derived before construction execution as
`100000000 + uint64_be(sha256("work-ii-evidence-to-action-large-grid-v1.0-qualification-{i}")[0:8])
mod 900000000`, for `i=1..5`. Future formal-reserved seeds
`863646350, 632064013, 880921191, 307344877, 412084395` use the identical `formal-{i}` derivation
and must not be evaluated here.

## Fixed oracle construction

Each cluster executes the registered `16` candidate/checkpoint queries and `320` oracle-grid queries
(`64` global Halton plus `256` public-candidate-neighborhood queries at span `0.18`) with exact replay.
Exact candidate feature rows are excluded. The fitter may read grid outcomes and candidate feature
locations, but not candidate outcomes, ranks, checkpoint outcomes, priors, or provider output.

Every metric uses the unchanged standardized one-hot ExtraTrees regressor with `512` trees,
`min_samples_leaf=1`, `max_features=1.0`, no bootstrap, and `random_state=20260824`. Predictions at
the eight candidates are distilled through standardized minimum-norm least squares into the existing
conditional-cubic typed-law schema. The artifact retains all `320` fit query IDs as provenance and
cites `128` deterministic evenly spaced IDs in the schema-bounded law summary. Candidate design rank
must be `8` and maximum reconstruction error must be `<=1e-9`.

## Measurements and pass/failure rules

Report exact registered/grid truth and replay denominators, provider calls, candidate opportunity
gate, fit/candidate overlap, candidate-outcome reads, predictor metadata, design rank, distillation
error, Spearman rho, Top-1 agreement, and every failure. Passing requires all `15/15` clusters to pass
the candidate gate and oracle `rho >= 0.80`, with rank `8`, distillation error `<=1e-9`, zero candidate
outcomes read, zero fit/candidate overlap, complete exact replay, and zero provider calls. Top-1 is
descriptive.

A platform defect restarts the affected qualification block from its first cluster in a new run root
after repair. The first scientific failure closes qualification immediately with all later clusters
not started. No seed replacement, threshold relaxation, task removal, or reuse of partial results is
allowed. Passing qualifies only this oracle method and still requires explicit user authorization and
a separate release freeze before participant/formal execution; it does not rewrite original W2-51.

## Expected outputs

One machine-readable summary, one readable report, retained truth/replay records, complete predictor
and distillation metadata, and progress with completed/total queries. Raw run data remain outside Git.
