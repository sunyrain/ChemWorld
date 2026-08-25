# Work II evidence-to-action large-grid oracle v1.0 construction screen

Status: frozen development construction screen; no prospective qualification or provider execution
is authorized by this note.

## Question and coverage

Does increasing the outcome-blind oracle grid from `32 global + 64 candidate-neighborhood = 96`
to `64 global + 256 candidate-neighborhood = 320` queries per task-world repair the known ranking
failures without making a previously low-margin task fail? The predictor remains the fixed v0.4
ExtraTrees model so this screen isolates grid coverage rather than changing two design dimensions.

The screen contains seven already exposed construction-only units: the four retained oracle failures
`electrochemical/seed762707071`, `electrochemical/seed241995082`,
`reaction-to-crystallization/seed836245547`, and
`reaction-to-crystallization/seed468887863`, plus the low-margin exposed controls
`electrochemical/seed2`, `reaction-to-crystallization/seed2`, and
`reaction-safety-constrained/seed3`. Their known outcomes are permitted only for construction
diagnosis and can never become qualification or participant evidence.

Five future prospective qualification seeds are frozen as
`799649867, 203573908, 796425860, 539943079, 967945108`; five distinct formal-reserved seeds are
`863646350, 632064013, 880921191, 307344877, 412084395`. Neither set may be evaluated in this
construction screen.

## Fixed construction

Each unit executes `320` grid queries and the registered `16` candidate/checkpoint queries with exact
replay. The grid contains `64` deterministic global Halton rows and `256` public-candidate-neighborhood
rows at the unchanged `0.18` span, giving approximately `32` local rows per candidate. Exact candidate
feature rows remain excluded. The fitter may read grid outcomes and candidate feature locations, but
not candidate outcomes, ranks, checkpoint outcomes, priors, or provider output.

Every metric uses a fixed standardized one-hot ExtraTrees regressor with `512` trees,
`min_samples_leaf=1`, `max_features=1.0`, no bootstrap, `random_state=20260824`, followed by the
unchanged standardized minimum-norm exact typed-law distillation. Candidate design rank must be `8`
and reconstruction error must be `<=1e-9`.

## Measurements and pass/failure rules

Report all seven units, exact grid/registered truth and replay denominators, candidate opportunity
gate, fit/candidate overlap, candidate-outcome reads, design rank, distillation error, Spearman rho,
Top-1 agreement, and provider calls. The construction candidate passes only if all `7/7` units pass
the candidate gate and `rho >= 0.80`, all ranks equal `8`, all distillation errors are `<=1e-9`, all
truth queries replay exactly, fit/candidate overlap and candidate-outcome reads are zero, and provider
calls are zero. All seven exposed units are evaluated even after a scientific miss because this is a
fixed construction diagnostic, not prospective qualification.

A platform defect stops the run and requires a new run root from the first unit after repair. No
failed unit may be removed or overwritten, no threshold may be relaxed, and neither prospective nor
formal seeds may replace a construction unit. Passing authorizes only freezing and running the
separate prospective qualification; it does not revive W2-51 or authorize participant/formal work.

## Expected outputs

One machine-readable summary, one readable report, retained per-unit artifacts, exact truth/replay
records, and progress with completed/total queries. Raw run data remain outside Git.
